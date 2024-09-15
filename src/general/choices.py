from django.db import models


class UserRoleType(models.TextChoices):
    user = 'user', 'User'
    employee = 'employee', 'Employee'


class UserGenderType(models.TextChoices):
    male = 'male', 'Male'
    female = 'female', 'Female'