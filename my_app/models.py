from django.db import models
from django.utils import timezone
from django.urls import reverse

# Reading status choices
STATUSES = (
    ('S', 'Started'),
    ('P', 'In Progress'),
    ('C', 'Completed'),
)

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    pages = models.IntegerField()
    genre = models.ManyToManyField(Genre)
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.id})

    def read_for_today(self):
        return self.reading_set.filter(date=timezone.localdate()).exists()

class Reading(models.Model):
    date = models.DateField('Reading date')
    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=STATUSES[0][0]
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_status_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']
