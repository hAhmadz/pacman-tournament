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
from util import nearestPoint

class myCustomAgent(CaptureAgent):

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    print "StartState: " + str(self.start)
    CaptureAgent.registerInitialState(self, gameState)


  def chooseAction(self, gameState):
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

    agent = ""
    if(self.index == 1):
      agent = "Dark Blue"
    else:
      agent = "Light Blue" #index = 3


    print "chosen Action of Agent " + agent + ": " + random.choice(bestActions)
    return random.choice(bestActions)

  def heuristic(self, state, problem):
    # position, foodGrid = state
    # food = foodGrid.asList()
    position = state.getAgentPosition(self.index)
    food = self.getFood(state).asList()
    walls = problem.walls

    heur = 0
    c = None
    for fd in food:
      # x = distances[fd][position]
      x = self.getMazeDistance(fd, position)
      if c == None or x < self.getMazeDistance(c, position): c = fd
    if c == None: return heur
    # heur = distances[c][position]
    heur = self.getMazeDistance(c, position)
    if len(food) > 1:
      for fd in food:
        if fd != c:
          closest = 99999
          for nxt in food:
            dist = self.getMazeDistance(fd, nxt)
            # dist = distances[fd][nxt]
            if nxt != fd and dist < closest:
              closest = dist
          heur += closest
    return heur

  def getSuccessor(self, gameState, action):
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      return successor.generateSuccessor(self.index, action)
    else:
      return successor


  def evaluate(self, gameState, action):
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights


  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 1.0}

  def getLocation(self,gameState, action):
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    xPos,yPos= myState.getPosition()
    if(xPos <= self.start[0]/2):
        return True
    else:
        return False


  #get the Enemy Position
  def getEnemyLocations(self, gameState):
    enemyLocation = []
    for enemyPlayers in self.getOpponents(gameState):
      location = gameState.getAgentPosition(enemyPlayers)
      if location != None:
        enemyLocation.append((enemyPlayers, location))
    return enemyLocation

  def getClosestCapsules(self, gameState):
    capsule = self.getCapsules(gameState)

  #Enemies that are the closest
  def getClosestEnemies(self, gameState):
    location = self.getEnemyLocations(gameState)
    min = None
    if len(location) > 0: #array has locations
      min = 9999 #random high dist
      myLoc = gameState.getAgentPosition(self.index)
      for enemy, coords in location:
        dist = self.getMazeDistance(coords, myLoc)
        if dist < min:
          min = dist
    return min

  def PacmanInEnemyLoc(self, currentPlayer):
    return currentPlayer.isPacman