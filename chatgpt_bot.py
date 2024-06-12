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
        """
        Initialize ChatGPTAutomation object.

        Parameters:
        - driver: Selenium WebDriver object.
        - bot_name: Name of the bot.
        """
        self.bot_name = bot_name
        self.driver = driver
        self.send_btn_visible = None
        self.stop_btn_visible = None
        self.last_response = ""
        self.bot_2_obj = None
        self.is_typing = False

    def set_reciever_bot_obj(self, bot_2_obj):
        """
        Set the receiver bot object.

        Parameters:
        - bot_2_obj: Bot object to set as the receiver.
        """
        self.bot_2_obj = bot_2_obj

    def send_response(self):
        """
        Send response to the receiver bot.
        """
        while self.bot_2_obj.is_typing:  # Wait until typing is finished
            time.sleep(0.5)  # Sleep for a short duration
        if self.last_response and self.bot_2_obj:
            print(f"{self.bot_name} : sending response")
            self.bot_2_obj.set_prompt_value(self.last_response)

    def click_btn_send_prompt(self):
        """
        Click the send prompt button.
        """
        try:
            send_button = self.driver.find_element(
                By.CSS_SELECTOR,
                '[data-testid="send-button"], [data-testid="fruitjuice-send-button"]',
            )
            if send_button is not None and send_button.is_displayed():
                send_button.click()
        except NoSuchElementException:
            print("Send button not found for click.")

    def find_send_button(self):
        """
        Find the send button on the page.
        """
        try:
            send_button = self.driver.find_element(
                By.CSS_SELECTOR,
                '[data-testid="send-button"], [data-testid="fruitjuice-send-button"]',
            )
            if send_button is not None and send_button.is_displayed():
                if not self.send_btn_visible:
                    self.send_btn_visible = True
                    self.print_last_response_content()
                    print("Send button found.")
                return True
            else:
                self.send_btn_visible = False
                return False
        except NoSuchElementException:
            self.send_btn_visible = False
            return False

    def find_stop_button(self):
        """
        Find the stop button on the page.
        """
        try:
            button = self.driver.find_elements(
                By.XPATH, '//button[@aria-label="Stop generating"]'
            )

            if button:
                if not self.stop_btn_visible:
                    self.stop_btn_visible = True
                    print("Stop button is visible.")
                return True
            else:
                self.stop_btn_visible = False
                return False
        except NoSuchElementException:
            self.stop_btn_visible = False
            return False

    def set_prompt_value(self, value):
        """
        Set the prompt value in the prompt text area.

        Parameters:
        - value: Value to set in the prompt text area.
        """
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

            self.click_btn_send_prompt()
            print("submit prompt done")
            self.is_typing = False
        except Exception as e:
            print("An error occurred:", e)

    def print_last_response_content(self):
        """
        Print the content of the last response.
        """
        markdown_elements = self.driver.find_elements(By.CLASS_NAME, "markdown")
        full_text = ""
        if markdown_elements:
            last_markdown_element = markdown_elements[-1]
            for markdown_element in [last_markdown_element]:
                paragraph_elements = markdown_element.find_elements(By.TAG_NAME, "p")
                for paragraph_element in paragraph_elements:
                    full_text += paragraph_element.text + "\n"

        if full_text:
            self.last_response = full_text
            self.send_response()
        else:
            print(
                f'{self.bot_name} No elements found with class "markdown" containing paragraph tags.'
            )

    def start_convo(self):
        """
        Start the conversation loop.
        """
        try:
            while self.continue_checking:
                self.find_send_button()
                self.find_stop_button()
                time.sleep(2)  # Wait for 2 seconds before checking again
        except Exception as e:
            print("An error occurred:", e)

    def start_convo_in_thread(self):
        """
        Start the conversation loop in a separate thread.
        """
        convo_thread = threading.Thread(target=self.start_convo)
        convo_thread.start()
