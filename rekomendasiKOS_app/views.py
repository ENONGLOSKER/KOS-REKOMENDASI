from django.shortcuts import render
# tree
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# app
from .models import Kos, Pesanan, Kriteria
from .forms import PesananForm, KosForm, KriteriaForm

# Create your views here.
# dashboad ---------------------------------------------------------
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

def dashboard_pesanan(request):
    data_pesanan = Pesanan.objects.all()
    context = {
        'data_pesanan': data_pesanan,
    }

    return render(request, 'dashboard_pesanan.html', context)

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
    
def about(request):
    return render(request, 'about.html')
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