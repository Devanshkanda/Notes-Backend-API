from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Notes(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes_title = models.CharField(max_length=50)
    notes_desc = models.TextField()
    is_done = models.BooleanField(default=False)


class Notes_Shared(models.Model):
    notes_id = models.ForeignKey(Notes, on_delete=models.CASCADE)
    share_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userr")
    share_to = models.ForeignKey(User, on_delete=models.CASCADE)