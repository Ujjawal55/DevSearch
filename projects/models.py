import uuid

from django.db import models
from users.models import Profile

# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    source_link = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField("Tag", related_name="project_tag", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)  # type: ignore
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)  # type: ignore
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["-vote_ratio", "-vote_total", "title"]

    @property
    def reviewers(self):
        querySet = self.review_set.all().values_list("owner_id", flat=True)
        return querySet

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVote = reviews.filter(value="up").count()

        totalVotes = reviews.count()

        voteRatio = (upVote / totalVotes) * 100

        self.vote_total = (int)(totalVotes)
        self.vote_ratio = voteRatio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ("up", "up vote"),
        ("down", "down vote"),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE
    )  ## create many to one relationship...
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = [["owner", "project"]]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name
