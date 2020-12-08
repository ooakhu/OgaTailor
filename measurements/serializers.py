from rest_framework import serializers
from .models import Measurements

class MeasurementDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurements
        fields = ["chest", "shoulder_width", "waist", "stomach", "arms_length", "biceps", "hips", "waist_to_ankle", "ankle", "neck", "thighs", "extra_comments"]
        #fields = '__all__'