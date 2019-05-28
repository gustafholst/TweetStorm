from django import forms

class CreatePostForm(forms.Form):
    post_text = forms.CharField(widget=forms.Textarea( \
    attrs={"rows":3, "cols":30}), label='Tweet away', required=True)
