from flask import Flask, render_template, request, jsonify
from graph import supermarket_graph, categories, get_coordinates
import itertools, heapq, math

app = Flask(__name__)

def heuristic(a, b):
    x1, y1 = get_coordinates(a)
    x2, y2 = get_coordinates(b)
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def a_star(graph, start, goal):
    queue = [(0 + heuristic(start, goal), 0, start, [start])]
    visited = set()
    while queue:
        _, cost, current, path = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            return path, cost
        for neighbor, dist in graph.get(current, []):
            if neighbor not in visited:
                new_cost = cost + dist
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(queue, (priority, new_cost, neighbor, path + [neighbor]))
    return None, float('inf')

def find_optimal_route(selected):
    start, end = "Pintu Masuk", "Kasir"
    if not selected:
        path, cost = a_star(supermarket_graph, start, end)
        return (list(dict.fromkeys(path)) if path else [], round(cost,1))
    min_cost, best = float('inf'), None
    for perm in itertools.permutations(selected):
        total_cost = 0
        path = [start]
        valid = True
        seg, c = a_star(supermarket_graph, start, perm[0])
        if seg:
            path.extend(seg[1:]); total_cost += c
        else:
            valid = False
        if not valid: continue
        for i in range(len(perm)-1):
            seg, c = a_star(supermarket_graph, perm[i], perm[i+1])
            if seg:
                path.extend(seg[1:]); total_cost += c
            else:
                valid = False; break
        if not valid: continue
        seg, c = a_star(supermarket_graph, perm[-1], end)
        if seg:
            path.extend(seg[1:]); total_cost += c
        else:
            continue
        if total_cost < min_cost:
            min_cost, best = total_cost, path
    return (list(dict.fromkeys(best)) if best else [], round(min_cost,1))

@app.route("/")
def index():
    return render_template("index.html", categories=categories)

@app.route("/compute", methods=["POST"])
def compute():
    selected = request.json.get("categories", [])
    route, distance = find_optimal_route(selected)
    return jsonify({"route": route, "distance": distance, "steps": route})

if __name__ == "__main__":
    app.run(debug=True)
