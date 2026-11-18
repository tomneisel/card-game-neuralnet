from tournament.match_result import MatchResult

class Leaderbord:
    def __init__(self):
        self.leaderbord = {}

    def add_result(self, match_result: MatchResult):
        updated_leaderbord = {x: self.leaderbord.get(x, 0) + match_result.points.get(x, 0)
                              for x in set(self.leaderbord).union(match_result.points)}
        self.leaderbord = updated_leaderbord

    def get_leaderbord(self):
        sorted_leaderbord = {k: v for k, v in sorted(self.leaderbord.items(), key=lambda item: item[1], reverse=True)}

        for index, (player_id, points) in enumerate(sorted_leaderbord.items()):
            print(f"Place {index + 1}: player {player_id} with {points} points")

        return sorted_leaderbord