from django import forms


class RoomForm(forms.Form):
    timeslots = forms.MultipleChoiceField(choices=[],
                                          widget=forms.CheckboxSelectMultiple(attrs={'class': 'timeslot-checkbox'}),
                                          label='')
    usernames = forms.CharField(
        label='User Names',
        max_length=100,
        help_text='Enter multiple usernames separated by spaces',
        required=True
    )

