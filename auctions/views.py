from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import forms
from .models import *
from django.db.models import Max
from django.contrib.auth.decorators import login_required

state = "valid"

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings":listings,
        "title":"Auctions",
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
# this func implements what happens if create list tab is pressed
def create_list(request):
    if request.method == "GET":
        form = forms.CreateForm()
        return render(request,"auctions/create_list.html",{
            "form":form
        })
    else:
        form = forms.CreateForm(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data["listing_title"]
            start_bid = str(form.cleaned_data["listing_start_bid"])
            description = form.cleaned_data["listing_description"]
            image_url = form.cleaned_data["listing_image"]
            if image_url == "":
                image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png"
            category_selected = form.cleaned_data["listing_category"]
            if category_selected == None:
                category_selected="Other"
            category = Categories.objects.get(category=category_selected)
            Listing.objects.create(title=title , description=description , start_bid=start_bid , listing_owner=request.user,category=category,image=image_url)
            return HttpResponseRedirect(reverse("index"))
# this func implements what happens if auction item is pressed
@login_required(login_url='login')
def show_listing(request,lis_id):
    listing = Listing.objects.filter(id=lis_id)
    watchlisted = Watchlist.objects.filter(listing=listing.first(),user=request.user)
    bids_cnt = Bid.objects.filter(listing=listing.first()).count()
    comments = Comment.objects.filter(listing=listing.first())
    global state
    if request.method == "GET":
        return render(request,"auctions/listing_page.html",{
            "listing":listing.first(),
            "watchlisted":watchlisted.first(),
            "bids_cnt":bids_cnt,
            "state":state,
            "comments":comments,
        })
    else:
        if "add_watchlist" in request.POST:
            Watchlist.objects.create(user=request.user,listing=listing.first())
        elif "remove_watchlist" in request.POST:
            watchlisted.delete()
        elif "bid" in request.POST:
            if int(request.POST["bid_inp"]) > listing.first().start_bid:
                listing.update(start_bid=request.POST["bid_inp"])
                Bid.objects.create(bid=request.POST["bid_inp"],listing=listing.first(),user=request.user)
                state="valid"
            else:
                state="error"
        elif "close_listing" in request.POST:
            listing_winner = Bid.objects.filter(bid=listing.first().start_bid,listing=listing.first()).first()
            if listing_winner != None:
                listing.update(winner=listing_winner.user)
            else:
                listing.update(winner=request.user)
            return HttpResponseRedirect(reverse("index"))
        elif "comment_btn" in request.POST:
            if request.POST["comment"] != "":
                Comment.objects.create(listing=listing.first(),comment=request.POST["comment"],commenator=request.user)
        return HttpResponseRedirect(reverse("show_listing",kwargs={"lis_id":listing.first().id}))
# this func implements what happens if Watchlist tab is pressed
def watchlist(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    listings = []
    for watchlist in watchlists:
        listings += (Listing.objects.filter(id=watchlist.listing_id))
    return render(request, "auctions/index.html",{
        "listings":listings,
        "title":"Watchlist"
    })
# this func implements what happens if Category tab is pressed
def show_categories(request,categ):
    #categories = Categories.ob
    if request.method == "GET":
        categories=Categories.objects.all()
        return render(request,"auctions/categories.html",{
            "categories" : categories
        })
    else:
        listings = Listing.objects.filter(category=categ)
        return render(request,"auctions/index.html",{
            "listings":listings,
            "titile":Categories.objects.filter(id=categ).first().category
        })