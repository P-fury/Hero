from django import forms

from Hero_app.models import Char, ActivityType, Activity, Day


class CharForm(forms.ModelForm):
    bmi = forms.IntegerField(required=False)
    class Meta:
        model = Char
        fields = '__all__'
        exclude = ['days']




class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = ActivityType
        fields = '__all__'



class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})



class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
