from django.urls import path, include
from .views import MainPageView, ArticleDetailView, AllArticlesByUserView, NewArticleView, ArticleEditView, RegistrationView
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', MainPageView.as_view(), name='mainPage'),
    path('article/new', NewArticleView.as_view(), name='newArticle'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='articleDetail'),
    path('article/<int:pk>/edit/', ArticleEditView.as_view(), name='articleEdit'),
    path('user/<slug:slug>/articles', AllArticlesByUserView.as_view(), name='allArticles'),
    path('accounts/registration/', RegistrationView.as_view(), name='registration'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout')
]
