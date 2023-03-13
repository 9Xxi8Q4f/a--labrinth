import time
from tracemalloc import start
import numpy as np
import pygame

mazeX = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 2, 2, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 1, 0, 2, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
] 
# 0: free spaces; 1: walls (not free); 2: stations (apples)

class Node(): #current node, start node vs.. (all closed and open list)
    
    """
    A node class for A* algorithm path
    parent; parent of current node
    position; current node position
    g; cost func
    h; heuristic func
    f; total cost of node
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):

        """This is ID for nodes"""

        #equality is true if positions and heuristics is same
        return self.position == other.position and self.h == other.h

def path(current_node, maze):

    """when reached to goal, 
    getting the path to the goal,
    and movements it has made
    """

    path = []
    current = current_node

    while current is not None:
        #listing path backwards
        path.append(current.position)
        current = current.parent

    #returning reversed path 
    path = path[::-1]

    return path

#Heuristic func calculating:
def heuristic(child, apple_position):

    """
    The heuristic func is:
    furtherest station (apple) distance from current situation + 
    furherest station from the furtherest station
    """

    furthest_goal_from_pos = furthest_dist(apple_position, child)
    furthest_from_furthest_goal = furthest_dist(apple_position, furthest_goal_from_pos)
    dist_bw_furthest_goals = ((furthest_goal_from_pos[0] - furthest_from_furthest_goal[0])**2 + (furthest_goal_from_pos[1] - furthest_from_furthest_goal[1])**2)**0.5
    closer_goal, dist_to_closer_goal = nearest_goal(apple_position, child)
    final_heuristic_distance = dist_bw_furthest_goals + dist_to_closer_goal
    return final_heuristic_distance
        
def furthest_dist(goals, child):

        #finding by euklid
        list_of_dist = []
        for goal in goals:
            dist = ((child[0] - goal[0])**2 + (child[1] - goal[1])**2)**0.5
            list_of_dist.append((goal,dist))
        list_of_dist.sort(key = lambda x : x[1], reverse = True)
        goal, dist = list_of_dist[0]
        return goal

def nearest_goal(goals, child):

        list_of_dist = []
        for goal in goals:
            dist = ((child[0] - goal[0])**2 + (child[1] - goal[1])**2)**0.5
            list_of_dist.append((goal,dist))
        list_of_dist.sort(key = lambda x : x[1])
        goal, dist = list_of_dist[0]
        return goal, dist

#A* Main algorithm
def a_star(start_node, maze): 

    """
    An A* Search algorithm for given maze
    analising maze; finds the number and location of stations(apples)
    """
    maze=maze
    apples_position=[]
    numberof_apples = 0
    eaten_apples = 0

    #gets number of apples and their locations in map
    for idx, x in np.ndenumerate(np.array(maze)):
        if x==2:
            numberof_apples += 1
            apples_position.append(idx)

    #creating start node
    start_node = Node(parent=None,position=start_node)
    start_node.g = start_node.h = start_node.f = 0

    # Initialize both open and closed list
    open_list=[] #open nodes
    closed_list=[] #visited nodes
    # adding the start point as start node
    open_list.append(start_node)

    #setting moves
    move = [(-1,0),(0,-1),(1,0),(0,1)] #up, left, down, right
    rows, cloumns = np.shape(maze)

    while len(open_list) >0:

        #getting the current node
        current_node = open_list[0] #open list items is Node class!!
        current_idx = 0

        #by comparing f values of current nod to others in finge we select the node
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_idx = index

        #remove current from open list, add to closed list
        #by this approch closed_list show us visited nodes
        open_list.pop(current_idx)
        closed_list.append(current_node)

        for apple in apples_position:
            if current_node.position == apple:
                eaten_apples +=1
                apples_position.remove(apple)
                open_list = []

        if eaten_apples == numberof_apples:
            return path(current_node, maze), closed_list

        #looking for child nodes
        children = []
        for new_position in move:

            #getting node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            #checking if it's out of maze
            if (node_position[0] > (rows - 1) or
                node_position[0]< 0 or
                node_position[1] > (cloumns -1) or
                node_position[1 ] < 0):
                continue

            #chekking if it's a wall
            if maze[node_position[0]][node_position[1]] == 1:
                continue

            #creating out of our new node
            new_node = Node(parent=current_node, position=node_position)

            #add to children list
            children.append(new_node)

            #loop through children
            for child in children:
                # path cost (g) value
                child.g = current_node.g + 1

                # heuristic (h) value; basic heuristic (öklid ve manhattan)
                # h1=0

                # # h1: sum of distance to apples
                # for apple in apples_position:
                #     h1 += ((child.position[0] - apple[0])**2 + (child.position[1] - apple[1])**2)**0.5
                    
                heuristic_value = heuristic(child.position, apples_position)
                child.h = heuristic_value

                # f value
                child.f = child.g + child.h

                #child is in the closed list?? aynı noktadan geçmeyi engelliyor !!!!
                for closed_child in closed_list:

                    if child == closed_child:
                        continue

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child) 

def visualising(map):

    gridDisplay = pygame.display.set_mode((500, 500))
    pygame.display.get_surface().fill((200, 200, 200))  # background

    matrix = map
    # we use the sizes to draw as well as to do our "steps" in the loops. 
    grid_node_width = 50
    grid_node_height = 50

    def createSquare(x, y, color):
        pygame.draw.rect(gridDisplay, color, [x, y, grid_node_width, grid_node_height ])

    def visualizeGrid():
        y = 0  # we start at the top of the screen
        for row in matrix:
            x = 0 # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    createSquare(x, y, (255, 255, 255))
                elif item == 1:
                    createSquare(x, y, (0, 0, 0))
                elif item == 5:
                    createSquare(x, y, (0, 0, 255))
                elif item >9:
                    createSquare(x, y, (0, 255, item*2))
                   
                else:
                    createSquare(x, y, (255,0,0))

                x += grid_node_width # for ever item/number in that row we move one "step" to the right
            y += grid_node_height   # for every new row we move one "step" downwards
        pygame.display.update()


    visualizeGrid()  # call the function    
    time.sleep(5)
    pygame.display.quit()

def main():

    start_node = [0,9]

    maze_original = mazeX.copy()
    maze_original=np.array(maze_original)
    maze_original[start_node[0], start_node[1]] = 5

    maze_path = maze_original.copy()

    paths, closed_list = a_star(start_node=(start_node[0], start_node[1]), maze= mazeX)

    total_eat = 0
    apples_position = []
    numberof_apples = 0

    # kısım kaç elma yendi vs, geliştirilebilir
    for idx, x in np.ndenumerate(np.array(mazeX)):
        if x==2:
            numberof_apples += 1
            apples_position.append(idx)

    color_value = 10
    for path in paths:
        for apple in apples_position:
            if apple==path:
                total_eat +=1
                apples_position.remove(apple)
        maze_path[path[0], path[1]] = color_value
        color_value +=3

    #burda patika yolu döndürüyor. Patika yolunu takip ederek yaptığı hareketi bulabilirsin
    print("Patika yolu : \n", paths)
    print("number of apples : ", numberof_apples)
    print("number of eats : ", total_eat)
    print("uneaten apple : ", apples_position)

    print("visited list number of nodes : \n", len(closed_list))

    #visualising original maze and after path 

    print("haritanin ilk halini görüyorsunuz\n5 sn sonra patika yolunu çizdirecektir")
    visualising(maze_original)
    visualising(maze_path)

if __name__ == '__main__':
    main()
