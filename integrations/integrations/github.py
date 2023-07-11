from django import forms


class Github:
    @classmethod
    def logo(cls):
        return "images/integrations/github.png"

    @classmethod
    def config_schema(cls):
        return {
            "type": "object",
            "properties": {
                "api_key": {"type": "string"},
                "owner": {"type": "string"},
                "repo": {"type": "string"},
            },
            "required": ["api_key"],
        }

    class Form(forms.Form):
        api_key = forms.CharField(required=True, label='Api Key',
            widget=forms.TextInput(attrs={"class": "form-control"}),
        )

        owner = forms.CharField(label='Owner',
            widget=forms.TextInput(attrs={"class": "form-control"}),
        )

        repo = forms.CharField(label='Repo',
            widget=forms.TextInput(attrs={"class": "form-control"}),
        )

        integration_identifier = forms.CharField(widget=forms.HiddenInput(), label="", required=True, initial="github")
