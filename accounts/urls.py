from allauth.account import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from accounts.views import MySignupView, MyLoginView, MyEmailVerificationSentView, MyConfirmEmailView, \
    MyPasswordChangeView, MyPasswordSetView, MySucessView, editprofileView, MyPasswordResetView, \
    MyPasswordResetDoneView, MyPasswordResetFromKeyView, MyEmailView

urlpatterns = [
    url(r"^signup/$", MySignupView.as_view(), name="account_signup"),
    url(r"^login/$", MyLoginView.as_view(), name="account_login"),
    url(r"^logout/$", views.logout, name="account_logout"),
    url(r"^profileedit/$", login_required(editprofileView.as_view()), name="account_edit"),

    url(r"^password/change/$", MyPasswordChangeView.as_view(),
        name="account_change_password"),
    url(r"^password/set/$", MyPasswordSetView.as_view(), name="account_set_password"),

    url(r"^inactive/$", views.account_inactive, name="account_inactive"),

    # E-mail
    url(r"^email/$", MyEmailView.as_view(), name="account_email"),
    url(r"^confirm-email/$", MyEmailVerificationSentView.as_view(),
        name="account_email_verification_sent"),
    url(r"^confirm-email/(?P<key>[-:\w]+)/$", MyConfirmEmailView.as_view(),
        name="account_confirm_email"),

    # password reset
    url(r"^password/reset/$", MyPasswordResetView.as_view(),
        name="account_reset_password"),
    url(r"^password/reset/done/$", MyPasswordResetDoneView.as_view(),
        name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        MyPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$", views.password_reset_from_key_done,
        name="account_reset_password_from_key_done"),
    url(r"^sucess/$", MySucessView.as_view()),
]
