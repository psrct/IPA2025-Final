#######################################################################################
# Yourname: psrct
# Your student ID: 66070191
# Your GitHub Repo: https://github.com/psrct/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import os, time, requests, json
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

import ansible_final
import netmiko_final
import restconf_final

load_dotenv()
#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

WEBEX_TOKEN = os.environ.get("WEBEX_TOKEN")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
WEBEX_ROOM_ID = os.environ.get("WEBEX_ROOM_ID")
STUDENT_ID = os.environ.get("STUDENT_ID")

print("Starting Webex Teams bot...")
while True:
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": WEBEX_ROOM_ID, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": f"Bearer {WEBEX_TOKEN}"}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    try:
        r = requests.get("https://webexapis.com/v1/messages", params=getParameters, headers=getHTTPHeader)
        
        # verify if the retuned HTTP status code is 200/OK
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )

        # get the JSON formatted returned data
        json_data = r.json()

        # check if there are any messages in the "items" array
        if len(json_data["items"]) == 0:
            raise Exception("There are no messages in the room.")

        # store the array of messages
        messages = json_data["items"]
        
        # store the text of the first message in the array
        message = messages[0]["text"]
        print("Received message: " + message)

        # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
        #  e.g.  "/66070123 create"
        if message.startswith(f"/{STUDENT_ID} "):
            # extract the command
            command = message.split(" ")[1]
            print(f"Extracted command: {command}")

# 5. Complete the logic for each command
            responseMessage = ""
            if command == "create":
                responseMessage = restconf_final.create()
            elif command == "delete":
                responseMessage = restconf_final.delete()
            elif command == "enable":
                responseMessage = restconf_final.enable()
            elif command == "disable":
                responseMessage = restconf_final.disable()
            elif command == "status":
                responseMessage = restconf_final.status()
            elif command == "gigabit_status":
                responseMessage = netmiko_final.gigabit_status()
            elif command == "showrun":
                responseMessage = ansible_final.showrun()
            else:
                responseMessage = "Error: No command or unknown command"
            print(f"Response message: {responseMessage}")
        
# 6. Complete the code to post the message to the Webex Teams room.

            postHTTPHeaders = {"Authorization": f"Bearer {WEBEX_TOKEN}"}
            
            if command == "showrun" and responseMessage == 'ok':
                filename = f"show_run_{STUDENT_ID}_CSR1kv.txt"
                m = MultipartEncoder(
                    fields={"roomId": WEBEX_ROOM_ID, "text": f"show_run_{STUDENT_ID}_CSR1kv.txt",
                            "files": (filename, open(filename, 'rb'), 'text/plain')}
                )
                postData = m
                postHTTPHeaders["Content-Type"] = m.content_type
            else:
                postData = json.dumps({"roomId": WEBEX_ROOM_ID, "text": responseMessage})
                postHTTPHeaders["Content-Type"] = "application/json"

            r = requests.post("https://webexapis.com/v1/messages", data=postData, headers=postHTTPHeaders)
            if not r.status_code == 200:
                print(f"Error posting message: {r.status_code} {r.text}")

    except Exception as e:
        print(f"An error occurred: {e}")