from django.db import models

class Teams(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Sprint(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Issue(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    resolved_at = models.DateTimeField()
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
