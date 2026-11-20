import random

class RandomAgent:
    def __init__(self, id):
        self.id = id

    def choose_action(self, observation):
        
        legal_actions = observation["legal_actions"]

        if not legal_actions:
            raise ValueError("No legal actions available!")

        return random.choice(legal_actions)