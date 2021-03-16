from django import forms
from .models import Categories
class CreateForm(forms.Form):
    listing_title = forms.CharField(label="Title",required=True,widget=forms.TextInput(
        attrs={'placeholder':'Title','class':'form-control'}
    ))
    listing_start_bid = forms.IntegerField(label="Start Bid",required=True,widget=forms.NumberInput(
        attrs={'placeholder':'Start Bid','class':'form-control'}
    ))
    listing_description = forms.CharField(label="Description",required=True,widget=forms.Textarea(
        attrs={'placeholder':'Description','class':'form-control','id':'description_textare'}
    ))
    listing_image = forms.CharField(label="Image URL",required=False,widget=forms.TextInput(
        attrs={'placeholder':'Image URL','class':'form-control','id':'image_field'}
    ))
    listing_category = forms.ModelChoiceField(queryset=Categories.objects.all(),required=False)