django-dajaxice
===============

.. image:: https://badge.fury.io/py/django-dajaxice.png
    :target: http://badge.fury.io/py/django-dajaxice

.. image:: https://travis-ci.org/jorgebastida/django-dajaxice.png?branch=master
    :target: https://travis-ci.org/jorgebastida/django-dajaxice

.. image:: https://pypip.in/d/django-dajaxice/badge.png
    :target: https://crate.io/packages/django-dajaxice/


Dajaxice is the communication core of dajaxproject. It's main goal is to trivialize the asynchronous communication within the django server side code and your js code.

dajaxice is JS-framework agnostic and focuses on decoupling the presentation logic from the server-side logic. dajaxice only requieres 5 minutes to start working.


Project status
----------------
From ``v0.6`` this project is not going to accept new features. In order to not break existing projects using this library, ``django-dajaxice`` will be maintained until ``django 1.8`` is released.


Should I use django-dajaxice?
------------------------------
In a word, No. I created this project 4 years ago as a cool tool in order to solve one specific problem I had at that time.

These days using this project is a bad idea.

Perhaps I'm more pragmatic now, perhaps my vision of how my django projects should be coupled to libraries like this has change, or perhaps these days I really treasure the purity and simplicity of a vanilla django development.

If you want to mimic what this project does, you would only need some simple views and jQuery.

Forget about adding more unnecessary complexity.  Keep things simple.


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
