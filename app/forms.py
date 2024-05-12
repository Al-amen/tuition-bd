



from django import forms
from .models import Post, Contact

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'My Name'
        self.fields['username'].initial = 'this name'
        self.fields['email'].label = 'My Email'
        self.fields['phone'].label = 'Phone'
        self.fields['phone'].initial = '+8801'
        
    class Meta:
        model = Contact
        fields = '__all__'

    def clean_username(self):
        value= self.cleaned_data["username"]
        number_of_w = value.split(' ')
        if len(number_of_w ) > 3 :
            self.add_error('username', 'Name can have a maximum of 3 words')
        else: return value
        
        
        
       
              
              
              
              
              
        #   widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Enter Your Name'}),
        #     'email' : forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Your Email'}),
        #     'phone' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Enter Your Phone Number'}),
        #     'content' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Say something','rows': 5}),
        #   }
        #   labels = {
        #     'username': 'Your Name',
        #     'email' : 'Your email',
        #     'phone' : 'your phone number'
                
        #   }
        #   help_texts = {
        #       'username' : 'username should be start with letter',
        #   }
class ContactFormTwo(forms.ModelForm):
     class Meta:
         model = Contact
         fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user','id','slug','created_date','likes','views']
        widgets = {
            'class_in': forms.CheckboxSelectMultiple(attrs={
                'multiple':True,
            }),
            'subject':forms.CheckboxSelectMultiple(attrs={
                'multiple':True,
            })
        }
    
    