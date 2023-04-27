from commands import Base

class AskQuestion(Base):
    @classmethod
    def required_arguments(cls):
        return ["question"]
    
    def execute(self, question):
        input(f"{question}").rstrip('\n')