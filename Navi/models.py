# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ownership(models.Model):
    pot_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    is_registered = models.BooleanField()
    date_of_registration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ownership'


class Pots(models.Model):
    pot_id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=1)
    pot_length = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pot_width = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pot_height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    plant = models.CharField(max_length=64)
    plant_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'pots'


class Redemption(models.Model):
    redemption_id = models.IntegerField(primary_key=True)
    reward_id = models.IntegerField()
    user_id = models.IntegerField()
    redeem_datetime = models.DateTimeField()
    has_been_used = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'redemption'


class Rewards(models.Model):
    reward_id = models.IntegerField(primary_key=True)
    reward = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    points_required = models.IntegerField()
    valid_till = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rewards'


class Tasks(models.Model):
    task_id = models.IntegerField(primary_key=True)
    task = models.CharField(max_length=64)
    target_pot = models.IntegerField()
    requester_id = models.IntegerField()
    assignee_id = models.IntegerField(blank=True, null=True)
    points_given = models.DecimalField(max_digits=65535, decimal_places=65535)
    datetime_opened = models.DateTimeField()
    is_done = models.BooleanField()
    urgency = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    contact_number = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        unique_together = (('user_id', 'email'),)
