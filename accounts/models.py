from django.db import models

class RolePermission(models.Model):
    name = models.CharField(max_length=10, default="permission")

    class Meta:
        permissions = [
                        # Bot
                        ("create_bot", "Can create bot"),
                        ("view_bot", "Can view bot"),
                        ("edit_bot", "Can edit bot"),
                        ("delete_bot", "Can delete bot"),
                        ("run_bot", "Can run bot"),
                        ("stop_bot", "Can stop bot"),

                        # Workflow
                        ("create_workflow", "Can create workflow"),
                        ("view_workflow", "Can view workflow"),
                        ("edit_workflow", "Can edit workflow"),
                        ("delete_workflow", "Can delete workflow"),
                        ("run_workflow", "Can run workflow"),

                        # Logs
                        ("view_logs", "Can view logs"),

                        # Users
                        ("manage_users", "Can manage users"),
                    ]

    def __str__(self):
        return self.name