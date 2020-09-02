from django import forms
from web.models import Link

class NewLink(forms.ModelForm):
    class Meta():
        model = Link
        fields ='__all__'




# class NumLink(forms.ModelForm):
#     class Meta():
#         model = Link
#         fields =(Num_OF_Line)
