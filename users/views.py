from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile, FriendRequest
from django.contrib.auth import login


def register(request):
    """ This view register the users"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form_var = form.save()
            messages.success(request, f'Your account has been created! You can now able to login')
            profile = Profile.objects.create(user=form_var)
            # saves relation between user & profile
            profile.save()
            login(request, form_var)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """This view creates the profile of the registered user"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def send_friend_request(request, user_id):
    """This view send requests to the other user"""
    from_user1 = request.user
    from_user = Profile.objects.get(user_id=from_user1)
    to_user = Profile.objects.get(user_id=user_id)
    check_exist = FriendRequest.objects.filter(from_user=to_user, to_user=from_user, status='accepted')
    if check_exist:
        messages.info(request, f'You are already friends!')
        return redirect(request.META['HTTP_REFERER'])

    else:
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            friend_request.status = 'sent'
            friend_request.save()
            messages.success(request, f'Friend request sent. Update your profile so that your friends know you better!')
            return redirect(request.META['HTTP_REFERER'])
        else:
            if friend_request.status == 'sent':
                messages.warning(request, f'Friend request already sent. '
                                          f'Update your profile so that your friends know you better!')
                return redirect(request.META['HTTP_REFERER'])
            elif friend_request.status == 'accepted':
                messages.info(request, f'You are already friends!')
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])


@login_required
def accept_friend_request(request, request_id):
    """This view accepts the request sent from other user"""
    my_profile_id = Profile.objects.get(user_id=request.user)
    friend_request = FriendRequest.objects.get(to_user_id=my_profile_id.id, from_user_id=request_id)

    if friend_request.to_user_id == my_profile_id.id:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.status = 'accepted'
        friend_request.save()
        messages.success(request, f'Friend request accepted!')  # f-string evaluates at runtime of the program,
        # no use of string.format
        return redirect('profile')
    else:
        messages.warning(request, f'Friend request not accepted!')
        return redirect('profile')


def all_friend_request(request):
    my_profile_id = Profile.objects.get(user_id=request.user)
    all_friend_requests = FriendRequest.objects.filter(to_user_id=my_profile_id.id, status='sent')
    return render(request, 'blog/base.html', {'all_friend_requests': all_friend_requests})
