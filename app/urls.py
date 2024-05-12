from app import views
from django.urls import path
from app.forms import ContactForm
from .views import ContactView, PostCreateView,PostListView,PostDetail,PostEditUpdateView,PostDeleteView

app_name = 'app' 

urlpatterns = [
    path('',views.home, name = 'home'),
    path('search/', views.search, name='search'), 
    path('filter/', views.filter, name='filter'),
    path('likepost/<int:id>/', views.likepost, name='likepost'), 
    path('contact/', ContactView.as_view(), name='contact'),
    path('addcomment/', views.addcomment, name='addcomment'),
   # path('contact2/',ContactView.as_view(form_class = ContactForm, template_name = 'contact2.html', ), name = 'contact2'),
    #path('contact/',views.contact, name = 'contact'),
    path('post/',views.postview,name='post'),
    path('postlist/',PostListView.as_view(), name = 'postlist'),
    path('postdetail/<str:pk>/', PostDetail.as_view(), name='postdetail'),
    path('edit/<str:pk>/', PostEditUpdateView.as_view(), name='edit'),
    path('delete/<str:pk>/', PostDeleteView.as_view(), name='delete'),
    path('sub/',views.subjectview,name = "sub"),
    #path('create/',views.postcreate, name='create')
    path('create/', PostCreateView.as_view(), name="create"),
    
]