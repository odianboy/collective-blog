from django.apps import AppConfig


class AppBlogConfig(AppConfig):
    name = 'apps.blog'

    def ready(self):
        import apps.blog.signals
