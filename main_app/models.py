from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})
    

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    image = models.ImageField(upload_to='main_app/static/uploads/', default="")
    toys = models.ManyToManyField(Toy)

    # Foreign Key of the User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})


# Feeding model:
class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(
        max_length=1, 
        choices=MEALS,
        default=MEALS[0][0]
    )
    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"

    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

# change the default sort
class Meta:
    ordering = ['-date']