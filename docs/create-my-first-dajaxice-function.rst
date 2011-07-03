Creating my first dajaxice function
===========================================

Create your ajax function
------------------------------
Create a file named ``ajax.py`` inside any django app. For example ``example/ajax.py``.

Inside this file create as many as your want ajax functions.::

	from django.utils import simplejson
	from dajaxice.core import dajaxice_functions

	def myexample(request):
            return simplejson.dumps({'message':'Hello World'})

	dajaxice_functions.register(myexample)

You can also register the dajaxice function using the ``dajaxice_register`` decorator.::

	from django.utils import simplejson
	from dajaxice.decorators import dajaxice_register

	@dajaxice_register
	def myexample(request):
            return simplejson.dumps({'message':'Hello World'})

Invoque it from your JS
---------------------------

.. note::

	Since **django-dajaxice 0.2** callbacks must be JS functions and not strings.

You can invoque your ajax fuctions from javascript using:

.. code-block:: javascript

	onclick="Dajaxice.example.myexample(my_js_callback);"

The function ``my_js_callback`` is your JS function that will use your example return data. For example alert the message:

.. code-block:: javascript

	function my_js_callback(data){
	    alert(data.message);
	}

That callback will alert the message ``Hello World``.

Strings as callbacks
---------------------------

.. note::

	String callbacks are deprecated since **django-dajaxice 0.2**

.. code-block:: javascript

	onclick="Dajaxice.example.myexample('my_js_callback');"


.. code-block:: javascript

	function my_js_callback(data){
	  if(data==Dajaxice.EXCEPTION){
	    alert('Error! Something happens!');
	  }
	  else{
	    alert(data.message);
	  }
	}
