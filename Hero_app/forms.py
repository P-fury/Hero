from django import forms

from Hero_app.models import Char, ActivityType


class CharCreateForm(forms.ModelForm):
    bmi = forms.IntegerField(required=False)
    class Meta:
        model = Char
        fields = '__all__'
        exclude = ['days']




class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = ActivityType
        fields = '__all__'