from django.shortcuts import render


def brute_force(request):
    return render(request, 'password_cracking/brute_force.html')


def dictionary(request):
    return render(request, 'password_cracking/dictionary.html')
