import time
from .config import Config

class Interface:
    
    @classmethod
    def create_event(cls, event, event_data):
        if Config.event_exists(event):
            event_class = Config.get_event(event)["event_class"]
            event_class.create(event_data)
        else:
            return None
        

    # while True:
    #     print("hello")
    #     time.sleep(10)
    # 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 