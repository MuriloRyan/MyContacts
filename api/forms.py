from django import forms

class UserSignInForm(forms.Form):
    user_name = forms.CharField(max_length=64)
    #password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(max_length=128)
    #email = forms.EmailField()
    email = forms.CharField(max_length=128)

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        # Adicione sua lógica de validação para user_name aqui
        return user_name

    def clean_password(self):
        password = self.cleaned_data['password']
        # Adicione sua lógica de validação para password aqui
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        # Adicione sua lógica de validação para email aqui
        return email


class UserLogInForm(forms.Form):
    #password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(max_length=128)
    #email = forms.EmailField()
    email = forms.CharField(max_length=128)

    def clean_password(self):
        password = self.cleaned_data['password']
        # Adicione sua lógica de validação para password aqui
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        # Adicione sua lógica de validação para email aqui
        return email

class TokenForm(forms.Form):
    token = forms.CharField(max_length=500)

    def clean_token():
        token = self.cleaned_data['token']

        return token