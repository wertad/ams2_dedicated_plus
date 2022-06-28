# TODO: a draw_a_car és track függvényekben a random intervallum kézzel lett megadva, ha eltérő az érték, akkor nagyobb számot is sorsolhat, mint ami létezik.

import json, random

rotate_config = "sms_rotate_config.json"
vehicle_list = "./pcars_res/vehicles.list"
track_list = "./pcars_res/tracks.list"
random_car = ""
random_track = ""
json_veh_object = ""
json_track_object = ""

# Beolvassa a kocsik listáját a vehicles.list-ből a json_veh_object-be
def load_car_list():
    global json_veh_object
    veh_file = open(vehicle_list, "r", encoding="utf-8")
    json_veh_object = json.load(veh_file)
    veh_file.close()

# Beolvassa a pályák listáját a tracks.list-ből a json_track_object-be
def load_track_list():
    global json_track_object, track_list
    track_file = open(track_list, "r", encoding="utf-8")
    json_track_object = json.load(track_file)
    track_file.close()

# random autót váasztó függvény
def draw_a_car():
    global random_car
    # generál egy random számot a kocsihoz
    rnd = random.randint(0, 233)
    # kiválasztja a random szám alapján az adott indexű kocsit a json_veh_object-ből és a random_car-ba tárolja
    random_car = json_veh_object["response"]["list"][rnd]["name"]

# random pályát váasztó függvény
def draw_a_track():
    global random_track
    # generál egy random számot a pályához
    rnd = random.randint(0, 147)
    # kiválasztja a random szám alapján az adott indexű pályát a json_track_object-ből és a random_car-ba tárolja
    random_track = json_track_object["response"]["list"][rnd]["name"]

# Beolvassa az sms_rotate_config.json fájlt a json_object-be
a_file = open(rotate_config, "r", encoding="utf-8")
json_object = json.load(a_file)
a_file.close()

load_car_list()
load_track_list()

# Minden eseményhez választ egy random kocsit és egy pályát
for rotation in json_object["config"]["rotation"]:
    draw_a_car()
    draw_a_track()
    rotation["VehicleModelId"] = random_car
    rotation["TrackId"] = random_track

# felülírja a config fájlt a módosított értékekkel
a_file = open(rotate_config, "w", encoding="utf-8")
json.dump(json_object, a_file, indent=4, ensure_ascii=False)
a_file.close()