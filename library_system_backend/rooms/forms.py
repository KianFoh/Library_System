from django import forms

class RoomForm(forms.Form):
    timeslots = forms.MultipleChoiceField(choices=[],
                                          widget=forms.CheckboxSelectMultiple(attrs={'class': 'timeslot-checkbox'}))