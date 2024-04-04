from django.db import models


# Create your models here.

class ActivityType(models.Model):
    name = models.CharField()
    type = models.CharField(null=True, blank=True)
    body_party = models.CharField(null=True, blank=True)


class Activity(models.Model):
    level_of_fatigue = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'High'),
        (5, 'Very High'),
    ]
    name = models.CharField()
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, )
    fatigue = models.CharField(choices=level_of_fatigue, null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)


class Day(models.Model):
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
    date = models.DateField()
    mood = models.CharField(choices=mood_level,null=True, blank=True)
    fatigue = models.CharField(choices=level_of_fatigue, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    activity = models.ManyToManyField(Activity, blank=True)


class Char(models.Model):
    name = models.CharField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    bmi = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    age = models.IntegerField()
    fat_percent = models.IntegerField(null=True, blank=True)
    days = models.ForeignKey(Day, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.height and self.weight:
            self.bmi = float(self.weight)/(float(self.height)/100)**2
        super(Char, self).save(*args, **kwargs)

