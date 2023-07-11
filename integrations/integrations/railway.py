from django import forms

class Railway:
    @classmethod
    def logo(cls):
        return "images/integrations/railway.png"
    
    @classmethod
    def config_schema(cls):
        return {
            "type": "object",
            "properties": {
                "api_key": {"type": "string"},
                "username": {"type": "string"},
                "project_id": {"type": "string"},
            },
            "required": ["api_key", "username", "project_id"],
        }

    class Form(forms.Form):
        api_key = forms.CharField(required=True, label='Api Key',
            widget=forms.TextInput(attrs={"class": "form-control"}),
        )

        username = forms.CharField(required=True, label='Username',
            widget=forms.TextInput(attrs={"class": "form-control"}),
        )

        project_id = forms.CharField(required=True, label='Project Id',
            widget=forms.TextInput(attrs={"class": "form-control"}),
        )

        integration_identifier = forms.CharField(widget=forms.HiddenInput(), label="", required=True, initial="railway")
