from django.forms import ModelForm
from users.models import User


class UserAdminForm(ModelForm):

    class Meta:
        model = User
        fields = ['email',
                  'first_name',
                  'last_name',
                  'password',
                  'phone_number',
                  'role']

    def clean(self) -> dict:
        cleaned_data = super().clean()
        cleaned_data.get("password")
        return cleaned_data

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
