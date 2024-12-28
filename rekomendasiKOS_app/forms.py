from django import forms
from .models import Pesanan,Kos, Kriteria

class KriteriaForm(forms.ModelForm):
    class Meta:
        model = Kriteria
        fields = '__all__'

        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'bobot': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipe': forms.Select(attrs={'class': 'form-control'}, choices=[('benefit', 'Benefit'), ('cost', 'Cost')]),
        }
class KosForm(forms.ModelForm):
    class Meta:
        model = Kos
        fields = "__all__"

        widgets = {
            'nama':forms.TextInput(attrs={'class':'form-control'}),
            'alamat':forms.Textarea(attrs={'class':'form-control'}),
            'harga':forms.NumberInput(attrs={'class':'form-control'}),
            'Jumlah_Kamar':forms.NumberInput(attrs={'class':'form-control'}),
            'jenis':forms.Select(attrs={'class':'form-control'}, choices=[('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan'), ('Pasutri', 'Pasutri')]),
            'jarak_ke_kampus':forms.NumberInput(attrs={'class':'form-control'}),
            'fasilitas':forms.NumberInput(attrs={'class':'form-control'}),
            'luas_kamar':forms.NumberInput(attrs={'class':'form-control'}),
            'deskripsi':forms.Textarea(attrs={'class':'form-control'}),
            'foto':forms.FileInput(attrs={'class':'form-control'}),
            # 'tersedia':forms.CheckboxInput(attrs={'class':'form-control'}),
        }


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
