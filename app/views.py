from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)

from app.models import Class_in, Contact, Post, Subject
from .models import Comment
from .forms import ContactForm, PostForm


def search(request):

    query = request.POST.get('search', '')

    if query:

        queryset = (Q(title__icontains=query)) | (Q(details__icontains=query)) | (Q(medium__icontains=query)) | (
            Q(category__icontains=query)) | (Q(subject__name__icontains=query)) | (Q(class_in__name__icontains=query))
        results = Post.objects.filter(queryset).distinct()
    else:

        results = []
    context = {
        'results': results
    }
    return render(request, 'tuition/search.html', context)


def filter(request):
    if request.method == 'POST':
        # Use request.POST.get instead of request.post
        subject = request.POST.get('subject', '')
        class_in = request.POST.get('class_in', '')
        salary_from = request.POST.get('salary_from', '')
        salary_to = request.POST.get('salary_to', '')
        available = request.POST.get('available')

        if subject or class_in:

            queryset = (Q(subject__name__icontains=subject)) & (
                Q(class_in__name__icontains=class_in))
            results = Post.objects.filter(queryset).distinct()
            if available:
                results = results.filter(available=True)
            if salary_from:
                results = results.filter(salary__gte=salary_from)

            if salary_to:
                results = results.filter(salary__lte=salary_to)

        else:
            results = []
        context = {
            'results': results
        }
        return render(request, 'tuition/search.html', context)


def home(request):

    return render(request, 'home.html')


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contact.html'
    # success_url = '/'

    def form_valid(self, form):
        form.save()
        # messages.error , messages.debug, messages.warning, message.info  can be used
        messages.success(self.request, 'Form successfully submitted')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('app:home')


# class ContactView(View):
#     form_class = ContactForm
#     template_name = 'contact.html'

#     def get(self,request, *args, **kwargs):

#         form = self.form_class()
#         return render(request, self.template_name, {'form':form})

#     def post(self,request, *args, **kwargs):
#         if request.method == 'POST':
#             form = self.form_class(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse("Success")
#         return render(request, self.template_name, {'form':form})


def contact(request):
    initials = {
        'username': 'my name',
        'email': 'abc@gmail.com',
        'phone': '+8801',
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, initial=initials)
        username = form.cleaned_data['username']
        email = form.changed_data['email']
        phone = form.cleaned_data['phone']
        content = form.cleaned_data['content']
        obj = Contact(username=username, email=email,
                      phone=phone, content=content)
        obj.save()
        print('sucess')
    else:
        form = ContactForm(initial=initials)

    return render(request, 'contact.html', {'form': form})


class PostListView(ListView):
    # model = Post

    queryset = Post.objects.all()
    template_name = "tuition/postlist.html"
    # context_object_name = 'post'
    # if send message with post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['post'] = context.get('object_list')
        context["subjects"] = Subject.objects.all()
        context["classes"] = Class_in.objects.all()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'tuition/postdetail.html'

    # def get_context_data(self, *args, **kwargs):
    #     self.object.views.add(self.request.user)
    #     liked = False
    #     if self.object.likes.filter(id = self.request.user.id ).exists():
    #         liked = True
    #     context = super().get_context_data(*args, **kwargs)
    #    # post = context.get('object')
    #     # comments = Comment.objects.filter(post=post.id,parent=None)
    #     # replies = Comment.objects.filter(post=post.id).exclude(parent=None)
    #     context["post"] = context.get('object')
    #     context['mgs'] = "Details of Post"
    #     context['liked'] = liked
    #     # context['comments'] = comments
    #     # context['replies '] = replies 
    #     print(liked)
    #     return context
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        post = context.get('object')

        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            # If authenticated, proceed with accessing user's ID and other information
            self.object.views.add(self.request.user)
            liked = self.object.likes.filter(id=self.request.user.id).exists()
        else:
            # If not authenticated, set liked to False
            liked = False

        # Continue with the rest of your context data
        comments = Comment.objects.filter(post=post.id, parent=None)
        replies = Comment.objects.filter(post=post.id).exclude(parent=None)
        
        context["post"] = post
        context['mgs'] = "Details of Post"
        context['liked'] = liked
        context['comments'] = comments
        context['replies '] = replies 

        return context



class PostEditUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "tuition/postcreate.html"

    def get_success_url(self):
        id = self.object.id
        return reverse_lazy('app:postdetail', kwargs={'pk': id})


class PostDeleteView(DeleteView):
    model = Post
    template_name = "tuition/delete.html"

    def get_success_url(self):
        return reverse_lazy('app:postlist')


def postview(request):

    post = Post.objects.all()

    return render(request, 'tuition/postview.html', {'post': post})


def subjectview(request):
    sub = Subject.objects.get(name='Biology')
    
    post = sub.subject_set.all()
    return render(request, 'tuition/subjectview.html', {'sub': sub, 'post': post})



# def subjectview(request):
#     selected_subjects = request.GET.getlist('subjects')  # Get list of selected subject names from query parameters
#     print("Selected Subjects:", selected_subjects)  # Debugging: Print selected subjects
#     subjects = Subject.objects.filter(name__in=selected_subjects)  # Filter subjects based on selected names
#     print("Filtered Subjects:", subjects)  # Debugging: Print filtered subjects
#     posts = Post.objects.filter(subject__name__in=selected_subjects)  # Filter posts based on selected subjects
#     print("Filtered Posts:", posts)  # Debugging: Print filtered posts
#     return render(request, 'tuition/subjectview.html', {'subjects': subjects, 'posts': posts})

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "tuition/postcreate.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('app:sub')

# def postcreate(request):
#     if request.method == "POST":
#         form = PostForm(request.POST,request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             sub = form.cleaned_data['subject']
#             for i in sub:
#                 obj.subject.add(i)
#                 obj.save()

#             class_in = form.cleaned_data['class_in']

#             for i in class_in:
#                 obj.class_in.add(i)
#                 obj.save()
#             return  HttpResponse("success")

#     else:
#         form = PostForm()

#     return render(request, 'tuition/postcreate.html', {'form':form})

from django.http import HttpResponseRedirect


def likepost(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def addcomment(request):
    if request.method  == "POST":
        comment = request.POST['comment']
        postid = request.POST['postid']
        parentid = request.POST['parentid']
        post = Post.objects.get(id=postid)
    
    if parentid:
        parent = Comment.objects.get(id=parentid)
        newcom = Comment(text=comment,user = request.user, post=post,parent=parent)
        newcom.save()
    else :
          newcom = Comment(text=comment,user = request.user, post=post)
          newcom.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

