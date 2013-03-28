"""
Django template loader that allows you to load a template from a
specific application. This allows you to both extend and override
a template at the same time. The default Django loaders require you
to copy the entire template you want to override, even if you only
want to override one small block.

Template usage example::

    {% extends "admin:admin/base.html" %}

It is also possible to exclude an app when extending a template. This is 
useful when you want to extend and override a template without explicitly 
specifying the base template to use. The above admin example usage would not work
properly when using an additional app that overrides the built in admin
templates, for instance django-grappelli 
(https://github.com/sehmaschine/django-grappelli) or django-admin-bootstrapped 
(https://github.com/riccardo-forina/django-admin-bootstrapped)

Exclude app usage example:

    {% extends "-myapp:admin/base.html" %}

Settings::

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'apptemplates.Loader',
    )

Based on: http://djangosnippets.org/snippets/1376/
"""

from os.path import dirname, join, abspath

from django.conf import settings
from django.utils.importlib import import_module
from django.template.loaders.app_directories import (
    Loader as AppDirLoader, app_template_dirs)

_cache = {}

def get_app_template_dir(app_name):
    """Get the template directory for an application

    We do not use django.db.models.get_app, because this will fail if an
    app does not have any models.

    Returns a full path, or None if the app was not found.
    """
    if app_name in _cache:
        return _cache[app_name]
    template_dir = None
    for app in settings.INSTALLED_APPS:
        if app.split('.')[-1] == app_name:
            # Do not hide import errors; these should never happen at this point
            # anyway
            mod = import_module(app)
            template_dir = join(abspath(dirname(mod.__file__)), 'templates')
            break
    _cache[app_name] = template_dir
    return template_dir


class Loader(AppDirLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = app_template_dirs

        if ':' in template_name:
            app_name, template_name = template_name.split(":", 1)

            # should we exclude this app?
            if app_name.startswith('-'):
                app_name = app_name[1:]
                try:
                    template_dirs = list(template_dirs)
                    template_dirs.remove(get_app_template_dir(app_name))
                except ValueError: 
                    pass
            # or use it exclusively?
            else:
                template_dirs = [get_app_template_dir(app_name)]

        return super(Loader, self).get_template_sources(
            template_name, template_dirs)