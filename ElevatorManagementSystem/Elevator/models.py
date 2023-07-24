from django.db import models

options = [
    ("Start","Start"),
    ("Stop","Stop"),
]

Door = [
    ("Open","Open"),
    ("Close","Close"),
]

Move = [
    ("Up","Up"),
    ("Down","Down"),
]

class Lift(models.Model):
    liftname = models.CharField(max_length=2)

    def __str__(self):
         return self.liftname

class Floor(models.Model):
    floornumber = models.CharField(max_length=2,unique=True)

    def __str__(self):
         return self.floornumber

class LiftDetails(models.Model):
    lift_det= models.ForeignKey(Lift,on_delete=models.CASCADE)
    whichfloor = models.ForeignKey(Floor,on_delete=models.CASCADE)
    runnning = models.CharField(max_length=5,choices=options,default="Start")
    door_status = models.CharField(max_length=5,choices=Door,default="Close")
    move_status = models.CharField(max_length=4,choices=Move,default="Up")
    lift_status = models.BooleanField(default=True)
    current_status = models.IntegerField(null=True,blank=True)

    def __str__(self):
         return str(f'{self.current_status}/{self.lift_det.liftname}/{self.move_status}') 

    
                  