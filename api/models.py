from django.db import models


# Create your models here.
# 使用者資訊
class User(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=150)
    gender = models.CharField(max_length=5)
    live = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    permission = models.IntegerField()
    about = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'user'

class Post(models.Model):
    no = models.IntegerField(primary_key=True)
    usermail = models.ForeignKey(User, models.DO_NOTHING, db_column='usermail')
    title = models.TextField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'discuss_post'

class Message(models.Model):
    no = models.IntegerField(primary_key=True)
    nopost = models.ForeignKey(Post, models.DO_NOTHING, db_column='nopost')
    usermail = models.ForeignKey(User, models.DO_NOTHING, db_column='usermail')
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'discuss_message'
