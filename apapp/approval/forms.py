from django import forms


class RejectionForm(forms.Form):
    reason = forms.CharField(max_length=200, widget=forms.Textarea())
