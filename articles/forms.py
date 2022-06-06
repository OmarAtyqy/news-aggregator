from django import forms

class QueryForm(forms.Form):
    # field to output query
    keywords = forms.CharField(label='Keywords', max_length=100, required=False)

    # choose language
    fr = forms.BooleanField(label="French", required=False)
    en = forms.BooleanField(label="English", required=False)
    ar = forms.BooleanField(label="Arabic", required=False)

    # choose source
    hespress = forms.BooleanField(label="Hespress", required=False)
    france24 = forms.BooleanField(label="France24", required=False)
    map = forms.BooleanField(label="Map", required=False)
    euronews = forms.BooleanField(label="Euronews", required=False)

    # Period
    start_date = forms.DateField(label="From", required=False)
    end_date = forms.DateField(label="To", required=False)