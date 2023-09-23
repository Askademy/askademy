from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from twilio.rest import Client


def send_verification_code_to_user(
    request, password_reset_request, send_to="phone_and_email"
):
    # Get the app name from the resolved URL
    user = password_reset_request.user
    code = password_reset_request.code
    received_list = []

    # Send the verification code to the user's phone number
    if send_to in ("phone_and_email", "phone"):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your verification code is {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.phone_number,
        )
        received_list.append(user.phone_number)
        
    if send_to in ("phone_and_email", "email") and user.email:
        reset_link = request.build_absolute_uri(
            reverse(f"web:reset-password", kwargs={"user": user.id})
        )
        subject = "Reset your Askademy password"
        message = f"Dear {user.get_full_name()},\n\nWe have received a request to reset the password for your Askademy account. To proceed with the password reset, please use the code provided below, and click on the following link:\n\nReset code: {code}\n\nReset link: {reset_link}\n\nPlease note that the reset code will expire in 24 hours. If you did not initiate this password reset request, please contact our support team immediately.\n\nBest regards,\nThe Askademy Team."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        received_list.append(user.email)
    return " or ".join(received_list)
