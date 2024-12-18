from django.contrib import admin
from .models import *
# Register your models here.
class ShowAdmin(admin.ModelAdmin):
    filter_horizontal = ('Show_Classification',) 

admin.site.register(User)
admin.site.register(Show,)
admin.site.register(Classification)
admin.site.register(Settings)
