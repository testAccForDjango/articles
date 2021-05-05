from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ArticleForm, RegistrationForm

from .services import get_articles, get_context_from_articles, create_or_update_article, delete_article


class MainPageView(TemplateView):
    """Main page. All articles on the site"""
    template_name = 'blog/main_page.html'

    def get(self, request):
        articles = get_articles()
        return render(request, self.template_name, get_context_from_articles(articles))


class ArticleDetailView(TemplateView):
    """Full text of the article"""
    template_name = 'blog/article_detail.html'

    def get(self, request, pk):
        article = get_articles(pk=pk)
        return render(request, self.template_name, get_context_from_articles(article))


class AllArticlesByUserView(TemplateView):
    """All articles by user"""
    template_name = 'blog/all_articles_by_user.html'

    def get(self, request, slug):
        articles = get_articles(author__username=slug)
        context = get_context_from_articles(articles)
        context.update({'articles_owner': slug})
        return render(request, self.template_name, context)


class NewArticleView(LoginRequiredMixin, TemplateView):
    """Create a new article"""
    template_name = 'blog/new_article.html'

    def get(self, request):
        form = ArticleForm
        context = {
            'form': form,
            'message': 'Create a new article'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            create_or_update_article(form=form, request=request)
        return redirect('allArticlesByUser', slug=request.user)


class EditArticleView(LoginRequiredMixin, TemplateView):
    """Edit article"""
    template_name = 'blog/article_edit.html'

    def get(self, request, pk):
        article = get_articles(pk=pk)[0]
        if article:
            if request.user != article.author and not request.user.is_staff:
                context = {'message': 'You don\'t have permission for that'}
                return render(request, self.template_name, context)
            form = ArticleForm(instance=article)
            context = {
                'form': form,
                'message': 'Edit you article'
            }
        else:
            context = get_context_from_articles(article)
        return render(request, self.template_name, context)

    def post(self, request, pk):
        article = get_articles(pk=pk)[0]
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            create_or_update_article(form=form, request=request)
        return redirect(article.get_absolute_url())


class DeleteArticleView(LoginRequiredMixin, TemplateView):
    """Delete article"""
    template_name = 'blog/article_delete.html'

    def get(self, request, pk):
        article = get_articles(pk=pk)[0]
        if article:
            if request.user != article.author and not request.user.is_staff:
                context = {
                    'success': False,
                    'message': 'You don\'t have permission for that'
                }
                return render(request, self.template_name, context)
            context = {
                'success': True,
                'message': f'Are you sure you want to delete {article.title}'
            }
        else:
            context = get_context_from_articles(article)
        return render(request, self.template_name, context)

    def post(self, request, pk):
        article = get_articles(pk=pk)[0]
        delete_article(article)
        return redirect('allArticlesByUser', slug=article.author)


class UserRegistrationView(TemplateView):
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
