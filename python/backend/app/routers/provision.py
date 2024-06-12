from fastapi import Request, APIRouter, BackgroundTasks
from controllers.vcenter import process_vm_provisioning
from models.mongo import MongoDB
import json


router = APIRouter(prefix="/provision/api", tags=["provision"])


@router.get("/vcenter/list/vm")
async def GetAllVms():
    cursor = MongoDB()
    data = cursor.getAllDocuments(projection={"_id": 0, "variables": 0})
    return data


@router.post("/vcenter/create/vm")
async def VMProvision(req: Request, background_tasks: BackgroundTasks):
    body = await req.body()
    payload = json.loads(body.decode("utf-8"))
    background_tasks.add_task(process_vm_provisioning, payload)
    return {"message": "VM Provisioning Process Started"}
