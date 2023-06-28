from .recipes.function_call import FunctionCall
from .recipes.recall import Recall
from .recipes.remember import Remember

class Recipe:
    RECIPES={
        'gpt-4-0613': {
            "recipe_class": FunctionCall,
            "config": {
                "model": "gpt-4-0613"
            }
        },
        'gpt-3.5-turbo-0613': {
            "recipe_class": FunctionCall,
            "config": {
                "model": "gpt-3.5-turbo-0613"
            } 
        },
        'recall-gpt-4-0613': {
            "recipe_class": Recall,
            "config": {
                "model": "gpt-4-0613"
            }
        },
        'recall-gpt-3.5-turbo-0613': {
            "recipe_class": Recall,
            "config": {
                "model": "gpt-3.5-turbo-0613"
            }
        },
        'remember-gpt-4-0613': {
            "recipe_class": Remember,
            "config": {
                "model": "gpt-4-0613"
            }
        },
        'remember-gpt-3.5-turbo-0613': {
            "recipe_class": Remember,
            "config": {
                "model": "gpt-3.5-turbo-0613"
            }
        }
    }


    @classmethod
    def get(cls, recipe):
        return cls.RECIPES[recipe]