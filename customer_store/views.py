from django.shortcuts import render


def user_location(request):
    return render(request,'user_location.html')