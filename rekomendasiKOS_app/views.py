from django.shortcuts import render
# tree
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Max, Min
from decimal import Decimal
# app
from .models import Kos, Pesanan, Kriteria, SubKriteria, Penilaian
from .forms import PesananForm, KosForm, KriteriaForm, SubKriteriaForm, PenilaianForm
# Create your views here.
# dashboad ---------------------------------------------------------

from django.db.models import Max, Min

def dashboard_rekomendasi(request):
    # Mengambil semua data penilaian
    data_penilaian = Penilaian.objects.all()

    # Menghitung nilai maksimal dan minimal untuk setiap kriteria
    max_values = {
        'kriteria1': Penilaian.objects.aggregate(Max('kriteria1__nilai'))['kriteria1__nilai__max'],
        'kriteria2': Penilaian.objects.aggregate(Max('kriteria2__nilai'))['kriteria2__nilai__max'],
        'kriteria3': Penilaian.objects.aggregate(Max('kriteria3__nilai'))['kriteria3__nilai__max'],
        'kriteria4': Penilaian.objects.aggregate(Max('kriteria4__nilai'))['kriteria4__nilai__max'],
        'kriteria5': Penilaian.objects.aggregate(Max('kriteria5__nilai'))['kriteria5__nilai__max'],
    }

    min_values = {
        'kriteria1': Penilaian.objects.aggregate(Min('kriteria1__nilai'))['kriteria1__nilai__min'],
        'kriteria2': Penilaian.objects.aggregate(Min('kriteria2__nilai'))['kriteria2__nilai__min'],
        'kriteria3': Penilaian.objects.aggregate(Min('kriteria3__nilai'))['kriteria3__nilai__min'],
        'kriteria4': Penilaian.objects.aggregate(Min('kriteria4__nilai'))['kriteria4__nilai__min'],
        'kriteria5': Penilaian.objects.aggregate(Min('kriteria5__nilai'))['kriteria5__nilai__min'],
    }

    # Definisikan tipe kriteria (benefit atau cost)
    kriteria_types = {
        'kriteria1': 'benefit',
        'kriteria2': 'benefit',
        'kriteria3': 'benefit',
        'kriteria4': 'cost',
        'kriteria5': 'benefit',
    }

    # Bobot kriteria (contoh, sesuaikan dengan kebutuhan)
    weights = {
        'kriteria1': Kriteria.objects.get(keterangan='kriteria1').bobot,
        'kriteria2': Kriteria.objects.get(keterangan='kriteria2').bobot,
        'kriteria3': Kriteria.objects.get(keterangan='kriteria3').bobot,
        'kriteria4': Kriteria.objects.get(keterangan='kriteria4').bobot,
        'kriteria5': Kriteria.objects.get(keterangan='kriteria5').bobot,
    }

    # Normalisasi data
    normalisasi_data = []
    skor_wsm = []
    skor_wpm = []
    penggabungan_skor = []

    for penilaian in data_penilaian:
        normalized = {'alternatif': penilaian.kos.nama}
        wsm_score = 0
        wpm_score = 1

        for kriteria, tipe in kriteria_types.items():
            nilai = getattr(penilaian, kriteria).nilai
            if tipe == 'benefit':
                normalized[kriteria] = nilai / (max_values[kriteria] or 1)
            elif tipe == 'cost':
                normalized[kriteria] = (min_values[kriteria] or 1) / (nilai or 1)

            # Perhitungan WSM
            wsm_score += Decimal(weights[kriteria]) * normalized[kriteria]

            # Perhitungan WPM
            wpm_score *= normalized[kriteria] ** Decimal(weights[kriteria])

        normalisasi_data.append(normalized)
        skor_wsm.append({'alternatif': penilaian.kos.nama, 'score': wsm_score})
        skor_wpm.append({'alternatif': penilaian.kos.nama, 'score': wpm_score})
        penggabungan_skor.append({'alternatif': penilaian.kos.nama, 'score': Decimal(0.5) * wsm_score + Decimal(0.5) * wpm_score})

    skor_gabungan_tertinggi = max(penggabungan_skor, key=lambda x: x['score'])
    alternatif_tertinggi = skor_gabungan_tertinggi['alternatif']
    skor_tertinggi = skor_gabungan_tertinggi['score']

    context = {
        'data_penilaian': data_penilaian,
        'max_values': max_values,
        'min_values': min_values,
        'normalisasi_data': normalisasi_data,
        'skor_wsm': skor_wsm,
        'skor_wpm': skor_wpm,
        'penggabungan_skor': penggabungan_skor,
        'alternatif_tertinggi': alternatif_tertinggi,
        'skor_tertinggi': skor_tertinggi,
    }
    return render(request, 'dashboard_penilaian.html', context)


def dashboard_rekomendasi_add(request):
    if request.method == 'POST':
        form = PenilaianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dsb_penilaian')
    else:
        form = PenilaianForm()    
    context = {
        'form': form,
    }

    return render(request, 'dashboard_form.html', context)

def dashboard_rekomendasi_edit(request, id):
    data_penilaian = get_object_or_404(Penilaian, id=id)
    if request.method == 'POST':
        form = PenilaianForm(request.POST, instance=data_penilaian)
        if form.is_valid():
            form.save()
            return redirect('dsb_penilaian')
    else:
        form = PenilaianForm(instance=data_penilaian)    
    context = {
        'form': form,
    }

    return render(request, 'dashboard_form.html', context)

def dashboard_rekomendasi_delete(request, id):
    data_penilaian = get_object_or_404(Penilaian, id=id)
    data_penilaian.delete()
    return redirect('dsb_penilaian')
    
@login_required
def dashboard_kriteria(request):
    data_kriteria = Kriteria.objects.all()
    context = {
        'data_kriteria': data_kriteria,
    }
    return render(request, 'dashboard_kriteria.html', context)
def dashboard_kriteria_add(request):
    if request.method == 'POST':
        form = KriteriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dsb_kriteria')
    else:
        form = KriteriaForm()    
    context = {
        'form': form,
    }

    return render(request, 'dashboard_form.html', context)
def dashboard_kriteria_edit(request, id):
    data_kriteria = get_object_or_404(Kriteria, id=id)
    if request.method == 'POST':
        form = KriteriaForm(request.POST, instance=data_kriteria)
        if form.is_valid():
            form.save()
            return redirect('dsb_kriteria')
    else:
        form = KriteriaForm(instance=data_kriteria)    
    context = {
        'form': form,
    }

    return render(request, 'dashboard_form.html', context)
def dashboard_kriteria_delete(request, id):
    data_kriteria = get_object_or_404(Kriteria, id=id)
    data_kriteria.delete()
    return redirect('dsb_kriteria')

def dashboard_subkriteria(request, id):
    data_kriteria = get_object_or_404(Kriteria, id=id)
    data_subkriteria = data_kriteria.subkriteria.all()

    context = {
        'data_kriteria': data_kriteria,
        'data_subkriteria': data_subkriteria,
    }
    return render(request, 'dashboard_subkriteria.html', context)
def dashboard_subkriteria_add(request):
    if request.method == 'POST':
        form = SubKriteriaForm(request.POST)
        if form.is_valid():
            form.save()
            sub_kriteria=form.instance
            return redirect('dsb_subkriteria', id=sub_kriteria.kriteria.id)
    else:
        form = SubKriteriaForm()    
    context = {
        'form': form,
    }

    return render(request, 'dashboard_form.html', context)
def dashboard_subkriteria_edit(request,id):
    data_kriteria = get_object_or_404(SubKriteria, id=id)
    if request.method == 'POST':
        form = SubKriteriaForm(request.POST, instance=data_kriteria)
        if form.is_valid():
            form.save()
            sub_kriteria=form.instance
            return redirect('dsb_subkriteria', id=sub_kriteria.kriteria.id)
    else:
        form = SubKriteriaForm(instance=data_kriteria)    
    context = {
        'form': form,
    }

    return render(request, 'dashboard_form.html', context)
def dashboard_subkriteria_delete(request, id):
    data_kriteria = get_object_or_404(SubKriteria, id=id)
    data_subkriteria = data_kriteria.kriteria.id
    data_kriteria.delete()
    return redirect('dsb_subkriteria', id=data_subkriteria)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
def dashboard_kos(request):
    data_kos = Kos.objects.all()
    context = {
        'data_kos': data_kos,
    }

    return render(request, 'dashboard_kos.html', context)
def dashboard_kos_add(request):
    if request.method == 'POST':
        form = KosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dsb_kos')
    else:
        form = KosForm()    
    context = {
        'form': form,
    }

    return render(request, 'dashboard_form.html', context)
def dashboard_kos_edit(request, id):
    data_kos = get_object_or_404(Kos, id=id)
    if request.method == 'POST':
        form = KosForm(request.POST, request.FILES, instance=data_kos)
        if form.is_valid():
            form.save()
            return redirect('dsb_kos')
    else:
        form = KosForm(instance=data_kos)    
    context = {
        'form': form,
    }

    return render(request, 'dashboard_form.html', context)
def dashboard_kos_delete(request, id):
    data_kos = get_object_or_404(Kos, id=id)
    data_kos.delete()
    return redirect('dsb_kos')
@login_required
def dashboard_pesanan(request):
    data_pesanan = Pesanan.objects.all()
    context = {
        'data_pesanan': data_pesanan,
    }

    return render(request, 'dashboard_pesanan.html', context)
@login_required
def status_update(request, id):
    data_pesanan = get_object_or_404(Pesanan, id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Pesanan._meta.get_field('status').choices):
            data_pesanan.status = new_status
            data_pesanan.save()
            return redirect('dsb_pesanan')  # Redirect ke halaman daftar pesanan
    return redirect('dsb_pesanan')



#home ---------------------------------------------------------
def index(request):
    
    data_kos = Kos.objects.all()

    context = {
        'data_kos': data_kos,
    }
    return render(request, 'index.html',context)
@login_required
def status(request):
    user_activ = request.user
    data_pesanan_all = Pesanan.objects.filter(user=user_activ)

    #jumlah data berdasarkan status untuk user yang aktif
    jlh_status_all = Pesanan.objects.filter(user=user_activ).count()
    jlh_status_pending = Pesanan.objects.filter(user=user_activ, status='pending').count()
    jlh_status_confirmed = Pesanan.objects.filter(user=user_activ, status='confirmed').count()
    jlh_status_canceled = Pesanan.objects.filter(user=user_activ, status='canceled').count()
    
    context = {
        'data_pesanan': data_pesanan_all,
        'jlh_status_all': jlh_status_all,
        'jlh_status_pending': jlh_status_pending,
        'jlh_status_confirmed': jlh_status_confirmed,
        'jlh_status_canceled': jlh_status_canceled,
    }                              
    return render(request, 'status.html', context)
def detail(request, id):
    data_kos = get_object_or_404(Kos, id=id)
    
    context = {
        'data_kos': data_kos,
    }                              
    return render(request, 'detail.html', context)
@login_required
def buat_pesanan(request, id):
    # Ambil data kos berdasarkan ID
    kos = get_object_or_404(Kos, id=id)

    if not kos.tersedia:
        messages.error(request, "Maaf, kos ini tidak tersedia untuk disewa.")
        return redirect('index')
    
    # Jika metode POST, proses penyewaan
    if request.method == "POST":
        form = PesananForm(request.POST)
        if form.is_valid():
            # Buat pesanan
            pesanan = form.save(commit=False)
            pesanan.user = request.user
            pesanan.kos = kos
            
            # Perbarui status kos
            if kos.Jumlah_Kamar > 0:
                pesanan.save()
                kos.Jumlah_Kamar -= 1
                kos.tersedia = kos.Jumlah_Kamar > 0
                kos.save()

                messages.success(request, "Penyewaan berhasil! Kos telah dipesan.")
                return redirect('index')
            else:
                messages.error(request, "Maaf, tidak ada kamar yang tersedia.")
        else:
            messages.error(request, "Terjadi kesalahan pada form penyewaan. Silakan periksa kembali.")
    else:
        # Jika GET, tampilkan form penyewaan
        form = PesananForm(initial={'kos': kos.nama})

    context = {
        'kos': kos,
        'form': form,
    }
    return render(request, 'form_sewa.html', context)
def batal_pesanan(request, id):
    pesanan = get_object_or_404(Pesanan, id=id)

    if request.method == "POST":
        if pesanan.status == 'pending':
            pesanan.status = 'canceled'
            pesanan.save()
            messages.success(request, "Penyewaan berhasil dibatalkan.")
            return redirect('status')
        else:
            messages.error(request, "Maaf, pesanan ini tidak dapat dibatalkan karena statusnya telah dikonfirmasi.")
            return redirect('status')

# auth  
def signin_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('dashboard')
            else:
                
                return redirect('index')
    return render(request, 'signin.html')
def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('signin')
            else:
                messages.error(request, 'user sudah ada!')
        else:
            messages.error(request, 'password tidak sama')
       
    return render(request, 'signup.html')
def signout_user(request):
    logout(request)
    return redirect('signin')