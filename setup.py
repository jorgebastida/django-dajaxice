from distutils.core import setup

setup(
    name = "django-dajaxice",
    version = "0.1.5",
    author = "Benito Jorge Bastida Perez",
    author_email = "jorge@thecodefarm.com",
    description = "Agnostic and easy to use ajax library for django",
    download_url = "http://cloud.github.com/downloads/jorgebastida/django-dajaxice/django-dajaxice-0.1.5.tar.gz",
    url = "http://dajaxproject.com",
    packages= ['dajaxice', 'dajaxice.templatetags', 'dajaxice.core', 'dajaxice.management.commands'],
    package_data = {'dajaxice': ['templates/dajaxice/*']},
    classifiers=['Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Utilities']
)