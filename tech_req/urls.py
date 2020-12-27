from django.urls import path
from . import views

urlpatterns = [
    path('', views.TechReqListView.as_view(), name='tech_reqs'),
    path('create/', views.TechReqCreate.as_view(), name='tech_req_create'),
    path('update/<int:pk>/', views.TechReqUpdate.as_view(), name='tech_req_update'),
    path('delete/<int:pk>/', views.TechReqDelete.as_view(), name='tech_req_delete'),
    path('<int:pk>/<int:tab_id>/', views.tech_req_details, name='tech_req_details'),
    # files
    path('file/create/<int:tech_req_id>/', views.TechReqFileCreate.as_view(), name='tech_req_file_create'),
    path('file/update/<int:pk>/', views.TechReqFileUpdate.as_view(), name='tech_req_file_update'),
    path('file/delete/<int:pk>/', views.TechReqFileDelete.as_view(), name='tech_req_file_delete'),
]
