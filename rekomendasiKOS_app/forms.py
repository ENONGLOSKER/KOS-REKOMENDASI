from django import forms
from .models import Pesanan,Kos, Kriteria,SubKriteria, Penilaian

class KriteriaForm(forms.ModelForm):
    class Meta:
        model = Kriteria
        fields = '__all__'

        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'keterangan': forms.TextInput(attrs={'class': 'form-control'}),
            'bobot': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipe': forms.Select(attrs={'class': 'form-control'}, choices=[('benefit', 'Benefit'), ('cost', 'Cost')]),
        }
class SubKriteriaForm(forms.ModelForm):
    class Meta:
        model = SubKriteria
        fields = '__all__'

        widgets = {
            'kriteria': forms.Select(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'nilai': forms.NumberInput(attrs={'class': 'form-control'}),
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

class PenilaianForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PenilaianForm, self).__init__(*args, **kwargs)

        # Mendapatkan semua kriteria
        all_kriteria = Kriteria.objects.all()

        # Melakukan iterasi untuk setiap kriteria
        for i in range(5):
            field_name = f'kriteria{i+1}'
            field = self.fields[field_name]

            # Mendapatkan objek kriteria ke-i
            kriteria = all_kriteria[i] if i < len(all_kriteria) else None

            if kriteria:
                # Mengisi pilihan (choices) dengan keterangan crips dan nilainya
                choices = [(subkriteria.id, f"{kriteria.nama} - {subkriteria.nama}") for subkriteria in kriteria.subkriteria.all()]
                field.choices = choices
            else:
                # Jika tidak ada kriteria, kosongkan pilihan
                field.choices = [("", "")]
    class Meta:
        model = Penilaian
        fields = '__all__'