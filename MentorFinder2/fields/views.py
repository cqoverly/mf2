from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Field, FieldCategory


class FieldList(ListView):
    model = Field
    template_name = 'field_list.html'
    context_object_name = "fields"

class FieldDetail(DetailView):
    model = Field
    template_name = 'field_detail.html'



def field_search(request, category):
    return render(request, 'field_search.html')


class CategoryList(ListView):
    model = FieldCategory
    template_name = 'field_categories.html'
    context_object_name = "categories"

