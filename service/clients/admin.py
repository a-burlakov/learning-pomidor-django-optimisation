from django.contrib import admin

from clients.models import Client
from services.models import Service, Plan, Subscription

admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Plan)
admin.site.register(Subscription)
