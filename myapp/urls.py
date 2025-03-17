from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'), 
   path('job_listing',views.job_listing,name="job_listing"),
   path('about',views.about,name="about"),
   path('contact',views.contact,name="contact"),
   path('register_view',views.register_view,name="register_view"),
   path('login_view',views.login_view,name="login_view"),
   path('home',views.home,name="home"),
   path('recruiter_dashboard',views.recruiter_dashboard,name="recruiter_dashboard"),
   path('logout/', views.logout_view, name='logout'),
   path('jobs/manage/', views.manage_jobs, name='manage_jobs'),
   path('jobs/post/', views.post_job, name='post_job'),
   path('jobs/<int:job_id>/', views.view_job, name='view_job'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:application_id>/update/', views.update_application_status, name='update_application_status'),
    path('myapplications/', views.my_applications, name='my_applications'),
    path('profile_view', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('jobs/<int:job_id>/', views.view_job, name='view_job'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
]   




