# 🧠 IPA2025 Final Lab Exam

**Student ID:** 66070191  
**Name:** Sirachet Chotthakunanan  
**Course:** Network and System Technology – King Mongkut’s Institute of Technology Ladkrabang  
**Instructor:** Aj. Chotipat
**Date:** 25 October 2025  

---

## 🧩 Overview

โครงการนี้เป็นส่วนขยายจาก **IPA2024-Final** โดยเพิ่มฟังก์ชันการทำงานให้รองรับทั้ง **RESTCONF**, **NETCONF**, และ **Ansible automation** ในการจัดการอุปกรณ์ Cisco Router (CSR1000v) ภายใต้การควบคุมของ API ที่พัฒนาเอง

---

## ⚙️ Function Summary

### 🔹 ส่วนที่ 1 – RESTCONF & NETCONF API Control

นักศึกษาพัฒนา API ที่สามารถจัดการ Router ผ่านสองวิธี ได้แก่

| Command | Description | Example |
|----------|--------------|----------|
| `/66070191 restconf` | ตั้งโหมด RESTCONF | `Ok: Restconf` |
| `/66070191 netconf` | ตั้งโหมด NETCONF | `Ok: Netconf` |
| `/66070191 create` | สร้าง Loopback Interface | `/66070191 10.0.15.61 create` |
| `/66070191 delete` | ลบ Loopback Interface | `/66070191 10.0.15.61 delete` |
| `/66070191 enable` | เปิดใช้งาน Interface | `/66070191 10.0.15.61 enable` |
| `/66070191 disable` | ปิดใช้งาน Interface | `/66070191 10.0.15.61 disable` |
| `/66070191 status` | ตรวจสอบสถานะ | `/66070191 10.0.15.61 status` |

> ✅ หากไม่ระบุ IP → `Error: No IP specified`  
> ✅ หากไม่ระบุ method → `Error: No method specified`

โค้ดประกอบด้วยสองไฟล์หลัก:
- **restconf_module.py** – ใช้ `requests` ในการส่ง `GET`, `POST`, `DELETE`, `PATCH` ผ่าน RESTCONF  
- **netconf_module.py** – ใช้ `ncclient.manager` ในการส่ง XML RPC (`edit-config`, `get-config`)  

มีการตรวจสอบ edge cases เช่น  
- Interface มีอยู่แล้ว → ตอบ `Cannot create`  
- Interface ไม่มีอยู่ → ตอบ `Cannot delete`  
- สถานะ down → `disabled (checked by Netconf)`  
- สถานะ up → `enabled (checked by Netconf)`

---

### 🔹 ส่วนที่ 2 – Ansible & Netmiko/TEXTFSM (MOTD)

เพิ่มคำสั่ง `/motd` สำหรับตั้งค่าและอ่าน MOTD ของ Router

| Command | Description | Example Output |
|----------|--------------|----------------|
| `/66070191 10.0.15.61 motd Authorized users only! Managed by 66070191` | ตั้งค่า MOTD ผ่าน **Ansible Playbook** | `Ok: success` |
| `/66070191 10.0.15.61 motd` | อ่านค่า MOTD ผ่าน **Netmiko + TextFSM** | `Authorized users only! Managed by 66070191` |
| หากไม่มี MOTD | `Error: No MOTD Configured` |

#### 🔧 Tools Used
- **Ansible Playbook:** ใช้ module `cisco.ios.ios_banner`  
- **Netmiko:** ใช้ `ConnectHandler` และคำสั่ง `show running-config`  
- **Regex:** ดึงข้อความภายใน `banner motd` ด้วย pattern  
  ```python
  banner motd (\S)\s*(.*?)\1
