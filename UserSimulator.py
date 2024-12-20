from Config import *
import copy
import random

class UserSimulator:

	def __init__(self):
		self.Reset()

	def Reset(self):		
		self.ResetUnusedSlotValues()
		self.GenerateUserGoal()

	def ResetUnusedSlotValues(self):
		# Used for keeping track of which slots haven't been chosen yet
		self.unusedSlotValues = copy.deepcopy(slotDictionary)

	def GenerateUserGoal(self):
		self.goal = {'category': 'any'}
		# Adds informs for necessary slots with random values from the slot dictionary
		for slot in necessarySlots:
			chosenValue = random.choice(slotDictionary[slot])
			self.goal[slot] = chosenValue

		self.SelectFirstAction()

	# Composes the first actions which consists of randomly but reasonably combined inform slots
	def SelectFirstAction(self):
		# Chance of informing several slots at once
		probability = random.random()
		self.firstAction = None

		# Inform all necessary slots with 40% chance
		if probability < 0.4:
			self.firstAction = {'intent':'inform', 'informSlots': {'category': self.goal['category']}}
		else:
			# Inform category with 60% chance
			self.firstAction = {'intent':'inform', 'informSlots': {'category': self.goal['category']}}

	# Returns a user action based on the last agent action
	def GetNextAction(self, turnCount, agentAction):
		result = None

		# Immediately return a fail if the turn limit has been reached
		if turnCount == TURN_LIMIT - 1:
			nextAction = {'intent':'reject', 'informSlots':{}}
			return nextAction, -TURN_LIMIT, FAIL
		else:
			if agentAction:
				# React to agent request by providing the corresponding information as inform
				if agentAction['intent'] == 'request':
					slot = agentAction['requestSlots']
					nextAction = {'intent':'inform', 'informSlots':{slot:self.goal[slot]}}
				# Evaluate the match proposed by the agent
				elif agentAction['intent'] == 'matchFound':
					# If there is no match, change random slot value
					if not agentAction['informSlots']:
						nextAction = self.ChangeSlotIfNoMatches()
					# If there is a match and it is fulfilling the goal...
					elif agentAction['informSlots'] and self.IsMatchAcceptable(agentAction):
						# ...confirm the match
						nextAction = {'intent':'confirm', 'informSlots':{}}
					# If there is a match and it does not fulfill the goal, reject it
					else:
						nextAction = {'intent':'reject', 'informSlots':{}}
				# Confirm if the agent has concluded the dialogue (meaning this actions has no further influence on the dialogue)
				else:
					nextAction = {'intent':'confirm', 'informSlots':{}}
			# Send first action if there is no previous agent action
			else:
				nextAction = self.firstAction

		# Check if agent has finished the dialogue
		if agentAction and agentAction['intent'] == 'done':
			result = SUCCESS
		else:
			result = NO_RESULT

		# Give rewards for the agent
		if result == SUCCESS:
			reward = 2 * TURN_LIMIT
			nextAction = {'intent':'confirm', 'informSlots':{}}
		elif result == FAIL:
			reward = -TURN_LIMIT
			nextAction = {'intent':'reject', 'informSlots':{}}
		else:	
			# Give reward of -3 for a normal dialogue turn with no outcome
			reward = -3

		return nextAction, reward, result

	# Changes a slot if no database entries match the user goal
	def ChangeSlotIfNoMatches(self):
		# Reset unused slots if all possible slots have been tried
		if not self.unusedSlotValues['category']:
			self.ResetUnusedSlotValues()			
		# Choose random slot to change
		slotToReplace = 'category'
		# Replace slot value with random value
		self.goal[slotToReplace] = random.choice(self.unusedSlotValues[slotToReplace])
		self.unusedSlotValues[slotToReplace].remove(self.goal[slotToReplace])
		# Inform about changed slot
		return {'intent':'inform', 'informSlots':{slotToReplace:self.goal[slotToReplace]}}

	# Checks if a match proposed by the agent fulfills the user goal
	def IsMatchAcceptable(self, agentAction):
		for slot in agentAction['informSlots'].keys():
			if slot not in self.goal:
				continue
			if self.goal[slot] == 'any':
				continue
			if agentAction['informSlots'][slot] != self.goal[slot]:
				return False
		return True