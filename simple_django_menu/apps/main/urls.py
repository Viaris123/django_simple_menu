from django.urls import path

from .views import MenuExampleView

urlpatterns = [
    path('menu_example/', MenuExampleView.as_view(), name='menu_example'),
]
