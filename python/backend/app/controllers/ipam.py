from routers.network import delete_host_record, create_host_record, next_available_ip


def IPAM(Network: str, dns: str):
    ip = next_available_ip(Network)
    if ip is not None:
        create_host_record(dns, ip)
        return ip, True
    else:
        return None, False


def IPAM_Rollback(dns: str):
    delete_host_record(dns)
