from django import forms
from .models import Pesanan

class PesananForm(forms.ModelForm):
    kos = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Pesanan
        fields = ['tanggal_mulai', 'tanggal_akhir']
        widgets = {
            'tanggal_mulai': forms.DateInput(attrs={'type': 'date'}),
            'tanggal_akhir': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'tanggal_mulai': 'Tanggal Mulai',
            'tanggal_akhir': 'Tanggal Akhir',
        }
