from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanListView.as_view(), name='testplans'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('<int:pk>/<int:tab_id>/', views.testplan_details, name='testplan_details'),
    path('clone/<int:pk>/', views.testplan_clone, name='testplan_clone'),
    path('clear_tests/<int:pk>/', views.clear_tests, name='clear_tests'),
    # categories
    path('category/create/<int:testplan_id>/', views.CategoryCreate.as_view(), name='category_create'),
    path('category/update/<int:pk>/', views.CategoryUpdate.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category_delete'),
    path('category/<int:pk>/<int:tab_id>/', views.category_details, name='category_details'),
    path('category/up/<int:pk>/', views.category_up, name='category_up'),
    path('category/down/<int:pk>/', views.category_down, name='category_down'),
    # tests
    path('test/create/<int:category_id>/', views.TestCreate.as_view(), name='test_create'),
    path('test/update/<int:pk>/', views.TestUpdate.as_view(), name='test_update'),
    path('test/delete/<int:pk>/', views.TestDelete.as_view(), name='test_delete'),
    path('test/<int:pk>/<int:tab_id>/', views.test_details, name='test_details'),
    path('test/up/<int:pk>/', views.test_up, name='test_up'),
    path('test/down/<int:pk>/', views.test_down, name='test_down'),
    # test configs
    path('test/config/add/', views.test_config_add, name='test_config_add'),
    path('test/config/create/<int:test_id>/', views.TestConfigCreate.as_view(), name='test_config_create'),
    path('test/config/update/<int:pk>/', views.TestConfigUpdate.as_view(), name='test_config_update'),
    path('test/config/delete/<int:pk>/', views.TestConfigDelete.as_view(), name='test_config_delete'),
    # test images
    path('test/image/add/', views.test_image_add, name='test_image_add'),
    path('test/image/create/<int:test_id>/', views.TestImageCreate.as_view(), name='test_image_create'),
    path('test/image/update/<int:pk>/', views.TestImageUpdate.as_view(), name='test_image_update'),
    path('test/image/delete/<int:pk>/', views.TestImageDelete.as_view(), name='test_image_delete'),
    # test files
    path('test/file/add/', views.test_file_add, name='test_file_add'),
    path('test/file/create/<int:test_id>/', views.TestFileCreate.as_view(), name='test_file_create'),
    path('test/file/update/<int:pk>/', views.TestFileUpdate.as_view(), name='test_file_update'),
    path('test/file/delete/<int:pk>/', views.TestFileDelete.as_view(), name='test_file_delete'),
    # test links
    path('test/link/add/', views.test_link_add, name='test_link_add'),
    path('test/link/create/<int:test_id>/', views.TestLinkCreate.as_view(), name='test_link_create'),
    path('test/link/update/<int:pk>/', views.TestLinkUpdate.as_view(), name='test_link_update'),
    path('test/link/delete/<int:pk>/', views.TestLinkDelete.as_view(), name='test_link_delete'),
    # test comments
    path('test/comment/add/', views.test_comment_add, name='test_comment_add'),
    path('test/comment/create/<int:test_id>/', views.TestCommentCreate.as_view(), name='test_comment_create'),
    path('test/comment/update/<int:pk>/', views.TestCommentUpdate.as_view(), name='test_comment_update'),
    path('test/comment/delete/<int:pk>/', views.TestCommentDelete.as_view(), name='test_comment_delete'),
    # files
    path('file/create/<int:testplan_id>', views.TestplanFileCreate.as_view(), name='testplan_file_create'),
    path('file/update/<int:pk>/', views.TestplanFileUpdate.as_view(), name='testplan_file_update'),
    path('file/delete/<int:pk>/', views.TestplanFileDelete.as_view(), name='testplan_file_delete'),
]
