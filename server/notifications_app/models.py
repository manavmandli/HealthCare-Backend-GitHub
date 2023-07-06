from django.db import models
from user_app.models import CustomUser

# Create your models here.


class NotificationModel(models.Model):
    # generated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reciever")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.content

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        get_latest_by = "timestamp"
        indexes = [
            models.Index(fields=["reciever"], name="user_notifications_idx")
        ]