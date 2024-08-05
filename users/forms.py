from django.forms import (
    ModelForm,
)  # first import the forms because we are making the forms here
from django.contrib.auth.models import (
    User,
)  # import the models for which you are creating the forms..

from .models import Profile, Skill, Message

# this is optional. we have imported this because we want to inherit the given userCreationForm and modify it....
from django.contrib.auth.forms import UserCreationForm, UsernameField


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # meta is the class where you define which models to use and which fields to includes and what should be the labels for the each field(field are the attribute of the models class and labels are the values that you want to show in the template just like the html labels)...
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        """
        In the django documentation we can look for the fields present in the User class.
        for now the password1 is the actual password
        and the password2 is the confirmation password..
        """

        labels = {
            "first_name": "Name",
            "password1": "password",
            "password2": "confirm password",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        # fields = "__all__"
        fields = "__all__"
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "name",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class MessageForm(ModelForm):
    class Meta:
        model = Message

        fields = ["name", "email", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
