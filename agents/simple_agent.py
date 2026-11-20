from game.action import Action

class SimpleAgent:
    def __init__(self, id):
        self.id = id
        

    def choose_action(self, observation, game_state):

        legal_actions: list[Action] = observation["legal_actions"]

        if not legal_actions:
            raise ValueError("No legal actions available!")

        if len(legal_actions) == 1:
            return legal_actions[0]

        if not legal_actions[0].is_pass:
            lowest_move = legal_actions[0]
        else:
            lowest_move = legal_actions[1]

        for action in range(len(legal_actions)):
            if not legal_actions[action].is_pass:
                if legal_actions[action].cards[0].rank.value < lowest_move.cards[0].rank.value:
                    lowest_move = legal_actions[action]


        return lowest_move