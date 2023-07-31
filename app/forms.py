from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from coder.models import CoderRecipe
from coder.interface import Interface as CoderInterface
from django.core.validators import RegexValidator
from commands.interface import Interface as CommandsInterface


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    # signup_code = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CoderRecipeForm(forms.Form):
    recipe = forms.CharField(required=True, label='Recipe Name', validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9_]+$',
                message='alphanumeric and underscores only',
                code='invalid_alphabet'
            ),
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Recipe name alphanumeric and underscores only'})
    )
    prompt = forms.CharField(widget=forms.Textarea)
    choices = map(lambda item: (item[0], item[1]["display"]), CommandsInterface.choosable_commands().items())
    # choices = [
    #     ('read_file', 'Reading Files'),
    #     ('write_file', 'Writing Files'),
    #     ('create_file', 'Creating Files'),
    #     ('github_pull_request', 'Viewing pull requests')
    # ]
    functions = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple, label='Select the actions that will be allowed for this recipe')

    def save(self, user, commit=True):
 
        recipe = self.cleaned_data['recipe']
        config = {
            'model': 'gpt-4-0613',
            'prompt': self.cleaned_data['prompt'],
            'functions': self.cleaned_data['functions'],
        }

        return CoderInterface.create_coder_recipe(recipe=recipe, user=user, config=config)
    
class CoderRecipeEditForm(forms.Form):
    recipe = forms.CharField(required=True, label='Recipe Name', validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9_]+$',
                message='alphanumeric and underscores only',
                code='invalid_alphabet'
            ),
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Recipe name alphanumeric and underscores only', 'readonly': 'readonly', 'disabled': 'disabled'})
    )
    prompt = forms.CharField(widget=forms.Textarea)
    choices = map(lambda item: (item[0], item[1]["display"]), CommandsInterface.choosable_commands().items())
    # choices = [
    #     ('read_file', 'Reading Files'),
    #     ('write_file', 'Writing Files'),
    #     ('create_file', 'Creating Files'),
    #     ('github_pull_request', 'Viewing pull requests')
    # ]
    functions = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple, label='Select the actions that will be allowed for this recipe')

    def save(self, user, commit=True):
 
        recipe = self.cleaned_data['recipe']
        config = {
            'model': 'gpt-4-0613',
            'prompt': self.cleaned_data['prompt'],
            'functions': self.cleaned_data['functions'],
        }

        CoderInterface.update_coder_recipe(recipe=recipe, user=user, config=config)

        return recipe