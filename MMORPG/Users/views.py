from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from .models import *
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CommentForm, CommentAddForm
from .filters import PostFilter
from django.contrib import messages
from django.http import HttpResponseRedirect


class SubscribeToCategory(LoginRequiredMixin, TemplateView):
    template_name = 'subscribe.html'
    model = UsersSubscribed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        UsersSubscribed.objects.create(user=self.request.user, category=Category.objects.get(pk=context['pk']))
        context['subscribed'] = Category.objects.get(pk=context['pk'])
        return context


class UnSubscribeToCategory(LoginRequiredMixin, TemplateView):
    template_name = 'unsubscribe.html'
    model = UsersSubscribed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_subscription = UsersSubscribed.objects.get(user=self.request.user, category=Category.objects.get(pk=context['pk']))
        delete_subscription.delete()
        context['unsubscribed'] = Category.objects.get(pk=context['pk'])
        return context


class PostsList(ListView):
     model = Post
     template_name = 'board.html'
     context_object_name = 'posts'
     queryset = Post.objects.order_by('-id')
     form_class = PostForm


     def get_context_data(self,**kwargs):
         context = super().get_context_data(**kwargs)
         context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
         return context


class DetailList(DetailView):
    model = Post
    template_name = 'detali.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(
            post=self.get_object())
        data['comments'] = comments
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(commentText=request.POST.get('commentText'),
        userEditor=self.request.user,
        post=self.get_object())
        new_comment.save()
        return render(request, 'detail.html', args=[self.id] )

class CommentView(DetailView):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comment'

    def reply(self,request, pk):
        reply_comment = Comment.objects.get(pk=pk)
        reply_id = request.POST.get('reply_id')
        reply_comment, created = Reply.objects.create(comment=reply_comment, id=reply_id)
        return redirect('comments', pk=reply_comment.pk)

    def reply_status(request,**kwargs):
        data = super().get_context_data(**kwargs)
        if 'status1' in request.POST:
         messages.success(request, 'Отклик принят')
        elif 'status2' in request.POST:
         messages.success(request, 'Отклик отклонён')
        return HttpResponseRedirect('comments.html', data)


class AddList(LoginRequiredMixin, CreateView):
    queryset = Post.objects.all()
    template_name = 'add.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.save()
        return render('board.html')




class EditList(LoginRequiredMixin, UpdateView):
    queryset = Post.objects.all()
    template_name = 'edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class PostDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)