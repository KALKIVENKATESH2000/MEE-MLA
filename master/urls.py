from django.urls import path
# from master import views 
 
# urlpatterns = [ 
#     path('reports/', views.report_list),
#     path('reports/<str:pk>/', views.report_detail),

#     # url(r'^api/tutorials$', views.tutorial_list),
#     # url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
#     # url(r'^api/tutorials/published$', views.tutorial_list_published)
# ]

from .views import *

urlpatterns = [
    path('reports/', ReportListCreateView.as_view(), name='reports-list-create'),
    path('reports/<int:pk>/', ReportRetrieveUpdateDeleteView.as_view(), name='report-retrieve-update-delete'),
    path('posts/', PostListCreateView.as_view(), name='posts-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-retrieve-update-delete'),
    path('schemas/', SchemaListCreateView.as_view(), name='schemas-list-create'),
    path('schemas/<int:pk>/', SchemaRetrieveUpdateDeleteView.as_view(), name='schema-retrieve-update-delete'),
    path('posts/<int:post_id>/like/', like_post, name='like-post'),
    path('posts/<int:post_id>/comments/', create_comment, name='create-comment'),
]