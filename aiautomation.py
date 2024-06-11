from abc import ABC, abstractmethod


class AIAutomation(ABC):
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def set_prompt_value(self, value):
        pass

    @abstractmethod
    def print_last_response_content(self):
        pass

    @abstractmethod
    def set_reciever_bot_obj(self):
        pass

    @abstractmethod
    def send_response(self):
        pass

    @abstractmethod
    def find_send_button(self):
        pass

    @abstractmethod
    def find_stop_button(self):
        pass

    @abstractmethod
    def start_convo(self):
        pass

    @abstractmethod
    def start_convo_in_thread(self):
        pass
