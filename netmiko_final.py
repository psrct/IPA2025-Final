from netmiko import ConnectHandler
from pprint import pprint
import re

username = "admin"
password = "cisco"

def get_device(ip_address):
    return {
        "device_type": "cisco_ios",
        "ip": ip_address,
        "username": username,
        "password": password,
    }


def gigabit_status(ip_address):
    ans = ""
    device_params = get_device(ip_address)

    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        
        result = ssh.send_command("show ip interface brief", use_textfsm=True)

        for status in result:
            # ตรวจเฉพาะ interface ที่เป็น GigabitEthernet
            if status["interface"].startswith("GigabitEthernet"):
                iface_name = status["interface"]
                iface_status = status["status"].lower()  #ดูสถานะว่า "up" , "down" หรือ "administratively down"

                if iface_status == "up":
                    up += 1
                elif iface_status == "down":
                    down += 1
                elif "administratively" in iface_status:
                    admin_down += 1

                ans += f"{iface_name} {iface_status}, "

        # ตัด comma ท้ายสุด
        ans = ans.rstrip(", ")
        # เพิ่มสรุปท้ายข้อความ
        ans += f" -> {up} up, {down} down, {admin_down} administratively down"

        pprint(ans)
        return ans

def get_motd(ip_address):
    device_params = get_device(ip_address)

    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command("show running-config", use_textfsm=False)
        
        m_inline = re.search(r"banner motd (\S)\s*(.*?)\1", result, re.DOTALL)
        print(m_inline)
        if m_inline:
            motd_text = m_inline.group(2).strip().lstrip('C^ ')
            if motd_text:
                return motd_text
            return "Error: No MOTD Configured"

        return "Error: No MOTD Configured"