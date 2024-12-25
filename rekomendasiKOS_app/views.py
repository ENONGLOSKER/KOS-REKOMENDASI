from django.shortcuts import render
# tree
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
def status(request, id):
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
def signin(request):
    return render(request, 'signin.html')
def signup(request):
    return render(request, 'signup.html')
