from django.urls import path
from .views import profile_detail_page, profile_list_page

urlpatterns = [
    path('', profile_list_page),
    path('<username>/', profile_detail_page)
]