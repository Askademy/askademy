from rest_framework import serializers

from records.schools.models import School, SchoolFeed, SchoolPicture, choices
from records.users.models import UserSchool


class SchoolPictureSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = SchoolPicture


class SchoolFeedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = SchoolFeed


class SchoolSerializer(serializers.ModelSerializer):
    pictures = SchoolPictureSerializer(many=True, read_only=True)
    owner = serializers.ChoiceField(choices=choices.SCHOOL_OWNER)
    url = serializers.HyperlinkedIdentityField(
        view_name="api:schools-detail", lookup_field="pk"
    )

    def get_fields(self):
        fields = super().get_fields()
        if self.context["view"].action == "list":
            new_fields = serializers.OrderedDict()
            new_fields["name"] = fields.pop("name")
            new_fields["district"] = fields.pop("district")
            new_fields["logo"] = fields.pop("logo")
            new_fields["url"] = fields.pop("url")
            return new_fields
        return fields

    def create(self, validated_data):
        validated_data["added_by"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = School
        exclude = ["added_by", "visible"]


