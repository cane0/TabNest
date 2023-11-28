from django.contrib import admin
from .models import Session, UniqueAuth, Tab

admin.site.register(Session)
admin.site.register(UniqueAuth)
admin.site.register(Tab)