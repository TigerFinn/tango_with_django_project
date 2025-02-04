from django.contrib import admin
from rango.models import Category, Page


#A class that allows pages to be displayed whilst editing a category
class PageOnCategory(admin.TabularInline):
    model = Page



#Customisation of split (sections), prepopulation and the displaying of pages#
# of the category admin page
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category Name', {'fields':['name']}),
        ('Interaction Information', {'fields':['likes','views']}),
        ('URL Slug', {'fields':['slug']})
    ]
    prepopulated_fields = {'slug':('name',)}
    
    inlines = [PageOnCategory]


#Customisation of the order of the page admin
class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category','url')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)