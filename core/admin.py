from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Accounts

admin.site.register(Accounts)
