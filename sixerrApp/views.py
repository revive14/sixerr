from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sixerrApp.models import Gig,Profile
from sixerrApp.forms import GigForm

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                    merchant_id="mfzfr529sc45j67c",
                                    public_key="5bmhzxt48hq4ddtn",
                                    private_key="ace58abe07ffd6d2c71de275e754d02e"
)

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
    client_token= braintree.ClientToken.generate()
    return render(request,'gig_detail.html',{'gig':gig,"client_token":client_token})

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
    try:
        gig = Gig.objects.get(id=id, user=request.user)
        error = ''
        if request.method =="POST":
            gig_form = GigForm(request.POST, request.FILES,instance=gig)
            if gig_form.is_valid():
                gig.save()
                return redirect('my_gigs')
            else:
                error= "DATA is Not Valid"
        return render(request,'edit_gig.html',{"gig":gig, "error":error})
    except Gig.DoesNotExist:
        return redirect("/")

@login_required
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)
    return render(request,'my_gigs.html',{"gigs":gigs})


def profile(request,username):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST["about"]
        profile.slogan = request.POST["slogan"]
        profile.save()
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return redirect('/')
    gigs = Gig.objects.filter(user=profile.user, status=True)
    return render(request,'profile.html',{"profile":profile,"gigs":gigs})


@login_required
def create_purchase(request):
    if request.method == 'POST':
        try:
            gig = Gig.objects.get(id = request.POST['gig_id'])
        except Gig.DoesNotExist:
            return redirect('/')

        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": gig.price,
            "payment_method_nonce": nonce
        })

        if result.is_success:
            print("Buy Gig Success!")
        else:
            print("Buy Gig Failed!")

    return redirect('/')

def category(request, link):
    categories = {
        "graphics-design": "GD",
        "digital-marketing": "DM",
        "video-animation":"VA",
        "music-audio":"MA",
        "programming-tech":"PT"
    }
    try:
        gigs = Gig.objects.filter(category=categories[link])
        return render(request,'home.html',{"gigs":gigs})
    except KeyError:
        return redirect('home')

def search(request):
    gigs = Gig.objects.filter(title__contains=request.GET['title'])
    return render(request,'home.html',{"gigs":gigs})
