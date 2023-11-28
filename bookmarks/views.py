import json
import secrets

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .models import Session, UniqueAuth, Tab
from .forms import TabSearchForm
from users.forms import ProfileUpdateForm, Profile


@login_required
def profile_page(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid():
            profile = Profile.objects.get(user=request.user)
            file = request.FILES.get('file')

            profile.image = file
            profile.save()
            messages.success(request, 'Your image has been updated!')
            return JsonResponse({'message': 'Image updated successfully'})
        else:
            return JsonResponse({'error': 'Form data is not valid'}, status=400)
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    query = request.GET.get('q', '')
    tabs = Tab.objects.filter(Q(title__icontains=query) | Q(url__icontains=query), session__unique_auth__user_id=request.user.id)
        
    search_form = TabSearchForm()
    
    context = {
        "p_form": p_form,
        'title': f'{request.user.username}\'s Profile Page',
        'tabs': tabs, 'query': query, 'search_form': search_form
    }

    return render(request, 'bookmarks/profile.html', context)

# def update_image(request):
#     if request.method == 'POST':


error = 'bookmarks/404.html'

@login_required
def session_detail(request, session_id):
    session = Session.objects.get(pk=session_id)

    query = request.GET.get('q', '')
    tabs = Tab.objects.filter(Q(title__icontains=query) | Q(url__icontains=query), session__unique_auth__user_id=request.user.id)
        
    search_form = TabSearchForm()

    if session.unique_auth.user == request.user:
        context = {
            'session': session,
            'title': f'{session.name} - {request.user.username}',
            'tabs': tabs, 'query': query, 'search_form': search_form
        }
        return render(request, 'bookmarks/session_detail.html', context)
    return render(request, error)

@login_required
def sessions(request, unique_auth_value):
    unique_auth = UniqueAuth.objects.get(value=unique_auth_value)
    sessions = Session.objects.filter(unique_auth=unique_auth).order_by('-created_at')

    if unique_auth.user == request.user:

        sessions_per_page = 5

        paginator = Paginator(sessions, sessions_per_page)
        page = request.GET.get('page')
        sessions = paginator.get_page(page)

        query = request.GET.get('q', '')
        tabs = Tab.objects.filter(Q(title__icontains=query) | Q(url__icontains=query), session__unique_auth__user_id=request.user.id)
            
        search_form = TabSearchForm()

        context = {
            'sessions': sessions,
            'title': f'{request.user.username}\'s Saved Sessions',
            'tabs': tabs, 'query': query, 'search_form': search_form
        }

        return render(request, 'bookmarks/sessions.html', context)
    return render(request, error)


@csrf_exempt
def save_session(request, unique_auth_value):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_name = data.get('session_name')
        unique_authentication = data.get('unique_auth')
        user_pin = data.get('user_pin')
        try:
            unique_auth = UniqueAuth.objects.get(value=unique_authentication)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'AUTH CODE ERROR: Wrong authentication code Your data was not saved online, please check and try again.'})
        
        if user_pin != unique_auth.user_pin:
            return JsonResponse({'error': 'PIN CODE ERROR: The PIN entered for this user is incorrect. Your data was not saved online, please check and try again.'})

        session_data = json.loads(data.get('session_data'))

        session = Session(name=session_name, unique_auth=unique_auth,)
        session.save()

        for tab_data in session_data:
            url = session_data[tab_data]['url']
            logo = session_data[tab_data]['logo']
            title = session_data[tab_data]['title'][:255]

            new_tab = Tab(session=session, url=url, logo=logo, title=title)
            new_tab.save()

        return JsonResponse({'message': 'Session added successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def delete_session(session_id):
    session = Session.objects.get(pk=session_id)
    session.delete()

    return JsonResponse({'message': 'Successful deletion'})


# @user_passes_test(lambda u: u == Session.objects.get(pk=session_id).unique_auth.user)
def rename_session(request, session_id, new_name):
    session = Session.objects.get(pk=session_id)
    
    query = request.GET.get('q', '')
    tabs = Tab.objects.filter(Q(title__icontains=query) | Q(url__icontains=query), session__unique_auth__user_id=request.user.id)
        
    search_form = TabSearchForm()

    if request.user == session.unique_auth.user:
        session.name = new_name
        session.save()
        return JsonResponse({'message': 'Successful deletion'})

    return render(request, error, {'tabs': tabs, 'query': query, 'search_form': search_form})

def generate_new_unique_auth(request):
    while True:
        value = secrets.token_hex(3)[:6]

        if not UniqueAuth.objects.filter(value=value).exists():
            break
    u = request.user
    u.unique_auth.value = value
    u.unique_auth.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def tab_search(request):
    query = request.GET.get('q', '')
    tabs = Tab.objects.filter(Q(title__icontains=query) | Q(url__icontains=query), session__unique_auth__user_id=request.user.id)

    search_form = TabSearchForm()

    return render(request, 'bookmarks/search_results.html', {'tabs': tabs, 'query': query, 'search_form': search_form})
