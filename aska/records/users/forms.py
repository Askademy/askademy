import calendar
from typing import Any
from django import forms
from django.db import models
from django.utils import timezone
from django.conf import settings

from .models import CustomUser, PasswordResetRequest
from .choices import SEND_CODE_TO


class UpdateUserForm(forms.ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        # If there is data in the request, exclude fields not in the request
        if data:
            available_fields = set(data.keys())
            fields_to_exclude = set(self.fields.keys()) - available_fields

            for field_name in fields_to_exclude:
                del self.fields[field_name]

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "nickname",
            "email",
            "birthdate",
            "gender",
            "bio",
            "profile_picture",
            # "cover_picture",
            "subjects",
            "level",
        ]
        widgets = {
            "subjects": forms.CheckboxSelectMultiple,
            "level": forms.RadioSelect,
        }


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="New password",
        min_length=5,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="New password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        model = CustomUser
        fields = [
            "phone_number",
            "first_name",
            "middle_name",
            "last_name",
            "birthdate",
            "gender",
            "password1",
            "password2",
        ]
        labels = {
            "birthdate": "Date of birth",
        }
        widgets = {
            "birthdate": forms.DateInput(
                format=("%Y-%m-%d"), attrs={"placeholder": "YYYY-MM-DD"}
            ),
            "gender": forms.Select(attrs={"class": "form-control"}),
        }

    def validate_age(self, birthdate):
        today = timezone.now()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )
        if age < 8 or age > 60:
            raise forms.ValidationError(
                "You must be between 8 and 60 years old to register."
            )
        return age

    def clean_birthdate(self):
        birthdate = self.cleaned_data["birthdate"]
        if birthdate.year < 1950 or birthdate.year > timezone.now().year:
            raise forms.ValidationError("Invalid birth year.")
        if birthdate.month not in range(1, 13):
            raise forms.ValidationError("Invalid birth month.")
        if birthdate.day not in range(
            1, calendar.monthrange(birthdate.year, birthdate.month)[1] + 1
        ):
            raise forms.ValidationError("Invalid birth day.")
        self.validate_age(birthdate)
        return birthdate

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if not phone_number.isdigit():
            raise forms.ValidationError("Invalid phone number")
        elif len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be 10 digits long")
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone_number

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ForgotPasswordForm(forms.Form):
    phone_or_email = forms.CharField(
        label="Phone number or email",
        widget=forms.TextInput(attrs={"class": "form-control", "required": True}),
    )
    send_to = forms.CharField(
        label="Send verification code to",
        widget=forms.Select(choices=SEND_CODE_TO),
    )

    def clean_phone_or_email(self):
        phone_or_email = self.cleaned_data["phone_or_email"]
        try:
            user = CustomUser.objects.get(
                models.Q(phone_number=phone_or_email) | models.Q(email=phone_or_email)
            )
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(
                "Phone number or email doesn't exist in our database"
            )
        return user

    def clean_send_to(self):
        user = self.cleaned_data["phone_or_email"]
        send_to = self.cleaned_data["send_to"]
        if send_to == "email" and not user.email:
            raise forms.ValidationError("The user has no email address")
        elif send_to == "phone" and not settings.CAN_SEND_SMS:
            raise forms.ValidationError(
                "Sorry, we are not able to send sms. Please try other option"
            )
        return send_to

    def create_password_reset_request(self):
        """Create a password reset request for the user"""
        user = self.cleaned_data["phone_or_email"]
        PasswordResetRequest.objects.filter(user=user).delete()
        reset_request = PasswordResetRequest.objects.create(user=user)
        return reset_request


class ResetPasswordForm(forms.Form):
    code = forms.CharField(
        label="Reset code",
        widget=forms.TextInput(attrs={"class": "form-control", "required": True}),
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "required": True}),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "required": True}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        return super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data["code"]
        try:
            reset_request = PasswordResetRequest.objects.get(user=self.user, code=code)
        except PasswordResetRequest.DoesNotExist:
            raise forms.ValidationError("Invalid reset code.")
        if not reset_request.is_valid():
            raise forms.ValidationError("Reset code has expired.")
        return code

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")
        return confirm_password

    def save(self):
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        self.user.save()
