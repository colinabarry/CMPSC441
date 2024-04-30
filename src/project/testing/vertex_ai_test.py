import vertexai
from vertexai.generative_models import GenerativeModel, Part


def generate_text(project_id, location):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    # Load the model
    multimodal_model = GenerativeModel(model_name="gemini-1.5-pro-preview-0409")

    # Query the model
    response = multimodal_model.generate_content(
        [
            "create a narrative and detailed play-by-play surrounding the following combat log. the text reading 'you lose' or 'you win' describes player 1's outcome",
            """
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
            """,
        ]
    )
    # print(response)
    return response.text


if __name__ == "__main__":
    text_response = generate_text("isentropic-disk-421817", "us-central1")
    print(text_response)
