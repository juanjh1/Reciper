from django.db import models



class Service(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    picture = models.ImageField(upload_to='pictures/')
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.price}"


# TODO: Implement as time block
class ClassSpaceModel(models.Model):
    SPACE_TYPES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
    ]

    # teacher = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    space_type = models.CharField(max_length=7, choices=SPACE_TYPES, default='ONLINE')
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    week_cyclic = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.day} - {self.start_time}-{self.end_time}'
    
    class Meta:
        app_label = 'panel'


class Reservation(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')
    class_space = models.ForeignKey(ClassSpaceModel, on_delete=models.CASCADE)
    tickets = models.IntegerField(default=1)

    class Meta:
        app_label = 'panel'
