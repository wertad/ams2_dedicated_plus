import json
import urllib.request
import requests
import time
import subprocess
'''
a_file = open("sms_stats_data.json", encoding="utf-8")
json_object = json.load(a_file)
a_file.close()
'''


def getLogs():
    global index, server_time, errCount

    try:
        with urllib.request.urlopen("http://127.0.0.1:9000/api/log/range?offset=-100&count=100") as url:
            data = json.load(url)
        # Nullázza a a hibaszámlálót, ha másodjára is szakad a kapcsolat a szerverrel is 3-nál kezelje az except ág
        errCount = 0

        for item in data["response"]["events"]:
            #if (item["name"] == "State" or item["name"] == "Impact" or item["name"] == "Sector") and (index < item["index"] or item["time"] > server_time):
            if (item["name"] == "State" or item["name"] == "Impact" or item["name"] == "Sector") and (index < item["index"]):
                if item["participantid"] == 0:
                    if (item["name"] == "Impact"):
                        if item["attributes"]["CollisionMagnitude"] > 100:
                            if item["attributes"]["OtherParticipantId"] < 0:
                                requests.post("http://127.0.0.1:9000/api/session/send_chat?message='Incident Counter +2x'")
                                print("Server message: Incident Counter +2x")
                            else:
                                requests.post("http://127.0.0.1:9000/api/session/send_chat?message='Incident Counter +4x'")
                                print("Server message: Incident Counter +4x")
                    print(item)
                    index = item["index"]
                    server_time = item["time"]
    # Ha megszakad a kapcsolat a szerverrel 3 próbálkozás után resetelje az eventid-t
    except Exception as ex:
        errCount += 1
        print(ex)
        if errCount == 3:
            index = 0
            print("Server is offline, eventid has been reseted.")

subprocess.check_call([r"DedicatedServerCmd.exe"])

stop = False
index = 0
server_time = 0
errCount = 0


def executeSomething():
    global stop

    getLogs()
    time.sleep(1)


while not stop:
    executeSomething()