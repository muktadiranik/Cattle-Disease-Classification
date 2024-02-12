from rest_framework import serializers
from diseases.models import *


class CattleDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CattleDisease
        fields = "__all__"
