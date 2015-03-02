from django.apps import AppConfig

class LoginConfig(AppConfig):
    name = "login"
    verbose_name = "Login system"

    # Custom vars
    open_registration = False # Users can register (True) or admins must do it via admin panel (False)?