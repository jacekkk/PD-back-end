from mongoengine import EmbeddedDocument
from mongoengine.fields import (
    StringField,
    IntField,
    FloatField,
    DateTimeField,
    ObjectIdField
)
from datetime import datetime
from bson import ObjectId


class Run(EmbeddedDocument):
    id = ObjectIdField(default=ObjectId)
    user_id = StringField()
    date = DateTimeField(default=datetime.now)
    time = IntField()
    distance = FloatField()
    calories_burned = IntField()

    def calculate_calories(self, time, distance, user_id):
        from .user import User

        if(time == 0 or distance == 0 or user_id is None):
            return 0

        user = User.objects.get(pk=user_id)
        mass_kg = user.mass
        kph = distance / time
        vo2 = 2.209 + 3.1633 * kph
        kcal_per_min = 4.86 * mass_kg * vo2 / 1000

        return kcal_per_min
