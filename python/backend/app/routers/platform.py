from awxkit import config, utils
from awxkit.api import ApiV2
from awxkit.api.resources import resources
from fastapi import APIRouter
from controllers.db import get_secret
from dotenv import load_dotenv
import json

load_dotenv()
router = APIRouter(prefix="/platform/api", tags=["platform"])


# awx credentials
SA_SECRET = get_secret("VMDeploy/service_account")
AWX_SECRET = get_secret("VMDeploy/awx")
AWX = {
    "awx_ip": AWX_SECRET["AWX_URL"],
    "awx_user": SA_SECRET["SA_USER"],
    "awx_pass": SA_SECRET["SA_PASS"],
}


# execute AWX playbook
@router.post("/awx/playbook")
def execPlaybookAWX(JOB_TEMPLATE: str, extra_vars: dict):
    try:
        print(f"AWX Job Initiated")

        # Create authenticated session
        config.base_url = AWX["awx_ip"]
        config.credentials = utils.PseudoNamespace(
            {"default": {"username": AWX["awx_user"], "password": AWX["awx_pass"]}}
        )
        session_connection = ApiV2().load_session().get()
        response = session_connection.get(resources)

        # Search Job Template
        unified_job_templates = response.unified_job_templates.get(name=JOB_TEMPLATE)
        unified_job_template = unified_job_templates.results[0]
        unified_job_template.extra_vars = json.dumps(extra_vars)
        unified_job_template.patch()

        # Launch Job Template
        response = unified_job_template.launch()
        JOB_URL = f'{AWX["awx_ip"]}#/jobs/playbook/{response.id}/output'
        JOB_STATUS = None

        while response.status in [
            "new",
            "pending",
            "waiting",
            "running",
            "updating",
            "none",
        ]:
            response = unified_job_template.get()
            if response.status in ["successful", "ok"]:
                print("Job completed Successful")
                JOB_STATUS = True
                break
            elif response.status in [
                "canceled",
                "missing",
                "failed",
                "error",
                "never updating",
            ]:
                JOB_STATUS = False
                break

        unified_job_template.extra_vars = json.dumps({})
        unified_job_template.patch()
    except Exception as e:
        print("AWX Error: ", e)
        JOB_STATUS = False
    return JOB_STATUS, JOB_URL
