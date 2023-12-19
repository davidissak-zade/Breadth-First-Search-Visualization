states_needed = set(["mt", "wa", "or", "id", "nv", "ut", "ca", "az"])

stations = {}
stations["kone"] = set(["id", "nv", "ut"])
stations["ktwo"] = set(["wa", "id", "mt"])
stations["kthree"] = set(["or", "nv", "ca"])
stations["kfour"] = set(["nv", "ut"])
stations["kfive"] = set(["ca", "az"])

answer = []  # a list of best stations to broadcast from
ReachedStates = set()  # a list of the states that are already reached

while ReachedStates != states_needed:
    biggestReach = 0
    biggestReachKey = None
    for station, statesReachedByStation in stations.items():
        reach = len(statesReachedByStation-ReachedStates)
        if reach > biggestReach:
            biggestReach = reach
            biggestReachKey = station
            answer.append(station)
            ReachedStates.update(stations[station])
        print("Adding station #" + station)
        print("Updated ReachedStates ", end=" -> ")
        print(ReachedStates)

# The key lies in defining the most valuable item to add (e.g. the radio that has the biggest reach of NEW!! (important) states)

print(answer)
print(ReachedStates)
