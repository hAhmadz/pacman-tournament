# baselineAgents.py
# -----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html


from captureAgents import CaptureAgent
from captureAgents import AgentFactory
import distanceCalculator
import random, time, util
from game import Directions
import keyboardAgents
import game
from util import nearestPoint
import os


def createTeam(firstIndex, secondIndex, isRed, first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

class ReflexCaptureAgent(CaptureAgent): #base class for agents behaviour

  def __init__( self, index, timeForComputing = .1 ):
    CaptureAgent.__init__( self, index, timeForComputing)
    self.visibleAgents = []

  def createPDDLobjects(self): #implement PDDL objects here
    return 0
  def createPDDLfluents(self): #implement PDDL predicates here
    return 0

  def createPDDLgoal( self ): #Implement PDDL Goal here
    return 0

  def generatePDDLproblem(self): #main PDDL file generator
    cd = os.path.dirname(os.path.abspath(__file__))
    f = open("%s/problem%d.pddl"%(cd,self.index),"w");
    lines = list();
    lines.append("(define (problem strips-log-x-1)\n");
    lines.append("   (:domain pacman-strips)\n");
    lines.append("   (:objects \n");
    lines.append( self.createPDDLobjects() + "\n");
    lines.append(")\n");
    lines.append("   (:init \n");
    lines.append("   ;primero objetos \n");
    lines.append( self.createPDDLfluents() + "\n");
    lines.append(")\n");
    lines.append("   (:goal \n");
    lines.append("	 ( and  \n");
    lines.append( self.createPDDLgoal() + "\n");
    lines.append("   ))\n");
    lines.append(")\n");
    f.writelines(lines);
    f.close();

  def runPlanner( self ):
	  cd = os.path.dirname(os.path.abspath(__file__))
	  os.system("%s/ff  -o %s/domain.pddl -f %s/problem%d.pddl > %s/solution%d.txt" %(cd,cd,cd,self.index,cd,self.index));

  def parseSolution( self ):
    cd = os.path.dirname(os.path.abspath(__file__))
    f = open("%s/solution%d.txt"%(cd,self.index),"r");
    lines = f.readlines();
    f.close();
    
    for line in lines:
      pos_exec = line.find("0: "); #First action in solution file
      if pos_exec != -1: 
        command = line[pos_exec:];
        command_splitted = command.split(' ')

        x = int(command_splitted[3].split('_')[1])
        y = int(command_splitted[3].split('_')[2])

        return (x,y)

      # Empty Plan, Use STOP action, return current Position
      if line.find("ff: goal can be simplified to TRUE. The empty plan solves it") != -1:
        return  self.getCurrentObservation().getAgentPosition( self.index )

  # A base class for reflex agents that chooses score-maximizing actions
  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    bestAction = 'Stop' #default action is stop : updates later on

    # Eval Time Start - Can Uncomment to evaluate function time (<15secs)
    # start = time.time()
    self.generatePDDLproblem() #Start & Run Planner
    self.runPlanner()
    (newx,newy) = self.parseSolution()

    for a in actions:
      succ = self.getSuccessor(gameState, a)
      if succ.getAgentPosition( self.index ) == (newx, newy): #First action of plan
        bestAction = a
        print self.index, bestAction, self.getCurrentObservation().getAgentPosition( self.index ) ,(newx,newy) 

    # Eval Time End
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    return bestAction

  #Finds the next successor which is a grid position (location tuple).
  def getSuccessor(self, gameState, action):
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      return successor.generateSuccessor(self.index, action) # Only half a grid position was covered
    else:
      return successor

  #Computes a linear combination of features and feature weights
  def evaluate(self, gameState, action):
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  #Returns a counter of features for the state
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 1.0}

class OffensiveReflexAgent(ReflexCaptureAgent): # Offensive Agent
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    foodList = self.getFood(successor).asList() # Compute distance to the nearest food
    if len(foodList) > 0:
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
      print action, features, successor
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}

  """
  def generatePDDLproblem(self): for Offense
  """

class DefensiveReflexAgent(ReflexCaptureAgent): #defensive agent

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # tells we are on defense
    features['onDefense'] = 1
    if myState.isPacman:
      features['onDefense'] = 0

    #distance to invader enemies
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]

    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP:
      features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]

    if action == rev:
      features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}

  """
  def generatePDDLproblem(self): for defense
  """
        
