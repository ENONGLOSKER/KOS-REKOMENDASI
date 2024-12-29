# Generated by Django 5.0.3 on 2024-12-28 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rekomendasiKOS_app', '0002_delete_penilaian'),
    ]

    operations = [
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
