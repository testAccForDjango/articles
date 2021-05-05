from django.urls import path
from .views import MainPageView, ArticleDetailView, AllArticlesByUserView, NewArticleView, EditArticleView, \
    UserRegistrationView, DeleteArticleView
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', MainPageView.as_view(), name='mainPage'),
    path('article/new', NewArticleView.as_view(), name='newArticle'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='articleDetail'),
    path('article/<int:pk>/edit/', EditArticleView.as_view(), name='articleEdit'),
    path('article/<int:pk>/delete/', DeleteArticleView.as_view(), name='articleDelete'),
    path('user/<slug:slug>/articles', AllArticlesByUserView.as_view(), name='allArticlesByUser'),
    path('accounts/registration/', UserRegistrationView.as_view(), name='registration'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout')
]
