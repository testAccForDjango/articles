import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ArticleForm, RegistrationForm
from django.shortcuts import redirect


class MainPageView(TemplateView):
    """Main page. All articles on the site"""
    template_name = 'blog/main_page.html'

    def get(self, request):
        context = {'articles': get_articles()}
        return render(request, self.template_name, context)


class ArticleDetailView(TemplateView):
    """Full text of the article"""
    template_name = 'blog/article_detail.html'

    def get(self, request, pk):
        article = get_articles(pk=pk)
        if not article:
            context = {'message': 'Article does not exists'}
            return render(request, self.template_name, context)
        context = {'article': article}
        return render(request, self.template_name, context)


class AllArticlesByUserView(TemplateView):
    """All articles by user"""
    template_name = 'blog/all_articles_by_user.html'

    def get(self, request, slug):
        context = {
            'articles': get_articles(author__username=slug),
            'article_owner': slug
        }
        return render(request, self.template_name, context)


class NewArticleView(LoginRequiredMixin, TemplateView):
    """Create a new article"""
    template_name = 'blog/new_article.html'

    def get(self, request):
        form = ArticleForm
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.date = datetime.datetime.now()
            article.save()
            form.save_m2m()
            return redirect(article.get_absolute_url())
        return redirect('allArticles')


class ArticleEditView(LoginRequiredMixin, TemplateView):
    """Edit article"""
    template_name = 'blog/article_edit.html'

    def get(self, request, pk):
        article = get_articles(pk=pk)
        if not article:
            context = {'message': 'Article does not exists'}
            return render(request, self.template_name, context)

        if request.user != article.author:
            context = {'message': 'You don\'t have permission for that'}
            return render(request, self.template_name, context)

        form = ArticleForm(instance=article)
        context = {
            'form': form,
            'message': 'Edit you article'
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        article = get_articles(pk=pk)
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.date = datetime.datetime.now()
            article.save()
            form.save_m2m()
            return redirect(article.get_absolute_url())
        return redirect('allArticles')


class RegistrationView(TemplateView):
    """New user registration"""
    template_name = 'registration/registration.html'

    def get(self, request):
        form = RegistrationForm
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mainPage')
        context = {'form': form}
        return render(request, self.template_name, context)


def get_articles(**kwargs):
    article = Article.objects.filter(**kwargs)
    if len(article) == 1:
        return article[0]
    return article
