from django.apps import AppConfig


class PhonebookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PhoneBook'
    
    def ready(self):
        """Імпортуємо сигнали при запуску додатку"""
        import PhoneBook.signals  # noqa