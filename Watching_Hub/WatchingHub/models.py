from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Classification(models.Model):
    Classification_Owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, default="",related_name="Classification_Owner")
    Classification = models.CharField(max_length=64 , blank=False)

    def __str__(self):
        return f"{self.Classification}"
    
class Show(models.Model):
    # required fileds
    Show_Owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, default="",related_name="Show_Owner")
    Show_title = models.CharField(max_length=64, blank=False)
    Show_img = models.URLField(blank=False,)
    Show_Classification = models.ManyToManyField('Classification', blank=False, related_name="shows")

    # Optional fields
    Show_discription = models.TextField(blank=True, null=True)
    Show_raring = models.FloatField(blank=True, null=True)
    Date_finished_watching = models.DateTimeField( blank=True, null=True)
    Publication_year = models.IntegerField(blank=True, null=True, max_length=4)
    duration = models.TimeField(blank=True, null=True)

    def __str__(self):
        classifications = ", ".join([classification.Classification for classification in self.Show_Classification.all()])
        return f"{self.Show_title} - Classifications: {classifications}"
    

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')

    Sort_Shows_By = models.CharField(
        max_length=50,
        choices=[
            ("Random", "Random"),
            ("Show_title", "Show Title"),
            ("Date_added_latest", "Date Added (Latest First)"),
            ("Date_added_oldest", "Date Added (Oldest First)"),
            ("Newest_in_release", "Newest in Release"),
            ("Oldest_in_release", "Oldest in Release"),
            ("Highest_rating", "Highest Rating"),
            ("Lowest_rating", "Lowest Rating"),
            ("Date_finished_watching_latest", "Date Finished Watching (Latest First)"),
            ("Date_finished_watching_oldest", "Date Finished Watching (Oldest First)"),
            ("Longest_duration", "Longest Duration"),
            ("Shortest_duration", "Shortest Duration"),
            
        ]
    )

    Filter_By_Classification = models.ForeignKey(Classification,on_delete=models.SET_NULL, blank=True, null=True, related_name="filtered_shows")

    def __str__(self):
        return f"Settings for {self.user.username}"