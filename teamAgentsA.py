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
import util
from teamStrategyA import myCustomAgent
from game import Directions

class TeamAttackerA(myCustomAgent):

  def getFeatures(self, gameState, action):
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

      #***********************************************

      #*******If Defense *****************************
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

      #**********************************************

      return features

  def getWeights(self, gameState, action):
      return {'successorScore': 100, 'distanceToFood': -1}

  def getDefenderWeights(self, gameState, action):
      return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}

  def isScared(self, currentPlayer):
      if currentPlayer.scaredTimer > 0:
        return True
      else:
        return False

