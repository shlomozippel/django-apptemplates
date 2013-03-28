(Forked from https://bitbucket.org/wojas/django-apptemplates)

django-apptemplates is a Django template loader that allows you to load a 
template from a specific application. This allows you to both extend and 
override a template at the same time. The default Django loaders require 
you to copy the entire template you want to override, even if you only
want to override one small block.

Template usage example (extend and override Django admin base template)::

    {% extends "admin:admin/base.html" %}

It is also possible to exclude an app when extending a template. This is 
useful when you want to extend and override a template without explicitly 
specifying the base template to use. The above admin example usage would not work
properly when using an additional app that overrides the built in admin
templates, for instance django-grappelli (https://github.com/sehmaschine/django-grappelli) or django-admin-bootstrapped (https://github.com/riccardo-forina/django-admin-bootstrapped)

Exclude app usage example:

    {% extends "-myapp:admin/base.html" %}

Settings::

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'apptemplates.Loader',
    )

Based on: http://djangosnippets.org/snippets/1376/
