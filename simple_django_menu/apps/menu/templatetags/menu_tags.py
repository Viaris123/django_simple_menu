from collections import OrderedDict

from django import template
from django.urls import reverse
from django.utils.html import mark_safe

from ..models import MenuItem

register = template.Library()


def flat_to_tree(menu_items):
    # this func was found and modified from stackoverflow
    menu_tree = OrderedDict()
    parents = set()
    root_id = None

    for item in menu_items:
        id, parent_id = item['id'], item['parent_item']
        menu_tree[id] = {**item, 'children': []}
        menu_tree[id]['url'] = f'{reverse(menu_tree[id]["url"])}?menu_item_id={item["id"]}'
        parents.add(parent_id)
        if id == parent_id:
            root_id = id

    for id in (parents - menu_tree.keys()):
        menu_tree[id] = {
            'id': id, 'parent_item': root_id, 'children': []
        }

    for id, item in menu_tree.items():
        parent_item = menu_tree[item.pop('parent_item')]
        if id != root_id:
            parent_item['children'].append(item)

    return menu_tree[root_id]['children']


def subtree_has_active_item(tree, active_id):
    for item in tree:
        if str(item['id']) == active_id:
            return item

        if item.get('children'):
            if found_item := subtree_has_active_item(item['children'], active_id):
                return found_item
    return None


def render_nested(menu_tree, active_id=None):
    nested_elements = []

    for item in menu_tree:
        is_active = str(item['id']) == active_id
        item_li = f'{item["name"]}'
        item_li = f'<a href="{item["url"]}">{item_li}</a>'  # wraps with link

        if is_active:
            item_li = f'<b>{item_li}</b>'  # highlight active item

        if item.get('children'):
            nested_rendered = render_nested(item['children'], active_id)
            if is_active or subtree_has_active_item(item['children'], active_id):  # adding caret arrow
                item_li = f'&#x25BC; {item_li}'  # &#x27B7;
                item_li = f'{item_li}{nested_rendered}'  # adding nested elements
            else:
                item_li = f'&#x25B6; {item_li}'  # &#x27B5;

        item_li = f'<li>{item_li}</li>'  # wrapping item with <li>
        nested_elements.append(item_li)

    return f'<ul>{"".join(nested_elements)}</ul>'


@register.simple_tag(name='draw_menu', takes_context=True)
def draw_menu(context, menu_name):
    active_item_id = context['request'].GET.get('menu_item_id')

    items = MenuItem.objects.filter(menu__name=menu_name).values('id', 'parent_item', 'name', 'url')  # single query

    menu_tree = flat_to_tree(items)

    rendered_menu = render_nested(menu_tree, active_id=active_item_id)

    menu_rendered = f'<span>{menu_name}</span><div class="{menu_name.replace(" ", "_")}">{rendered_menu}</div>'

    return mark_safe(menu_rendered)
