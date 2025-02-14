from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


level_of_fatigue = [
    (1, 'Very Low'),
    (2, 'Low'),
    (3, 'Moderate'),
    (4, 'High'),
    (5, 'Very High'),
]
mood_level = [
    (1, 'Unmotivated'),
    (2, 'Neutral'),
    (3, 'Ready'),
    (4, 'Motivated'),
    (5, 'Eager'),
]


class ActivityType(models.Model):
    name = models.CharField()
    type = models.CharField(null=True, blank=True)
    body_party = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField()
    date = models.DateField(null=True, blank=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, )
    fatigue = models.IntegerField(choices=level_of_fatigue, null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Activity)
def create_day_with_activity(sender, instance, created, **kwargs):
    if created:
        try:
            day = Day.objects.get(date=instance.date)
            day.activity.add(instance)
        except ObjectDoesNotExist:
            new_day = Day.objects.create(date=instance.date)
            new_day.activity.add(instance)


class Day(models.Model):
    date = models.DateField(unique=True)
    mood = models.IntegerField(choices=mood_level, null=True, blank=True)
    fatigue = models.IntegerField(choices=level_of_fatigue, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    activity = models.ManyToManyField(Activity, null=True, blank=True)


class Char(models.Model):
    name = models.CharField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    bmi = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    age = models.IntegerField()
    fat_percent = models.IntegerField(null=True, blank=True)
    days = models.ForeignKey(Day, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_char = Char.objects.get(pk=self.pk)
            if old_char.height != self.height or old_char.weight != self.weight:
                self.bmi = float(self.weight) / (float(self.height) / 100) ** 2
        else:
            self.bmi = float(self.weight) / (float(self.height) / 100) ** 2
        super(Char, self).save(*args, **kwargs)


@receiver(post_save, sender=Char)
def add_weight_in(sender, instance, created, **kwargs):
    if created:
        WeightIn.objects.create(weight=instance.weight)


class WeightIn(models.Model):
    char = models.ForeignKey(Char, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    create_date = models.DateField(auto_now_add=True)


@receiver(post_save, sender=WeightIn)
def update_weight(sender, instance, created, **kwargs):
    if created:
        instance.char.weight = instance.weight
        instance.char.save()
