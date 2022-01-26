from datetime import datetime
import time
import configparser

import requests
from rich.console import Console
from rich.live import Live
from rich.table import Table

from mintopoly import get_rank


def generate_table(round: int, address: str, bearer: str) -> Table:
    """Make a new table."""
    rank = get_rank(round=round, address=address, bearer=bearer)
    table = Table(
        title="Mintopoly leaderboard",
        caption=f"Last updated: {datetime.now().strftime('%I:%M:%S %p')}",
    )
    table.add_column("Rank")
    table.add_column("Name")
    table.add_column("Networth")
    table.add_column("Forks")
    table.add_column("Fork (%)")
    table.add_column("Cash")
    table.add_column("Staked")
    table.add_column("Cash + Staked")
    table.add_column("Last stake")
    table.add_column("Earnings")
    table.add_column("Total block earnings")
    table.add_column("Networth Gap")
    startNumber = rank - 10
    if startNumber < 0:
        startNumber = 0
    leaderboardUrl = f"https://api.mintopoly.io/game/leaderboard?round={round}&sliceStart={startNumber}&sliceEnd={rank + 10}"
    response = requests.get(leaderboardUrl)
    data = response.json()
    for player in data:
        if player["player"]["address"].lower() == address.lower():
            myNetworth = player["netWorth"]
            break
    for player in data:
        rank = str(player["rank"])
        name = player["player"]["username"]
        forks = str(player["forks"]["number"])
        forkBonus = str(player["forks"]["bonus"] * 100)
        cash = str(player["cashOnHand"])[:10]
        earning = str(player["lastTally"]["earningsPerBlock"])[:10]
        staked = str(player["lastTally"]["stakedValue"])[:10]
        cashAndStaked = str(player["cashOnHand"] + player["lastTally"]["stakedValue"])
        networth = str(player["netWorth"])[:10]
        stakeGap = str(
            int(player["cashOnHand"] / player["lastTally"]["earningsPerBlock"])
        )
        netWorthGap = str(player["netWorth"] - myNetworth)[:10]
        totalEarnings = str(
            player["lastTally"]["earningsPerBlock"]
            + (player["lastTally"]["stakedValue"] / 5000)
        )[:10]
        if player["player"]["address"] == address:
            table.add_row(
                rank,
                name,
                networth,
                forks,
                forkBonus,
                cash,
                staked,
                cashAndStaked,
                stakeGap,
                earning,
                totalEarnings,
                netWorthGap,
                style="bold green",
            )
        else:
            table.add_row(
                rank,
                name,
                networth,
                forks,
                forkBonus,
                cash,
                staked,
                cashAndStaked,
                stakeGap,
                earning,
                totalEarnings,
                netWorthGap,
            )
    return table


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    round = config["LEADERBOARD"]["Round"]
    address = config["SECRETS"]["Address"]
    bearerToken = config["SECRETS"]["BearerToken"]
    with Live(
        generate_table(round=round, address=address, bearer=bearerToken),
        auto_refresh=False,
    ) as live:
        while True:
            time.sleep(60 * 3)
            live.update(
                generate_table(round=round, address=address, bearer=bearerToken),
                refresh=True,
            )


if __name__ == "__main__":
    main()
