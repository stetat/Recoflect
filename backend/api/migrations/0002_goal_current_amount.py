from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="goal",
            name="current_amount",
            field=models.IntegerField(default=0),
        ),
    ]
