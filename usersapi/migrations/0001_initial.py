
from django.db import migrations
from django.contrib.auth.models import User

def create_users(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    user = User()
    user.username = 'admin'
    user.password = 'admin'
    user.email = 'edgar.ceron@correounivalle.edu.co'
    user.first_name = 'Edgar'
    user.last_name = 'Ceron'
    user.save()

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_users),
    ]