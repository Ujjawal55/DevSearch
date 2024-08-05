from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Profile, Skill


def pagination(request, profiles, objects):
    page = request.GET.get("page")
    paginator = Paginator(profiles, objects)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page)) - 4  # type:ignore

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page)) + 5  # type:ignore

    if rightIndex > paginator.num_pages:  # type:ignore
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex)  # type:ignore

    return profiles, custom_range


def searchProfiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skills = Skill.objects.filter(name__icontains=search_query)  # type: ignore
    profiles = Profile.objects.distinct().filter(  # type: ignore
        Q(name__icontains=search_query)  # type: ignore
        | Q(short_intro__icontains=search_query)
        | Q(skill__in=skills)
    )

    return profiles, search_query
