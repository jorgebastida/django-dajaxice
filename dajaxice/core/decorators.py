"""
Future
"""
def dajaxice_post_request(function):
	function.method = 'POST'
	return function
	
def dajaxice_get_request(function):
	function.method = 'GET'
	return function