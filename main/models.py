from django.db import models


class Authors(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Authors'


class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Users'


class Books(models.Model):
    author = models.ForeignKey(Authors, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Books'


class Bookings(models.Model):
    book = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.book.name

    class Meta:
        verbose_name_plural = 'Bookings'

class Chattings(models.Model):
    author = models.ForeignKey(Authors, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name_plural = 'Messages'
