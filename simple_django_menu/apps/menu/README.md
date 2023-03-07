# Menu - 3rd party Django app to provide tree-like menu

This could be a full-ready 3d-party Django integrated app and be installed 
in a way like `pip install django-great-menu`

## Setting up

### Add menu application to `INSTALLED_APP` in Django settings file

```python
INSTALLED_APPS = [
    ...
    'apps.menu',
    ...
]
```


### Apply migrations

`python manage.py makemigraions`

`python manage.py migrate`

## Usage

### Create admin user `python manage.py createsuperuser`

### Create menu items using django-admin

### In template file load tags by `{% load menu_tags %}`

### To render the menu use `draw_menu` tag 

### Usage example:
```html
<html>
    {% load menu_tags %}
    ...
    <head>
    ...
    </head>
    ...
    <body>
        ...
        {% draw_menu 'Some Menu Name' %}
        ...
    </body>
    ...
</html>
```