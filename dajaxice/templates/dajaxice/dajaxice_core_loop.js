{{ module.name }}: {
    {% for function in module.functions %}
            {{ function.name }}: function(callback_function, argv){
                Dajaxice.call('{{function.get_callable_path}}', callback_function, argv);
            }{% if not forloop.last %},{% endif %}
    {% endfor %}
            
    {% for sub_module in module.sub_modules %}
    {% with "dajaxice/dajaxice_core_loop.js" as filename %}  
    {% with sub_module as module %}
        {% include filename %}
    {% endwith %}
    {% endwith %}
    {% endfor %}
        }{% if not forloop.last %},{% endif %}