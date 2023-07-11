from .recipes.function_call import FunctionCall
from .recipes.recall import Recall
from .recipes.remember import Remember
from .recipes.custom import Custom
from .recipes.honey_badger import HoneyBadger
from .recipes.github_comment_reply import GithubCommentReply
from .models import CoderRecipe

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
        },
        'honeybadger-gpt-4-0613': {
            "recipe_class": HoneyBadger,
            "config": {
                "model": 'gpt-4-0613'
            }
        },
        'honeybadger-gpt-3.5-turbo-0613': {
            "recipe_class": HoneyBadger,
            "config": {
                "model": 'gpt-3.5-turbo-0613'
            }
        },
        'github_comment_reply-gpt-4-0613': {
            "recipe_class": GithubCommentReply,
            "config": {
                "model": 'gpt-4-0613'
            }
        },
        'github_comment_reply-3.5-turbo-0613': {
            "recipe_class": GithubCommentReply,
            "config": {
                "model": 'gpt-3.5-turbo-0613'
            }
        }
    }


    @classmethod
    def get(cls, user, recipe):
        user_recipes = CoderRecipe.objects.filter(user=user, recipe=recipe)
        config = {}
        # get the user's custom recipes
        [config.update({recipe.recipe: {"recipe_class": Custom, "config": recipe.config}}) for recipe in user_recipes]
        # merge the default recipes in
        config.update(cls.RECIPES)

        return config[recipe]