from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    access_key = fields.CharField(max_length=255)
    permissions = fields.JSONField(default=['USER_ALL'])
    is_banned = fields.BooleanField(default=False)
    badges = fields.JSONField(default=[])
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    views = fields.IntField(default=0)
    uploads = fields.IntField(default=0)

    class Meta:
        table = "users"