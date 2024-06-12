from fastapi import APIRouter
from controllers.notify import vmdeploy_slack_notify
import requests
import sys
import json


router = APIRouter(prefix="/notification/api", tags=["notification"])


# slack notification request
@router.post("/slack")
def slack_notify(output: dict, channel: str):
    slack_data = vmdeploy_slack_notify(output)
    byte_length = str(sys.getsizeof(slack_data))
    headers = {"Content-type": "application/json", "Content-Length": byte_length}
    response = requests.post(
        channel, headers=headers, data=json.dumps(slack_data), verify=False
    )
    if response.status_code == 200:
        return {"message": "Request sent successfully."}

    return {"message": "Request failed with status code:"}

