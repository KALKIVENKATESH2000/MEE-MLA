from django.db import models

# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'states'
    
class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'districts'
    
class Constituency(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'constituencys'
    
    
class PollingStation(models.Model):
    constituency    = models.ForeignKey(Constituency, on_delete=models.CASCADE,null=True)
    no              = models.IntegerField(null=True)
    name            = models.CharField(max_length=150)
    location        = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'polling_stations'