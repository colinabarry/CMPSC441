import vertexai
from vertexai.generative_models import GenerativeModel


class Storyteller:
    def __init__(self):
        self._story = []
        vertexai.init(project="isentropic-disk-421817", location="us-central1")
        self.multimodal_model = GenerativeModel(
            model_name="gemini-1.5-pro-preview-0409"
        )

    def add(self, text):
        self._story.append(text)

    def tell(self):
        return " ".join(self._story)

    def generate_text(self, input_array):
        output = self.multimodal_model.generate_content(input_array)
        self.add(output.text)
        print(output)
        return output.text

    def generate_combat_story(self, combat_log):
        return self.generate_text(
            [
                "create a narrative play-by-play surrounding the following combat log, taking care to be exact about the weapons used each round. the text reading 'you lose' or 'you win' describes Oillill's outcome. the opponent should be given a name appropriate for the fantasy medieval setting. combat log: ",
                combat_log,
            ]
        )

    def generate_travel_story(self, travel_log):
        return self.generate_text(
            [
                "create a short narrative surrounding the following travel log. explain Oillill's strategic choices related to travel cost and other consideration. travel log: ",
                travel_log,
            ]
        )


if __name__ == "__main__":
    storyteller = Storyteller()
    combat_log = """
        Player 1 used Arrow, Player 2 used Sword
        Player 1 used Arrow, Player 2 used Arrow
        Player 1 used Arrow, Player 2 used Arrow
        Player 1 used Arrow, Player 2 used Arrow
        Player 1 used Sword, Player 2 used Arrow
        Player 1 used Sword, Player 2 used Arrow
        Player 1 used Sword, Player 2 used Arrow
        Player 1 used Sword, Player 2 used Fire
        Player 1 used Fire, Player 2 used Fire
        Player 1 used Fire, Player 2 used Fire
        Player 1 used Fire, Player 2 used Fire
        Player 1 used Fire, Player 2 used Sword
        You Lose
    """

    travel_log = """
        Start: Morkomasto
        End: Londathrad
        Cost: 10
        Starting Gold: 100
    """

    # print(storyteller.generate_combat_story(combat_log))
    print(storyteller.generate_travel_story(travel_log))
