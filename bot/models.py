from django.db import models


class Training(models.Model):
    reference_id = models.TextField(max_length=128, db_index=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)