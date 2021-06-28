from django import forms
from .models import Category, Institution


class DonationForm(forms.Form):
    quantity = forms.IntegerField()
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    institution = forms.ModelChoiceField(queryset=Institution.objects.all())
    address = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=9)
    city = forms.CharField(max_length=255)
    zip_code = forms.CharField(max_length=10)
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.Textarea()
