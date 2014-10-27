from django import forms
from records.models import UserProfile, Record

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label='Your e-mail address')
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message
    
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name']
#     user_id = forms.CharField(max_length = 20)
#     nick_name = forms.CharField(max_length = 60)

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['companyname_cn']
    
