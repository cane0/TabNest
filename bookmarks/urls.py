from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_page, name='profile'),
    path('add_session/<unique_auth_value>', save_session, name="add-session"),
    path('session_detail/<session_id>', session_detail, name="session-detail"),
    path('sessions/<unique_auth_value>', sessions, name="sessions"),
    path('update/', generate_new_unique_auth, name="update"),
    path('delete_session/<session_id>', delete_session, name='delete-session'),
    path('rename_session/<session_id>/<new_name>', rename_session, name="rename-session"),
    path('search/', tab_search, name='tab-search'),
]