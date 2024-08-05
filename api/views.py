from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "/api/projects"},
        {"GET": "/api/projects/id"},
        {"GET": "/api/projects/id/vote"},
        {"GET": "/api/users/token"},
        {"GET": "/api/users/token/refresh"},
    ]

    return Response(routes)


@api_view(["GET"])
def getProjects(request):
    projects = Project.objects.all()  # type: ignore
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProject(request, pk):
    projects = Project.objects.get(id=pk)  # type: ignore
    serializer = ProjectSerializer(projects)
    return Response(serializer.data)
