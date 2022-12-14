import string
import requests

MODES = {"time": ["15", "30", "60", "120"],
         "words": ["10", "25", "50", "100"]
         }
LANGUAGES = ["english", "spanish", "german",
             "portuguese", "indonesian", "italian"]


#   FUNCTION:
#   ARGS:   sublink - The subdirectory of the api which to request from
#           headers - Header for the request, should be a dict with a key "Authorization" with a value "ApeKey <your key>"
#           params  - Parameters for the request, should be a dict with keys depending on the subdirecty. Ex. "mode", "mode2"
#   RETURN: json if success, NONE if error
def getMonkeyTypeRequest(sublink: string, headers: dict, params: dict):
    response = requests.get("http://api.monkeytype.com/" +
                            sublink, headers=headers, params=params)
    if response.json()['message'].endswith("retrieved"):
        return response.json()
    else:
        # print("Not Received")
        return None

def genAuthHeader(apekey:string):
    return {"Authorization" : "ApeKey " + apekey}


### FUNCTIONS THAT ONLY SEE DATA FOR GIVEN APEKEY ###

#   FUNCTION:   Get general stats of an account given its ApeKey
#   ARGS:   apekey  - Your ApeKey from MonkeyType
#   RETURN: json if success, NONE if error
def getStats(apekey: string):
    return getMonkeyTypeRequest("users/stats", genAuthHeader(apekey), {})

#   FUNCTION:   Get personalbests of an account given its ApeKey
#   ARGS:   apekey  - Your ApeKey from MonkeyType
#           mode    - Mode of MonkeyType; "time" or "words"
#           mode2   - SubMode of MonkeyType; refer to MODES dict
#   RETURN: json if success, NONE if error
def getPersonalBest(apekey: string, mode: string, mode2: string):
    if mode not in MODES:
        print("ERROR: unfound mode")
        return None
    params = {"mode": mode}
    if mode2 != None:
        if mode2 not in MODES[mode]:
            print("ERROR: unfound mode2")
            return None
        params["mode2"] = mode2
    return getMonkeyTypeRequest("users/personalBests", genAuthHeader(apekey), params)

#   FUNCTION:   Get leaderboard rank of an account given its ApeKey
#   ARGS:   apekey  - Your ApeKey from MonkeyType
#           mode    - Mode of MonkeyType; "time" or "words"
#           mode2   - SubMode of MonkeyType; refer to MODES dict
#   RETURN: json if success, NONE if error
def getLeadboardRank(apekey: string, mode: string, mode2: string):
    if mode not in MODES:
        print("ERROR: unfound mode")
        return None
    params = {"mode": mode}
    if mode2 not in MODES[mode]:
        print("ERROR: unfound mode2")
        return None
    params["mode2"] = mode2
    return getMonkeyTypeRequest("leaderboards", genAuthHeader(apekey), params)

#   FUNCTION:   Get last test of an account given its ApeKey
#   ARGS:   apekey  - Your ApeKey from MonkeyType
#   RETURN: json if success, NONE if error
def getLast(apekey: string):
    return getMonkeyTypeRequest("results/last", genAuthHeader(apekey), {})


### FUNCTIONS THAT SEE DATA OF OTHER USERS ###

#   FUNCTION:   Get any users profile (general stats and personal stats)
#   ARGS:   apekey  - Your ApeKey from MonkeyType
#           uid     - Username of any user
#   RETURN: json if success, NONE if error
def getProfile(apekey: string, uid: string):
    return getMonkeyTypeRequest("users" + uid + "/profile", genAuthHeader(apekey), {})

#   FUNCTION:   Get leaderboard entries of a given category
#   ARGS:   apekey  - Your ApeKey from MonkeyType
#           mode    - Mode of MonkeyType; "time" or "words"
#           mode2   - SubMode of MonkeyType; refer to MODES dict
#           skip    - Skips the first x amount of entries on the leaderboard
#           limit   - # of entries to get, max 50
#   RETURN: json if success, NONE if error
def getLeaderboard(apekey: string, language: string, mode: string, mode2: string, skip: int, limit: int):
    if language not in LANGUAGES:
        print("ERROR: unfound language")
        return None
    params = {"language": language}
    if mode not in MODES:
        print("ERROR: unfound mode")
        return None
    params["mode"] = mode
    if mode2 not in MODES[mode]:
        print("ERROR: unfound mode2")
        return None
    params["mode2"] = mode2
    if skip != None:
        params["skip"] = skip
    if limit != None:
        params["limit"] = limit
    return getMonkeyTypeRequest("leaderboards", genAuthHeader(apekey), params)


### OTHER HELPER FUNCTIONS ###

#   FUNCTION:   Create list of keys from a text file. Each key is its own line in the text file. If the line starts with '###', then the line will be ignored.
#   ARGS:   filename - The filename of the text file (including the file extension)
#   RETURNS:    A list (each element being a key)
def keysFromTextFileToList(filename: string = "apekeys.txt"):
    keys = []
    file = open(filename, "r")
    for line in file.readlines():
        if not line.startswith("###"):
            x = line.replace("\n", "")
            if getStats(x) != None:
                keys.append(x)
            else:
                print("{l} is an invalid ApeKey. Moving to next line...".format(l=x))
    file.close()
    return keys


def main():
    print("MonkeyType.py main function")
    ## TESTING OF MONKEYTYPE FUNCTIONS
    # l = keysFromTextFileToList()
    # print(l)
    # print(getLeaderboard(l[0], "english", "time", "15", 0, 50))


if __name__ == "__main__":
    main()
