from distutils.core import setup

setup(
    name = "django-dajaxice",
    version = "0.2",
    author = "Benito Jorge Bastida Perez",
    author_email = "me@jorgebastida.com",
    description = "Agnostic and easy to use ajax library for django",
    download_url = "http://cloud.github.com/downloads/jorgebastida/django-dajaxice/django-dajaxice-0.2.tar.gz",
    url = "http://dajaxproject.com",
    packages= ['dajaxice', 'dajaxice.templatetags', 'dajaxice.core', 'dajaxice.management', 'dajaxice.management.commands'],
    package_data = {'dajaxice': ['templates/dajaxice/*']},
    long_description="""\
Easy to use AJAX library for django, all the presentation logic
resides outside the views and doesn't require any JS Framework.
Dajaxice uses the unobtrusive standard-compliant (W3C) XMLHttpRequest
1.0 object.
""",
    classifiers=['Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Utilities']
)
