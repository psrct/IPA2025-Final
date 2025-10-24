# 🧠 IPA2025 Final Lab Exam

ให้นักศึกษาทำต่อจาก **IPA2024-Final** โดยมีการเพิ่มเติมดังนี้  
---

## ส่วนที่ 1

**IP ของ Router:**  
10.0.15.61, 10.0.15.62, 10.0.15.63, 10.0.15.64, 10.0.15.65  
รวม 5 IP

นักศึกษาจะต้องระบุใน API ว่าให้ไป Configure Router ไหน เช่น  
`/66070123 10.0.15.61 create` → ให้ create ที่ 10.0.15.61  

หากไม่ระบุ IP เช่น `/66070123 create` → ตอบว่า  
`Error: No IP specified`

ให้ใช้ทั้ง **Restconf** และ **Netconf** ในการทำส่วนที่ 1 โดยจะต้องระบุว่าใช้อะไร เช่น  
- `/66070123 restconf` → API ของส่วนที่ 1 ทั้งหมดให้ใช้ Restconf  
- `/66070123 netconf` → API ของส่วนที่ 1 ทั้งหมดให้ใช้ Netconf  

หากไม่ระบุ → ตอบว่า  
`Error: No method specified`

ใช้แค่ห้อง **IPA2025** เพื่อทดสอบเท่านั้น  
ไม่อนุญาตให้ใช้ห้องส่วนตัว และมีการเก็บ Log การทดลองพิมพ์คำสั่ง  

ให้นักศึกษา Push Code ลง **GitHub Repository ใหม่ชื่อ IPA2025**  
ต้องมีการ Commit ที่แสดงกระบวนการทำงานที่ชัดเจน  
หากพบว่า Commit ไม่ได้มาจากการทำด้วยตนเอง ถือว่าทุจริต  

ให้อธิบายขั้นตอนที่สำคัญตั้งแต่ IPA2024 ว่าเกิดอะไรขึ้น ติดในขั้นตอนไหน และแก้อย่างไร  
เพื่อแสดงความเข้าใจว่าทำด้วยตนเอง (ห้ามใช้ AI เขียนเด็ดขาด)

---

### ตัวอย่างการทำงาน

/66070123 create
Error: No method specified

/66070123 restconf
Ok: Restconf

/66070123 create
Error: No IP specified

/66070123 10.0.15.61
Error: No command found.

/66070123 10.0.15.61 create
Interface loopback 66070123 is created successfully using Restconf

/66070123 10.0.15.61 create
Cannot create: Interface loopback 66070123

/66070123 delete
Error: No IP specified

/66070123 netconf
Ok: Netconf

/66070123 10.0.15.61 delete
Interface loopback 66070123 is deleted successfully using Netconf

/66070123 10.0.15.61 delete
Cannot delete: Interface loopback 66070123

/66070123 10.0.15.61 create
Interface loopback 66070123 is created successfully using Netconf

/66070123 10.0.15.61 enable
Cannot enable: Interface loopback 66070123

/66070123 10.0.15.61 enable
Interface loopback 66070123 is enabled successfully using Netconf

/66070123 10.0.15.61 disable
Interface loopback 66070123 is shutdowned successfully using Netconf

/66070123 10.0.15.61 disable
Cannot shutdown: Interface loopback 66070123 (checked by Netconf)

/66070123 10.0.15.61 status
Interface loopback 66070123 is disabled (checked by Netconf)

/66070123 10.0.15.61 enable
Interface loopback 66070123 is enabled successfully using Netconf

/66070123 restconf
Ok: Restconf

/66070123 10.0.15.61 status
Interface loopback 66070123 is enabled (checked by Restconf)

/66070123 10.0.15.61 status
No Interface loopback 66070123 (checked by Restconf)

---

## ส่วนที่ 2

ให้ใช้ **Ansible** เพิ่มคำสั่ง เช่น  
`/66070123 10.0.15.61 motd Authorized users only! Managed by 66070123`  
เพื่อทำการ configure MOTD เป็นข้อความ  
`"Authorized users only! Managed by 66070123"`

ให้ใช้ **Netmiko/TextFSM** ในการอ่านค่า MOTD  
เมื่อใช้คำสั่ง `/66070123 10.0.15.61 motd`  
ให้แสดงข้อความ  
`Authorized users only! Managed by 66070123`

---

### ตัวอย่างการทำงาน
/66070123 10.0.15.61 motd Authorized users only! Managed by 66070123
Ok: success

/66070123 10.0.15.61 motd
Authorized users only! Managed by 66070123

/66070123 10.0.15.45 motd
Error: No MOTD Configured