from constants import EMOTIONS, NEEDS, SAFETY_PROMPT
from db import log_session, log_intensity
import time


def daily_checkin(user_id):
    """Run a recovery session and record user input.

    The procedure includes:
      1. Showing a safety prompt and requiring acknowledgement.
      2. Collecting emotion and need selections from numbered lists.
      3. Asking about relapse and additional notes.

    Args:
        user_id: identifier for the user initiating the session.
    """

    # Show the safety message first.
    print(SAFETY_PROMPT)

    # Require an explicit Enter keypress to continue.
    input("It's time to check in for the day. Take your time. Press Enter whenever you're ready...")

    # Offer a list of emotions and let the user select multiple entries.
    first_attempt = True
    while True:
        if first_attempt:
            print("How are you doing today? Select any emotions you're feeling today, separated by commas:")
        else:
            print("Pick at least one — there's no wrong answer:")
        for i, emotion in enumerate(EMOTIONS):
            print(f"{i + 1}. {emotion}")
        emotion_choices = input("Enter the numbers of the emotions you are feeling: ")

        try:
            emotion_indices = [int(x.strip()) - 1 for x in emotion_choices.split(",")]
        except ValueError:
            print("Just enter the numbers from the list, separated by commas.")
            first_attempt = False
            continue

        emotion_indices = [i for i in emotion_indices if 0 <= i < len(EMOTIONS)]
        selected_emotions = [EMOTIONS[i] for i in emotion_indices]

        if not selected_emotions:
            first_attempt = False
            continue
        else:
            break

    # Offer a list of needs and let the user select multiple entries.
    first_attempt = True
    while True:
        if first_attempt:
            print("Now, what feels unmet right now? Select as many as feel true:")
        else:
            print("Pick at least one need from the list:")
        for i, need in enumerate(NEEDS):
            print(f"{i + 1}. {need}")
        needs_choices = input("Enter the numbers of the needs you are feeling: ")

        try:
            needs_indices = [int(x.strip()) - 1 for x in needs_choices.split(",")]
        except ValueError:
            print("Just enter the numbers from the list, separated by commas.")
            first_attempt = False
            continue

        needs_indices = [i for i in needs_indices if 0 <= i < len(NEEDS)]
        selected_needs = [NEEDS[i] for i in needs_indices]

        if not selected_needs:
            first_attempt = False
            continue
        else:
            break

    # Ask about relapse and notes.
    relapsed = 1 if input("Did you relapse today? (y/n): ").strip().lower() == "y" else 0

    notes = input("Anything else you want to note? There is no pressure, you can always press Enter to skip: ").strip()

    # Log the session to the database.
    log_session(user_id, ", ".join(selected_emotions), ", ".join(selected_needs), relapsed, notes)
    print("Thanks for checking in. Even checking in is a win, keep up the good work! See you tomorrow.")

def craving_session(user_id):
    """Launch an immediate urge surfing session when a craving hits.

    The procedure includes:
      1. Starting a 60-second interval timer immediately.
      2. Recording craving intensity (1-10) at each interval.
      3. Stopping after 20 minutes or when the user types done.
      4. Displaying a craving curve at the end of the session.
      5. Logging all intensity readings to the database.

    Args:
        user_id: identifier for the user initiating the session.
    """
    print("Take a deep breath. Let's surf this urge together. Type 'done' when you're ready to stop.")
    print("First, how are you feeling right now?")
    # Offer the emotions list again for the user to select from.
    for i, emotion in enumerate(EMOTIONS):
        print(f"{i + 1}. {emotion}")
    emotion_choice = input("Enter the number of the emotion you're feeling: ")
    try:
        emotion_index = int(emotion_choice.strip()) - 1
        selected_emotion = EMOTIONS[emotion_index] if 0 <= emotion_index < len(EMOTIONS) else "unknown"
    except ValueError:
        selected_emotion = "unknown"

    print("Let's get through these urges together. For a while, I'll ask you to rate your craving intensity on a scale of 1 to 10. ")
    print("Remember, it's okay to feel this way. Just do your best to stay present and ride it out.")
    
    # Create a minute counter starting at 0, a list called intensity_readings to store results, a while loop that stops at 20 minutes, or waiting for done
    minute_counter = 0
    intensity_readings = []
    while minute_counter < 20:
        user_input = input(f"Minute {minute_counter + 1}: Rate your craving intensity (1-10): ")
        if user_input.lower() == "done":
            print("Great job riding that out. Remember, cravings are temporary and you have the strength to get through them.")
            break
        try:
            intensity = int(user_input)
            if 1 <= intensity <= 10:
                intensity_readings.append(intensity)
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")
        minute_counter += 1
        print("Hang in there. Check back in 60 seconds...")
        time.sleep(60)
    session_id = log_session(user_id, selected_emotion, "craving session", 0)
    for i, intensity in enumerate(intensity_readings):
        log_intensity(session_id, i + 1, intensity)
    print("Session saved. Well done for riding it out.")

