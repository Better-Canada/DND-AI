from DeepQNetwork import *
from Database import *
import numpy as np
from keras.utils import CustomObjectScope
from keras.losses import mean_squared_error

class Agent:

	def __init__(self, stateSize):
		# Replay buffer for storing and sampling experience for learning
		self.memory = ReplayBuffer()
		# Online network for choosing actions
		self.onlineNetwork = InitializeDqn(stateSize)
		# Target network for computing target values in learning
		self.targetNetwork = InitializeDqn(stateSize)
		# Initialize epsilon with 1 for epsilon-decreasing strategy
		self.epsilon = 1

	# Takes the current state and its size to choose an action
	def PredictNextAction(self, state, stateSize):
		rand = random.random()
		# Determine if random or policy-based action
		if IN_TRAINING and rand < self.epsilon:
			nextAction = random.choice(agentActions)
		else:
			# Network outputs value for each agent action based on the state
			actionValues = self.onlineNetwork.predict(state.reshape(1, stateSize)).flatten()
			# Gets index of action with highest Q-value
			nextActionIndex = np.argmax(actionValues)
			# Returns corresponding action based on the chosen index
			nextAction = self.IndexToAction(nextActionIndex)

		# Decrease the epsilon
		if self.epsilon > EPSILON_MIN:
			self.epsilon *= EPSILON_DECREASE

		return nextAction

	# Takes an index and returns the corresponding agent action
	def IndexToAction(self, index):
		for (i, action) in enumerate(agentActions):
			if index == i:
				return copy.deepcopy(action)

	# Takes an agent action and returns the corresponding index
	def ActionToIndex(self, action):
		for (i, a) in enumerate(agentActions):
				if action == a:
					return i

	# Reset the agent for usage in new dialogue
	def Reset(self):
		pass

	# Adapts the network weights by learning from memory
	def Learn(self, stateSize):
		# Only start learning if a complete batch can be sampled from the buffer
		if self.memory.indexCounter < BATCH_SIZE:
			return

		batch = self.memory.SampleBatchFromBuffer()

		# For each tuple in the batch
		for state, action, reward, nextState in batch:
			# Compute Q-values of online network
			qNow = self.onlineNetwork.predict(state.reshape(1, stateSize)).flatten()
			# Initialize target Q-values with online Q-values
			qTarget = qNow.copy()

			# If the tuple has no next state, the Q-value is the reward
			if isinstance(nextState, list):
				qTarget[self.ActionToIndex(action)] = reward
			else:
				# Compute Q-values of the next state using the target network
				qNext = self.targetNetwork.predict(nextState.reshape(1, stateSize)).flatten()
				# Set target Q-value of the tuple action to the reward plus the discounted maximal Q-value of the next state
				qTarget[self.ActionToIndex(action)] =  reward + GAMMA * max(qNext)
			
			# Adjust the weights according to the difference of online and target values
			self.onlineNetwork.fit(state.reshape(1, stateSize), qTarget.reshape(1, len(agentActions)), epochs=1, verbose=0)

	# Copies weights of the online network to the target network
	def CopyToTargetNetwork(self):
		self.targetNetwork.set_weights(self.onlineNetwork.get_weights())

	# Saves online network
	def SaveModel(self):
		self.onlineNetwork.save(FILE_NAME)

	# Loads online network
	def LoadModel(self):
		with CustomObjectScope({'mse': mean_squared_error}):
			self.onlineNetwork = load_model(FILE_NAME) 

	# Choose request utterance based on the slot
	def GenerateRequestResponse(self, nextAction):
		slot = nextAction['requestSlots']
		responses = {
			'greeting': [
				'Hello! How can I assist you today?', 
				'Hi there! What can I do for you?', 
				'Hey! Need any help?', 
				'Hi! How\'s your day going?', 
				'Hello! What brings you here today?'
			],
			'farewell': [
				'Goodbye! Have a great day!', 
				'See you later!', 
				'Take care!', 
				'Bye! Stay safe!', 
				'Goodbye! Talk to you soon!'
			],
			'weather': [
				'What would you like to know about the weather?', 
				'Is there something specific about the weather you\'re curious about?', 
				'Do you need a weather update?', 
				'How can I help with the weather information?'
			],
			'news': [
				'What kind of news are you interested in?', 
				'Looking for something specific in the news?', 
				'Do you want the latest headlines?', 
				'What news topic are you curious about?'
			],
			'sports': [
				'Which sport are you interested in?', 
				'Do you follow any particular sports?', 
				'Looking for updates on a specific game?', 
				'What sports news can I help you with?'
			],
			'trivia': [
				'Would you like to hear a fun fact?', 
				'Interested in some trivia?', 
				'How about a random fact?', 
				'Want to know something interesting?'
			],
			'small_talk': [
				'What would you like to chat about?', 
				'Let\'s have a casual conversation. What\'s on your mind?', 
				'Anything specific you want to talk about?', 
				'What\'s new with you?'
			],
			'compliments': [
				'Would you like to give or receive a compliment?', 
				'Feeling like spreading some positivity?', 
				'Want to hear something nice?', 
				'Do you have a compliment to share?'
			],
			'dnd': [
				'Are you interested in discussing Dungeons & Dragons?', 
				'Let\'s talk about D&D. What\'s your favorite part?', 
				'Do you have any D&D stories to share?', 
				'What\'s your favorite D&D character?'
			],
			'technology': [
				'What aspect of technology are you curious about?', 
				'Interested in the latest tech trends?', 
				'Do you have any tech questions?', 
				'What\'s your favorite piece of technology?'
			],
			'health': [
				'Do you have any health-related questions?', 
				'Looking for health tips?', 
				'How can I assist with your health queries?', 
				'What health topic are you interested in?'
			],
			'food': [
				'What type of food are you interested in?', 
				'Looking for restaurant recommendations?', 
				'Do you have a favorite cuisine?', 
				'What\'s your go-to dish?'
			],
			'travel': [
				'Where would you like to travel?', 
				'Do you have a dream destination?', 
				'Looking for travel tips?', 
				'What\'s your favorite travel memory?'
			],
			'books': [
				'Do you have any book recommendations or questions?', 
				'What\'s the best book you\'ve read recently?', 
				'Do you have a favorite author?', 
				'What genre of books do you enjoy?'
			]
		}

		if slot in responses:
			return random.choice(responses[slot])
		else:
			return f'Can you provide more details about {slot}?'

	# Compose response to propose a matching topic
	def GenerateMatchFoundResponse(self, nextAction):
		responseString = []
		# Missing inform slots indicate that there is no matching database entry
		if nextAction['informSlots']:
			match = nextAction['informSlots']
			responseString.append(f"How about we talk about \"{match['category']}\"? ")
			responseString.append(f"Here's something: {random.choice(match['responses'])}")
		else:
			responseString.append('No matching topic found. Would you like to try a different topic?')
		return ''.join(responseString)

	# Compose response for finishing the dialogue
	def GenerateDoneResponse(self, filledSlots):
		return "It was nice talking to you! Have a great day!"

	# Returns a database entry given a category
	def GetEntryFromDb(self, category):
		for entry in copy.deepcopy(database):
			if 'category' in entry and entry['category'] == category:
				return entry
		return {}