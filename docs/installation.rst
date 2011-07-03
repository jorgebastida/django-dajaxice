Installation
===========================================
Follow this instructions to start using dajaxice in your django project.

Installing dajaxice
--------------------------

Add `dajaxice` in your project settings.py inside ``INSTALLED_APPS``::

    INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'dajaxice',
            ...
    )

Ensure that ``TEMPLATE_LOADERS``, looks like the following. Probably you need to uncomment the last line.::

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )

Ensure that ``TEMPLATE_CONTEXT_PROCESSORS`` has ``django.core.context_processors.request``.::

    TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                                   "django.core.context_processors.debug",
                                   "django.core.context_processors.i18n",
                                   "django.core.context_processors.media",
                                   "django.core.context_processors.static",
                                   "django.core.context_processors.request",
                                   "django.contrib.messages.context_processors.messages")

Add ``DAJAXICE_MEDIA_PREFIX`` to your settings.py::

	DAJAXICE_MEDIA_PREFIX="dajaxice"

Configure dajaxice url
------------------------

Add the following code inside urls.py::

	from dajaxice.core import dajaxice_autodiscover
	dajaxice_autodiscover()

Add a new line in urls.py urlpatterns with this code::

	(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

Probably you need to import settings::

	from django.conf import settings

Install dajaxice in your templates
-------------------------------------
Dajaxice needs to include some js in your template, you should load ``dajaxice_templatetags`` and use ``dajaxice_js_import`` TemplateTag inside your head section. This TemplateTag will print needed js.

.. code-block:: html

	{% load dajaxice_templatetags %}

	<html>
	  <head>
	    <title>My base template</title>
	    ...
	    {% dajaxice_js_import %}
	  </head>
        ...
	</html>


This templatetag include dynamic dajaxice core. It's a good idea in production environment serving this file statically.
Check :doc:`production-environment` for more production-performance help.

Use Dajaxice!
--------------------------
Now you can follow :doc:`create-my-first-dajaxice-function`.

If you need more help, you can download the example project here: http://github.com/downloads/jorgebastida/django-dajaxice/dajaxice-examples.tar.gz
