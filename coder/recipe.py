from .recipes.function_call import FunctionCall

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
        }
    }


    @classmethod
    def get(cls, recipe):
        return cls.RECIPES.get(recipe)