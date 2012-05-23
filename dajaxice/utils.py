from django.http import QueryDict


def deserialize_form(data):
    """
    Create a new QueryDict from a serialized form.
    """
    data = QueryDict(query_string=unicode(data).encode('utf-8'))
    return data
