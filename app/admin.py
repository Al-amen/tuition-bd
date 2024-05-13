from django.contrib import admin
from app.models import Contact,Post,Subject,Class_in,Comment
# Register your models here.
from django.utils import timezone
from django.utils.html import format_html

admin.site.site_header = "TuitionBD Admin Panel"
admin.site.site_title = 'TuitionBD Admin Panel'
admin.site.index_title = ' '
class ComentsInlines(admin.TabularInline):
    model = Comment
    
class PostAdmin(admin.ModelAdmin):
    #fields = ('user','title')
    exclude = ('user','title')
    readonly_fields = ('slug',)
    list_display = ('user','title','title_html_dispaly','created_date', 'get_subjects','salary','created_since','get_class_in',)
    list_filter = ('user','subject','class_in',)
    search_fields = ('details','title','user__username','subject__name','class_in__name',)
    filter_horizontal = ('subject','class_in')
    list_editable = ('salary',)
    list_display_links = ('title', 'user')
    actions = ('change_salary_3000')
    inlines = [
        ComentsInlines,
    ]
    
    def title_html_dispaly(self,obj):
        return format_html(
           f'<span style ="font-size : 20px; color: blue;">{obj.title} </span>'  
        )
    
    def change_salary_3000(self, request,queryset):
        count = queryset.update(salary = 3000)
        self.message_user(request,'{} posts updated'.format(count,))
    change_salary_3000.short_description = 'Change salary'
    
    def created_since(self, Post):
         diff = timezone.now() - Post.created_date
         return diff.days
    created_since.short_description = 'Since Created'
    
    def get_subjects(self, obj):
        return " ".join([p.name for p in obj.subject.all()])
         
    get_subjects.short_description = 'Subjects'
    
    def get_class_in(self, obj):
        return " ".join([p.name for p in obj.class_in.all()])
         
    get_class_in.short_description = 'Class'
    
     






admin.site.register(Contact)
admin.site.register(Post,PostAdmin)
admin.site.register(Subject)
admin.site.register(Class_in)
admin.site.register(Comment)