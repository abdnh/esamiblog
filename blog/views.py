from blog import context_processors
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect
from django.db.models import Q

from .models import Category, Post, User, Comment
from .forms import UserRegistrationForm, PreferencesForm


def index(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    return HttpResponseRedirect(reverse('user-detail', kwargs={'username': request.user.get_username()}))


class UserListView(ListView):
    model = User
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        if query:
            return self.model.objects.filter(
                Q(username__contains=query) |
                Q(bio__contains=query) |
                Q(first_name__contains=query) |
                Q(last_name__contains=query)
            )
        else:
            return self.model.objects.all()


class UserDetailView(DetailView):
    model = User

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(self.model, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(writer=self.get_object())
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'bio', 'profile_picture']

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return self.model.objects.filter(username=username).get()

    def test_func(self):
        return self.request.user == self.get_object()


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        if query:
            return self.model.objects.filter(Q(title__contains=query) | Q(content__contains=query))
        else:
            return self.model.objects.all()


def comment_children(comment, padding):
    tree = []
    for child in Comment.objects.filter(parent_comment=comment):
        tree += [(padding, child)] + comment_children(child, padding+50)
    return tree

def post_comment_tree(post, padding):
    tree = []
    for comment in Comment.objects.filter(post=post, parent_comment__isnull=True):
        tree += [(padding, comment)] + comment_children(comment, padding+50)
    return tree


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = post_comment_tree(self.get_object(), 10)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'categories']

    def form_valid(self, form):
        self.object = form.save()
        self.object.writer = self.request.user
        self.object.save()
        return FormMixin.form_valid(self, form)


def is_post_owner(self):
    return self.request.user == self.get_object().writer


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'categories']
    test_func = is_post_owner


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')
    test_func = is_post_owner


class CategoryListView(ListView):
    model = Category
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        if query:
            return self.model.objects.filter(name__contains=query)
        else:
            return self.model.objects.all()


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(categories__name=self.object.name)
        return context


def is_admin_test(self):
    return self.request.user.is_superuser


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']
    test_func = is_admin_test


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    test_func = is_admin_test


class SignUpView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CommentDetailView(DetailView):
    model = Comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = comment_children(self.get_object(), 10)
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.comment_parent_post = Post.objects.get(id=self.kwargs.get('pk'))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.writer = self.request.user
        self.object.post = self.comment_parent_post
        self.object.save()
        return FormMixin.form_valid(self, form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.comment_parent_post
        return context

    def get_success_url(self) -> str:
        return reverse('post-detail', kwargs={'pk': self.kwargs.get('pk')})


class CommentReplyView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/reply_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.parent_comment = Comment.objects.get(id=self.kwargs.get('pk'))
        self.comment_parent_post = self.parent_comment.post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.writer = self.request.user
        self.object.post = self.comment_parent_post
        self.object.parent_comment = self.parent_comment
        self.object.save()
        return FormMixin.form_valid(self, form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.parent_comment
        return context

    def get_success_url(self) -> str:
        if self.request.GET.get('next'):
            next = self.request.GET.get('next')
            return self.request.build_absolute_uri(next)
        if self.object.parent_comment:
            return reverse('comment-detail', kwargs={'pk': self.object.parent_comment.id})
        else:
            return reverse('post-detail', kwargs={'pk': self.comment_parent_post.id})


def preferences(request):
    if request.method == 'POST':
        form = PreferencesForm(data=request.POST)
        if form.is_valid():
            request.session['bgcolor'] = form.cleaned_data['bgcolor']
            return HttpResponseRedirect(reverse('preferences'))
    else:
        data = {
        }
        data['bgcolor'] = request.session.get('bgcolor', context_processors.context_vars['DEFAULT_BG_COLOR'])
        form = PreferencesForm(data=data)

    context = {
        'form': form
    }

    return render(request, 'blog/preferences_form.html', context)
