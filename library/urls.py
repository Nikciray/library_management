from django.urls import path

from . import views
app_name = 'library'
urlpatterns = [
    path("",views.index,name='index'),
    path("search/<int:pg_no>/",views.search,name='search'),
    path("detail/<int:pk>/",views.book_detail,name='book_detail')
]