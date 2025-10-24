from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.62"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
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
