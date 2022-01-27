import time
import pickle
import logging

import requests


def get_rank(round: int, address: str, bearer: str) -> int:
    rank = 0
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {bearer}",
    }
    url = f"https://api.mintopoly.io/game/round/{round}/player/{address}/rank"
    while rank == 0:
        response = requests.get(
            url,
            headers=headers,
        )
        data = response.json()
        rank = data["rank"]
        if rank != 0:
            return rank
        time.sleep(60)


def get_buildings(bearer: str) -> dict:
    # try to use the cached version so we don't slam the server too often
    # delete the file to fetch a fresh copy
    try:
        data = pickle.load(open("buildings.p", "rb"))
    except IOError as error:
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {bearer}",
        }

        response = requests.get(
            "https://api.mintopoly.io/game/investments", headers=headers
        )
        data = response.json()
    pickle.dump(data, open("buildings.p", "wb"))

    buildings = {}

    for building in data:
        buildingData = {
            "investmentID": building["investmentID"],
            "name": building["name"],
            "verb": building["verb"],
            "color": building["color"],
            "unlockCost": building["unlockCost"],
            "initialPrice": building["initialPrice"],
            "currentCost": building["initialPrice"],
            "coefficient": building["coefficient"],
            "earnings": building["earnings"],
            "betterThanStaking": True,
            "quantity": 0,
        }
        if building["unlockCost"] == 0:
            buildingData["unlocked"] = True
        else:
            buildingData["unlocked"] = False
        buildings[building["name"]] = buildingData
    return buildings
