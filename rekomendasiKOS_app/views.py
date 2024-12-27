from django.shortcuts import render
# tree
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# app
from .models import Kos, Pesanan
from .forms import PesananForm

# Create your views here.
def index(request):
    data_kos = Kos.objects.all()

    context = {
        'data_kos': data_kos,
    }
    return render(request, 'index.html',context)
def status(request):
    user_activ = request.user
    data_pesanan_all = Pesanan.objects.filter(user=user_activ)

    #jumlah data berdasarkan status
    jlh_status_all = Pesanan.objects.all().count()
    jlh_status_pending = Pesanan.objects.filter(status='pending').count()
    jlh_status_confirmed = Pesanan.objects.filter(status='confirmed').count()
    jlh_status_canceled = Pesanan.objects.filter(status='canceled').count()
    
    # debug
    print('-------------------------------------------')
    print('data status  all =', jlh_status_all)
    print('data status  pending =', jlh_status_pending)
    print('data status  confirm =', jlh_status_confirmed)
    print('data status  cancel =', jlh_status_canceled)
    print('-------------------------------------------')
     
    
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
                return redirect('/admin/')
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