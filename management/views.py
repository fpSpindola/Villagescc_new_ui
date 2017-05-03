from django.shortcuts import render


def management_urls(request):
    return render(request, 'management_urls.html')
