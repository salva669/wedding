from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)

            # Check user type and redirect accordingly
            if user.user_type.name == 'Admin':
                return redirect('home_content')  # Use URL pattern name here
            else:
                # Redirect other user types or provide a message
                messages.error(request, 'Access restricted for this user type.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect back to login page on failure
    else:
        return render(request, 'home_content.html')  # Display login form if method is GET


def IndexPageView(request):
    return render(request, 'index.html')

def LoginPageView(request):
    return render(request, 'ingia.html')
