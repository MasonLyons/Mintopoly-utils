import time

import requests


def get_rank(round: int, address: str, bearer: str) -> int:
    rank = 0
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {bearer}",
    }
    while rank == 0:
        response = requests.get(
            f"https://api.mintopoly.io/game/round/{round}/player/{address}/rank",
            headers=headers,
        )
        data = response.json()
        rank = data["rank"]
        if rank != 0:
            return rank
        time.sleep(60)