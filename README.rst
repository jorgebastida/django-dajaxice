django-dajaxice
===============

.. image:: https://travis-ci.org/markuz/django-dajaxice.svg
    :target: https://travis-ci.org/markuz/django-dajaxice


Dajaxice is the communication core of dajaxproject. It's main goal is to trivialize the asynchronous communication within the django server side code and your js code.

dajaxice is JS-framework agnostic and focuses on decoupling the presentation logic from the server-side logic. dajaxice only requieres 5 minutes to start working.

This is a fork that will keep dajaxice compatible with django.


Project status
----------------
From ``v0.6`` this project is not going to accept new features. In order to not break existing projects using this library, The original ``django-dajaxice`` will be maintained until ``django 1.8`` is released. 

This is a fork that will keep dajaxice compatible with django.


Should I use django-dajaxice?
------------------------------
The original autor discourages the usage of this project, but you can use this fork to if you want to have a compatible version of dajaxice with django.


Project Aims
------------

  * Isolate the communication between the client and the server.
  * JS Framework agnostic (No Prototype, JQuery... needed ).
  * Presentation logic outside the views (No presentation code inside ajax functions).
  * Lightweight.
  * Crossbrowsing ready.
  * Unobtrusive standard-compliant (W3C) XMLHttpRequest 1.0 object usage.

Official site http://dajaxproject.com
Documentation http://readthedocs.org/projects/django-dajaxice/
