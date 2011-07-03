Available Settings
===========================================

DAJAXICE_MEDIA_PREFIX
------------------------
**Optional**

Dajaxice internally generates urls to every method registered, this prefix will be include in that url. http://domain.com/dajaxice/...

Defaults to ``dajaxice``

DAJAXICE_DEBUG
------------------------

**Optional**

Force/Avoid show debug info in development server.

Defaults to ``True``

DAJAXICE_NOTIFY_EXCEPTIONS
----------------------------

**Optional**

Force/Avoid send Exception messages to  settings.ADMINS

Defaults to ``False``

DAJAXICE_CACHE_CONTROL
------------------------

**Optional**

Cache max_age for dajaxice.core.js file.

Defaults to ``5 x 24 x 60 x 60``

DAJAXICE_XMLHTTPREQUEST_JS_IMPORT
-----------------------------------

**Optional**

include XmlHttpRequest.js inside dajaxice.core.js

Defaults to ``True``

DAJAXICE_JSON2_JS_IMPORT
-----------------------------------

Include json2.js inside dajaxice.core.js

**Optional**

Defaults to ``True``

DAJAXICE_EXCEPTION
-----------------------------------

**Optional**

Default data sent when an exception occurs.

Defaults to ``"DAJAXICE_EXCEPTION"``

DAJAXICE_JS_DOCSTRINGS
------------------------

**Optional**

If True, Dajaxice will add your ajax functions docstrings as a comment before the js functions in dajaxice.core.js

Defaults to ``False``


DAJAXICE_FUNCTIONS
-----------------------------------

.. note::

    Deprecated since **django-dajaxice 0.1.5**

This option contains a list of all functions callable via ajax.

**Since 0.1.5 dajaxice functions should be registered using.**::

    dajaxice_functions.register(function)

Defaults to ``()``
