# read_data(filepath):
#   - check if the file exists at the given path
#   - if it does not exist, return an empty list
#   - if it does, open it and load the contents as JSON
#   - return the loaded data

# write_data(filepath, data):
#   - open the file at the given path in write mode
#   - serialise 'data' as JSON and write it to the file

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAVEL_LOG_FILE = os.path.join(BASE_DIR, "data", "travel_log.json")
LOGIN_FILE = os.path.join(BASE_DIR, "data", "login_info.json")

def read_data(filepath):
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def write_data(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def read_travel_logs():
    data = read_data(TRAVEL_LOG_FILE)
    if data is None:
        return []
    if isinstance(data, list):
        return  data
    else:
        return []

def read_login_info():
    data = read_data(LOGIN_FILE)
    if data is None:
        return []
    
    if isinstance(data, list):
        return data
    
    return []

def get_user_by_username(username: str):
    login_data = read_travel_logs()

    for user in login_data:
        if user.get("username") == username:
            return user

    return None

#authed
def get_username_travel_log(username: str):
    travel_log_data = read_travel_logs()

    for user in travel_log_data:
        if user.get("username") == username:
            return user  #return the whole dictionary for that user
    return None

def get_id_travel_log(id: str):
    travel_log_data = read_travel_logs()

    for user in travel_log_data:
        if user.get("id") == id:
            return user  #return the whole dictionary for  that user
    return None