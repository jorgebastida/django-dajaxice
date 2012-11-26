{% load url from future %}
    call: function(dajaxice_function, method, dajaxice_callback, argv, custom_settings)
    {
        var custom_settings = custom_settings || {},
            error_callback = Dajaxice.get_setting('default_exception_callback');

        if('error_callback' in custom_settings &&
           typeof(custom_settings['error_callback']) == 'function'){
            error_callback = custom_settings['error_callback'];
        }

        jqxhr = $.ajax({
            url: '{% url 'dajaxice-endpoint' %}'+dajaxice_function+'/',
            type: method,
            data: 'argv='+encodeURIComponent(JSON.stringify(argv)),
            dataType: 'json',
            success: function(data) { dajaxice_callback(data); },
            headers: { "X-Requested-With": "XMLHttpRequest",
                       "X-CSRFToken": Dajaxice.get_cookie('csrftoken') },
        }).error(function(j, t, e) { error_callback(j, t, e); });
        return jqxhr;
    },
