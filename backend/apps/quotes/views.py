# Temporary import HttpResponse
from django.http import HttpResponse


# Temporary view to display welcome page.
def quote_cms(request):
    return HttpResponse("<h3>Welcome to quotes cms</h3>")
