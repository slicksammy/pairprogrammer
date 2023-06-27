from django.db import migrations, models
from app.models import UserPreference


def create_user_preferences(apps, schema_editor):
    # We can't import the UserPreference model directly as it may be a newer version than this migration expects.
    # We use the historical version.
    User = apps.get_model('auth', 'User')
    UserPreference = apps.get_model('app', 'UserPreference')

    for user in User.objects.all():
        UserPreference.objects.get_or_create(user=user, defaults={'preferences': {"model": "gpt-4-0613"}})


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_userpreference'),
    ]

    operations = [
        migrations.RunPython(create_user_preferences),
    ]
