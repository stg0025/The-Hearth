from constants import EMOTIONS, NEEDS, SAFETY_PROMPT
from db import log_session, log_intensity


def start_session(user_id):
    """Run a recovery session and record user input.

    The procedure includes:
      1. Showing a safety prompt and requiring acknowledgement.
      2. Collecting emotion and need selections from numbered lists.
      3. (Optional) Tracking urge intensity readings over time.
      4. Asking about relapse and additional notes.
      5. Logging the session and any intensity data.

    Args:
        user_id: identifier for the user initiating the session.
    """

    # Show the safety message first.
    print(SAFETY_PROMPT)

    # Require an explicit Enter keypress to continue.
    input("Press Enter to continue...")

    # Offer a list of emotions and let the user select multiple entries.
    print("How are you doing today? Pick as many emotions as you want, separated by commas:")
    for i, emotion in enumerate(EMOTIONS):
        print(f"{i + 1}. {emotion}")
    emotion_choices = input("Enter the numbers of the emotions you are feeling: ")

    # Parse the comma-separated choices into valid indices.
    emotion_indices = [int(x.strip()) - 1 for x in emotion_choices.split(",")]
    emotion_indices = [i for i in emotion_indices if 0 <= i < len(EMOTIONS)]
    selected_emotions = [EMOTIONS[i] for i in emotion_indices]

    # Offer a list of unmet needs and prompt for multiple selections.
    print("What needs do you feel are unmet? Pick as many needs as you want, separated by commas:")
    for i, need in enumerate(NEEDS):
        print(f"{i + 1}. {need}")
    needs_choices = input("Enter the numbers of the needs you are feeling: ")

    # Parse and validate the needs selections.
    needs_indices = [int(x.strip()) - 1 for x in needs_choices.split(",")]
    needs_indices = [i for i in needs_indices if 0 <= i < len(NEEDS)]
    selected_needs = [NEEDS[i] for i in needs_indices]
