from urllib3 import disable_warnings
from dotenv import load_dotenv
import bcrypt
import hvac
import os


load_dotenv()
disable_warnings()


# read vault secret
def get_secret(key):
    client = hvac.Client(
        url=os.getenv("VAULT_URL"),
        token=os.getenv("VAULT_TOKEN"),
        verify=False,
    )
    creds = client.secrets.kv.read_secret_version(
        mount_point=os.getenv("VAULT_MOUNT"), path=key
    )["data"]["data"]
    return creds


# encrypt token/password
def encrypt(token):
    hashed = bcrypt.hashpw(token, bcrypt.gensalt(14))
    return hashed
