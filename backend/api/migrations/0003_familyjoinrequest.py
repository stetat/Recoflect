import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_goal_current_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="FamilyJoinRequest",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "desired_role",
                    models.IntegerField(choices=[(1, "Parent"), (2, "Child"), (3, "None")]),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Pending"), (2, "Approved"), (3, "Rejected")],
                        default=1,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "family",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="join_requests",
                        to="api.family",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="family_join_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
