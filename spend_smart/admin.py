from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserPreferences)
admin.site.register(Source)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Category)
