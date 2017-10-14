# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from captureAgents import CaptureAgent
import random, util
import util
from game import Directions
from util import nearestPoint

I_AM_SCARED_GHOST_ENEMY_CLOSE = 0
I_AM_ACTIVE_GHOST_ENEMY_CLOSE = 1
I_AM_POWERED_PACMAN_ENEMY_CLOSE = 2
I_AM_SIMPLE_PACMAN_ENEMY_CLOSE = 3
I_AM_SCARED_GHOST_ENEMY_FAR = 4
I_AM_ACTIVE_GHOST_ENEMY_FAR = 5
I_AM_PACMAN_ENEMY_FAR = 6

ans = []
ans.append('I_AM_SCARED_GHOST_ENEMY_CLOSE')
ans.append('I_AM_ACTIVE_GHOST_ENEMY_CLOSE')
ans.append('I_AM_POWERED_PACMAN_ENEMY_CLOSE')
ans.append('I_AM_SIMPLE_PACMAN_ENEMY_CLOSE')
ans.append('I_AM_SCARED_GHOST_ENEMY_FAR')
ans.append('I_AM_ACTIVE_GHOST_ENEMY_FAR')
ans.append('I_AM_PACMAN_ENEMY_FAR')


class myCustomAgent(CaptureAgent):
    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        print "StartState: " + str(self.start)
        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):
        # start = time.time() #for time evaluation

        actions = gameState.getLegalActions(self.index)
        values = [self.evaluate(gameState, a) for a in actions]
        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]
        a = self.getFoodCount(gameState)
        foodLeft = len(self.getFood(gameState).asList())
        if foodLeft <= 2:
            bestDist = 9999
            for action in actions:
                successor = self.getSuccessor(gameState, action)
                pos2 = successor.getAgentPosition(self.index)
                dist = self.getMazeDistance(self.start, pos2)
                if dist < bestDist:
                    bestAction = action
                    bestDist = dist
            return bestAction

        agent = ""
        if (self.index == 1):
            agent = "Dark Blue"
        else:
            agent = "Light Blue"  # index = 3

        print "chosen Action of Agent " + agent + ": " + random.choice(bestActions)
        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        # features = self.getFeatures(gameState, action)
        # weights = self.getWeights(gameState, action)
        # return features * weights
        myState = gameState.getAgentState(self.index)
        enemies = self.getOpponents(gameState)
        isEnemyScared = False

        if len(self.getEnemyLocations(gameState)) > 0:
            if not myState.isPacman:
                if myState.scaredTimer > 0:
                    return I_AM_SCARED_GHOST_ENEMY_CLOSE
                else:
                    return I_AM_ACTIVE_GHOST_ENEMY_CLOSE
            else:
                for enemyIndex in enemies:
                    if enemyIndex is not None and gameState.getAgentState(enemyIndex).scaredTimer > 0:
                        isEnemyScared = True
                        break
                if isEnemyScared:
                    return I_AM_POWERED_PACMAN_ENEMY_CLOSE
                else:
                    return I_AM_SIMPLE_PACMAN_ENEMY_CLOSE
        else:
            if not myState.isPacman:
                if myState.scaredTimer > 0:
                    return I_AM_SCARED_GHOST_ENEMY_FAR
                else:
                    return I_AM_ACTIVE_GHOST_ENEMY_FAR

        return I_AM_PACMAN_ENEMY_FAR

    #
    # def getFeatures(self, gameState, action):
    #     features = util.Counter()
    #     successor = self.getSuccessor(gameState, action)
    #     features['successorScore'] = self.getScore(successor)
    #     return features
    #
    # def getWeights(self, gameState, action):
    #     return {'successorScore': 1.0}

    def getLocation(self, gameState, action):
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        xPos, yPos = myState.getPosition()
        if (xPos <= self.start[0] / 2):
            return True
        else:
            return False

    # get the Enemy Position
    def getEnemyLocations(self, gameState):
        enemyLocation = []
        for enemyPlayers in self.getOpponents(gameState):
            location = gameState.getAgentPosition(enemyPlayers)
            if location != None:
                enemyLocation.append((enemyPlayers, location))
        return enemyLocation

    # Capsules that are the closest
    def getClosestCapsules(self, gameState):
        capsules = self.getCapsules(gameState)
        min = None
        closestCap = None
        if len(capsules) > 0:  # array has locations
            min = 9999  # random high dist
            myLoc = gameState.getAgentPosition(self.index)
            for coords in capsules:
                dist = self.getMazeDistance(coords, myLoc)
                if dist < min:
                    min = dist
                    closestCap = coords
        return closestCap

    # Enemies that are the closest
    def getClosestEnemies(self, gameState):
        location = self.getEnemyLocations(gameState)
        min = None
        if len(location) > 0:  # array has locations
            min = 9999  # random high dist
            myLoc = gameState.getAgentPosition(self.index)
            for enemy, coords in location:
                dist = self.getMazeDistance(coords, myLoc)
                if dist < min:
                    min = dist
        return min

    def PacmanInEnemyLoc(self, currentPlayer):
        return currentPlayer.isPacman

    def eatFood(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myLoc = self.getLocation(gameState, action)
        foodList = self.getFood(successor).asList()
        features['successorScore'] = -len(foodList)  # self.getScore(successor)
        self.getLocation(gameState, action)
        if len(foodList) > 0:
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
        return features

    def eatEnemy(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        myLoc = self.getLocation(gameState, action)

        features['onDefense'] = 1  # Computes whether we're on defense (1) or offense (0)
        if myState.isPacman: features['onDefense'] = 0

        # current Pacman
        currentPlayer = gameState.getAgentState(self.index)

        self.isScared(currentPlayer)  # isScared function
        self.PacmanInEnemyLoc(currentPlayer)  # is in Enemy Location function

        # Computes distance to invaders we can see
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        features['numInvaders'] = len(invaders)
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        closest = self.getClosestEnemies(gameState)
        if closest != None:
            print "Enemy detected"
        if action == Directions.STOP:
            features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev:
            features['reverse'] = 1

        return features


        # ********************** for A Star ********************

    def nullHeuristic(state, problem=None):
        return 0

    def aStarSearch(problem, heuristic=nullHeuristic):
        """Question 4"""
        Queue_Astar = util.PriorityQueue()
        currentStateXY = problem.getStartState()
        currentStateAction = []
        currentStateCost = 0
        Queue_Astar.push([currentStateXY, currentStateAction, currentStateCost], heuristic(currentStateXY, problem))
        visited = []

        while not Queue_Astar.isEmpty():
            currentState = Queue_Astar.pop()
            currentStateXY = currentState[0]
            currentStateAction = currentState[1]
            currentStateCost = currentState[2]
            if problem.isGoalState(currentStateXY):
                return currentStateAction

            if currentStateXY not in visited:
                visited.append(currentStateXY)
                successors = problem.getSuccessors(currentStateXY)
                for children in successors:
                    currentStateXY = children[0]
                    currentDir = children[1]
                    currentChildCost = children[2]

                    allActions = currentStateAction + [currentDir]
                    gN = problem.getCostOfActions(allActions)
                    hN = heuristic(currentStateXY, problem)
                    AStarTotalCost = gN + hN
                    Queue_Astar.push((currentStateXY, allActions, gN), AStarTotalCost)
        return []

        # ********************** for A Star END ********************

    def getClosestFood(self, foodList, position):
        closestFood = -1
        FoodPos = -1
        for food in foodList:
            currFoodDist = self.getMazeDistance(food, position)
            if closestFood is 0 or currFoodDist < closestFood:
                FoodPos = food
                closestFood = currFoodDist
        return (FoodPos, closestFood)

    def getFoodCount(self, gameState):
        foodCount = len(self.getFood(gameState).asList())
        return foodCount

    def whoAmI(self, gameState):
        """
        It returns global variable values and finds in which situation agent is
        :param gameState:
        :return:
        """
        myState = gameState.getAgentState(self.index)
        enemies = self.getOpponents(gameState)
        isEnemyScared = False

        if len(self.getEnemyLocations(gameState)) > 0:
            if not myState.isPacman:
                if myState.scaredTimer > 0:
                    return I_AM_SCARED_GHOST_ENEMY_CLOSE
                else:
                    return I_AM_ACTIVE_GHOST_ENEMY_CLOSE
            else:
                for enemyIndex in enemies:
                    if enemyIndex is not None and gameState.getAgentState(enemyIndex).scaredTimer > 0:
                        isEnemyScared = True
                        break
                if isEnemyScared:
                    return I_AM_POWERED_PACMAN_ENEMY_CLOSE
                else:
                    return I_AM_SIMPLE_PACMAN_ENEMY_CLOSE
        else:
            if not myState.isPacman:
                if myState.scaredTimer > 0:
                    return I_AM_SCARED_GHOST_ENEMY_FAR
                else:
                    return I_AM_ACTIVE_GHOST_ENEMY_FAR

        return I_AM_PACMAN_ENEMY_FAR

    def getFoodDiff(self, gameState):
        toEatFoodCount = len(self.getFood(gameState).asList())
        toDefendFoodCount = len(self.getFoodYouAreDefending(gameState).asList())
        foodDiff = toEatFoodCount - toDefendFoodCount
        return foodDiff

    def isScared(self, currentPlayer):
        if currentPlayer.scaredTimer > 0:
            return True
        else:
            return False

