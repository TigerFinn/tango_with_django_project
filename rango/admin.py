from django.contrib import admin
from rango.models import Category, Page

class PageOnCategory(admin.TabularInline):
    model = Page



class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category Name', {'fields':['name']}),
        ('Interaction Information', {'fields':['likes','views']})
    ]
    inlines = [PageOnCategory]


class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category','url')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)