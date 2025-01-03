# Generated by Django 5.0.3 on 2024-12-28 15:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('alamat', models.TextField()),
                ('harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('jarak_ke_kampus', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fasilitas', models.PositiveIntegerField()),
                ('luas_kamar', models.DecimalField(decimal_places=2, max_digits=5)),
                ('deskripsi', models.TextField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='kos_fotos/')),
                ('tersedia', models.BooleanField(default=True)),
                ('jenis', models.CharField(default='Laki-Laki', max_length=255)),
                ('Jumlah_Kamar', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Kriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('bobot', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tipe', models.CharField(choices=[('benefit', 'Benefit'), ('cost', 'Cost')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Pesanan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_pesan', models.DateTimeField(auto_now_add=True)),
                ('tanggal_mulai', models.DateField()),
                ('tanggal_akhir', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='pending', max_length=20)),
                ('kos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rekomendasiKOS_app.kos')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubKriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('nilai', models.DecimalField(decimal_places=2, max_digits=5)),
                ('kriteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subkriteria', to='rekomendasiKOS_app.kriteria')),
            ],
        ),
        migrations.CreateModel(
            name='Penilaian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rekomendasiKOS_app.kos')),
                ('kriteria1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kriteria1', to='rekomendasiKOS_app.subkriteria')),
                ('kriteria2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kriteria2', to='rekomendasiKOS_app.subkriteria')),
                ('kriteria3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kriteria3', to='rekomendasiKOS_app.subkriteria')),
                ('kriteria4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kriteria4', to='rekomendasiKOS_app.subkriteria')),
                ('kriteria5', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kriteria5', to='rekomendasiKOS_app.subkriteria')),
            ],
        ),
    ]
