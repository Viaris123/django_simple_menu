from django.db import models

from .const import MENU_NAME_LENGTH, MENU_ITEM_LENGTH, MENU_URL_LENGTH


class Menu(models.Model):
    name = models.CharField(max_length=MENU_NAME_LENGTH, verbose_name='Menu name')
    meta_info = models.TextField(null=True, blank=True, verbose_name='Some metadata about the menu')

    class Meta:
        ordering = ['name']
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=MENU_ITEM_LENGTH, verbose_name='Menu item name', null=False)
    parent_item = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    url = models.CharField(max_length=MENU_URL_LENGTH, help_text='Use reverse URL. Example: \'main:menu_example\'')

    class Meta:
        ordering = ['name']
        verbose_name = 'Menu item'
        verbose_name_plural = 'Menu items'

    def __str__(self):
        return f"{self.menu} -> {self.name}"
