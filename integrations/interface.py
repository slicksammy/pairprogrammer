import jsonschema
from jsonschema.exceptions import ValidationError
from .models import Integration
from django import forms
from django.core.validators import RegexValidator
from .config import Config

class Interface:
    @classmethod
    def create_integration(cls, integration_identifier, user, config):
        integration_class = Config.INTEGRATIONS[integration_identifier]["integration_class"]
        config_schema = integration_class.config_schema()
        jsonschema.validate(config, config_schema)
        
        return Integration.objects.create(
            user=user,
            integration=integration_identifier,
            config=config
        )
    
    @classmethod
    def upsert_integration(cls, integration_identifier, user, config):
        integration_class = Config.INTEGRATIONS[integration_identifier]["integration_class"]
        config_schema = integration_class.config_schema()
        jsonschema.validate(config, config_schema)

        integration = Integration.objects.filter(user=user, integration=integration_identifier).order_by('-created_at').first()
        if integration is not None:
            integration.config = config
            integration.save()
        
            return integration
        else:
            return Integration.objects.create(
                user=user,
                integration=integration_identifier,
                config=config
            )

    @classmethod
    def available_integrations(cls):
        integrations = []
        for key, value in Config.INTEGRATIONS.items():
            integrations.append({
                "name": key,
                "logo": value["integration_class"].logo(),
            })
        
        return integrations

    @classmethod
    def form(cls, user, integration_identifier):
        # will fail if integration identifier doesnt exist
        Config.INTEGRATIONS[integration_identifier]

        integration = Integration.objects.filter(user=user, integration=integration_identifier).first()
        initial={}
        if integration is not None:
            initial = integration.config
        
        integration_class = Config.INTEGRATIONS[integration_identifier]["integration_class"]
        form = integration_class.Form(initial=initial)
        # for field in form:
        #     breakpoint()

        return form
    
    @classmethod
    def save_form(cls, **kwargs):
        user = kwargs.pop('user')
        
        integration_class = Config.INTEGRATIONS[kwargs['integration_identifier']]["integration_class"]
        form = integration_class.Form(kwargs)
        
        if form.is_valid():
            try:
                # TODO validate the config
                config = {k: v for k, v in form.cleaned_data.items() if k != "integration_identifier"}
                integration = cls.upsert_integration(user=user, integration_identifier=form.cleaned_data["integration_identifier"], config=config)
                return { "integration_identifier": integration.integration }
            except ValidationError as e:
                return { "error_message": e.message, "form": form }
        else:
            return { "form": form }
        
    @classmethod
    def get_integrations(cls, user):
        integrations = []
        for integration in Integration.objects.filter(user=user).order_by('-created_at'):
            integrations.append({
                "id": integration.id,
                "integration": integration.integration,
                "config": integration.config,
            })
        
        return integrations
    
    @classmethod
    def get_config(cls, user, integration_identifier):
        integration = Integration.objects.filter(user=user, integration=integration_identifier).order_by('-created_at').first()
        if integration is not None:
            return integration.config
        else:
            return None