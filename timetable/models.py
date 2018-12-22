from django.db import models
from colorfield.fields import ColorField


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=400)
    color = ColorField(default='#42d1f4')

    def __str__(self):
        return self.name


class StudyHour(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.course_name.name + ' (' + str(self.start_time) + ' - ' + str(self.end_time) + ')'
