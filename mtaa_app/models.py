from django.db import models
#add auto-incrementing
# Create your models here.
class Users(models.Model):
    id_users = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False)
    user_image = models.BinaryField()
    class Meta:
        managed = False
        db_table = 'users'
class Restaurants(models.Model):
    id_restaurants = models.AutoField(primary_key=True)
    restaurant_name = models.TextField(max_length=100, blank=False)
    restaurant_image = models.BinaryField()
    description = models.TextField(max_length=100, blank=False)
    class Meta:
        managed = False
        db_table = 'restaurants'
class Bookings(models.Model):
    id_bookings = models.AutoField(primary_key=True)
    num_ppl = models.PositiveIntegerField()
    date_time = models.DateTimeField()
    rest_id = models.ForeignKey('Restaurants', models.DO_NOTHING, db_column="rest_id")
    user_id = models.ForeignKey('Users', models.DO_NOTHING, db_column="user_id")
    class Meta:
        managed = False
        db_table = 'bookings'
