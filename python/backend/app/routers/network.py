from fastapi import APIRouter, Response, HTTPException
from controllers.db import get_secret
from dotenv import load_dotenv
import requests
import json

load_dotenv()
router = APIRouter(prefix="/network/api", tags=["network"])

# Infoblox details (replace these with your actual credentials)
SA_SECRET = get_secret("VMDeploy/service_account")
INFOBLOX_SECRET = get_secret("VMDeploy/infoblox")
Infoblox = {
    "ib_hostname": INFOBLOX_SECRET["INFOBLOX_URL"],
    "ib_username": SA_SECRET["SA_USER"],
    "ib_password": SA_SECRET["SA_PASS"],
}


# GET host record entry reference from Infoblox using FQDN
@router.get("/infoblox/search/dns/{dns}")
def get_host_record(dns: str):
    print(f"Searching for host record entry, DNS: {dns} ...")
    try:
        uri = f"{Infoblox['ib_hostname']}/wapi/v2.10/record:host?name~=^{dns}$"
        auth = (Infoblox["ib_username"], Infoblox["ib_password"])
        response = requests.get(uri, auth=auth, verify=False).json()
        if len(response):
            ip4vaddr = response[0]["ipv4addrs"][0]["ipv4addr"]
            return Response(content=ip4vaddr, status_code=200)
        return Response(content=None, status_code=404)
    except Exception as e:
        print(e)
        return Response(content="Internal Server Error", status_code=501)


# CREATE Host Record Entry in Infoblox
@router.post("/infoblox/add/dns")
def create_host_record(dns: str, ip: str):
    try:
        api_endpoint = f"{Infoblox['ib_hostname']}/wapi/v2.10/record:host"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        data = {
            "name": dns,
            "ipv4addrs": [{"ipv4addr": ip}],
            "view": "Internal",
        }

        response = requests.post(
            api_endpoint,
            auth=(Infoblox["ib_username"], Infoblox["ib_password"]),
            headers=headers,
            data=json.dumps(data),
            verify=False,
        )

        if response.status_code == 201:
            print(f"Host record '{dns}' created successfully.")
            return Response(
                content=f"Host record '{dns}' created successfully.", status_code=201
            )
        else:
            return Response(
                content=f"Failed Host record '{dns}' entry.", status_code=500
            )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# DELETE host record entry from Infoblox using FQDN
@router.delete("/infoblox/delete/{dns}")
def delete_host_record(dns: str):
    try:
        uri = f"{Infoblox['ib_hostname']}/wapi/v2.10/record:host?name~=^{dns}$"
        auth = (Infoblox["ib_username"], Infoblox["ib_password"])
        response = requests.get(uri, auth=auth, verify=False).json()
        if response:
            record_ref = response[0]["_ref"]
            delete_uri = f"{Infoblox['ib_hostname']}/wapi/v2.10/{record_ref}"
            delete_response = requests.delete(delete_uri, auth=auth, verify=False)
            if delete_response.ok:
                return Response(
                    content=f"Host record '{dns}' deleted successfully.",
                    status_code=200,
                )
            else:
                return Response(
                    content=f"Failed deleting Host record '{dns}' entry.",
                    status_code=500,
                )
        else:
            return Response(content=f"DNS : {dns} not found", status_code=404)
    except Exception as e:
        print(e)
        return Response(content=f"Internal Server Error", status_code=501)


# Search for Available IP
@router.get("/infoblox/search/ip")
def next_available_ip(network: str):
    try:
        payload = {
            "status": "UNUSED",
            "network_view": "default",
            "network": network,
            "_return_as_object": 1,
            "_max_results": 1,
        }
        uri = f"{Infoblox['ib_hostname']}/wapi/v2.10/ipv4address"
        auth = (Infoblox["ib_username"], Infoblox["ib_password"])
        response = requests.get(uri, params=payload, auth=auth, verify=False).json()
        if response:
            ipv4addr = response["result"][0]["ip_address"]
            return ipv4addr
        else:
            return None
    except Exception as e:
        print(e)
        return None
