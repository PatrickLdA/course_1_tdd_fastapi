from tortoise import fields, models
from tortoise.contrib.pydantic.creator import pydantic_model_creator  # new


# New database model
class TextSummary(models.Model):
    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url


SummarySchema = pydantic_model_creator(TextSummary)
