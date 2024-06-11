# from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from chatgpt_bot import ChatGPTAutomation

# from gemini_bot import GeminiAIAutomation
import yaml

# import time
import urllib.error

# Path to your YAML file
yaml_file_path = "propmt.yaml"

# Open and read the YAML file
with open(yaml_file_path, "r") as file:
    prompts = yaml.safe_load(file)

# Access the prompt
starter_prompt = prompts["prompt1"]
alternate_prompt = prompts["prompt4"]


def main():
    try:
        # url1 = "https://gemini.google.com/"
        url2 = "https://chatgpt.com/?model=gpt-4o"

        options1 = uc.ChromeOptions()
        options1.add_argument("--no-sandbox")
        options1.add_argument("--disable-dev-shm-usage")

        driver1 = uc.Chrome(options=options1)

        options2 = uc.ChromeOptions()
        options2.add_argument("--no-sandbox")
        options2.add_argument("--disable-dev-shm-usage")

        driver2 = uc.Chrome(options=options2)

        # Set initial window sizes
        driver1.set_window_size(800, 600)
        driver2.set_window_size(800, 600)

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

        # <=== ChatGpt ===

        bot_1_obj = ChatGPTAutomation(driver1, "[Bot 1]")
        bot_2_obj = ChatGPTAutomation(driver2, "[Bot 2]")
        bot_1_obj.set_reciever_bot_obj(bot_2_obj)
        bot_2_obj.set_reciever_bot_obj(bot_1_obj)

        print("Open GPT 1")
        # time.sleep(3)
        driver1.get(url2)
        # time.sleep(3)
        print("Open GPT 2")
        driver2.get(url2)

        print("=" * 20)
        input("Hit Enter when all is set and ready to work.")
        print("=" * 20)

        bot_1_obj.set_prompt_value(starter_prompt)
        bot_1_obj.start_convo_in_thread()

        bot_2_obj.set_prompt_value(alternate_prompt)
        bot_2_obj.start_convo_in_thread()

    except urllib.error.URLError as e:
        print("URLError:", e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
