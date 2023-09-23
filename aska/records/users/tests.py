from django.test import TestCase
from django.utils import timezone

from .models import Friendship, CustomUser, PasswordResetRequest



class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            phone_number="1234567890",
            first_name="Kwaku",
            last_name="Asiedu",
            gender="M",
            birthdate="2000-01-01",
        )
        self.user2 = CustomUser.objects.create(
            phone_number="2345678901",
            first_name="Vida",
            middle_name="Akua",
            last_name="Mensah",
            gender="F",
            birthdate="2006-04-02",
        )

        self.friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
        )

    def test_full_name(self):
        self.assertEqual(self.user1.get_full_name(), "Kwaku Asiedu")
        self.user1.middle_name = "Aska"
        self.assertEqual(self.user1.get_full_name(), "Kwaku Aska Asiedu")

    def test_get_friendship_status(self):
        user3 = CustomUser.objects.create(
            first_name="Jane",
            last_name="Doe",
            phone_number="0987654321",
            gender="F",
            birthdate="1990-01-01",
        )

        # Test without any friendship
        self.assertIsNone(self.user1.get_friendship_status(user3))
        self.assertIsNone(user3.get_friendship_status(self.user1))

        # Test Receiver and Sender
        friendship = Friendship.objects.create(sender=user3, receiver=self.user1)
        self.assertEqual(user3.get_friendship_status(self.user1), "sent")
        self.assertEqual(self.user1.get_friendship_status(user3), "received")

        # Test when friendship is accepted
        friendship.status = "accepted"
        friendship.save()
        self.assertEqual(user3.get_friendship_status(self.user1), "accepted")
        self.assertEqual(self.user1.get_friendship_status(user3), "accepted")

    def test_request_password_reset_code(self):
        request = PasswordResetRequest.objects.create(user=self.user1)
        msg = "You have already requested password reset code. Wait for some time to request new code Or use the code you already have to reset your password"

        # test when user has already requested reset password
        self.user1.request_password_reset_code()
        self.assertEqual(self.user1.request_password_reset_code(), msg)

        request.delete()
        # test when user hasn't been requested password reset
        code = self.user1.request_password_reset_code()
        expected_code = PasswordResetRequest.objects.get(user=self.user1).code
        self.assertEqual(code, expected_code)

    def test_password_reset_request_is_valid(self):
        request = PasswordResetRequest.objects.create(user=self.user1)

        # Test when request is valid
        self.assertTrue(request.is_valid())

        # Test when request is invalid
        request.timestamp = timezone.now() - timezone.timedelta(seconds=601)
        self.assertFalse(request.is_valid())
