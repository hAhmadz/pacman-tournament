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
        self.collectedFoods = 0.0

        self.lastEatenFood = None
        self.numCapsules = len(self.getCapsules(gameState))
        self.deadLockLength = 2 * max(gameState.data.layout.width, gameState.data.layout.height)
        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):
        # time.sleep(0.3)
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
        opponents = self.getOpponents(gameState)
        successor = self.getSuccessor(gameState, action)
        invaders = [agent for agent in opponents if successor.getAgentState(agent).isPacman]

        myState = gameState.getAgentState(self.index)

        self.updateLastEatenFood(gameState)

        if len(self.getEnemyLocations(gameState)) > 0 and not myState.isPacman and myState.scaredTimer == 0:
            """
            If agent is active ghost and enemy is close, defend
            """
            self.lastEatenFood = None
            return self.eatEnemy(gameState, action)
        elif len(invaders) > 0:
            """
            If someone crossed to our area and tries to eat our food, back to own area
            """
            return self.backToDefend(gameState, action)

        return self.eatFood(gameState, action)

    def eatFood(self, gameState, action):
        print "eat Food"
        # Provide feature
        successor = self.getSuccessor(gameState, action)
        width = gameState.data.layout.width
        height = gameState.data.layout.height

        features, weights = self.initFeaturesWeights(gameState, action)

        foodList = self.getFood(successor).asList()
        features['successorScore'] = self.getScore(successor)  # self.getScore(successor)
        weights.update({'successorScore': 800})
        myPos = successor.getAgentState(self.index).getPosition()

        # Check how many foods we ate as our food count increases, try to go back to starting position
        # features['startingDistance'] = self.getMazeDistance(myPos, self.start) * flag

        if len(foodList) > 0:
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
            features['eatFood'] = 100 * self.getScore(successor) - len(foodList)
            weights.update({'eatFood': 4000, 'distanceToFood': -10})

        # If there is a reason to warning
        minDistEnemy = self.getClosestEnemiesDist(successor)
        if (minDistEnemy != None):
            if (minDistEnemy <= 2):
                features['warning'] = 4 / minDistEnemy
            elif (minDistEnemy <= 4):
                features['warning'] = 1
            else:
                features['warning'] = 0
            weights.update({'warning': -1000})

        # How close to the power capsule
        powerCapsules = self.getCapsules(successor)
        if (len(powerCapsules) > 0):
            minCapsuleDist = min([self.getMazeDistance(myPos, powerCapsule) for powerCapsule in powerCapsules])
            features['collectPowerCapsule'] = -len(powerCapsules)
        else:
            minCapsuleDist = .1
        features['powerCapsuleDist'] = 1.0 / minCapsuleDist
        weights.update({'collectPowerCapsule': 5000, 'powerCapsuleDist': 700})

        if successor.getAgentState(self.index).isPacman:
            switch = 1.0
        else:
            switch = 0.0
        # If I am eating food from opposite side
        if myPos in self.getFood(gameState).asList():
            self.collectedFoods += 1.0
        if switch == 0.0:
            self.collectedFoods = 0.0
        features['collectedFood'] = self.collectedFoods * (min([self.distancer.getDistance(myPos, pos) for pos
                 in [(width / 2, i) for i
                     in range(1, height) if not gameState.hasWall(width / 2, i)]])) * switch
        # If I need to drop the food
        features['deposit'] = self.collectedFoods * switch
        weights.update({'collectedFood': -20, 'deposit': 100})

        # Is powered heuristic
        if self.powerTimer > 0:
            features['powered'] = self.powerTimer / capture.SCARED_TIME
            features['collectedFood'] = 0.0
            features['eatFood'] = 100 * features['eatFood']
        else:
            features['powered'] = 0.0
        weights.update({'powered': 5000000})

        # Distance to the partner
        if successor.getAgentState(self.index).isPacman:
            partnerDistance = self.maintainPartnerDistance(successor)
            # distanceToAgent is always None for one of the agents (so they don't get stuck)
            if partnerDistance is not None:
                features['partnerDistance'] = 1.0 / partnerDistance
                weights.update({'partnerDistance': -6000})

        features['isDeadLock'] = self.isDeadLock(gameState, action)
        weights.update({'partnerDistance': -200})

        # We shouldn't stop in most cases
        if action == Directions.STOP:
            features['stop'] = 1.0
        else:
            features['stop'] = 0.0
        weights.update({'stop': -1000})

        return self.dotProduct(features, weights)



    def eatEnemy(self, gameState, action):
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myLoc = myState.getPosition()
        features, weights = self.initFeaturesWeights(gameState, action)


        # features['onDefense'] = 1  # Computes whether we're on defense (1) or offense (0)
        # weights.update({'onDefense': -10})

        allEnemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        attackerEnemy = [a for a in allEnemies if a.isPacman and a.getPosition() != None]
        features['numAttacker'] = len(attackerEnemy)
        if len(attackerEnemy) > 0:
            dists = [self.getMazeDistance(myLoc, a.getPosition()) for a in attackerEnemy]
            features['attackerDistance'] = min(dists)
        weights.update({'numAttacker': -200, 'attackerDistance': -20})

        #strategise based on direction of enemy action
        if action == Directions.STOP:
            features['stop'] = 1
            weights.update({'stop': -10000})

        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev:
            features['reverse'] = 1
            weights.update({'reverse': -10000})

        #Strategise based on distance to team memeber
        if self.pacmanInEnemyLoc(myState):
            partnerDist = self.maintainPartnerDistance(gameState)
            if partnerDist != 0:
                features['partnerDist'] = 1
                weights.update({'partnerDist': -5000})

        return self.dotProduct(features, weights)

    def backToDefend(self, gameState, action):
        currentPlayer = gameState.getAgentState(self.index)
        enemies = self.getOpponents(gameState)
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        features, weights = self.initFeaturesWeights(gameState, action)
        # features['onDefense'] = 1  # Computes whether we're on defense (1) or offense (0)
        # weights.update({'onDefense': -10})

        #identifies close enemies. brk
        closeEnemies = [en for en in enemies if successor.getAgentState(en).isPacman]

        features['closeEnemies'] = len(closeEnemies)

        if action == Directions.STOP:
            features['stop'] = 1
        rev = Directions.REVERSE[currentPlayer.configuration.direction]
        if action == rev:
            features['reverse'] = 1

        #identifies known locations of enemies based on last food eaten.
        if self.lastEatenFood is not None:
            features['knownFarEnemy'] = self.getMazeDistance(myPos, self.lastEatenFood)
            weights.update({'knownFarEnemy': -10})

        #identify distance to teammate
        if self.pacmanInEnemyLoc(myState):
            partnerDist = self.maintainPartnerDistance(gameState)
            if partnerDist != 0:
                features['partnerDist'] = 1

        weights.update({'stop': -5000, 'reverse': -5000,
                        'closeEnemies': -100,'partnerDist': -2500})
        return self.dotProduct(features, weights)

    def initFeaturesWeights(self, gameState, action):
        features = util.Counter()
        weights = {}
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
    def getClosestEnemiesDist(self, gameState):
        location = self.getEnemyLocations(gameState)
        min = 99999
        if len(location) > 0:  # array has locations
            myLoc = gameState.getAgentPosition(self.index)
            for enemy, coords in location:
                dist = self.getMazeDistance(coords, myLoc)
                if dist < min:
                    min = dist
        return min

    def getClosestEnemies(self, gameState):
        closeEnemies = []
        enemies = self.getOpponents(gameState)
        for enemyIndex in enemies:
            enemy = gameState.getAgentState(enemyIndex)
            if gameState.getAgentState(enemyIndex) is not None:
                closeEnemies.append(enemyIndex)
        return closeEnemies

    def pacmanInEnemyLoc(self, currentPlayer):
        return currentPlayer.isPacman

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
            return 0.0

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
                return 0.0
        return 1.0

    """
    returns the minimum distance between a team
    #Only assigns distance calc responsibility to one agent
    Returns None if agent index == first index
    else returns min distance    
    """
    def maintainPartnerDistance(self, gameState):
        currPlayer = gameState.getAgentState(self.index)
        teammate = None
        totalDist = 999999

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
        min = 0
        if len(ApproxDistances) > 0:
            min = 9999
            myLoc = gameState.getAgentPosition(self.index)
            for enemyAgents in enemies:
                dist = ApproxDistances[enemyAgents]
                if dist < min:
                    min = dist
        return 0

    def updateLastEatenFood(self, gameState):
        oldState = self.getPreviousObservation()
        # if oldState is not None:
        #     oldEnemies = self.getClosestEnemies(oldState)
        currentEnemies = self.getClosestEnemies(gameState)
        #     eatenEnemies = list(set(oldEnemies) - set(curentEnemies))
        #     if len(eatenEnemies) > 0:
        #         self.lastEatenFood = None

        if oldState is not None:
            oldFoods = self.getFoodYouAreDefending(oldState).asList()
            currentFoods = self.getFoodYouAreDefending(gameState).asList()

            eaten = list(set(oldFoods) - set(currentFoods))
            if len(eaten) > 0 and len(currentEnemies) == 0:
                self.lastEatenFood = eaten[0]

            # oldEnemies = self.getClosestEnemies(oldState)
            # curentEnemies = self.getClosestEnemies(gameState)
            # eatenEnemies = list(set(oldEnemies) - set(curentEnemies))
            # if len(eatenEnemies) > 0:
            #     self.lastEatenFood = None


        # elif eatenEnemies:
        #     self.lastEatenFood = None

            # enemies = self.getClosestEnemies(gameState)
        # for enemyIndex in enemies:
        #     if self.pacmanInEnemyLoc(enemyIndex):
        #         self.lastEatenFood = ()

    # def runOut(self, gameState, action, closeEnemies):
    #     print "runout is running"
    #     # time.sleep(0.5)
    #     # Provide feature
    #     features = util.Counter()
    #     successor = self.getSuccessor(gameState, action)
    #     myState = successor.getAgentState(self.index)
    #     myPos = myState.getPosition()
    #     features, weights = self.initFeaturesWeights(gameState, action)
    #
    #     for enemyIndex in closeEnemies:
    #         enemyPos = gameState.getAgentState(enemyIndex).getPosition()
    #         if enemyPos is not None:
    #             features['enemyDistance'] += self.getMazeDistance(myPos, enemyPos)
    #
    #     features['numEnemies'] = len(closeEnemies)
    #     # features['isDeadLock'] = self.isDeadLock(gameState, action)
    #     # print action, features['isDeadLock']
    #
    #     #  Provide weight
    #     weights.update({'enemyDistance': 8000, 'numEnemies': -10000})#, 'isDeadLock': -1000000})
    #
    #     return self.dotProduct(features, weights)