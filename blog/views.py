import io
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


from blog.models import Post
from blog.serializers import PostSerializer
from users.models import Profile, FriendRequest

"""
Generic views used are:
 ListView: contain the list of objects
 DetailView: self.object will contain the object that the view is operating upon
 CreateView: displays a form for creating an object
 UpdateView: displays a form for editing an existing object
 DeleteView: displays a confirmation page for deletion of existing object
Mixin: a mixin is a class which contains a combination of methods from other classes
"""


@login_required()
def home(request):
    profile_id = Profile.objects.get(user_id=request.user.id)
    friend_lists = FriendRequest.objects.filter(Q(from_user_id=profile_id.id) | Q(to_user_id=profile_id.id),
                                                status='accepted'
                                                ).select_related(
        'to_user', 'from_user'
    ).values('from_user_id', 'to_user_id')

    frien_id = [friend_list["to_user_id"]
                if friend_list["from_user_id"] == profile_id.id
                else friend_list['from_user_id']
                for friend_list in friend_lists]

    # getting user id for the related profile id's
    all_user_id = [request.user.id, ]
    friend_user_id = Profile.objects.filter(id__in=frien_id).select_related('author').values_list('user_id', flat=True)
    all_user_id += friend_user_id

    context = {
        'posts': Post.objects.filter(author_id__in=all_user_id).order_by('-date_posted')
    }
    return render(request, 'blog/home.html', context)


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,
                     CreateView):  # CreateView >> BaseCreateView in edit.py>> ProcessFormView in edit.py >> View in base.py
    model = Post
    fields = ['content']

    # the following method checks if the form contains a valid entry
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     UpdateView):  # LoginRequiredMixin in mixin.py >> AccessMixin in mixin.py
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # tests if the author is updating its own post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about_friend(request, friend_id):
    friend_info = Profile.objects.get(id=friend_id)
    user_id = friend_info.user_id
    user_info = User.objects.get(id=user_id)
    return render(request, 'blog/about_friend.html',
                  {'title': 'About', 'friend_info': friend_info, 'user_info': user_info})


def find_friends(request):
    from_user = Profile.objects.get(user_id=request.user)
    friend_lists = FriendRequest.objects.filter(Q(from_user_id=from_user) | Q(to_user_id=from_user),
                                                status='accepted').select_related(
        'to_user', 'from_user'
    ).values('from_user_id', 'to_user_id')

    frien_id = [friend_list["to_user_id"]
                if friend_list["from_user_id"] == from_user.id
                else friend_list['from_user_id']
                for friend_list in friend_lists]

    friends = Profile.objects.filter(id__in=frien_id)
    friends = set(friends)

    if request.method == 'POST':
        query = request.POST['search-friends']
        try:
            profiles = Profile.objects.filter(Q(user_id__email__icontains=query) | Q(mobile_number__icontains=query) |
                                              Q(user_id__username__icontains=query)).exclude(user_id=from_user.user_id)
        except Exception as err:
            print(err)
            profile = None
        return render(request, 'blog/list_friends.html', {'query': query, 'profiles': profiles, 'friends': friends})
    return render(request, 'blog/find_friends.html')


def list_friends(request):
    return render(request, 'blog/list_friends.html')


def remove_friends(request, remove_id):
    profile_id = Profile.objects.get(user_id=request.user.id)
    remove_friend = FriendRequest.objects.get(Q(from_user_id=remove_id, to_user_id=profile_id.id) |
                                              Q(to_user_id=remove_id, from_user_id=profile_id.id),
                                              status='accepted')
    remove_friend.delete()
    messages.success(request, f'You are no more friends!')
    return redirect(request.META['HTTP_REFERER'])


def list_all_friends(request):
    from_user = Profile.objects.get(user_id=request.user)
    friend_lists = FriendRequest.objects.filter(Q(from_user_id=from_user) | Q(to_user_id=from_user),
                                                status='accepted').select_related(
        'to_user', 'from_user'
    ).values('from_user_id', 'to_user_id')

    frien_id = [friend_list["to_user_id"]
                if friend_list["from_user_id"] == from_user.id
                else friend_list['from_user_id']
                for friend_list in friend_lists]

    friends = Profile.objects.filter(id__in=frien_id)
    print(friends)
    friends = set(friends)

    return render(request, 'blog/list_all_friends.html', {'friends': friends})


# def post_via_json(request):
#     post = Post.objects.get(id=42)
#     # post = Post.objects.all()
#     serializer = PostSerializer(post)
#     # serializer = PostSerializer(post, many=True)
#     json_data = JSONRenderer().render(serializer.data)
#     template_context = {
#         'my_json': json.loads(json_data)
#     }
#     print("---------------------------------------",template_context)
#     return render(request, 'blog/about.html', template_context)
#     #return HttpResponse(json_data, content_type='application/json')
#     #return JsonResponse(serializer.data)
#     #return JsonResponse(serializer.data, safe=False)


# def post_from_dummy_client(request):
#     if request.method == 'POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         python_data = JSONParser().parse(stream)
#         serializer = PostSerializer(data=python_data)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Data Created'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         json_data = JSONRenderer().render(serializer.errors)
#         return HttpResponse(json_data, content_type='application/json')
