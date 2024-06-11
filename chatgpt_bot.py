from aiautomation import AIAutomation
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import threading


class ChatGPTAutomation(AIAutomation):
    # Initialize class variable to control checking
    continue_checking = True

    def __init__(self, driver, bot_name):
        self.bot_name = bot_name
        self.driver = driver
        self.send_btn_visible = None
        self.stop_btn_visible = None
        self.last_response = ""
        self.bot_2_obj = None
        self.is_typing = False

    def set_reciever_bot_obj(self, bot_2_obj):
        self.bot_2_obj = bot_2_obj

    def send_response(self):
        while self.is_typing:  # Wait until typing is finished
            time.sleep(0.5)  # Sleep for a short duration
        # while True:
        if self.last_response and self.bot_2_obj:
            print(f"{self.bot_name} : sending response")
            self.bot_2_obj.set_prompt_value(self.last_response)
            # time.sleep(2)

    def find_send_button(self):
        try:
            send_button = self.driver.find_element(
                By.CSS_SELECTOR, '[data-testid="send-button"]'
            )
            if send_button:
                if not self.send_btn_visible:
                    self.send_btn_visible = True
                    self.print_last_response_content()
                    print("Send button found.")
                return True
            else:
                self.send_btn_visible = False
                return False
            # send_button.click()
        except NoSuchElementException:
            # print("Send button not found.")
            self.send_btn_visible = False
            return False

    def find_stop_button(self):
        try:
            # Check if the button is present on the page
            button = self.driver.find_elements(
                By.XPATH, '//button[@aria-label="Stop generating"]'
            )

            if button:
                if not self.stop_btn_visible:
                    self.stop_btn_visible = True
                    print("Stop button is visible.")
                return True
            else:
                # print("The button is not visible or not found.")
                self.stop_btn_visible = False
                return False
        except NoSuchElementException:
            # print("Send button not found.")
            self.stop_btn_visible = False
            return False

    def set_prompt_value(self, value):
        try:
            self.is_typing = True
            prompt_textarea = self.driver.find_element(By.ID, "prompt-textarea")
            prompt_textarea.clear()
            lines = value.split("\n")

            for line in lines:
                prompt_textarea.send_keys(line)

                prompt_textarea.send_keys(
                    Keys.SHIFT + Keys.ENTER
                )  # Press Shift+Enter after each line
                prompt_textarea.send_keys(
                    Keys.SHIFT + Keys.ENTER
                )  # Press Shift+Enter after each line

                # print(line)
                # print()
            # Submit prompt
            prompt_textarea.send_keys(Keys.ENTER)
            self.is_typing = False
        except Exception as e:
            print("An error occurred:", e)

    def print_last_response_content(self):
        # Use find_elements instead of querySelectorAll
        markdown_elements = self.driver.find_elements(By.CLASS_NAME, "markdown")
        full_text = ""
        if markdown_elements:  # Check if the list is not empty
            last_markdown_element = markdown_elements[
                -1
            ]  # Select the last element in the list

            # Concatenate text from all <p> tags inside the last markdown element
            for markdown_element in [last_markdown_element]:
                # Get all <p> tags inside the markdown element
                paragraph_elements = markdown_element.find_elements(By.TAG_NAME, "p")
                for paragraph_element in paragraph_elements:
                    # Concatenate the text from each <p> tag
                    full_text += paragraph_element.text + "\n"

        if full_text:
            # Print the concatenated text
            self.last_response = full_text
            self.send_response()
            # print(
            #     f'{self.bot_name} Text content of all paragraphs within "markdown" elements:\n',
            #     full_text,
            # )
        else:
            print(
                f'{self.bot_name} No elements found with class "markdown" containing paragraph tags.'
            )

    def start_convo(self):
        try:
            while self.continue_checking:

                self.find_send_button()
                self.find_stop_button()
                # Wait for 2 seconds before checking again
                time.sleep(2)

        except Exception as e:
            print("An error occurred:", e)

    def start_convo_in_thread(self):
        convo_thread = threading.Thread(target=self.start_convo)
        convo_thread.start()
