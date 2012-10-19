from django import forms

from django.contrib.auth.forms import SetPasswordForm
from satchmo_store.contact.models import Contact
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext

class SetPasswordOnceInputForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password = forms.CharField(label=_("Password"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordOnceInputForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password'])
        if commit:
            self.user.save()
        return self.user
class ContactEmailPasswordForm(SetPasswordOnceInputForm):
    error_messages = dict(SetPasswordOnceInputForm.error_messages, **{
        'email_incorrect': _("Your email was entered incorrectly because someone has used it. "
                                "Please enter it again."),
    })
    
    email = forms.EmailField (label=_("Email"),
                                   widget=None)

    def clean_email(self):
        """
        Validates that the old_password field is correct.
        """
        email = self.cleaned_data.get("email")
        contacts_with_email = Contact.objects.filter(email=email)
        users_with_email = User.objects.filter(email=email)
        if users_with_email.count():
            if self._contact.user.email != email:
                raise forms.ValidationError(
                    self.error_messages['email_incorrect'])
        if contacts_with_email.count():
            if self._contact.email != email:
                raise forms.ValidationError(
                    self.error_messages['email_incorrect'])
        return email

    def __init__(self, contact, *args, **kwargs):
        self.error_messages.update({'invalid_login':_('Some strange error occurs, please try again')})
        self._contact = contact
        super(ContactEmailPasswordForm, self).__init__(contact, *args, **kwargs)    

    def save(self, commit=True):
        self._contact.user.set_password(self.cleaned_data['password'])
        self._contact.email = self.cleaned_data['email']
        if commit:
            self._contact.save()
            self._contact.user.save()
        return self._contact