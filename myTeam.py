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
import random, time, util
from game import Directions
import game

def createTeam(firstIndex, secondIndex, isRed,first = 'DummyAgent', second = 'DummyAgent'):
  return [eval(first)(firstIndex), eval(second)(secondIndex)]


class DummyAgent(CaptureAgent): #base class for agents behaviour

  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''

  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index) #Picks among actions randomly.
    return random.choice(actions)

