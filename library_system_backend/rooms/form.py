from django import forms

class RoomForm(forms.Form):
    timeslots = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label='Select timeslots', choices=[])