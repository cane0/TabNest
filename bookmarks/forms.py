from django import forms

class TabSearchForm(forms.Form):
    q = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search for saved tabs'}))

# class RenameSessionForm(forms.Form):
