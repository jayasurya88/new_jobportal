from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from myapp.models import CustomUser

# Home Page
def index(request):
    return render(request, 'index.html')

# Job Listing Page
from django.shortcuts import render
from .models import Job

from django.shortcuts import render
from .models import Job

def job_listing(request):
    jobs = Job.objects.filter(status='Open')

    # Get filter parameters
    category = request.GET.get('category')
    location = request.GET.get('location')
    experience = request.GET.get('experience')

    # Apply category filter
    if category:
        jobs = jobs.filter(job_type=category)

    # Apply location filter (case-insensitive)
    if location:
        jobs = jobs.filter(location__icontains=location)

    # Apply experience filter
    if experience:
        min_exp, max_exp = map(int, experience.split('-'))
        jobs = jobs.filter(experience_min__gte=min_exp, experience_max__lte=max_exp)

    context = {'jobs': jobs}
    return render(request, 'job_listing.html', context)

def about(request):
    return render(request, 'about.html')

# Contact Page
def contact(request):
    return render(request, 'contact.html')

# Register View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from myapp.models import CustomUser
from myapp.models import JobApplication
def register_view(request):
    if request.method == "POST":
        user_type = request.POST.get('account_type')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('register_view')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_view')

        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_view')

        user = CustomUser(username=email, email=email, user_type=user_type)
        user.set_password(password)  # Hash the password before saving

        if user_type == "job_seeker":
            user.phone = request.POST.get('phone', '')
            user.skills = request.POST.get('skills', '')
        elif user_type == "employer":
            user.employer_name = request.POST.get('employer_name', '')
            user.company_name = request.POST.get('company_name', '')
            user.company_website = request.POST.get('company_website', '')
            user.company_logo = request.FILES.get('company_image', None)

        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login_view')

    return render(request, 'register.html')



# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")

            # Redirect based on user type
            if user.user_type == "employer":  # Assuming 'employer' represents recruiters
                return redirect('recruiter_dashboard')
            else:
                return redirect('home')  # Default redirect for job seekers
            
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login_view')

    return render(request, 'login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login_view')  # Redirect to login page after logout


def home(request):
    return render(request, 'home.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Job

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from django.db.models import Count

@login_required
def recruiter_dashboard(request):
    # Ensure only the logged-in employer's jobs are shown
    recent_jobs = Job.objects.filter(employer=request.user).annotate(applicant_count=Count('applications'))

    context = {
        'total_jobs': recent_jobs.count(),
        'recent_jobs': recent_jobs,
        'total_applications': JobApplication.objects.filter(job__employer=request.user).count(),  # Total applications
    }
    return render(request, 'recruiter_dashboard.html', context)


def view_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'view_job.html', {'job': job})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job

from django.shortcuts import render, redirect
from .models import Job
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from decimal import Decimal, InvalidOperation
import logging

logger = logging.getLogger(__name__)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from decimal import Decimal, InvalidOperation
import logging

logger = logging.getLogger(__name__)

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == "POST":
        job.title = request.POST.get('title', job.title)
        job.description = request.POST.get('description', job.description)
        job.location = request.POST.get('location', job.location)

        try:
            job.salary_min = Decimal(request.POST.get('salary_min')) if request.POST.get('salary_min') else job.salary_min
            job.salary_max = Decimal(request.POST.get('salary_max')) if request.POST.get('salary_max') else job.salary_max
        except InvalidOperation:
            logger.error("Invalid salary input.")

        job.status = request.POST.get('status', job.status)

        # Validate experience range
        experience_min = int(request.POST.get('experience_min', job.experience_min))
        experience_max = int(request.POST.get('experience_max', job.experience_max))
        if experience_min > experience_max:
            messages.error(request, "Minimum experience cannot be greater than maximum experience.")
            return redirect('edit_job', job_id=job.id)

        job.experience_min = experience_min
        job.experience_max = experience_max

        job.save()
        return redirect('manage_jobs')

    return render(request, 'edit_job.html', {'job': job})



@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == "POST":
        job.delete()
        return redirect('manage_jobs')

    return render(request, 'delete_job.html', {'job': job})

@login_required
def manage_jobs(request):
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'manage_jobs.html', {'jobs': jobs})

@login_required
def post_job(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location', 'Not specified')
        salary_min = request.POST.get('salary_min') or None
        salary_max = request.POST.get('salary_max') or None
        job_type = request.POST.get('job_type')
        status = request.POST.get('status', 'Open')

        # Get experience range and ensure valid input
        experience_min = int(request.POST.get('experience_min', 0))
        experience_max = int(request.POST.get('experience_max', 0))
        if experience_min > experience_max:
            messages.error(request, "Minimum experience cannot be greater than maximum experience.")
            return redirect('post_job')

        Job.objects.create(
            employer=request.user,
            title=title,
            description=description,
            location=location,
            salary_min=salary_min,
            salary_max=salary_max,
            job_type=job_type,
            status=status,
            experience_min=experience_min,
            experience_max=experience_max
        )
        return redirect('manage_jobs')

    return render(request, 'post_job.html')




from django.shortcuts import render, get_object_or_404
from .models import Job

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Check if the logged-in user (job seeker) has already applied for this job
    has_applied = False
    if request.user.is_authenticated and request.user.user_type == 'job_seeker':
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()

    return render(request, 'job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.phone = request.POST.get('phone', user.phone)
        if user.user_type == 'job_seeker':
            user.skills = request.POST.get('skills', user.skills)
        elif user.user_type == 'employer':
            user.company_name = request.POST.get('company_name', user.company_name)
            user.company_website = request.POST.get('company_website', user.company_website)
            if 'company_logo' in request.FILES:
                user.company_logo = request.FILES['company_logo']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile_view')

    return render(request, 'edit_profile.html', {'user': user})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job

@login_required
def view_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    return render(request, 'view_job.html', {'job': job})



from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST' and request.user.user_type == 'job_seeker':
        resume = request.FILES.get('resume')
        year_of_passout = request.POST.get('year_of_passout')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience', 0)  # Defaults to 0 if not provided

        # Ensure resume is uploaded and required fields are filled
        if not resume or not year_of_passout or not qualification:
            messages.error(request, "All required fields must be filled.")
            return redirect('job_detail', pk=job.id)

        # Check if the applicant has already applied for this job
        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            messages.warning(request, "You have already applied for this job.")
            return redirect('job_detail', pk=job.id)

        # Save the application
        JobApplication.objects.create(
            job=job,
            applicant=request.user,
            resume=resume,
            year_of_passout=year_of_passout,
            qualification=qualification,
            experience=experience
        )

        messages.success(request, "Your application has been submitted successfully!")
        return redirect('job_detail', pk=job.id)

    return redirect('job_detail', pk=job.id)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Job, JobApplication

@login_required
def view_applicants(request, job_id):
    # Ensure only the employer who posted the job can view applicants
    job = get_object_or_404(Job, id=job_id, employer=request.user)

    # Fetch all applications for this job
    applications = JobApplication.objects.filter(job=job)

    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'view_applicants.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobApplication

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    # Ensure only the job's employer can update the status
    if application.job.employer != request.user:
        messages.error(request, "Unauthorized access.")
        return redirect('view_applicants', job_id=application.job.id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        # Ensure the new status is valid
        if new_status in ['Pending', 'Reviewed', 'Accepted', 'Rejected']:
            application.status = new_status
            application.save()
            messages.success(request, f"Application status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('view_applicants', job_id=application.job.id)

@login_required
def my_applications(request):
    if request.user.user_type != 'job_seeker':
        return redirect('home')
    
    status_filter = request.GET.get('status')
    applications = JobApplication.objects.filter(applicant=request.user)
    
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'applications': applications,
        'status_choices': JobApplication._meta.get_field('status').choices,
    }
    return render(request, 'my_applications.html', context)
