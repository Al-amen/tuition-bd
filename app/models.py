from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from multiselectfield import MultiSelectField
from PIL import Image


class PostManager(models.Manager):
    def sorted(self, title):
        return self.order_by(title)

    def less_then(self, size):
        return self.filter(salary__lt=size)


class Contact(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.username


class Subject(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Class_in(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),

    )
    MEDIUM = (
        ('Bangla', 'bangla'),
        ('English', 'English'),
        ('Urdu', 'Urdu'),
        ('Hindi', 'Hindi')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, default=title)
    email = models.EmailField()
    salary = models.FloatField()
    details = models.TextField(default='No details provided')
    available = models.BooleanField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_date = models.DateTimeField(default=now)
    image = models.ImageField(default='default.jpg',
                              upload_to='tuition/images')
    medium = MultiSelectField(
        max_length=100, max_choices=4, choices=MEDIUM,  default='bangla')
    subject = models.ManyToManyField(Subject, related_name='subject_set')
    class_in = models.ManyToManyField(Class_in, related_name='class_set')
    likes = models.ManyToManyField(User, related_name= 'post_likes')
    views = models.ManyToManyField(User,related_name='post_views')
    
    def total_likes(self):
        return self.likes.count()
    def total_views(self):
        return self.views.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)  # Call the real save() method
        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        if self.user:
            return f"{self.title} by: {self.user.username}"

        else:
            return self.title

    def get_subjectlist(self):
        sub = Subject.objects.all()
        subject = ""
        for i in sub:
            subject = subject + str(i) + ','
        return subject

    def get_classlist(self):
        clas = Class_in.objects.all()
        clss = ""
        for i in clas:
            clss = clss + str(i) + ','
        return clss

    def ProperCase(self):
        return self.title.title()

    def UperCase(self):
        return self.title.upper()

    def LowerCase(self):
        return self.title.lower()

    def details_short(self):
        words = self.details.split(' ')

        if len(words) > 10:
            return " ".join(words[:10]) + '....'
        else:
            return self.details


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.TextField()
    parent =  models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.user.username + " : "+self.text[0:15]
    
    
class PostFile(models.Model):
    image = models.ImageField(upload_to='tuition/images')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='images')
    def save(self, *args, **kwargs):
        
        super(PostFile, self).save(*args, **kwargs)  # Call the real save() method
        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
objects = models.Manager()
items = PostManager()
