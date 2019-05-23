from django import forms

# this class is not used at the moment (consider refactor?)
class LoginForm(forms.Form):
    username = forms.CharField(label="User name", required="True")
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput())

class CreatePostForm(forms.Form):
    post_text = forms.CharField(widget=forms.Textarea( \
    attrs={"rows":10, "cols":60}), label='Tweet away', required=True)
