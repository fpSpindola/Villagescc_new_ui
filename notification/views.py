from django.shortcuts import render


def notification_soon(request):
    return render(request, 'in_construction.html')