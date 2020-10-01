from django.contrib import admin
from .models import Treasure


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ('name',)
    search_fields = ('name',)


# Register your models here.
admin.site.register(Treasure, PageAdmin)
