from django.forms import ModelForm
from diseases.models import *


class CattleImageAndDiseaseDescriptionForm(ModelForm):
    class Meta:
        model = CattleImageAndDiseaseDescription
        fields = ["user_phone", "image_front", "image_back", "image_left",
                  "image_right", "description", "doctor_advice", "diagonosis", "disease", "treatment"]
