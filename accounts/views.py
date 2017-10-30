from allauth.account.views import SignupView, LoginView, EmailVerificationSentView, ConfirmEmailView, \
    PasswordChangeView, PasswordSetView, PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView, EmailView
from django.contrib.auth.models import User
from django.views.generic import TemplateView, FormView

from accounts.forms.forms import editform


class editprofileView(FormView):
    template_name = 'profile_edit.html'
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
    template_name = 'signup.html'


class MyLoginView(LoginView):
    template_name = 'login.html'


class MyPasswordResetView(PasswordResetView):
    template_name = 'forgotpassword.html'


class MyEmailVerificationSentView(EmailVerificationSentView):
    template_name = 'Emailverficationsent.html'


class MyConfirmEmailView(ConfirmEmailView):
    template_name = 'ConfirmEmail.html'


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'passwordchange.html'
    success_url = '/account/sucess/'


class MyPasswordSetView(PasswordSetView):
    template_name = 'passwordset.html'
    success_url = '/account/sucess/'


class MySucessView(TemplateView):
    template_name = 'sucess.html'


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'resetmailsent.html'


class MyPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'passwordreset.html'
    success_url = '/account/sucess/'


class MyEmailView(EmailView):
    template_name = 'emailchange.html'
