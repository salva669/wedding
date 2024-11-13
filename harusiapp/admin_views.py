from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required
def admin_home(request):
    # Check if the user is an Admin
    if request.user.user_type.name != 'Admin':
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    # Render the admin dashboard page
    return render(request, 'admin_template/home_content.html')
