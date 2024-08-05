from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag


def pagination(request, projects, objects):
    page = request.GET.get("page")  # this variable store the value of the current page
    paginator = Paginator(projects, objects)

    """
    project is the list of projects and the objects is the number of project in each page.

    the paginator class give the set of objects with the given objects

    basically a collections of boxes with each box contain the 6 objects..
    
    you can access each box with its number.

    """

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    """
       paginator.page is the method which take the page no. and return the projects on that page.

       paginator.num_pages gives the total number of pages created by the paginator.

        PageNotAnInteger:
            This exception is raised when the Paginator.page() method is given a value that isn't an integer. For example:

            When the page number passed is not a number (e.g., a string like 'abc').
            When the page number is None.

        EmptyPage:
        This exception is raised in the following scenarios:

            When the requested page number is valid (an integer) but there are no objects on that page.
            When the page number is less than 1.
            When the page number is greater than the total number of pages.

    """

    leftIndex = (int(page)) - 4  # type:ignore

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page)) + 5  # type:ignore

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex)  # type:ignore

    return projects, custom_range


def searchProjects(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__icontains=search_query)  # type: ignore

    projects = Project.objects.distinct().filter(  # type: ignore
        Q(title__icontains=search_query)  # type: ignore
        | Q(description__icontains=search_query)
        | Q(owner__name__icontains=search_query)
        | Q(tags__in=tags)
    )

    return projects, search_query
