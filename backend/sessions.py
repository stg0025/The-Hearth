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

    print(SAFETY_PROMPT)

    input("It's time to check in for the day. Take your time. Press Enter whenever you're ready...")
    print()

    first_attempt = True
    while True:
        if first_attempt:
            print("How are you doing today? Select any emotions you're feeling today:")
            print("---------------------------------------")
        else:
            print("Pick at least one — there's no wrong answer:")
            print("---------------------------------------")
        for i, emotion in enumerate(EMOTIONS):
            print(f"{i + 1}. {emotion}")
        print()
        emotion_choices = input("Enter the numbers of the emotions you are feeling, separated by commas: ")
        print()

        try:
            emotion_indices = [int(x.strip()) - 1 for x in emotion_choices.split(",")]
        except ValueError:
            print("Just enter the numbers from the list, separated by commas.")
            print()
            first_attempt = False
            continue

        emotion_indices = [i for i in emotion_indices if 0 <= i < len(EMOTIONS)]
        selected_emotions = [EMOTIONS[i] for i in emotion_indices]

        if not selected_emotions:
            first_attempt = False
            continue
        else:
            break

    first_attempt = True
    while True:
        if first_attempt:
            print("Now, what feels unmet right now? Select as many as feel true:")
            print("---------------------------------------")
        else:
            print("Pick at least one need from the list:")
            print("---------------------------------------")
        for i, need in enumerate(NEEDS):
            print(f"{i + 1}. {need}")
        print()
        needs_choices = input("Enter the numbers of the needs you are feeling, separated by commas: ")
        print()

        try:
            needs_indices = [int(x.strip()) - 1 for x in needs_choices.split(",")]
        except ValueError:
            print("Just enter the numbers from the list, separated by commas.")
            print()
            first_attempt = False
            continue

        needs_indices = [i for i in needs_indices if 0 <= i < len(NEEDS)]
        selected_needs = [NEEDS[i] for i in needs_indices]

        if not selected_needs:
            first_attempt = False
            continue
        else:
            break

    relapsed = 1 if input("Did you relapse today? (y/n): ").strip().lower() == "y" else 0
    print()

    notes = input("Anything else you want to note? You can always press Enter to skip: ").strip()
    print()

    log_session(user_id, ", ".join(selected_emotions), ", ".join(selected_needs), relapsed, notes)
    print("Thanks for checking in. Even checking in is a win. See you tomorrow.")


def craving_session(user_id):
    """Launch an immediate urge surfing session when a craving hits.

    The procedure includes:
      1. Starting a 5 minute interval timer immediately.
      2. Recording craving intensity (1-10) at each interval.
      3. Stopping after 30 minutes or when the user types done.
      4. Displaying a craving curve at the end of the session.
      5. Logging all intensity readings to the database.

    Args:
        user_id: identifier for the user initiating the session.
    """

    print("Take a deep breath. Let's surf this urge together. Type 'done' when you're ready to stop.")
    print()
    print("First, how are you feeling right now?")
    print("---------------------------------------")
    for i, emotion in enumerate(EMOTIONS):
        print(f"{i + 1}. {emotion}")
    print()
    emotion_choice = input("Enter the number of the emotion you're feeling: ")
    print()

    try:
        emotion_index = int(emotion_choice.strip()) - 1
        selected_emotion = EMOTIONS[emotion_index] if 0 <= emotion_index < len(EMOTIONS) else "unknown"
    except ValueError:
        selected_emotion = "unknown"

    print("For the next few minutes, rate your craving intensity on a scale of 1 to 10.")
    print("It's okay to feel this way. Stay present and ride it out.")
    print()

    interval_counter = 0
    intensity_readings = []
    session_id = log_session(user_id, selected_emotion, "craving session", 0)

    while interval_counter < 6:
        user_input = input(f"Interval {interval_counter + 1}: Rate your craving intensity (1-10), or type 'done' to stop: ")
        if user_input.lower() == "done":
            print()
            print("Great job riding that out. Cravings are temporary — you have the strength to get through them.")
            break
        try:
            intensity = int(user_input)
            if 1 <= intensity <= 10:
                intensity_readings.append(intensity)
                if intensity == 1:
                    print("Looks like the craving has mostly subsided. Great work riding that out!")
                    for i, intensity in enumerate(intensity_readings):
                        log_intensity(session_id, i + 1, intensity)
                    print()
                    print("Session saved.")
                    return
            else:
                print("Please enter a number between 1 and 10.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue
        interval_counter += 1
        print("Hang in there. Check back in 5 minutes...")
        print()
        time.sleep(300)

    for i, intensity in enumerate(intensity_readings):
        log_intensity(session_id, i + 1, intensity)
    print()
    print("Session saved.")
