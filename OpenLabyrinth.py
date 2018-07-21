from enum import Enum
from typing import Tuple
import numpy as np
import scipy.misc as smp
import matplotlib.pyplot as plt
from drawnow import drawnow

fig = plt.figure()

#  LRTA
class LiveMazeAgent(object):
    class Move(Enum):
        NORTH = (0, -1)
        SOUTH = (0, 1)
        WEST = (-1, 0)
        EAST = (1, 0)

    def __init__(self, pos: Tuple[int], maze: Tuple[Tuple[int]], goal: Tuple[int]):
        self.pos = pos
        self.maze = maze
        self.goal = goal
        self.learned_maze = dict()
        self.stopcost = (len(maze[0]) * len(maze[1]))/20

    def __repr__(self):
        return self.__str__

    def __str__(self):
        return str(self.pos)

    def euclidianDistToGoal(self, pos):
        return np.sqrt((self.goal[0] - pos[0])**2 + (self.goal[1] - self.pos[1])**2)

    def moveTo(self, pos):
        assert(pos in self.possibleMoves())
        self.pos = (pos[0], pos[1])
        if pos not in self.learned_maze:
            self.learned_maze[pos] = self.euclidianDistToGoal(pos)
        else:
            self.learned_maze[pos] = self.learned_maze[pos] + self.stopcost

    def score(self, pos):
        if pos not in self.learned_maze:
            return self.euclidianDistToGoal(pos)
        return self.learned_maze[pos]

    def predictMove(self, dir):
        newPos = (self.pos[0] + dir.value[0], self.pos[1] + dir.value[1])
        if (newPos[0] < 0 or newPos[0] > len(self.maze) or newPos[1] < 0 or newPos[1] > len(self.maze[newPos[0]])):
            return None
        if (not self.maze[newPos[0]][newPos[1]]):
            return None
        return newPos

    def possibleMoves(self):
        possibleMoves = list()
        for dir in self.Move:
            newMove = self.predictMove(dir)
            if (newMove is not None):
                possibleMoves.append(newMove)
        return possibleMoves

    def startAgent(self):
        self.maze[self.goal[0]][self.goal[1]] = 100
        i = 0
        while True:
            i += 1
            if self.pos == self.goal:
                print(i)
                break
            drawnow(self.updateImage)

            moves = self.possibleMoves()
            print(moves)
            bestMove = moves[0]
            for move in moves:
                if self.score(move) < self.score(bestMove):
                    bestMove = move

            if self.maze[bestMove[0]][bestMove[1]] > 10:
                self.maze[bestMove[0]][bestMove[1]] = self.maze[bestMove[0]][bestMove[1]] - 30
            self.moveTo(bestMove)
            print(bestMove)
        plt.show()

    def updateImage(self):
        mazeImage = smp.toimage(np.array(self.maze), mode="P")
        mazeImage = mazeImage.resize((200, 200))
        plt.axis('off')
        plt.imshow(mazeImage)



if __name__ == "__main__":
    start_location = (1, 1)
    goal = (16, 17)
    maze = (
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
            255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0),
        (0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0),
        (0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
            255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0),
        (0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255,
            255, 255, 255, 255, 255, 255, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0, 255, 0, 0, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255,
            0, 255, 255, 255, 255, 255, 0, 255, 255, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255,
            255, 255, 255, 0, 255, 255, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255,
            0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 255, 0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255,
            255, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255,
            0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255,
            255, 255, 255, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 0, 0, 0, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255,
            255, 255, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 0, 0, 0, 0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255,
            255, 0, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 0, 0, 255, 0, 255, 0, 0, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0),
        (0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 0,
            255, 255, 255, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
            255, 255, 255, 255, 255, 255, 0, 255, 0),
        (0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0),
        (0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
            255, 255, 255, 255, 255, 255, 255, 255, 255, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    print("BEGIN")
    listMaze = list()
    for row in maze:
        listMaze.append(list(row))
    agent = LiveMazeAgent(start_location, listMaze, goal)
    agent.startAgent()
    print("step cost: " + str(agent.stopcost))
