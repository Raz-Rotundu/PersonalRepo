# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # TODO: Read teams into memory from file
    with open(sys.argv[1], "r") as file:
        # read in each line
        for line in csv.DictReader(file):
            # update each line to have its value to be the int version of its original value
            line.update({'rating': int(line.get('rating'))})
            # append it to the list of teams
            teams.append(line)

    # {"name": number of wins}
    counts = {}

    # TODO: Simulate N tournaments and keep track of win counts
    for i in range(N):
        winner = simulate_tournament(teams)
        if winner in counts:
            counts[winner] = counts[winner] + 1
        else:
            counts.update({winner: 1})

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # teams =  a list of dictionaries({"name": rating})
    # TODO
    remaining = teams
    while len(remaining) > 1:
        remaining = simulate_round(remaining)
    # this is a dict{"team": name, "rating": num}
    winnerDict = remaining[0]
    winnerName = winnerDict['team']
    return winnerName


if __name__ == "__main__":
    main()
