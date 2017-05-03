from django.shortcuts import render
from categories.models import SubCategories


def view_subcategories(request):
    subcategories = SubCategories.objects.all()
    return render(request, 'manage_subcategories.html', {'subcategories': subcategories})