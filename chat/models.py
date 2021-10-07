from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Message(models.Model):
    author = models.ForeignKey(User, related_name="author_messages", on_delete=CASCADE) 
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username
    
    class Meta:
        ordering =['-timestamp']
