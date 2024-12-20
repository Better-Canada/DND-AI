import random, copy

### Constants

# Defines whether the program is in training
IN_TRAINING = True
# Defines whether the program is used by a real user or the user sim
REAL_USER = False
# For printing the dialogues in training
PRINTING = True
# For printing the success rate
PRINT_PROGRESS_INTERVAL = 1000
# Minimum epsilon value for epsilon-decreasing exploration
EPSILON_MIN = 0.01
# Value which epsilon is multiplied by to decrease its impact over time
EPSILON_DECREASE = 0.9999
# Learning rate alpha
ALPHA = 0.0002
# Discount factor gamma for value updates
GAMMA = 0.99
# Capacity of the replay buffer
MEMORY_CAPACITY = 100000
# Batch size of sampled tuples from the replay buffer for training
BATCH_SIZE = 16
# File name of the the dqn model saved at the end of training
FILE_NAME = 'dqn_model.keras'
# How many rounds can occur in a conversation at most
TURN_LIMIT = 20
# How many episodes/dialogues to train in total
TRAIN_AMOUNT = 100000
# Number of neurons in the deep q networks hidden layer
HIDDEN_SIZE = 80
# Number of turns between target network updates based on the online network
TARGET_UPDATE_INTERVAL = 100
# Used to check for result of dialogue in user simulator
FAIL = -1
NO_RESULT = 0
SUCCESS = 1

# Slots
allSlots = ['category']
fillableSlots = ['category']
necessarySlots = ['category']
optionalSlots = []
requestableSlots = []

slotDictionary = { 'category' : ['greeting', 'farewell', 'weather', 'news', 'sports', 'trivia', 'small_talk', 'compliments', 'dnd', 'technology', 'health', 'food', 'travel', 'books'] }

# For one-hot encoding in state representation
userIntents = ['inform', 'reject', 'confirm']
agentIntents = ['done', 'matchFound', 'request']

# Set all possible actions of the agent
agentActions = []
agentActions.append({'intent':'done', 'requestSlots': None})
agentActions.append({'intent':'matchFound', 'requestSlots': None, 'informSlots':{}})

for slot in allSlots:
	agentActions.append({'intent':'request', 'requestSlots': slot})