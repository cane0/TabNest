from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account have been created. You can now login')
            
            # social_account = SocialAccount.objects.filter(user=user).first()
            # if social_account:
            #     # If the user registered with a social account, we log them in immediately
            #     auth_login(request, user)
            #     return redirect('profile')

            
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
        'title': 'User Register Page'
    }

    return render(request, 'users/register.html', context)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         # u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

#         # if u_form.is_valid() and p_form.is_valid():
#         if p_form.is_valid():    
#             # u_form.save()
#             p_form.save()
#             messages.success(request, f'Your image has been updated !')
#             return redirect('profile')
#     else:
#         # u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         # 'u_form': u_form,
#         'p_form': p_form,
#     }

#     return render(request, 'bookmarks/home.html', context)
