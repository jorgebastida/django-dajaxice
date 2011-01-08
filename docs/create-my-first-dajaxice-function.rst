Creating my first dajaxice function
===========================================

Create your ajax function
------------------------------
Create a file named ``ajax.py`` inside any django app. For example ``example/models.py``.

Inside this file create as many as your want ajax functions.::

	from django.utils import simplejson
	from dajaxice.core import dajaxice_functions

	def myexample(request):
            return simplejson.dumps({'message':'Hello World'})
	
	dajaxice_functions.register(myexample)


Invoque it from your JS
---------------------------

Since ``django-dajaxice>=0.1.6`` callbacks should be **JS functions**. You can invoque your AJAX methods using ``Dajaxice.example.myexample(my_js_callback)``, ``example`` will be the name of the app containing ajax.py

.. code-block:: javascript

	onclick="Dajaxice.example.myexample(my_js_callback);"

The function ``my_js_callback`` is your JS function that will use your example return data. For example:

.. code-block:: javascript

	function my_js_callback(data){
	  if(data==Dajaxice.EXCEPTION){
	    alert('Error! Something happens!');
	  }
	  else{
	    alert(data.message);
	  }
	}

That callback will alert the message ``Hello World``.

Deprecated invoque < 0.1.6
---------------------------

For backward compatibility, old style string representation is still allowed but it'isnt recomended.

Javascript call using string notation:

.. code-block:: javascript

	onclick="Dajaxice.example.myexample('my_js_callback');"

The function ``my_js_callback`` is your JS function that will use your example return data. For example:

.. code-block:: javascript

	function my_js_callback(data){
	  if(data==Dajaxice.EXCEPTION){
	    alert('Error! Something happens!');
	  }
	  else{
	    alert(data.message);
	  }
	}

That callback will alert the message ``Hello World``.
