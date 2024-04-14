from django.db import models
from django.utils import timezone
import uuid

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=64)
    email = models.CharField(max_length=256)
    password_hash = models.CharField(max_length=430)
    salt = models.BinaryField(max_length=16)

    creation_date = models.DateField(auto_now_add=True)

    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            'user_name': self.user_name,
            'email': self.email,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'creation_date': self.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
        }