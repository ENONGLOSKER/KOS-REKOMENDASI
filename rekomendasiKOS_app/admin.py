from django.contrib import admin
from .models import *

class KosAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'harga', 'jarak_ke_kampus', 'fasilitas', 'luas_kamar', 'deskripsi', 'foto', 'tersedia')

admin.site.register(Kos, KosAdmin)

class KriteriaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'bobot', 'tipe')

admin.site.register(Kriteria, KriteriaAdmin)

class KosKriteriaAdmin(admin.ModelAdmin):
    list_display = ('kos', 'kriteria', 'nilai')

admin.site.register(KosKriteria, KosKriteriaAdmin)

class RekomendasiAdmin(admin.ModelAdmin):
    list_display = ('user', 'kos', 'skor_wsm', 'skor_wpm', 'skor_waspas', 'tanggal_rekomendasi')

admin.site.register(Rekomendasi, RekomendasiAdmin)

class PesananAdmin(admin.ModelAdmin):
    list_display = ('user', 'kos', 'tanggal_pesan', 'tanggal_mulai', 'tanggal_akhir', 'status')

admin.site.register(Pesanan, PesananAdmin)


# Register your models here.
