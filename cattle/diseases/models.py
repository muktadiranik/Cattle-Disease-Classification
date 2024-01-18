from django.db import models


class CattleImageAndDiseaseDescription(models.Model):
    user_phone = models.CharField(max_length=255, blank=True, null=True)
    image_front = models.ImageField(upload_to="images/", blank=True, null=True)
    image_back = models.ImageField(upload_to="images/", blank=True, null=True)
    image_left = models.ImageField(upload_to="images/", blank=True, null=True)
    image_right = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    doctor_advice = models.TextField(blank=True, null=True)
    diagonosis = models.TextField(blank=True, null=True)
    disease = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user_phone
