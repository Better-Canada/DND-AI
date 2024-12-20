import random

# Day-to-Day Conversation Topics Database
database = [
    # Small talk and normal conversation
    { 'category': 'greeting', 'responses': ["Hi there! How can I help you today?", "Hello! What can I do for you?", "Hey! Need any assistance?", "Hi! How's your day going?", "Hello! What brings you here today?"] },
    { 'category': 'farewell', 'responses': ["Goodbye! Have a great day!", "See you later!", "Take care!", "Bye! Stay safe!", "Goodbye! Talk to you soon!"] },
    { 'category': 'weather', 'responses': ["It's sunny outside!", "Looks like it might rain today.", "It's quite chilly today, isn't it?", "The weather is perfect for a walk!", "It's pretty hot outside, make sure to stay hydrated!"] },
    { 'category': 'news', 'responses': ["Did you hear about the recent tech breakthrough?", "There's some interesting news about space exploration today.", "The stock market is quite volatile today.", "There's a lot happening in the world of politics right now.", "Have you read about the latest health trends?"] },
    { 'category': 'sports', 'responses': ["The local team won their game last night!", "Did you catch the big game yesterday?", "There's a major sports event coming up this weekend.", "The latest football match was intense!", "Are you following the basketball playoffs?"] },
    { 'category': 'trivia', 'responses': ["Did you know? A group of flamingos is called a 'flamboyance'.", "Here's a fun fact: Honey never spoils.", "Did you know that bananas are berries, but strawberries aren't?", "The Eiffel Tower can be 15 cm taller during the summer.", "Octopuses have three hearts and blue blood."] },
    { 'category': 'small_talk', 'responses': [
        "I hope you're having a wonderful day!", "What's your favorite hobby?", "Do you like reading books?", 
        "Have you seen any good movies lately?", "What's your go-to comfort food?", "How do you usually spend your weekends?",
        "Do you have any pets?", "What's your favorite type of music?", "Are you into any TV shows right now?",
        "What’s something interesting you’ve learned recently?", "Do you enjoy cooking?", "What's your dream travel destination?",
        "What’s your favorite holiday and why?", "Are you more of an early bird or a night owl?", "What’s your favorite season of the year?"
    ]},
    { 'category': 'compliments', 'responses': ["You have a great sense of humor!", "You're really thoughtful.", "I appreciate how kind you are.", "You're a great conversationalist!", "You have a positive vibe!"] },
    { 'category': 'general', 'responses': ["Tell me more about that.", "That's really interesting!", "How do you feel about that?", "What do you think?", "Can you elaborate on that?"] },

    # Dungeons & Dragons related topics
    { 'category': 'dnd', 'responses': [
        "What's your favorite class to play in D&D?", "Do you have a memorable character you've created?", 
        "What's the most epic moment you've experienced in a campaign?", "How do you typically handle role-playing difficult situations?",
        "What kind of quests do you enjoy the most?", "Do you prefer homebrew campaigns or official modules?",
        "What's your favorite spell in the game?", "How do you come up with character backstories?", 
        "What was the most challenging encounter your party faced?", "Do you have any tips for new players?",
        "What's your favorite D&D monster?", "How do you balance combat and role-playing?", "What's the funniest thing that's happened in your game?", 
        "Do you prefer being a player or a Dungeon Master?", "What's your most cherished D&D memory?"
    ]},

    # Additional categories to expand
    { 'category': 'technology', 'responses': ["Have you heard about the latest smartphone release?", "What do you think about the rise of AI?", "Are you interested in any tech gadgets?", "What’s your favorite piece of technology?", "Do you follow any tech blogs or podcasts?"] },
    { 'category': 'health', 'responses': ["How do you stay active and healthy?", "Do you follow any particular diet?", "What's your favorite way to relax and unwind?", "Do you have any tips for maintaining mental health?", "What’s your go-to exercise routine?"] },
    { 'category': 'food', 'responses': ["What’s your favorite cuisine?", "Do you enjoy cooking?", "What’s the best dish you’ve ever made?", "Have you tried any new restaurants lately?", "What's your favorite comfort food?"] },
    { 'category': 'travel', 'responses': ["What's your dream travel destination?", "Do you prefer beach vacations or mountain getaways?", "What’s the most interesting place you’ve visited?", "Do you like to plan your trips or be spontaneous?", "What's your favorite travel memory?"] },
    { 'category': 'books', 'responses': ["What’s the best book you’ve read recently?", "Do you have a favorite author?", "What genre of books do you enjoy?", "Have you read any interesting non-fiction lately?", "What's a book you would recommend to everyone?"] }
]
