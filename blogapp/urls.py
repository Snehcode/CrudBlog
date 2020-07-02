from django.urls import path
from blogapp import views
from blogapp.views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView
from django.contrib.auth import views as auth_views



urlpatterns=[ 
    path('',views.index, name="home"),
    path('about/',views.about),
    path('contact/',views.contact),
    path('signup/',views.signup, name='signup'),
    path('login/',auth_views.LoginView.as_view(), {'template_name':'login.html'},name='login'),
    path('blogpage/',PostListView.as_view(), name='blogpage'),
    path('blogpage/post/<int:pk>/', PostDetailView.as_view(),name="post-detail"),
    path('blogpage/post/new/',PostCreateView.as_view(), name="post-create"),
    path('blogpage/post/<int:pk>/update', PostUpdateView.as_view(),name="post-update"),
    path('blogpage/post/<int:pk>/delete', PostDeleteView.as_view(),name="post-delete"),
]