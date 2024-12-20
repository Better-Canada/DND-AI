from Config import *
from gensim import models
from gensim import utils
import gensim.downloader as api

class NaturalLanguageProcessor:

    def __init__(self):
        # Load the gensim model
        self.model = api.load('glove-wiki-gigaword-50')

    # Transform user utterance into semantic frame
    def GetSemanticFrame(self, userInput, lastAgenAction):
        # Get inform slots
        informSlots = self.GetSlots(userInput.lower(), lastAgenAction)

        # Intent is 'inform' if there are inform slots
        if informSlots:
            intent = 'inform'
        else:
            # Intent has to be determined
            intent = self.GetIntent(userInput.lower())

        # Return user action
        return {'intent': intent, 'requestSlots': {}, 'informSlots': informSlots}

    # Detects intent using the gensim model
    def GetIntent(self, userInput):
        categories = [
            'confirm', 'reject', 'greeting', 'farewell', 'weather', 'news',
            'sports', 'trivia', 'small_talk', 'compliments', 'dnd', 'technology',
            'health', 'food', 'travel', 'books'
        ]
        intent_probabilities = {category: 0.0 for category in categories}

        for word in userInput.split():
            if word in self.model.key_to_index:
                for category in categories:
                    intent_probabilities[category] += self.model.similarity(word, category)

        detected_intent = max(intent_probabilities, key=intent_probabilities.get)
        return detected_intent

    # Returns dictionary of detected inform slots
    def GetSlots(self, userInput, lastAgenAction):
        slots = {}
        keywords = {
            'greeting': ['hello', 'hi', 'hey'],
            'farewell': ['bye', 'goodbye', 'see you', 'take care'],
            'weather': ['weather', 'sunny', 'rain', 'chilly', 'hot'],
            'news': ['news', 'headline', 'tech', 'space', 'market'],
            'sports': ['sports', 'game', 'match', 'football', 'basketball'],
            'trivia': ['fact', 'trivia', 'interesting', 'did you know'],
            'small_talk': ['hobby', 'pet', 'music', 'movie', 'book', 'reading', 'cooking'],
            'compliments': ['compliment', 'great', 'kind', 'positive', 'humor'],
            'dnd': ['dnd', 'dungeon', 'dragon', 'campaign', 'spell', 'quest'],
            'technology': ['tech', 'ai', 'gadget', 'device', 'smartphone'],
            'health': ['health', 'exercise', 'diet', 'mental', 'relax'],
            'food': ['food', 'cuisine', 'dish', 'cook'],
            'travel': ['travel', 'vacation', 'trip', 'destination', 'place'],
            'books': ['book', 'author', 'read', 'novel', 'genre']
        }

        for category, words in keywords.items():
            for word in words:
                if word in userInput:
                    slots[category] = word

        return slots

    # Check if word is number by numerical value or high similarity to the word number
    def IsNumber(self, word):
        if word.isnumeric() or (word in self.model.key_to_index and self.model.similarity(word, 'number') > 0.7):
            return True
        else:
            return False
