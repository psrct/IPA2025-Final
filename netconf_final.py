from ncclient import manager
import xmltodict
import xml.etree.ElementTree as ET

def get_loopback_ip(student_id):
    if not student_id:
        raise ValueError("STUDENT_ID is empty")
    abc = student_id[-3:]
    x = abc[0]
    y = abc[1:]
    return f"172.{x}.{y}.1"

def connect_netconf(ip_address):
    try:
        m = manager.connect(
            host=ip_address,
            port=830,
            username="admin",
            password="cisco",
            hostkey_verify=False,
            device_params={'name': 'csr'},
            timeout=30
        )
        return m
    except Exception as e:
        print(f"Error connecting via NETCONF to {ip_address}: {e}")
        return None

def create(ip_address, student_id):
    Loopback_ip = get_loopback_ip(student_id)
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback{student_id}</name>
          <description>Loopback interface for student {student_id} created by NETCONF</description>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
          <enabled>true</enabled>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>{Loopback_ip}</ip>
              <netmask>255.255.255.0</netmask>
            </address>
          </ipv4>
        </interface>
      </interfaces>
    </config>
    """

    m = connect_netconf(ip_address)
    if not m:
        return f"Error connecting to {ip_address}"
        
    try:
        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        
        if '<ok/>' in xml_data:
            return f"Interface Loopback{student_id} is created successfully using Netconf"
        return "Error: NETCONF create failed"
    except Exception as e:
        print(f"NETCONF Error: {e}")
        if "data-exists" in str(e):
            return f"Cannot create: Interface Loopback {student_id} already exists"
        return f"Error: NETCONF create failed: {e}"
    finally:
        if m: m.close_session()


def delete(ip_address, student_id):
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
          <name>Loopback{student_id}</name>
        </interface>
      </interfaces>
    </config>
    """
    
    m = connect_netconf(ip_address)
    if not m:
        return f"Error connecting to {ip_address}"

    try:
        # ตรวจสอบก่อนว่า interface มีอยู่จริงหรือไม่
        if "No Interface" in status(ip_address, student_id):
            return f"Cannot delete: Interface loopback {student_id}"

        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {student_id} is deleted successfully using Netconf"
        return "Error: NETCONF delete failed"
    except Exception as e:
        print(f"NETCONF Error: {e}")
        return f"Cannot delete: Interface loopback {student_id}"
    finally:
        if m: m.close_session()


def enable(ip_address, student_id):
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback{student_id}</name>
          <enabled>true</enabled>
        </interface>
      </interfaces>
    </config>
    """
    
    m = connect_netconf(ip_address)
    if not m:
        return f"Error connecting to {ip_address}"

    try:
        if "No Interface" in status(ip_address, student_id):
            return f"Cannot enable: Interface loopback {student_id}"

        netconf_reply = m.edit_config(target="running", config=netconf_config, default_operation="merge")
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {student_id} is enabled successfully using Netconf"
        return "Error: NETCONF enable failed"
    except Exception as e:
        print(f"NETCONF Error: {e}")
        return f"Cannot enable: Interface loopback {student_id}"
    finally:
        if m: m.close_session()


def disable(ip_address, student_id):
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback{student_id}</name>
          <enabled>false</enabled>
        </interface>
      </interfaces>
    </config>
    """

    m = connect_netconf(ip_address)
    if not m:
        return f"Error connecting to {ip_address}"

    try:
        if "No Interface" in status(ip_address, student_id):
             return f"Cannot shutdown: Interface loopback {student_id}"
             
        netconf_reply = m.edit_config(target="running", config=netconf_config, default_operation="merge")
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {student_id} is shutdowned successfully using Netconf"
        return "Error: NETCONF disable failed"
    except Exception as e:
        print(f"NETCONF Error: {e}")
        return f"Cannot shutdown: Interface loopback {student_id}"
    finally:
        if m: m.close_session()


def status(ip_address, student_id):
    netconf_filter = f"""
  <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" type="subtree">
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>Loopback{student_id}</name>
        <admin-status/>
        <oper-status/>
      </interface>
    </interfaces-state>
  </filter>
    """
    
    m = connect_netconf(ip_address)
    if not m:
        return f"Error connecting to {ip_address}"

    try:
        # ใช้ .get() เพื่อดึง operational data
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply.xml)
        
        doc = xmltodict.parse(netconf_reply.xml)
        
        iface_data = doc.get("rpc-reply", {}).get("data", {}).get("interfaces-state", {}).get("interface")

        if iface_data:
            admin_status = iface_data.get("admin-status", "down")
            oper_status = iface_data.get("oper-status", "down")
            
            if admin_status == 'up' and oper_status == 'up':
                return f"Interface loopback {student_id} is enabled (checked by Netconf)"
            else:
                return f"Interface loopback {student_id} is disabled (checked by Netconf)"
        else:
            return f"No Interface loopback {student_id}"
            
    except Exception as e:
       print(f"NETCONF Error: {e}")
       return f"No Interface loopback {student_id}"
    finally:
        if m: m.close_session()