from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanPatternListView.as_view(), name='testplan_patterns'),
    path('create/', views.TestplanPatternCreate.as_view(), name='testplan_pattern_create'),
    path('update/<int:pk>/', views.TestplanPatternUpdate.as_view(), name='testplan_pattern_update'),
    path('delete/<int:pk>/', views.TestplanPatternDelete.as_view(), name='testplan_pattern_delete'),
    path('<int:pk>/<int:tab_id>/', views.testplan_pattern_details, name='testplan_pattern_details'),
    path('category/create/<int:testplan_pattern_id>/', views.CategoryPatternCreate.as_view(),
         name='category_pattern_create'),
    path('category/update/<int:pk>/', views.CategoryPatternUpdate.as_view(), name='category_pattern_update'),
    path('category/delete/<int:pk>/', views.CategoryPatternDelete.as_view(), name='category_pattern_delete'),
    path('category/<int:pk>/<int:tab_id>/', views.category_pattern_details, name='category_pattern_details'),
    path('category/up/<int:pk>/', views.category_pattern_up, name='category_pattern_up'),
    path('category/down/<int:pk>/', views.category_pattern_down, name='category_pattern_down'),
    path('test/create/<int:category_pattern_id>/', views.TestPatternCreate.as_view(), name='test_pattern_create'),
    path('test/update/<int:pk>/', views.TestPatternUpdate.as_view(), name='test_pattern_update'),
    path('test/delete/<int:pk>/', views.TestPatternDelete.as_view(), name='test_pattern_delete'),
    path('test/<int:pk>/<int:tab_id>/', views.test_pattern_details, name='test_pattern_details'),
    path('test/up/<int:pk>/', views.test_pattern_up, name='test_pattern_up'),
    path('test/down/<int:pk>/', views.test_pattern_down, name='test_pattern_down'),
    path('test/device_types_update/<int:pk>/', views.test_pattern_device_types_update,
         name='test_pattern_device_types_update'),
    path('test/names_update/', views.test_names_update, name='test_names_update'),
    path('test/purposes_update/', views.test_purposes_update, name='test_purposes_update'),
    path('test/procedures_update/', views.test_procedures_update, name='test_procedures_update'),
    path('test/expected_update/', views.test_expected_update, name='test_expected_update'),
    path('test/redmine_wiki_update/', views.test_redmine_wiki_update, name='test_redmine_wiki_update'),
    path('test/config/create/<int:test_pattern_id>/', views.TestPatternConfigCreate.as_view(),
         name='test_pattern_config_create'),
    path('test/config/update/<int:pk>/', views.TestPatternConfigUpdate.as_view(),
         name='test_pattern_config_update'),
    path('test/config/delete/<int:pk>/', views.TestPatternConfigDelete.as_view(),
         name='test_pattern_config_delete'),
    path('test/image/create/<int:test_pattern_id>/', views.TestPatternImageCreate.as_view(),
         name='test_pattern_image_create'),
    path('test/image/update/<int:pk>/', views.TestPatternImageUpdate.as_view(),
         name='test_pattern_image_update'),
    path('test/image/delete/<int:pk>/', views.TestPatternImageDelete.as_view(),
         name='test_pattern_image_delete'),
    path('test/file/create/<int:test_pattern_id>/', views.TestPatternFileCreate.as_view(),
         name='test_pattern_file_create'),
    path('test/file/update/<int:pk>/', views.TestPatternFileUpdate.as_view(),
         name='test_pattern_file_update'),
    path('test/file/delete/<int:pk>/', views.TestPatternFileDelete.as_view(),
         name='test_pattern_file_delete'),
    path('test/link/create/<int:test_pattern_id>/', views.TestPatternLinkCreate.as_view(),
         name='test_pattern_link_create'),
    path('test/link/update/<int:pk>/', views.TestPatternLinkUpdate.as_view(),
         name='test_pattern_link_update'),
    path('test/link/delete/<int:pk>/', views.TestPatternLinkDelete.as_view(),
         name='test_pattern_link_delete'),
    path('test/comment/create/<int:test_pattern_id>/', views.TestPatternCommentCreate.as_view(),
         name='test_pattern_comment_create'),
    path('test/comment/update/<int:pk>/', views.TestPatternCommentUpdate.as_view(),
         name='test_pattern_comment_update'),
    path('test/comment/delete/<int:pk>/', views.TestPatternCommentDelete.as_view(),
         name='test_pattern_comment_delete'),
]
