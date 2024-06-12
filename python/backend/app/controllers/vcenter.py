from models.mongo import MongoDB
from routers.platform import execPlaybookAWX
from controllers.ipam import IPAM, IPAM_Rollback
from controllers.db import get_secret
from routers.notification import slack_notify
from dotenv import load_dotenv
from datetime import datetime
import requests

load_dotenv()

# vcenter creds
SA_SECRET = get_secret("VMDeploy/service_account")
vcenter = {
    "vcenter_password": SA_SECRET["SA_PASS"],
    "vcenter_username": SA_SECRET["SA_USER"],
}


def process_vm_provisioning(payload):
    try:
        task_id = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        cursor = MongoDB()
        documents = []

        for index in range(payload["count"]):
            ip, host_record_entry = IPAM(
                payload["vms"][index]["Network"], payload["vms"][index]["fqdn"]
            )

            doc = {
                "ticket_ref": payload["ticket_ref"],
                "task_id": task_id,
                "created_at": datetime.utcnow(),
                "index": index + 1,
                "status": False,
                "users": {
                    "executor": payload["executor"],
                    "requestor": payload["requestor"],
                },
                "variables": {**payload["vms"][index], **vcenter, "ipv4addr": ip},
            }

            if ip is not None and host_record_entry:
                print(f"New VM Provisioning ...")
                try:
                    job_status, job_url = execPlaybookAWX(
                        JOB_TEMPLATE="VM Automation Template",
                        extra_vars=doc["variables"],
                    )
                    if not job_status:
                        print("Failed VM provisoning, Rollback Host Record Entry ...")
                        IPAM_Rollback(payload["vms"][index]["fqdn"])

                    doc["status"] = job_status
                except Exception as e:
                    doc["status"] = e
                finally:
                    doc["job_url"] = job_url
                    documents.append(doc)

                try:
                    DeployVM_CHANNEL = get_secret("VMDeploy/slack")["DeployVM_WEBHOOK"]
                    DEPLOY_EVENT_URL = get_secret("VMDeploy/stream")["DEPLOY_EVENT"]
                    slack_notify(
                        output=doc,
                        channel=DeployVM_CHANNEL,
                    )
                    requests.post(DEPLOY_EVENT_URL)
                except Exception as e:
                    print(e)
        if len(documents) != 0:
            cursor.insertManyDocuments(documents)

    except Exception as e:
        print("Internal Server Error", e)
