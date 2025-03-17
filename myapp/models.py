from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    def __str__(self):
        return self.username


from django.db import models

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]

    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'employer'})
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, default="Not specified")  # ✅ Fixed default for location
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_min = models.PositiveIntegerField(default=0)  # Minimum experience
    experience_max = models.PositiveIntegerField(default=0)  # Maximum experience
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'job_seeker'})
    resume = models.FileField(upload_to='resumes/')

    # Essential fields
    year_of_passout = models.PositiveIntegerField()
    qualification = models.CharField(max_length=255)
    experience = models.PositiveIntegerField(default=0, blank=True, null=True)  # Optional experience

    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ], default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
