from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, pagination
# Create your views here.


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        # print(request.POST)
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "uername does not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account")
        else:
            messages.error(request, "something wrong with the username or the password")
    return render(request, "users/login_register.html")


def logoutUser(request):
    logout(request)
    messages.info(request, "user has been logout")
    return redirect("login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "user has been created...")

            login(request, user)
            return redirect("edit-account")

        else:
            messages.success(
                request, "some error has been occurred while submiting the form.."
            )

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    profiles, custom_range = pagination(request, profiles, 6)

    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "users/profile.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)  # type: ignore

    topSkills = profile.skill_set.exclude(description__exact="")  # type: ignore
    otherSkills = profile.skill_set.filter(description="")

    context = {"profile": profile, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")  # type: ignore
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid:
            form.save()
            return redirect("account")
    context = {"form": form}
    return render(request, "users/profile-form.html", context)


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "skill has been created successfully.")
            return redirect("account")
    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "skill has been updated successfully.")
            return redirect("account")
    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        return redirect("account")

    context = {"object": skill}
    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messagesRequest = profile.messages.all()
    unReadMessagesCount = messagesRequest.filter(is_read=False).count()
    context = {
        "messagesRequest": messagesRequest,
        "unReadMessagesCount": unReadMessagesCount,
    }
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read:
        message.lastRead = timezone.localtime(timezone.now())
        message.save()
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)  # type: ignore
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.recipient = recipient
            message.sender = sender

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, "message has been send successfully")
            return redirect("user-profile", pk=pk)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)
