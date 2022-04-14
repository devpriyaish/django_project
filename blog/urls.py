from django.urls import path
from blog import views
from blog.views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('home/', views.home, name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('find_friends/', views.find_friends, name='find-friends'),
    path('list_friends/', views.list_friends, name='list-friends'),
    path('list_all_friends/', views.list_all_friends, name='list-all-friends'),
    path('remove_friends<int:remove_id>/', views.remove_friends, name='remove-friends'),
    #path('about/', views.about, name='blog-about'),
    path('about_friend/<int:friend_id>', views.about_friend, name='about-friend'),
    # path('post_via_json/', views.post_via_json, name='post-via-json'),
    # path('post_from_dummy_client/', views.post_from_dummy_client, name='post-from-dummy-client'),
]