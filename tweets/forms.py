"""Custom forms."""
from django import forms


class CreatePostForm(forms.Form):
    """Form for tweeting."""
    post_text = forms.CharField(widget=forms.Textarea(
        attrs={"rows": 3, "cols": 30}), label='Tweet away', required=True)
