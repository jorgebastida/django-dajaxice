from dajaxice.core import dajaxice_functions

def dajaxice_register_function(original_function):
    """
    Register the original funcion and returns it
    """
    
    dajaxice_functions.register(original_function)
    return original_function
