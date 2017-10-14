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
import random, capture
import util
from game import Directions
from util import nearestPoint
import time


def createTeam(firstIndex, secondIndex, isRed, first='myCustomAgent', second='myCustomAgent'):
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

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
        self.powerTimer = 0
        self.numCapsules = len(self.getCapsules(gameState))
        self.deadLockLength = 2 * max(gameState.data.layout.width, gameState.data.layout.height)
        # print "StartState: " + str(self.start)
        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):
        # start = time.time() #for time evaluation

        myState = gameState.getAgentState(self.index)

        if len(self.getCapsules(gameState)) < self.numCapsules:
            self.numCapsules = len(self.getCapsules(gameState))
            self.powerTimer = capture.SCARED_TIME - 1

        if self.powerTimer > 0:
            self.powerTimer = self.powerTimer - 1

        actions = gameState.getLegalActions(self.index)
        values = [self.evaluate(gameState, a) for a in actions]
        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]
        a = self.getFoodCount(gameState)
        foodLeft = len(self.getFood(gameState).asList())

        dist = self.getClosestApproximateDistance(gameState)
        print dist

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

        # print "chosen Action of Agent " + agent + ": " + random.choice(bestActions)
        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        It returns dot product of features and weight values and finds in which situation agent is
        :param gameState:
        :return:
        """
        myState = gameState.getAgentState(self.index)

        enemies = self.getOpponents(gameState)
        closeEnemies = []

        if len(self.getEnemyLocations(gameState)) > 0:
            if not myState.isPacman:
                if myState.scaredTimer > 0:
                    """
                    return I_AM_SCARED_GHOST_ENEMY_CLOSE
                    """
                    return self.eatFood(gameState, action)
                else:
                    """
                    if enemy in own area:
                        #get closer to enemy while staying in your area
                    elif
                        eatEnemy(gameState,action)

                    #return I_AM_ACTIVE_GHOST_ENEMY_CLOSE
                    """
                    return self.eatEnemy(gameState, action)
            else:
                for enemyIndex in enemies:
                    if enemyIndex is not None and gameState.getAgentState(enemyIndex).scaredTimer > 0:
                        closeEnemies.append(enemyIndex)
                    elif enemyIndex is not None:
                        self.powerTimer = 0
                if self.isPoweredPacman():
                    """
                    #return I_AM_POWERED_PACMAN_ENEMY_CLOSE
                    """
                    # if self.getMazeDistance() enemy is < 2 maze Distance away:
                    #     eat Enemy
                    # else:
                    return self.eatFood(gameState, action)

                else:
                    """
                    if enemy is < 5 maze Distance away
                        run to own side
                    else
                        run to closest food
                    #return I_AM_SIMPLE_PACMAN_ENEMY_CLOSE
                    """
                    if self.powerTimer > 0:
                        return self.eatFood(gameState, action)
                    else:
                        return self.runOut(gameState, action, closeEnemies)
        else:
            if not myState.isPacman:
                if myState.scaredTimer > 0:
                    """
                    self.eatFood(gameState,action)
                    #return I_AM_SCARED_GHOST_ENEMY_FAR
                    """
                    return self.eatFood(gameState, action)
                else:
                    """
                    if Last food is eaten
                        Add position to global variable and run after that location
                    else
                        Apply advanced algo and do from the following:
                            1. go to nearest food (become the pacman)
                            2. check if partner needs help

                    #return I_AM_ACTIVE_GHOST_ENEMY_FAR
                    """
                    return self.eatFood(gameState, action)

        """
        self.eatFood(gameState,action)
        #return I_AM_PACMAN_ENEMY_FAR
        """
        return self.eatFood(gameState, action)

    def eatFood(self, gameState, action):
        # Provide feature
        successor = self.getSuccessor(gameState, action)
        features, weights = self.initFeaturesWeights(gameState, action)

        foodList = self.getFood(successor).asList()
        features['successorScore'] = -len(foodList)  # self.getScore(successor)
        self.getLocation(gameState, action)
        if len(foodList) > 0:
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        # Provide weight
        weights.update({'successorScore': 100, 'distanceToFood': -1})

        return self.dotProduct(features, weights)

    def eatEnemy(self, gameState, action):
        # Provide feature
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        features, weights = self.initFeaturesWeights(gameState, action)

        features['onDefense'] = 1  # Computes whether we're on defense (1) or offense (0)
        if myState.isPacman: features['onDefense'] = 0

        # current Pacman
        currentPlayer = gameState.getAgentState(self.index)

        # Computes distance to invaders we can see
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        features['numInvaders'] = len(invaders)
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        closest = self.getClosestEnemies(gameState)
        # if closest != None:
        #     print "Enemy detected"
        if action == Directions.STOP:
            features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev:
            features['reverse'] = 1

        # Provide weight
        weights.update({'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2})

        return self.dotProduct(features, weights)

    def runOut(self, gameState, action, closeEnemies):
        # time.sleep(0.5)
        # Provide feature
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        features, weights = self.initFeaturesWeights(gameState, action)

        for enemyIndex in closeEnemies:
            enemyPos = gameState.getAgentState(enemyIndex).getPosition()
            if enemyPos is not None:
                features['enemyDistance'] += self.getMazeDistance(myPos, enemyPos)

        features['numEnemies'] = len(closeEnemies)
        features['isDeadLock'] = self.isDeadLock(gameState, action)
        # print action, features['isDeadLock']

        #  Provide weight
        weights.update({'enemyDistance': 500, 'numEnemies': 500, 'isDeadLock': -100})

        return self.dotProduct(features, weights)

    def initFeaturesWeights(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # We should negatively reward Stop action
        if action == Directions.STOP:
            features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]

        # We should negatively reward reverse action
        if action == rev:
            features['reverse'] = 1
        weights = {'stop': -100, 'reverse': -20}

        # we should positively reward the distance between two partners

        return (features, weights)

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

    def getFoodDiff(self, gameState):
        toEatFoodCount = len(self.getFood(gameState).asList())
        toDefendFoodCount = len(self.getFoodYouAreDefending(gameState).asList())
        foodDiff = toEatFoodCount - toDefendFoodCount
        return foodDiff

    def isScared(self, currentPlayer):
        return currentPlayer.scaredTimer > 0

    def dotProduct(self, features, weights):
        return features * weights

    def isPoweredPacman(self):
        return self.powerTimer > 0

    def getAgentPosition(self, currentPlayer):  # currentPlayer = gameState.getAgentState(self.index)
        return currentPlayer.getPosition()

    def getDistances(self, gameState):  # returns the noisy distances
        return gameState.getAgentDistances()

    def isDeadLock(self, gameState, action):
        """
        run this method only if action is not stop, True otherwise
        :param gameState:
        :param action:
        :return:
        """
        if action == Directions.STOP:
            return 0

        depth = self.deadLockLength

        visited = set()
        myPos = gameState.getAgentState(self.index).getPosition()
        visited.add(myPos)

        successor = self.getSuccessor(gameState, action)
        queue = util.Queue()
        queue.push(successor)

        while not queue.isEmpty():
            currentState = queue.pop()
            myPos = currentState.getAgentState(self.index).getPosition()

            # Check if pacman already visited this state
            if myPos not in visited:
                visited.add(currentState)
                depth = depth - 1

                for action in currentState.getLegalActions(self.index):
                    if action != Directions.STOP:
                        newState = self.getSuccessor(currentState, action)
                        newPos =  newState.getAgentState(self.index).getPosition()
                        if newPos not in visited:
                            queue.push(newState)
            if depth <= 0:
                return 0
        return 1

    """
    returns the minimum distance between a team
    #Only assigns distance calc responsibility to one agent
    Returns None if agent index == first index
    else returns min distance    
    """
    def maintainPartnerDistance(self, gameState):
        currPlayer = gameState.getAgentState(self.index)
        teammate = None
        totalDist = None

        if self.index != self.getTeam(gameState)[0]: #Index calculation
            teammate = self.getTeam(gameState)[0]
            myLocation = self.getAgentPosition(currPlayer)
            teamMateLocation = gameState.getAgentState(teammate).getPosition()

            totalDist = self.getMazeDistance(myLocation, teamMateLocation)

            # putting in a minimum distance if both are together
            if totalDist == 0:
                totalDist = 0.1

        return totalDist

    def getClosestApproximateDistance(self, gameState):
        enemies = self.getOpponents(gameState)
        ApproxDistances = gameState.getAgentDistances()
        min = None
        if len(ApproxDistances) > 0:
            min = 9999
            myLoc = gameState.getAgentPosition(self.index)
            for enemyAgents in enemies:
                dist = ApproxDistances[enemyAgents]
                if dist < min:
                    min = dist
        return min