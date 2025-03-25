from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('Don', '0001_initial'),  # Remplacez par le nom réel de la dernière migration
    ]

    operations = [
        migrations.RemoveField(
            model_name='donneur',
            name='taille',
        ),
    ]