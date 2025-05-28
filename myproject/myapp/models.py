from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    marital_status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    joining_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    hours = models.PositiveIntegerField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    progress = models.IntegerField(default=0)  # 0 to 100
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    members = models.ManyToManyField('Employee', blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    deadline = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'), ('Completed', 'Completed')
    ])

    def __str__(self):
        return self.title





