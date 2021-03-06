from django import forms
from django.forms import extras
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from mainapp.models import Report, ReportUpdate, ReportSubscriber
from django.utils.translation import ugettext_lazy
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import ugettext as _


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control required', 'placeholder': _('Name')}),
                           label="")
    email = forms.EmailField(widget=forms.TextInput(attrs=dict({'class': 'form-control required',
                                                                'placeholder': _('Email')},
                                                               maxlength=200)),
                             label="")
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-margin-fix required', 'rows': '5', 'cols': '20',
                                     'placeholder': _('Message')}),
        label="")

    def save(self, fail_silently=False):
        message = render_to_string("emails/contact/message.txt", self.cleaned_data)
        send_mail('FixMyStreet.ge User Message from %s' % self.cleaned_data['email'], message,
                  settings.EMAIL_FROM_USER, [settings.ADMIN_EMAIL], fail_silently=False)


class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = ReportUpdate
        fields = ('desc', 'author', 'email', 'phone', 'photo')


class ReportSubscriberForm(forms.ModelForm):
    class Meta:
        model = ReportSubscriber
        fields = ('email',)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title', 'street', 'photo')


class ReportStart(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': "Problem Title"
        }))

    street = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': "Street"
        }))

    desc = forms.CharField()

    author = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': _("Name/Last name")
        }))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': _("Email")
        }))

    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': _("Phone Number")
        }))
    step = forms.CharField(widget=forms.TextInput(attrs={'class': 'required form-control input-small'}))
    lon = forms.CharField(widget=forms.TextInput(attrs={'class': 'required', 'type': 'hidden'}))
    lat = forms.CharField(widget=forms.TextInput(attrs={'class': 'required', 'type': 'hidden'}))


class sortingForm(forms.Form):
    CHOICES = (('-created_at', _('Created descending'),), ('created_at', _('Created ascending',)))
    sorting = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': ''}), choices=CHOICES)
    created_after = forms.DateField(widget=AdminDateWidget(attrs={'class': 'datepicker form-control'}))
    created_before = forms.DateField(widget=AdminDateWidget(attrs={'class': 'datepicker form-control'}))
