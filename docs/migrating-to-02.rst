Migrating to 0.2
===========================================

django-dajaxice 0.2 has some backwards incompatible changes.


String callbacks are now deprecated
-------------------------------------
String based callbacks are now deprecated in favor of functions.

Old:

.. code-block:: javascript

    onclick="Dajaxice.example.myexample('my_js_callback');"

New:

.. code-block:: javascript

    onclick="Dajaxice.example.myexample(my_js_callback);"

Error handling
------------------------------
Dajaxice now handles your ajax function exceptions so you should update your callbacks.

Old error handling:

.. code-block:: javascript

    function my_js_callback(data){
      if(data==Dajaxice.EXCEPTION){
        alert('Error! Something happens!');
      }
      else{
        alert(data.message);
      }
    }

If all your callbacks shows the same message you can now configure Dajaxice to return
the same error message when an exception occours.

.. code-block:: javascript

    Dajaxice.setup({'default_exception_callback': function(){ alert('Error! Something happens!'); }});


If your callbacks handles exception in diferent ways you can also configure error callbacks per dajaxice call.

.. code-block:: javascript

    function custom_error(){
        alert('Error! Something happens!');
    }

    Dajaxice.simple.my_function(my_js_callback, {'user': 'tom'}, {'error_callback': custom_error});

New logger name
------------------

Dajaxice now uses the logger 'dajaxice' and not 'dajaxice.DajaxiceRequest'.
