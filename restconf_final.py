import os, json, requests
requests.packages.urllib3.disable_warnings()

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")

def get_loopback_ip(student_id):
    if not student_id:
        raise ValueError("STUDENT_ID is empty")
    abc = student_id[-3:]
    x = abc[0]
    y = abc[1:]
    return f"172.{x}.{y}.1"

def create(ip_address, student_id):
    api_url = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{student_id}"
    Loopback_ip = get_loopback_ip(student_id)
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{student_id}",
            "description": f"Loopback interface for student {student_id} created by RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {"address": [{"ip": Loopback_ip, "netmask": "255.255.255.0"}]}
        }
    }
    
    resp = requests.put(api_url, data=json.dumps(yangConfig),
                        auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 201:
        return f"Interface Loopback{student_id} is created successfully using Restconf"
    elif resp.status_code == 204:
        return f"Cannot create: Interface loopback {student_id}"
    return f"Error: create Interface Loopback {student_id} already exists"

def delete(ip_address, student_id):
    api_url = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{student_id}"
    resp = requests.delete(api_url, auth=basicauth, headers=headers, verify=False)
    if resp.status_code in (200, 204):
        return f"Interface loopback {student_id} is deleted successfully using Restconf"
    elif resp.status_code == 404:
        return f"Cannot delete: Interface loopback {student_id} not found"
    else:
        return f"Error deleting interface {student_id}: {resp.status_code}"

def enable(ip_address, student_id):
    api_url = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{student_id}"
    yangConfig = {
        "ietf-interfaces:interface": {"name": f"Loopback{student_id}", "enabled": True}
    }

    resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        return f"Interface loopback {student_id} is enabled successfully using Restconf"
    elif resp.status_code == 404:
        return f"Cannot enable: Interface loopback {student_id} not found"
    else:
        return f"Error enabling interface {student_id}: {resp.status_code}"

def disable(ip_address, student_id):
    api_url = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{student_id}"
    yangConfig = {
        "ietf-interfaces:interface": {"name": f"Loopback{student_id}", "enabled": False}
    }

    resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        return f"Interface loopback {student_id} is shutdowned successfully using Restconf"
    elif resp.status_code == 404:
        return f"Cannot shutdown: Interface loopback {student_id}"
    else:
        return f"Error disabling interface {student_id}: {resp.status_code}"

def status(ip_address, student_id):
    api_url_status = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback{student_id}"
    resp = requests.get(api_url_status, auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        interfaces = resp.json().get("ietf-interfaces:interface", {})
        admin_status = interfaces.get("admin-status", "down")
        oper_status = interfaces.get("oper-status", "down")
        if admin_status == 'up' and oper_status == 'up':
            return f"Interface loopback {student_id} is enabled (checked by Restconf)"
        return f"Interface loopback {student_id} is disabled (checked by Restconf)"
    elif resp.status_code == 404:
        return f"No Interface loopback {student_id}"
    return f"Error getting status: {resp.status_code}"