var Dajaxice = {
    {% for module,functions in dajaxice_js_functions.items %}
        {{ module }}: {
            {% for function in functions %}
                {{ function }}: function(callback_function,argv){
                    Dajaxice.call('{{module}}.{{function}}',callback_function,argv);
	            }{% ifnotequal forloop.counter functions|length %},{% endifnotequal %}
            {% endfor %}
        },
    {% endfor %}
    
    call: function(dajaxice_function, dajaxice_callback, argv)
    {
        var send_data = [];
        send_data.push('callback='+dajaxice_callback);
        if(typeof(argv) == 'object')
        {
            for(arg in argv)
            {
                send_data.push(arg+'='+escape(argv[arg]));
            }
        }
        send_data = send_data.join('&');
        var oXMLHttpRequest = new XMLHttpRequest;
        oXMLHttpRequest.open('POST', '/{{DAJAXICE_URL_PREFIX}}/'+dajaxice_function+'/');
        oXMLHttpRequest.onreadystatechange = function() {
            if (this.readyState == XMLHttpRequest.DONE) {
                eval(this.responseText);
            }
        }
        oXMLHttpRequest.send(send_data);
    }
};
window['Dajaxice'] = Dajaxice;