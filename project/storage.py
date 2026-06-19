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

TRAVEL_LOG_FILE = "project/data/travel_log.json"
LOGIN_FILE = "project/data/login_info.json"

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
    login_data = read_login_info()

    for user in login_data:
        if user.get("username") == username:
            return user

    return None


# filepath = "project/data/travel_log.json"
# data = read_data(filepath)
# print(data)