from django.apps import AppConfig

class CustomThemeIframeConfig(AppConfig):
    name = 'custom_theme_iframe'
    verbose_name = "Custom Theme Iframe Plugin"

    # Register as an Open edX plugin
    plugin_app = {
        'url_config': {},
    }

    def ready(self):
        from django.conf import settings
        middleware_path = 'custom_theme_iframe.middleware.ForceLightModeMiddleware'
        # Dynamically inject the middleware into the global settings
        if middleware_path not in settings.MIDDLEWARE:
            settings.MIDDLEWARE.append(middleware_path)
