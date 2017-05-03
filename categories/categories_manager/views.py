from categories.models import Categories, SubCategories
from django.shortcuts import render


def view_categories(request):
    categories = Categories.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})