from django.shortcuts import render

# Create your views here.


def profile(request):
    '''
    View to render user's profile page with all their info
    and order history
    '''
    return render(request, 'profiles/profile.html')
