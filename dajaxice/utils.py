def deserialize_form(data):
    """
    Create a new QueryDict from a serialized form.
    """
    from django.http import QueryDict
    data = QueryDict(query_string=unicode(data).encode('utf-8'))
    return data