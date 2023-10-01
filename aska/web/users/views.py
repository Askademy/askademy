from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from records.users.models import CustomUser
from records.users.forms import RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from utils.helpers.verifications import send_verification_code_to_user


from web import dummy


class UserProfileView(generic.TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, pk, **kwargs):
        user = get_object_or_404(CustomUser, pk=pk)
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(CustomUser, pk=pk)
        context["user_has_school_info"] = any(
            x for x in [user.schools.all(), user.subjects.count(), user.level]
        )
        context["user_school"] = user.get_current_school()
        context["posts"] = user.posts.all()
        return context


def login_view(request):
    form = {"error": None, "message": ""}
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect("web:home")
        else:
            form["error"] = True
            form["message"] = "Unable to log in with provided credentials."
    return render(request, "auth/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("web:home")
    else:
        form = RegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            reset_request = form.create_password_reset_request()
            send_to = form.cleaned_data.get("send_to")
            user = reset_request.user
            recipient = send_verification_code_to_user(
                request=request, password_reset_request=reset_request, send_to=send_to
            )

            messages.success(
                request,
                f'A password Reset Code has been sent to "{recipient}".',
            )
            return redirect("web:reset-password", user=user.id)
    else:
        form = ForgotPasswordForm()
    return render(request, "auth/reset-password/forgot_password.html", {"form": form})


def reset_password_view(request, user):
    user = get_object_or_404(CustomUser, id=user)
    if request.method == "POST":
        form = ResetPasswordForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Password reset successful. Enter your login credentials"
            )
            return redirect("web:login")
    else:
        form = ResetPasswordForm()
    return render(request, "auth/reset-password/reset_password.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("web:login")
