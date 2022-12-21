from django import template

"""
    The following below are template filters. They work like this:
    
    First, we load it in a template as we do with the widget_tweaks or static template tags. 
    Note that after creating this file, you will have to manually stop the development server and start it again 
    so Django can identify the new template tags
    
        {% load form_tags %}
    
    Then after that, we can use them in a template:
        
        {{ form.username|field_type }}
        
    Will return: 'TextInput'
    
    Or in case of the input_class:
    
        {{ form.username|input_class }}

        <!-- if the form is not bound, it will simply return: -->
        'form-control '
        
        <!-- if the form is bound and valid: -->
        'form-control is-valid'
        
        <!-- if the form is bound and invalid: -->
        'form-control is-invalid'
    
"""

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return f'form-control {css_class}'
