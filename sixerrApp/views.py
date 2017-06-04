from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sixerrApp.models import Gig
from sixerrApp.forms import GigForm

# Create your views here.

def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(request,'home.html',{"gigs":gigs})

@login_required
def gig_detail(request,id):
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect('/')

    return render(request,'gig_detail.html',{'gig':gig})

@login_required
def create_gig(request):
    error = ''
    if request.method == 'POST':
        gig_form = GigForm(request.POST, request.FILES)
        if gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.user = request.user
            gig.save()
            return redirect('my_gigs')
        else:
            error = "Data is not valid"

    gig_form = GigForm()
    return render(request,'create_gig.html',{'error': error})

@login_required
def edit_gig(request, id):
    return render(request,'edit_gig.html',{})

@login_required
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)
    return render(request,'my_gigs.html',{"gigs":gigs})
