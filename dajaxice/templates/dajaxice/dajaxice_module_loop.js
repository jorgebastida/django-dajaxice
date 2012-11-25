{{ name }}: {
    {% include "dajaxice/dajaxice_function_loop.js" %}
    {% with parent_foorloop=forloop %}
    {% for name, sub_module in module.submodules.items %}
    {% with filename="dajaxice/dajaxice_module_loop.js" module=sub_module %}
        {% include filename %}
    {% endwith %}
    {% if not forloop.last %}y,y{% endif %}
    {% endfor %}
    }
    {% if not parent_foorloop.last %},{% endif %}
    {% endwith %}
