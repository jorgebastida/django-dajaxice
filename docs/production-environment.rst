Dajaxice in production environment
===========================================

Dajaxice generates dynamically its JS core in every request using::

    {% load dajaxice_templatetags %}
    {% dajaxice_js_import %}

This is a good feature when you run your project in your development machine, but when you need performance in your production environment this file should be generated and served statically.

.. note::
    New in **dango-dajaxice 0.2**

``dajaxice_js_import`` templatetag can also handle ``dajaxice.core.js`` statically generated files.
You can add as first argument the path where the static file will reside inside your ``STATIC_ROOT`` and the template tag
will include this file if your ``DAJAXICE_DEBUG`` is ``False``. If not or if this argument isn't present it will include
the dynamically generated file::

    {% dajaxice_js_import "js/dajaxice.core.js"%}

This decorator also ensures that django sets the ``csrftoken`` into the response when we use dajaxice in the templates.


Generating Uncompiled version
-------------------------------
You can generate the core using ``generate_static_dajaxice``::

    python manage.py generate_static_dajaxice > dajaxice.core.js

Now you can serve this dajaxice.core.js with your favourite `CDN. <http://en.wikipedia.org/wiki/Content_Delivery_Network>`_

Generating Compiled version using Google Closure
---------------------------------------------------

The `Closure Compiler <http://code.google.com/intl/es/closure/>`_ compiles JavaScript into compact, high-performance code. The compiler removes dead code and rewrites and minimizes what's left so that it downloads and runs quickly. It also also checks syntax, variable references, and types, and warns about common JavaScript pitfalls. These checks and optimizations help you write apps that are less buggy and easier to maintain.::

    python manage.py generate_static_dajaxice --compile closure > dajaxice.core.js
