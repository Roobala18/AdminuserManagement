from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project, Task, Employee
from .forms import ProjectForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import AddUserForm, EditUserForm, CustomUserEditForm, UserProfileForm
from myapp.models import UserProfile



def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    context = {
        'projects': Project.objects.all(),
        'tasks': Task.objects.all(),
        'employees': Employee.objects.all(),
    }
    return render(request, 'admin/admin_dashboard.html', context)



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@user_passes_test(is_admin)
@login_required
def projects_page(request):
    return render(request, 'admin/projects.html', {'projects': Project.objects.all()})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def employees_page(request):
    
    def user_list():
        return User.objects.all().exclude(is_superuser=True)

    employees = Employee.objects.all()
    users = user_list()

    return render(request, 'admin/employees.html', {
        'employees': employees,
        'users': users
    })
 

@login_required
def admin_employees(request):
    users = User.objects.all()
    return render(request, 'admin/employees.html', {'users': users})

@user_passes_test(is_admin)
@login_required
def tasks_page(request):
    return render(request, 'admin/tasks.html', {'tasks': Task.objects.all()})

@user_passes_test(is_admin)
@login_required
def productivity_page(request):
    return render(request, 'admin/productivity.html')


#add employee
@login_required
def add_employee(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User added successfully!')
            return redirect('admin_dashboard')
    else:
        form = AddUserForm()
    return render(request, 'admin/addemp.html', {'form': form})
# Edit user
@login_required
def edit_employee(request, user_id):
    if not request.user.is_superuser:
        return redirect('user_dashboard')

    user = get_object_or_404(User, pk=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = CustomUserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "User and profile updated successfully.")
            return redirect('employees_page')
    else:
        user_form = CustomUserEditForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'admin/editemp.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    })


#delete employee
@login_required
def delete_employee(request, user_id):
    if not request.user.is_superuser:
        return redirect('user_dashboard')
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('employees_page')


#employees
@login_required
def employee_dashboard(request):
    return render(request, 'employee/employee_dashboard.html')

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'admin/project_create.html', {'form': form})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'admin/projects.html', {'projects': projects})

