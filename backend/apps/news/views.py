# from django.shortcuts import render

# Temporary import
from django.http import HttpResponse


# Temporary view to display welcome page.
def welcome(request):
    return HttpResponse("<h3>Welcome to news cms</h3>")
