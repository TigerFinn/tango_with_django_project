from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     name = cleaned_data.get('name')
    #     if not name:
    #         name = "No_Name_Given"
    #     name = self.amend_name_for_duplicates(name)
    #     print(name)
    #     cleaned_data['name'] = name
    #     return cleaned_data

    def amend_name_for_duplicates(self, new_name):
        if Category.objects.filter(name=new_name).exists():
            print("I exist")
            return self.amend_name_for_duplicates(new_name + "*")
        else:
            return new_name

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.NAME_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # if url and not url.startswith('http//'):
        #     url = f'http://{url}'
        #     cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)

