# from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from chatgpt_bot import ChatGPTAutomation

# from gemini_bot import GeminiAIAutomation
import yaml

import time
import urllib.error
import signal

# import sys

# Path to your YAML file
YAML_FILE_PATH = "propmt.yaml"

# Open and read the YAML file
with open(YAML_FILE_PATH, "r") as file:
    prompts = yaml.safe_load(file)

# Access the prompt
starter_prompt = prompts["prompt1"]
alternate_prompt = prompts["prompt4"]

# Define global variables to hold driver instances
driver1 = None
driver2 = None


def get_chrome_driver_with_options():
    """
    Returns Chrome options with common settings applied.
    """
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return uc.Chrome(options=options)


# Set initial window sizes and positions for both drivers
def set_window_sizes_and_positions(driver1, driver2):
    """
    Set initial window sizes and positions for both drivers.

    Args:
        driver1 (undetected_chromedriver.Chrome): The Selenium driver for the first browser window.
        driver2 (undetected_chromedriver.Chrome): The Selenium driver for the second browser window.
    """
    # Set initial window sizes
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    driver1.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    driver2.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Get screen resolution
    screen_width = driver1.execute_script("return screen.width;")
    screen_height = driver1.execute_script("return screen.height;")

    # Calculate positions for windows
    left_window_position = 0
    right_window_position = screen_width / 2

    driver1.set_window_size(right_window_position, screen_height)
    driver2.set_window_size(right_window_position, screen_height)

    # Position windows side by side
    driver1.set_window_position(left_window_position, 0)
    driver2.set_window_position(right_window_position, 0)


def cleanup():
    # Close the browser windows and release resources
    print("Cleanup, Quit drivers")
    if driver1:
        driver1.quit()
    if driver2:
        driver2.quit()


def main():
    try:
        # URL1  = "https://gemini.google.com/"
        URL2 = "https://chatgpt.com/?model=gpt-4o"

        # <=== ChatGpt ===

        bot_1_obj = ChatGPTAutomation(driver1, "[Bot 1]")
        bot_2_obj = ChatGPTAutomation(driver2, "[Bot 2]")
        bot_1_obj.set_reciever_bot_obj(bot_2_obj)
        bot_2_obj.set_reciever_bot_obj(bot_1_obj)

        print("Open GPT 1")
        # time.sleep(3)
        driver1.get(URL2)
        time.sleep(3)
        print("Open GPT 2")
        driver2.get(URL2)

        print("=" * 20)
        input("\nHit Enter when all is set and ready to work.")
        print("=" * 20)

        bot_1_obj.set_prompt_value(starter_prompt)
        bot_1_obj.start_convo_in_thread()

        bot_2_obj.set_prompt_value(alternate_prompt)
        bot_2_obj.start_convo_in_thread()

    except KeyboardInterrupt:
        print("\n** Exiting program due to Ctrl+C. **")
        cleanup()
        # sys.exit(0)
    except urllib.error.URLError as e:
        print("URLError occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


if __name__ == "__main__":

    def handle_interrupt(sig, frame):
        print("\n** Exiting program due to Ctrl+C. **")
        cleanup()
        # exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)  # Register Ctrl+C handler

    print("*" * 40)
    print("[                                      ]")
    print("|            GPT Showdown              |")
    print("[          **Ctrl+C to Exit**          ]")
    print("*" * 40)

    # Initialize driver1 and driver2
    driver1 = get_chrome_driver_with_options()
    driver2 = get_chrome_driver_with_options()
    set_window_sizes_and_positions(driver1, driver2)

    # Call the main function
    main()
