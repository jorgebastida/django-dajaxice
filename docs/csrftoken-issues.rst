CSRF Token issues
====================

.. note::
    New in **django-dajaxice 0.2**


The templatetag ``dajaxice_js_import`` ensures that django sets the ``csrftoken`` into the response when we use dajaxice in our templates.
This is the reason behind the new ``django.core.context_processors.request`` requirement in ``TEMPLATE_CONTEXT_PROCESSORS``. This templatetag
forces django to include the ``csrftoken`` in every response that uses a template with this decorator.::

    {% dajaxice_js_import %}

Further information:

* https://github.com/jorgebastida/django-dajaxice/issues/30
* https://docs.djangoproject.com/en/1.2/ref/contrib/csrf/#ajax
