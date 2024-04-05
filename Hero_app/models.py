from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class ActivityType(models.Model):
    name = models.CharField()
    type = models.CharField(null=True, blank=True)
    body_party = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    level_of_fatigue = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'High'),
        (5, 'Very High'),
    ]
    name = models.CharField()
    date = models.DateField(null=True, blank=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, )
    fatigue = models.IntegerField(choices=level_of_fatigue, null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


#     def save(self, *args, **kwargs):
#         try:
#             existing_date = Day.objects.get(date=self.date)
#         except Day.DoesNotExist:
#             new_day = Day.objects.create(date=self.date)
#             new_day.activity.add(self)
#             new_day.save()
#         super().save(*args, **kwargs)
#
@receiver(post_save, sender=Activity)
def create_day_with_activity(sender, instance, created, **kwargs):
    if created:
        if Day.objects.get(date=instance.date):
            Day.objects.get(date=instance.date).activity.add(instance)
        else:
            new_day = Day.objects.create(date=instance.date)
            new_day.activity.add(instance)



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
    date = models.DateField(unique_for_date=True)
    mood = models.IntegerField(choices=mood_level, null=True, blank=True)
    fatigue = models.IntegerField(choices=level_of_fatigue, null=True, blank=True)
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
            self.bmi = float(self.weight) / (float(self.height) / 100) ** 2
        super(Char, self).save(*args, **kwargs)
