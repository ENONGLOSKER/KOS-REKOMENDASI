from django.db import models
from django.contrib.auth.models import User

# Model untuk menyimpan informasi kos
class Kos(models.Model):
    nama = models.CharField(max_length=255)
    alamat = models.TextField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)  # Harga dalam Rp
    jarak_ke_kampus = models.DecimalField(max_digits=5, decimal_places=2)  # Jarak dalam km
    fasilitas = models.PositiveIntegerField()  # Skor fasilitas (1-5)
    luas_kamar = models.DecimalField(max_digits=5, decimal_places=2)  # Luas kamar dalam m²
    deskripsi = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='kos_fotos/', blank=True, null=True)
    tersedia = models.BooleanField(default=True)
    jenis = models.CharField(max_length=255, default='Laki-Laki')
    Jumlah_Kamar = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nama

# Model untuk kriteria SPK
class Kriteria(models.Model):
    nama = models.CharField(max_length=255)
    keterangan = models.CharField(max_length=255)
    bobot = models.DecimalField(max_digits=5, decimal_places=2)  # Bobot kriteria (0.0 - 1.0)
    tipe = models.CharField(max_length=10, choices=(('benefit', 'Benefit'), ('cost', 'Cost')))

    def __str__(self):
        return self.nama

class SubKriteria(models.Model):
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name="subkriteria")
    nama = models.CharField(max_length=255)
    nilai = models.DecimalField(max_digits=5, decimal_places=2)  # Nilai subkriteria (untuk skoring jika diperlukan)

    def __str__(self):
        return f"{self.nilai}"
 
    
# Model untuk memesan kos
class Pesanan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kos = models.ForeignKey(Kos, on_delete=models.CASCADE)
    tanggal_pesan = models.DateTimeField(auto_now_add=True)
    tanggal_mulai = models.DateField()  # Tanggal mulai penyewaan
    tanggal_akhir = models.DateField()  # Tanggal akhir penyewaan
    status = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')),
        default='pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.kos.nama} ({self.status})"

class Penilaian(models.Model):
    kos = models.ForeignKey(Kos, on_delete=models.CASCADE)
    kriteria1 = models.ForeignKey(SubKriteria, related_name='kriteria1', on_delete=models.CASCADE)
    kriteria2 = models.ForeignKey(SubKriteria, related_name='kriteria2', on_delete=models.CASCADE)
    kriteria3 = models.ForeignKey(SubKriteria, related_name='kriteria3', on_delete=models.CASCADE)
    kriteria4 = models.ForeignKey(SubKriteria, related_name='kriteria4', on_delete=models.CASCADE)
    kriteria5 = models.ForeignKey(SubKriteria, related_name='kriteria5', on_delete=models.CASCADE)
