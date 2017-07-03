# from django.shortcuts import render
from django.views.generic.base import TemplateView
from photos.models import PhotoUpload


# The user can only see the photos if he's logedin
from allauth.account.views import SignupView
from allauth.account.forms import LoginForm


class CustomSignupView(SignupView):
    # here we add some context to the already existing context
    def get_context_data(self, **kwargs):
        # we get context data from original view
        context = super(CustomSignupView,
                        self).get_context_data(**kwargs)
        # add form to context
        context['login_form'] = LoginForm()
        return context


# The user can only see the photos
# that are approved by the admin
class CarouselView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(CarouselView, self).get_context_data(**kwargs)
        context['photos'] = PhotoUpload.objects.order_by(
            'date_upload').filter(status='ap')[:8]
        return context
