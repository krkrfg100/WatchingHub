
from django.urls import path
from . import views

urlpatterns = [

 #main path
 path('', views.index, name="index"),
 path('login', views.login_view, name="login"),
 path('logout', views.logout_view, name="logout"),
 path('register', views.register, name="register"),
 path('addshow', views.addshow, name="addshow"),
 path('show_info/<int:show_id>', views.show_info, name="show_info"),
 path('edit_show/<int:show_id>', views.edit_show, name="edit_show"),
 path('DateFinishedWatching/<int:show_id>', views.DateFinishedWatching, name="DateFinishedWatching"),
 path('delete_show', views.delete_show, name="delete_show"),
 path('shorted_by', views.shorted_by, name="shorted_by"),
 path('edit_filter', views.edit_filter, name="edit_filter"),
 path('add_Classification', views.add_Classification, name="add_Classification"),

]