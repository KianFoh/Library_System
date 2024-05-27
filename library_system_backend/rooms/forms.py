from django import forms

class RoomForm(forms.Form):
    timeslots = forms.MultipleChoiceField(
        choices=[], 
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'timeslot-checkbox'}), 
        label='',
        required=False
    )
    number_of_users = forms.ChoiceField(
        label='Number of Users'
    )

    def __init__(self, *args, **kwargs):
        min_users = kwargs.pop('min_users', 1)
        max_users = kwargs.pop('max_users', 10)
        super(RoomForm, self).__init__(*args, **kwargs)
        self.add_username_fields()
        self.fields['number_of_users'].choices = [(i, str(i)) for i in range(min_users, max_users + 1)]


    def add_username_fields(self):
        # Determine the number of users based on form data or initial value
        if self.is_bound:  # Form is bound to POST data
            number_of_users = int(self.data.get('number_of_users', 1))
        else:  # Initial load
            number_of_users = int(self.initial.get('number_of_users', 1))

        # Add username fields based on the number of users
        for i in range(1, number_of_users + 1):
            self.fields[f'username_{i}'] = forms.CharField(
                label=f'Username {i}',
                max_length=100,
                required=True
            )

    def clean(self):
        cleaned_data = super().clean()
        number_of_users = int(cleaned_data.get('number_of_users', 1))
        usernames = [cleaned_data.get(f'username_{i}') for i in range(1, number_of_users + 1)]
        cleaned_data['usernames'] = usernames
        return cleaned_data
