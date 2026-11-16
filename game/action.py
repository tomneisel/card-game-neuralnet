class Action:
    def __init__(self, cards=None, is_pass=False):
        self.cards = cards if cards is not None else []
        self.is_pass = is_pass

    def __eq__(self, other):
        if not isinstance(other, Action):
            return NotImplemented

        return (
            self.is_pass == other.is_pass and self.cards == other.cards
        )