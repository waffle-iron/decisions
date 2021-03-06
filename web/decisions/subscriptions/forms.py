from __future__ import unicode_literals

from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _, string_concat
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import (
    validate_password, password_validators_help_text_html
)
from django.contrib.auth.models import User

from decisions.subscriptions.models import Subscription


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label=_("Email address"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("user@example.com"),
                "autocomplete": "username",
            }
        ),
    )
    username = forms.CharField(
        label=_("Display name"),
        required=False,
        widget=forms.TextInput(attrs={
            "autocomplete": "nickname"
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password"
        }),
        label=_("Password")
    )
    password_again = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Password again"),
        help_text=string_concat(
            _("Your password must meet these requirements:"),
            password_validators_help_text_html())
    )

    def clean(self):
        if ("password" in self.cleaned_data
            and "password_again" in self.cleaned_data):
            if self.cleaned_data["password"] != self.cleaned_data["password_again"]:
                self.add_error("password",
                               forms.ValidationError(_("Passwords don't match")))
                self.add_error("password_again",
                               forms.ValidationError(_("Passwords don't match")))

        if "email" in self.cleaned_data:
            self.cleaned_data["username"] = self.get_username()

        if "username" in self.cleaned_data:
            username_exists = User.objects.filter(
                username=self.cleaned_data["username"]).count()
            if username_exists:
                self.add_error("username", forms.ValidationError(
                    _("Please choose another display name")))

        if "email" in self.cleaned_data:
            email_exists = User.objects.filter(
                email=self.cleaned_data["email"]).count()
            if email_exists:
                self.add_error("email", forms.ValidationError(
                    _("Please choose another email address")))

        if "password" in self.cleaned_data:
            validate_password(self.cleaned_data["password"])

        return self.cleaned_data

    def get_username(self):
        if self.cleaned_data.get("username"):
            return self.cleaned_data["username"]
        return self.cleaned_data["email"].split("@", 1)[0]

class LoginForm(forms.Form):
    user = None

    email = forms.EmailField(
        label=_("Email address"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("user@example.com"),
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password"
        }),
        label=_("Password")
    )
    next = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean(self):
        self.user = authenticate(**self.cleaned_data)
        if not self.user:
            raise forms.ValidationError(_("Email or password did not match. Please try again."))
        return self.cleaned_data

class BSRadioChoiceInput(widgets.RadioChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        from django.utils.html import format_html

        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        print self.attrs
        active = "active" if self.is_checked() else ""
        return format_html(
            '<label{} class="btn {}">{} {}</label>', label_for, active, self.tag(attrs), self.choice_label
        )

class BSRadioFieldRenderer(widgets.ChoiceFieldRenderer):
    choice_input_class = BSRadioChoiceInput
    outer_html = '<div{id_attr} class="btn-group" data-toggle="buttons">{content}</div>'
    inner_html = '{choice_value}{sub_widgets}'

class BSRadioSelect(forms.RadioSelect):
    renderer = BSRadioFieldRenderer

class SubscriptionForm(forms.Form):
    search_term = forms.CharField(
        label=_('Search term'),
        widget=forms.TextInput(
            attrs={
            })
    )
    send_mail = forms.BooleanField(
        label=_('Sends email'),
        help_text=_('If checked, notifications about new search results are also sent by email. Otherwise they will just show up in your feed.'),
        required=False,
        widget=BSRadioSelect(choices=[
            (True, _("Sends email")),
            (False, _("No"))
        ])
    )

class SubscriptionEditForm(SubscriptionForm):
    active = forms.BooleanField(
        label=_('Active'),
        help_text=_('If you do not wish to receive any more notifications from this subscriptions, you can disable it. Old notifications will not disappear from your feed.'),
        required=False,
        widget=BSRadioSelect(choices=[
            (True, _("Active")),
            (False, _("No"))
        ])
    )
