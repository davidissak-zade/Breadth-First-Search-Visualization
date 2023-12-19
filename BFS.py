import pygame
from collections import deque
pygame.init()

TEXT_COLLOR = (30, 250, 10)
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption('BFS')


# Adding a label
font = pygame.font.Font("freesansbold.ttf", 20)
# creating a textholder object
text = font.render('BFS Visualization', True, TEXT_COLLOR)
# making the textholder rectangular
textRect = text.get_rect()

# setting the position for the textholder
textRect.center = (360, 25)
screen.blit(text, textRect)


text = font.render('Run!', True, TEXT_COLLOR)
textRect2 = text.get_rect()
textRect2.center = (600, 25)
screen.blit(text, textRect2)
# GoButton = pygame.Rect(self.pos[0], self.pos[1], 40, 40)
# pygame.draw.rect(screen, (255, 255, 255), rect=CELL, width=2)


# Now, I will create two buttons in the bottom to choose between BFS and DFS
BFS = True
DFS = False


class Node:
    def __init__(self, id):
        self.id = id
        self.obstacle = False
        self.explored = False
        self.parent = None
        self.pos = self.getCoordinatesByID()
        self.neighbors = None   # Will be updated to geNeighborsByID after reating the obsta

        CELL = pygame.Rect(self.pos[0], self.pos[1], 40, 40)
        pygame.draw.rect(screen, (255, 255, 255), rect=CELL, width=2)

    def getNeighborsByID(self):  # returns a list of neighbor's IDs for this node
        # Getting Vertical(matrix-wise) neighbors
        posy = self.id // 16
        posx = self.id % 16
        # general neighbor checking algorithm
        neighbors = [self.id-16, self.id+1,
                     self.id+16, self.id-1]  # clockwise

        # reducing the neighbors for edge cells
        if posx == 0:
            neighbors[3] = None
        elif posx == 15:
            neighbors[1] = None
        if posy == 0:
            neighbors[0] = None
        elif posy == 15:
            neighbors[2] = None

        neighborsNodes = [cells[neighbor]
                          for neighbor in neighbors if neighbor is not None]

        filteredNeighbors = list(
            filter(lambda x: False if x is None or x.obstacle else True, neighborsNodes))
        return filteredNeighbors

    # posx and posy are the coordinates of the node in 16x16 grid, not the xy on the screen plane

    def getCoordinatesByID(self):
        posy = self.id // 16
        posx = self.id % 16
        Y = 50 + posy*40
        X = 40 + posx * 40
        return (X, Y)

    def FillColor(self, color):
        CELL = pygame.Rect(self.pos[0]+2, self.pos[1]+2, 36, 36)
        pygame.draw.rect(screen, color, rect=CELL, width=0)
        pygame.display.flip()


def SetStart(ClickPosition):
    posx = ClickPosition[0] // 40 - 1
    posy = ClickPosition[1] // 40 - 1
    CellID = posy * 16 + posx
    cells[CellID].FillColor((0, 255, 0))
    return CellID


def SetFinish(ClickPosition):
    posx = ClickPosition[0] // 40 - 1
    posy = ClickPosition[1] // 40 - 1
    CellID = posy * 16 + posx
    cells[CellID].FillColor((255, 0, 0))
    return CellID


def CreateObstacle(ClickPosition):
    posx = ClickPosition[0] // 40 - 1
    posy = ClickPosition[1] // 40 - 1
    CellID = posy * 16 + posx
    if posx >= 0 and posx <= 63 and posy >= 0 and posy <= 63:
        cells[CellID].FillColor((155, 150, 150))
    cells[CellID].obstacle = True


graph = {}   # graph[node1] will return the list of the neighbors for node1
cells = []   # this list contains all of the cells
ExploredNodes = []
NodesToExplore = deque()
StartNodeID = None
FinishNodeID = None


for i in range(256):
    node = Node(i)
    cells.append(node)


pygame.display.flip()
running = True
START_SET = False
FINISH_SET = False
STAGE_SET = False
PATHNOTFOUND = True
FINISHED = False
# loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and not STAGE_SET:
            ClickPosition = pygame.mouse.get_pos()
            clickx, clicky = ClickPosition[0], ClickPosition[1]
            print(ClickPosition)
            if START_SET and not FINISH_SET:
                FinishNodeID = SetFinish(ClickPosition)
                print("Cell #{startnode} is declared as a finish node".format(
                    startnode=FinishNodeID))
                FINISH_SET = True
                print("FINISH SET")

            if not START_SET:
                StartNodeID = SetStart(ClickPosition)
                print("Cell #{startnode} is declared as a start node".format(
                    startnode=StartNodeID))
                NodesToExplore.append(cells[StartNodeID])
                cells[StartNodeID].explored = True
                START_SET = True
                print("START SET")

            if clickx > 578 and clickx < 620 and clicky > 13 and clicky < 32 and START_SET and FINISH_SET and not STAGE_SET:
                STAGE_SET = True
                for cell in cells:
                    if not cell.obstacle:
                        cell.neighbors = cell.getNeighborsByID()
                        graph[cell.id] = cell.neighbors
                print('run!')

        if event.type == pygame.MOUSEMOTION and START_SET and FINISH_SET and not STAGE_SET:
            if pygame.mouse.get_pressed()[0]:
                ClickPosition = pygame.mouse.get_pos()
                CreateObstacle(ClickPosition)

        if STAGE_SET and not FINISHED:  # when algorithm was done we will set STAGE_SET to false again so that this block of code will only run once
            while bool(NodesToExplore) and PATHNOTFOUND:
                #  explore
                # Get the first element of the queue
                node = NodesToExplore.popleft()
                if node.id == FinishNodeID:
                    print("Reached goal node #{}".format(node.id))
                    node.explored = True
                    PATHNOTFOUND = True
                    FINISHED = True

                    # Trace back to the beginning
                    while node.id != StartNodeID:
                        node.FillColor((25, 25, 255))
                        node = node.parent
                    node.FillColor((25, 25, 255))

                    break  # Once reached the final node
                node.explored = True
                node.FillColor((63, 220, 23))
                for neighbor in node.neighbors:
                    if not neighbor.explored:
                        neighbor.parent = node
                        NodesToExplore.append(neighbor)
                        neighbor.FillColor((255, 255, 51))
            FINISHED = True
            print("All possible nodes explored.")

        elif event.type == pygame.QUIT:
            running = False
