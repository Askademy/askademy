from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import School
from records.locations.models import District


class SchoolModelTestCase(TestCase):
    def setUp(self):
        self.district = District.objects.create(name="Upper Denkyira West", region="CEN")
        self.school = School.objects.create(
            name="Akwaboso D/A Basic",
            code="123456",
            owner="GOV",
            gender="B",
            district=self.district,
            town="Akwaboso",
            logo=SimpleUploadedFile(
                "test_image.jpg",
                b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b",
                content_type="image/jpeg",
            ),
        )

    def test_get_school_info(self):
        expected_school_info = {
            "name": "Akwaboso D/A Basic",
            "owner": "Government",
            "telephone": None,
            "address": "Akwaboso, Central Region",
            "logo": self.school.logo.url,
        }
        self.assertEqual(self.school.get_school_info(), expected_school_info)
