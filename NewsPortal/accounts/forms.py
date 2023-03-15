from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        Author = Group.objects.get(name="Author")
        user.groups.add(Author)
        return user
