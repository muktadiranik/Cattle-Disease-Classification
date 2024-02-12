from django.db import models


class CattleDisease(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class CattleDiseaseDescription(models.Model):
    user_phone = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    doctor_advice = models.TextField(blank=True, null=True)
    diagonosis = models.TextField(blank=True, null=True)
    disease = models.ForeignKey(
        CattleDisease, on_delete=models.CASCADE, blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.user_phone


class CattleDiseaseImage(models.Model):
    cattle_disease_description = models.ForeignKey(
        CattleDiseaseDescription, on_delete=models.CASCADE, blank=True, null=True)
    cattle_image = models.ImageField(upload_to="images/")


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
