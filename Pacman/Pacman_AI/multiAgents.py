
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):


    def getAction(self, gameState):
        movesCanBeDone = gameState.getLegalActions()
        scoresToDo = [self.evaluationFunction(gameState, action) for action in movesCanBeDone]
        OptimizedScore = max(scoresToDo)
        optimizedMoves = [index for index in range(len(scoresToDo)) if scoresToDo[index] == OptimizedScore]
        moveToBeDone = random.choice(optimizedMoves) # Pick randomly among the best

        return movesCanBeDone[moveToBeDone]

    def evaluationFunction(self, currentGameState, action):
        gameStatesOfChildNotes = currentGameState.generatePacmanSuccessor(action)
        childPossession = gameStatesOfChildNotes.getPacmanPosition()
        childFood = gameStatesOfChildNotes.getFood()
        childGhosts = gameStatesOfChildNotes.getGhostStates()
        childScaredTime = [ghostState.scaredTimer for ghostState in childGhosts]
        currentFood = childFood.asList()
        totalFood = len(currentFood)
        closestGhost = 1e6
        for i in xrange(totalFood):
          manhattanDis = manhattanDistance(currentFood[i],childPossession) + totalFood*100
          if manhattanDistance < closestGhost:
            closestGhost = manhattanDistance
            closestFood = currentFood
        if totalFood == 0 :
          closestGhost = 0
        evaluationScore = -closestGhost

        for i in xrange(len(childGhosts)):
          ghostPos = gameStatesOfChildNotes.getGhostPosition(i+1)
          if manhattanDistance(childPossession,ghostPos)<=1 :
            evaluationScore -= 1e6

        return evaluationScore

def scoreEvaluationFunction(currentGameState):

    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):


    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        totalAgentNumber = gameState.getNumAgents()
        ScoresOfAction = []
        def _rmStop(List):
          return [x for x in List if x != 'Stop']
        def _miniMax(s, iterCount):
          if iterCount >= self.depth*totalAgentNumber or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
          if iterCount%totalAgentNumber != 0:
            finalResult = 1e10
            for a in _rmStop(s.getLegalActions(iterCount%totalAgentNumber)):
              foods = s.generateSuccessor(iterCount%totalAgentNumber,a)
              finalResult = min(finalResult, _miniMax(foods, iterCount+1))
            return finalResult
          else: 
            finalResult = -1e10
            for a in _rmStop(s.getLegalActions(iterCount%totalAgentNumber)):
              foods = s.generateSuccessor(iterCount%totalAgentNumber,a)
              finalResult = max(finalResult, _miniMax(foods, iterCount+1))
              if iterCount == 0:
                ScoresOfAction.append(finalResult)
            return finalResult
          
        result = _miniMax(gameState, 0);
        return _rmStop(gameState.getLegalActions(0))[ScoresOfAction.index(max(ScoresOfAction))]

class AlphaBetaAgent(MultiAgentSearchAgent):
    
    def getAction(self, gameState):
        
        totalAgentNumber = gameState.getNumAgents()
        ScoresOfAction = []

        def _rmStop(List):
          return [x for x in List if x != 'Stop']

        def _alphaBeta(s, iterCount, alpha, beta):
          if iterCount >= self.depth*totalAgentNumber or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
          if iterCount%totalAgentNumber != 0:
            finalResult = 1e10
            for a in _rmStop(s.getLegalActions(iterCount%totalAgentNumber)):
              foods = s.generateSuccessor(iterCount%totalAgentNumber,a)
              finalResult = min(finalResult, _alphaBeta(foods, iterCount+1, alpha, beta))
              beta = min(beta, finalResult)
              if beta < alpha:
                break
            return finalResult
          else:
            finalResult = -1e10
            for a in _rmStop(s.getLegalActions(iterCount%totalAgentNumber)):
              foods = s.generateSuccessor(iterCount%totalAgentNumber,a)
              finalResult = max(finalResult, _alphaBeta(foods, iterCount+1, alpha, beta))
              alpha = max(alpha, finalResult)
              if iterCount == 0:
                ScoresOfAction.append(finalResult)
              if beta < alpha:
                break
            return finalResult
        result = _alphaBeta(gameState, 0, -1e20, 1e20)
        return _rmStop(gameState.getLegalActions(0))[ScoresOfAction.index(max(ScoresOfAction))]

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        totalAgentNumber = gameState.getNumAgents()
        ScoresOfAction = []
        def _rmStop(List):
          return [x for x in List if x != 'Stop']
        def _expectMinimax(s, iterCount):
          if iterCount >= self.depth*totalAgentNumber or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
          if iterCount%totalAgentNumber != 0:
            successorScore = []
            for a in _rmStop(s.getLegalActions(iterCount%totalAgentNumber)):
              foods = s.generateSuccessor(iterCount%totalAgentNumber,a)
              finalResult = _expectMinimax(foods, iterCount+1)
              successorScore.append(finalResult)
            avgPoint = sum([ float(x)/len(successorScore) for x in successorScore])
            return avgPoint
          else:
            finalResult = -1e10
            for a in _rmStop(s.getLegalActions(iterCount%totalAgentNumber)):
              foods = s.generateSuccessor(iterCount%totalAgentNumber,a)
              finalResult = max(finalResult, _expectMinimax(foods, iterCount+1))
              if iterCount == 0:
                ScoresOfAction.append(finalResult)
            return finalResult
          
        result = _expectMinimax(gameState, 0);
        return _rmStop(gameState.getLegalActions(0))[ScoresOfAction.index(max(ScoresOfAction))]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    def _scoreFromGhost(gameState):
      evaluationFuncScore = 0
      for ghost in gameState.getGhostStates():
        manhattanDisOfGhost = manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition())
        if ghost.scaredTimer > 0:
          evaluationFuncScore += pow(max(8 - manhattanDisOfGhost, 0), 2)
        else:
          evaluationFuncScore -= pow(max(7 - manhattanDisOfGhost, 0), 2)
      return evaluationFuncScore

    def _scoreFromFood(gameState):
      foodsDistances = []
      for food in gameState.getFood().asList():
        foodsDistances.append(1.0/manhattanDistance(gameState.getPacmanPosition(), food))
      if len(foodsDistances)>0:
        return max(foodsDistances)
      else:
        return 0
    def _scoreFromCapsules(gameState):
      capsulesScore = []
      for Cap in gameState.getCapsules():
        capsulesScore.append(50.0/manhattanDistance(gameState.getPacmanPosition(), Cap))
      if len(capsulesScore) > 0:
        return max(capsulesScore)
      else:
        return 0
    def _suicide(gameState):
      score = 0
      ghostDistance = 1e6
      for ghost in gameState.getGhostStates():
        ghostDistance = min(manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition()), ghostDistance)
      score -= pow(ghostDistance, 2)
      if gameState.isLose():
        score = 1e6
      return score
    score = currentGameState.getScore()
    scoreGhosts = _scoreFromGhost(currentGameState)
    scoreFood = _scoreFromFood(currentGameState)
    scoreCapsules = _scoreFromCapsules(currentGameState)

    return score + scoreGhosts + scoreFood + scoreCapsules
    util.raiseNotDefined()
better = betterEvaluationFunction

