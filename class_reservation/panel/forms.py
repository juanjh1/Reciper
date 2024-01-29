from typing import Any
from django import forms
from .models import ClassSpaceModel, Reservation, Service


class ClassSpaceForm(forms.ModelForm):
    class Meta:
        model = ClassSpaceModel
        fields = ['space_type', 'day', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super(ClassSpaceForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = forms.Select(choices=[(f'{i}:00', f'{i}:00') for i in range(0, 24)])
        self.fields['end_time'].widget = forms.Select(choices=[(f'{i}:00', f'{i}:00') for i in range(0, 24)])
        self.fields['day'].widget = forms.SelectDateWidget()

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError({"start_time": 'End time must be greater than start time'})

        return cleaned_data


class ClassSpaceEditForm(forms.ModelForm):
    class Meta:
        model = ClassSpaceModel
        fields = ['space_type', 'day', 'start_time', 'end_time']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'description', 'location', 'picture']


class ReservationForm(forms.ModelForm):
    # space = forms.CharField()

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone_number', 'service', 'class_space', 'tickets']


class PaymentForm(forms.ModelForm):
    total_cost = forms.CharField(disabled=True)
    tickets = forms.CharField(disabled=True)
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone_number', 'service', 'class_space', 'tickets', 'total_cost']
