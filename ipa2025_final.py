#######################################################################################
# Yourname: psrct
# Your student ID: 66070191
# Your GitHub Repo: https://github.com/psrct/IPA2024-Final

#######################################################################################
# 1. Import libraries
import os, time, requests, json
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder
import re # Import regex

import ansible_final
import netmiko_final
import restconf_final
import netconf_final

load_dotenv()
#######################################################################################
# 2. Assign environment variables
WEBEX_TOKEN = os.environ.get("WEBEX_TOKEN")
WEBEX_ROOM_ID = os.environ.get("WEBEX_ROOM_ID")
STUDENT_ID = os.environ.get("STUDENT_ID")

#######################################################################################
# 3. Global variables for state
VALID_IPS = ["10.0.15.61", "10.0.15.62", "10.0.15.63", "10.0.15.64", "10.0.15.65"]
selected_ip = None
selected_method = None # "restconf" or "netconf"

print("Starting Webex Teams bot...")
while True:
    time.sleep(1)

    # 4. Prepare parameters to get the latest message
    getParameters = {"roomId": WEBEX_ROOM_ID, "max": 1}
    getHTTPHeader = {"Authorization": f"Bearer {WEBEX_TOKEN}"}

    try:
        r = requests.get("https://webexapis.com/v1/messages", params=getParameters, headers=getHTTPHeader)
        if not r.status_code == 200:
            raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")

        json_data = r.json()
        if len(json_data["items"]) == 0:
            raise Exception("There are no messages in the room.")

        messages = json_data["items"]
        message_id = messages[0]["id"]
        
        message = messages[0]["text"]
        print(f"Received message: {message}")

        # 5. Parse command
        responseMessage = ""
        postData = None
        filename = None
        command = None
        
        if message.startswith(f"/{STUDENT_ID} "):
            parts = message.strip().split(" ")
            command_parts = parts[1:]

            if len(command_parts) == 0 or command_parts[0].lower() not in ["restconf", "netconf"]:
                selected_ip = None
            
            # ตรวจสอบคำสั่งแบบ 1 ส่วน (restconf, netconf, หรือ command ที่ใช้ IP/method ที่เก็บไว้)
            if len(command_parts) == 1:
                cmd_part_1 = command_parts[0].lower()
                if cmd_part_1 == "restconf":
                    selected_method = "restconf"
                    responseMessage = "Ok: Restconf"
                elif cmd_part_1 == "netconf":
                    selected_method = "netconf"
                    responseMessage = "Ok: Netconf"
                elif cmd_part_1 in ["create", "delete", "enable", "disable", "status", "gigabit_status", "showrun", "motd"]:
                    if not selected_method:
                        responseMessage = "Error: No method specified"
                    elif not selected_ip:
                        responseMessage = "Error: No IP specified" 
                    else:
                        command = cmd_part_1 # ใช้ IP/method ที่เก็บไว้
                else:
                    responseMessage = "Error: No command found."

            # ตรวจสอบคำสั่งแบบ 2 ส่วน (IP + command, หรือ command + args)
            elif len(command_parts) >= 2:
                part1 = command_parts[0].lower()
                part2 = command_parts[1].lower()
                
                if part1 in VALID_IPS:
                    selected_ip = part1 # เก็บ IP
                    command = part2
                    args = " ".join(command_parts[2:])
                elif part1 not in VALID_IPS :
                    responseMessage = "Error: No MOTD Configured"
                elif part1 == "motd":
                    if not selected_ip:
                         responseMessage = "Error: No IP specified"
                    else:
                        command = "motd"
                        args = " ".join(command_parts[1:])
                else:
                    responseMessage = "Error: No command found."
            
            # 6. Execute command
            if command:
                if not selected_ip:
                    responseMessage = "Error: No IP specified"
                else:
                    # Part 1 commands
                    if command in ["create", "delete", "enable", "disable", "status"]:
                        if not selected_method:
                            responseMessage = "Error: No method specified"
                        elif not selected_ip:
                            responseMessage = "Error: No IP specified"
                        elif selected_method == "restconf":
                            if command == "create":
                                responseMessage = restconf_final.create(selected_ip, STUDENT_ID)
                            elif command == "delete":
                                responseMessage = restconf_final.delete(selected_ip, STUDENT_ID)
                            elif command == "enable":
                                responseMessage = restconf_final.enable(selected_ip, STUDENT_ID)
                            elif command == "disable":
                                responseMessage = restconf_final.disable(selected_ip, STUDENT_ID)
                            elif command == "status":
                                responseMessage = restconf_final.status(selected_ip, STUDENT_ID)
                        
                        elif selected_method == "netconf":
                            if command == "create":
                                responseMessage = netconf_final.create(selected_ip, STUDENT_ID)
                            elif command == "delete":
                                responseMessage = netconf_final.delete(selected_ip, STUDENT_ID)
                            elif command == "enable":
                                responseMessage = netconf_final.enable(selected_ip, STUDENT_ID)
                            elif command == "disable":
                                responseMessage = netconf_final.disable(selected_ip, STUDENT_ID)
                            elif command == "status":
                                responseMessage = netconf_final.status(selected_ip, STUDENT_ID)

                    # Part 2 commands
                    elif command == "motd":
                        if args: # Set MOTD
                            responseMessage = ansible_final.set_motd(selected_ip, args, STUDENT_ID)
                        else: # Get MOTD
                            motd_text = netmiko_final.get_motd(selected_ip)
                            responseMessage = motd_text
                    
                    # Original commands
                    elif command == "gigabit_status":
                        responseMessage = netmiko_final.gigabit_status(selected_ip)
                    
                    elif command == "showrun":
                        responseMessage = ansible_final.showrun(selected_ip, STUDENT_ID)
                        if responseMessage == "ok":
                            # อัปเดตชื่อไฟล์ให้มี IP
                            filename = f"show_run_{STUDENT_ID}_{selected_ip}.txt" 
                            responseMessage = f"File: {filename}"
                        else:
                            responseMessage = "Error: Ansible showrun failed"

                    elif responseMessage == "": # ถ้ายังไม่มี response
                        responseMessage = "Error: No command found"
            
            print(f"Response message: {responseMessage}")
        
# 7. Post the message to the Webex Teams room.
            if responseMessage:
                postHTTPHeaders = {"Authorization": f"Bearer {WEBEX_TOKEN}"}
                
                if command == "showrun" and filename:
                    try:
                        m = MultipartEncoder(
                            fields={"roomId": WEBEX_ROOM_ID, "text": responseMessage,
                                    "files": (filename, open(filename, 'rb'), 'text/plain')}
                        )
                        postData = m
                        postHTTPHeaders["Content-Type"] = m.content_type
                    except FileNotFoundError:
                        responseMessage = "Error: Could not find generated showrun file."
                        postData = json.dumps({"roomId": WEBEX_ROOM_ID, "text": responseMessage})
                        postHTTPHeaders["Content-Type"] = "application/json"
                
                if not postData:
                    postData = json.dumps({"roomId": WEBEX_ROOM_ID, "text": responseMessage})
                    postHTTPHeaders["Content-Type"] = "application/json"

                r = requests.post("https://webexapis.com/v1/messages", data=postData, headers=postHTTPHeaders)
                if not r.status_code == 200:
                    print(f"Error posting message: {r.status_code} {r.text}")

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(2)