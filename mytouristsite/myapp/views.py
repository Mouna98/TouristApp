from django.shortcuts import render, redirect
from .forms import VisitForm


def home(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after saving
    else:
        form = VisitForm()
    return render(request, 'myapp/home.html', {'form': form})
