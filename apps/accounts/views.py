from allauth.account.views import SignupView, LoginView, EmailVerificationSentView, ConfirmEmailView, \
    PasswordChangeView, PasswordSetView, PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView, EmailView
from django.contrib.auth.models import User
from django.views.generic import TemplateView, FormView

from apps.accounts.forms.forms import editform


class editprofileView(FormView):
    template_name = 'accounts/profile_edit.html'
    form_class = editform
    success_url = '/account/sucess/'

    def form_valid(self, form):
        user = User.objects.get_by_natural_key(username=form.cleaned_data['username'])
        user.first_name = form.cleaned_data['firstname']
        user.last_name = form.cleaned_data['lastname']
        user.email = form.cleaned_data['email']
        user.save()
        return super(editprofileView, self).form_valid(form)


class MySignupView(SignupView):
    template_name = 'accounts/signup.html'


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'


class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/forgotpassword.html'


class MyEmailVerificationSentView(EmailVerificationSentView):
    template_name = 'accounts/Emailverficationsent.html'


class MyConfirmEmailView(ConfirmEmailView):
    template_name = 'accounts/ConfirmEmail.html'


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/passwordchange.html'
    success_url = '/account/sucess/'


class MyPasswordSetView(PasswordSetView):
    template_name = 'accounts/passwordset.html'
    success_url = '/account/sucess/'


class MySucessView(TemplateView):
    template_name = 'accounts/sucess.html'


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/resetmailsent.html'


class MyPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'accounts/passwordreset.html'
    success_url = '/account/sucess/'


class MyEmailView(EmailView):
    template_name = 'accounts/emailchange.html'
