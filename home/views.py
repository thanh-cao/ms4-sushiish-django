from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from home.models import ContactForm
from profiles.models import UserProfile

# Create your views here.


def index(request):
    '''
    Render landing page.
    If user is logged in, get user's information to
    prefill the contact form
    '''
    if request.user.is_authenticated:
        current_user = request.user
        all_addressess = UserProfile.objects.get(
            user=current_user).address_set.all()
        if all_addressess.count() > 0:
            default_address = all_addressess.filter(isDefault=True).first()
            if default_address is None:
                default_address = all_addressess.first()
            current_user.phone_number = default_address.phone_number

        context = {
            'current_user': current_user,
        }
        return render(request, 'home/index.html', context)
    else:
        return render(request, 'home/index.html')


@require_POST
def contact_us(request):
    '''
    Handle contact us form on landing page and send confirmation email
    to site owner and user
    '''
    try:
        contact_form = {'name': request.POST['full_name'],
                        'email': request.POST['email'],
                        'phone': request.POST['phone'],
                        'message': request.POST['message']}
        ContactForm.objects.create(**contact_form)

        # send contact form email to site owner and sender
        reply_to = contact_form['email']
        subject = f'Sushiish Contact Form: {contact_form["name"]}'
        body = render_to_string(
            'home/contact_us_email/contact_us_email.txt',
            {'contact': contact_form}
        )

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [reply_to, settings.EMAIL_HOST_USER],
        )
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(e, status=400)


def error_404(request, exception):
    '''Render 404 page'''
    return render(request, '404.html')


def error_500(request):
    '''Render 500 page'''
    return render(request, '500.html')
