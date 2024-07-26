# import necessary libraries and initializes sound files for break notifications

import time
import os # notifications for MacOS 
import pygame # used for sound notifications 

#intializing sounds 
pygame.mixer.init()

# customize short and long break sounds with .wav file // make sure the files in your working directory
short_break_sound = pygame.mixer.Sound("Blow.wav")
long_break_sound = pygame.mixer.Sound("Glass.wav")


def get_user_inputs():
    """
    Prompts the user for Pomodoro timer settings and returns them as a tuple.

    This function collects four pieces of information from the user:
    1. Number of Pomodoro intervals
    2. Duration of each work period
    3. Duration of short breaks
    4. Duration of the long break

    All inputs are converted to integers, assuming whole number inputs.

    Returns:
    tuple: A tuple containing four integers in the following order:
        (number_of_intervals, work_period, short_break_period, long_break_period)

    Note: Input values must be whole numbers. The function will raise a ValueError 
    if non-integer values are entered.
    """
    
    number_of_intervals = int(input("How many pomodoros would you like to complete today? "))  
    work_period = int(input("For how long would you like to work (minutes)? "))
    short_break_period = int(input("How long would you like your short break to be (minutes)? "))
    long_break_period = int(input("How long would you like your long break to be? (minutes) "))
    return number_of_intervals, work_period, short_break_period, long_break_period


# notification alert system function 
def send_notification(title, message):

    """
    Sends a desktop notification on macOS using osascript.
    
    Args:
    title (str): The title of the notification.
    message (str): The body text of the notification.
    
    This function uses the os.system call to execute an AppleScript command,
    allowing notifications to be displayed outside the terminal.
    """

    os.system(f'''
              osascript -e 'display notification "{message}" with title "{title}"'
              ''')

# pomodoro cycle function
def start_pomodoro_cycle(number_of_intervals):

    """
    Executes the main Pomodoro timer cycle based on user-defined settings.

    This function runs the Pomodoro timer, alternating between work periods and breaks.
    It uses sound alerts and desktop notifications to inform the user of transitions.

    Args:
    number_of_intervals (int): The number of Pomodoro cycles to complete.

    The function performs the following steps:
    1. Initiates the timer and prints a start message.
    2. For each interval:
       a. Waits for the work period duration.
       b. Plays a sound and sends a notification for the short break.
       c. Waits for the short break duration.
       d. Sends a notification to resume work.
    3. After all intervals are complete:
       a. Plays a sound and sends a notification for the long break.
       b. Waits for the long break duration.
       c. Plays a sound and sends a final notification.

    Note: 
    - Work and break durations are multiplied by 60 to convert minutes to seconds.
    - The function assumes global variables for work_period, short_break_period, 
      long_break_period, and sound files are defined.
    """

    print("The pomodoro timer has started, let's get to work!")
    count = 0
    while count < number_of_intervals:
        time.sleep(work_period * 60)  # custom work period 
        count += 1
        pygame.mixer.Sound(short_break_sound).play()
        send_notification("Session complete. Good work!", f"Time for a short break! You have completed {count} pomodoros so far")
        time.sleep(short_break_period * 60)  # custom short break period 
        send_notification("Back to work!", f"Only {number_of_intervals - count} pomodoros to go until your long break.")
    pygame.mixer.Sound(long_break_sound).play()
    send_notification("Time for a long break!", "")
    time.sleep(long_break_period * 60)  # custom long break period
    pygame.mixer.Sound(long_break_sound).play()
    send_notification("Long break complete!", "Want to do another round?")

if __name__ == "__main__":
    #This section gets user inputs, starts the Pomodoro cycle, and handles repeat sessions.

    # Initial Pomodoro cycle
    number_of_intervals, work_period, short_break_period, long_break_period = get_user_inputs()
    start_pomodoro_cycle(number_of_intervals)

    # Loop for repeat sessions
    while True:
        answer = input("Yes or no? ")
        if answer.lower() == "yes":
            print("Let's goooooooo!")
            number_of_intervals, work_period, short_break_period, long_break_period = get_user_inputs()
            start_pomodoro_cycle(number_of_intervals)
        else:
            print("See you next time!")
            break
