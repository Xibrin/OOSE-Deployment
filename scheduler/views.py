from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PreferenceForm, EventSearchForm
from .models import User, Event
from .support import states, algorithm


def user_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if 'events' not in request.session:
        request.session['events'] = []
    return render(request, "scheduler/user.html", context={
        "user": request.user,
        "navItems": {
            "Profile": reverse("profile"),
            "Logout": reverse("logout"),
        }
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        current_user = authenticate(request, username=username, password=password)
        if current_user:
            login(request, current_user)
            return HttpResponseRedirect(reverse("user"))
        else:
            messages.error(request, message="Invalid Username and/or Password")
            return render(request, "scheduler/login.html")
    return render(request, "scheduler/login.html")


@login_required(login_url='login')
def profile_view(request):
    return render(request, "scheduler/profile.html", context={
        "navItems": {
            "Profile": reverse("profile"),
            "Logout": reverse("logout"),
        }
    })


def logout_view(request):
    logout(request)
    messages.success(request, message="Successfully Logged Out")
    return render(request, "scheduler/login.html")


def register_view(request):
    if request.method != "POST":
        return render(request, "scheduler/register.html")
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    username = request.POST["username"]
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]
    address1 = request.POST["address1"]
    city = request.POST["city"]
    state = states.get_state_code(request.POST["state"])
    country = request.POST["country"]

    if state is None:
        messages.error(request, message="Invalid State")
        return render(request, "scheduler/register.html", context={
            "preference_form": PreferenceForm(),
        })

    if password != confirm_password:
        messages.error(request, message="Passwords do not Match")
        return render(request, "scheduler/register.html", context={
            "preference_form": PreferenceForm(),
        })

    try:
        current_user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            address1=address1,
            city=city,
            state=state,
            country=country,
        )
        current_user.save()
        login(request, current_user)
    except IntegrityError:
        messages.error(request, "Email address already in use")
        return render(request, "scheduler/register.html")
    messages.success(request, "Successfully Created User")
    return render(request, "scheduler/preferences.html", context={
        "preference_form": PreferenceForm(),
    })


@login_required(login_url='login')
def preferences_view(request):
    if request.method == "POST":
        preferences = PreferenceForm(request.POST)
        if preferences.is_valid():
            music = preferences.cleaned_data["music"]
            visual = preferences.cleaned_data["visual"]
            performing = preferences.cleaned_data["performing"]
            film = preferences.cleaned_data["film"]
            lectures = preferences.cleaned_data["lectures"]
            fashion = preferences.cleaned_data["fashion"]
            food = preferences.cleaned_data["food"]
            festivals = preferences.cleaned_data["festivals"]
            charity = preferences.cleaned_data["charity"]
            sports = preferences.cleaned_data["sports"]
            nightlife = preferences.cleaned_data["nightlife"]
            family = preferences.cleaned_data["family"]

            try:
                current_user = User.objects.get(pk=request.user.pk)
                current_user.music = music
                current_user.visual = visual
                current_user.performing = performing
                current_user.film = film
                current_user.lectures = lectures
                current_user.fashion = fashion
                current_user.food = food
                current_user.festivals = festivals
                current_user.charity = charity
                current_user.sports = sports
                current_user.nightlife = nightlife
                current_user.family = family
                current_user.save()
            except IntegrityError:
                messages.error(request, message="Invalid Selection")
                return render(request, "scheduler/preferences.html", context={
                    "preference_form": PreferenceForm(),
                    "navItems": {
                        "Profile": reverse("profile"),
                        "Logout": reverse("logout"),
                    }
                })
            messages.success(request, message="Successfully saved preferences")
            return HttpResponseRedirect(reverse('user'))

    return render(request, "scheduler/preferences.html", context={
        "preference_form": PreferenceForm(),
        "navItems": {
            "Profile": reverse("profile"),
            "Logout": reverse("logout"),
        }
    })


@login_required(login_url='login')
def search_view(request):
    if request.method == "POST":
        event_search_form = EventSearchForm(request.POST)
        if event_search_form.is_valid():
            criteria = event_search_form.cleaned_data
            start_time = criteria["start_time"]
            end_time = criteria["end_time"]
            address1 = criteria["address1"]
            city = criteria["city"]
            state = states.get_state_code(criteria["state"])
            country = criteria["country"]
            commute_hrs = criteria["commute_hrs"]
            commute_mins = criteria["commute_mins"]
            cost = criteria["cost"]
            optimized = criteria["optimized"]

            if state is None:
                messages.error(request, message="Invalid State")
                return render(request, "scheduler/search.html", context={
                    "event_search_form": EventSearchForm(),
                })

            request.session['events'] = []

            events = Event.objects.filter(
                start_time__gte=start_time,
                end_time__lte=end_time,
                city=city,
                state=state,
            )

            if optimized:
                events = algorithm.get_schedule(address1, events, request.user)
            else:
                events = algorithm.sort_events_by_time(events)

            # algorithm.compute_distance(address, events)

            for event in events:
                request.session["events"] += [event.pk]
            return HttpResponseRedirect(reverse('events'))
    return render(request, "scheduler/search.html", context={
        "event_search_form": EventSearchForm(),
        "navItems": {
            "Profile": reverse("profile"),
            "Logout": reverse("logout"),
        }
    })


@login_required(login_url='login')
def events_view(request):
    event_pks = request.session['events']
    events = [Event.objects.get(pk=event_pk) for event_pk in event_pks]
    return render(request, "scheduler/events.html", context={
        "events": events,
        "navItems": {
            "Profile": reverse("profile"),
            "Logout": reverse("logout"),
        }
    })
