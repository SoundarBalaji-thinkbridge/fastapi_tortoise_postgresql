from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, null=False)

    def __str__(self):
        return "Users"


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
