from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import User

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
# username, password 필드의 정의는 AuthenticationForm에
class LoginForm(AuthenticationForm):
    pass