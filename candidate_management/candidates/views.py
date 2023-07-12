from django.shortcuts import render, get_object_or_404, redirect
from .models import Candidate
from .forms import CandidateForm
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP

def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'candidates/candidate_list.html', {'candidates': candidates})

def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    return render(request, 'candidates/candidate_detail.html', {'candidate': candidate})

def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('candidate_list')
    else:
        form = CandidateForm()
    return render(request, 'candidates/add_candidate.html', {'form': form})

def edit_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect('candidate_detail', pk=pk)
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'candidates/edit_candidate.html', {'form': form, 'candidate': candidate})

def delete_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        candidate.delete()
        return redirect('candidate_list')
    return render(request, 'candidates/delete_candidate.html', {'candidate': candidate})

# def decrypt_number(self,encrypted_number1):
#          cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
#          decrypted = cipher.decrypt(bytes.fromhex(encrypted_number1))
#          return decrypted.decode()
