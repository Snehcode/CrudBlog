from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import UserInfo





# Create your views here.
def index(request):
    return render (request,"index.html")


def about(request):
    return render(request,"about.html")


def contact(request):
    return render(request,"contact.html")


def signup(request):
    # registered=False
    if request.method=="POST":
        form=UserInfo(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('login')
    else:
        form=UserInfo()

    return render(request,"signup.html",{"form":form})


@login_required
def blogpage(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,"blogpage.html", context)

class PostListView(ListView):
    model= Post
    template_name='blogpage.html'
    context_object_name='posts'
    ordering=['-date_posted']


class PostDetailView(DetailView):
    model=Post
    template_name='post_detail.html'


class PostCreateView(CreateView):
    model=Post
    fields=['title','content']
    template_name='post_form.html'

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']
    template_name='post_form.html'

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            raise PermissionDenied

class PostDeleteView(UserPassesTestMixin,DeleteView):
    model=Post
    template_name='post_confirm_delete.html'

    success_url='/blogpage'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            raise PermissionDenied
    




       