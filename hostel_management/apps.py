from django.apps import AppConfig


class HostelManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hostel_management'

    def ready(self):
        import hostel_management.signals  # Register signals
