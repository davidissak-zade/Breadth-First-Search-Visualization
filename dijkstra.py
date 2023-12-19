graph = {}
# establishing another hash table (dictionary) within the graph to keep the weights too
graph["start"] = {}
graph["start"]["a"] = 6
graph["start"]["b"] = 2

graph["a"] = {}
graph["a"]["fin"] = 1

graph["b"] = {}
graph["b"]["a"] = 3
graph["b"]["fin"] = 5

costs = {}
infinity = float('inf')
costs["a"] = 6
costs["b"] = 2
costs["fin"] = infinity


parents = {}
parents["a"] = "start"
parents["b"] = "start"
parents["fin"] = None

processed = []


def find_lowest_cost_node(costs):
    lowest_cost = float("inf")
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node


def dijkstra(graph, costs, parents):
    processed = []
    # Find the closest node to the start node
    node = find_lower_cost_node(costs)
    while node is not None:  # seems like this will go on forevergr
        cost = costs[node]
        neighbors = graph[node]
        for neighbor in neighbors:
            if cost < costs[neighbor]:  # Update cost and parent for this neighbor
                costs[neighbor] = cost
                parents[neighbor] = node
        processed.append(node)
        node = find_lowest_cost_node(costs)

# Not the best interpretation.
