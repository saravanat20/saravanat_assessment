from django.contrib import admin
from django.urls import path
from . import views
from .api import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.home, name='home'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('register/',views.register, name='register'),
    path('record/<int:pk>',views.customer_record, name='record'),
    path('delete_record/<int:pk>',views.delete_record, name='delete'),
    path('add_record/',views.add_record, name='add_record'),
    path('update_record/<int:pk>',views.update_record, name='update_record'),
    path('search_name/', views.search_name, name='search_name'),
    path('api/recordmodels/', views.RecordModelListCreate.as_view(), name='recordmodel-list-create'),
    path('api/recordmodels/<int:pk>/', views.RecordModelRetrieveUpdateDestroy.as_view(), name='recordmodel-retrieve-update-destroy'),
    path('create/', views.create_object, name='create_object'),
    path('<int:id>/', views.retrieve_object, name='retrieve_object'),
    path('<int:id>/update/', views.update_object, name='update_object'),
    path('<int:id>/delete/', views.delete_object, name='delete_object'),

]