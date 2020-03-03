# from implementation import *
from graph import *
def heuristic(a, b):
    # w = math.sqrt((a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1]))
    (x1, y1) = a
    (x2, y2) = b
    w = abs(x1 - x2) + abs(y1 - y2)
    return round(w,2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    has_been_next = []

    open_list = []
    close_list = []
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        print(f'#########current = {current}')
        for next in graph.neighbors(current):
            

            if next not in came_from:
                print(f'next={next}')
                if next not in has_been_next:
                    has_been_next.append(next)

                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
    
    print(f'has_been_next = {has_been_next}')

    return came_from, cost_so_far


def construct_path(pdict, plist):
    path = []
    for pos in plist:
        path.append(pdict[pos])
    return path
