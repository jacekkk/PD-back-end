import graphene
from graphene import (
    Schema,
    Mutation,
    Field,
    List,
    ObjectType,
    InputObjectType,
    String,
    Int,
    Float,
    DateTime,
    ID,
    Boolean
)
from graphene_mongo import MongoengineObjectType

from models.user import User
from models.run import Run


class UserType(MongoengineObjectType):
    class Meta:
        model = User

class RunType(MongoengineObjectType):
    class Meta:
        model = Run

class CreateUserInputType(InputObjectType):
    first_name = String(required=True)
    last_name = String(required=True)
    mass = Float(required=True)
    age = Int()
    email = String()

class AddRunInputType(InputObjectType):
    user_id = String(required=True)
    time = Float(required=True)
    distance = Float(required=True)
    date = DateTime()

class CreateUserMutation(Mutation):
    user = Field(UserType)
    success = Boolean()

    class Arguments:
        user_input = CreateUserInputType(required=True)
        
    def mutate(self, info, user_input=None):
        user = User(
            first_name = user_input.first_name,
            last_name = user_input.last_name,
            mass = user_input.mass,
            age = user_input.age,
            email = user_input.email,
        )

        success = True
        user.save()

        return CreateUserMutation(user=user, success=success)

class AddRunMutation(Mutation):
    run = Field(RunType)

    class Arguments:
        run_input = AddRunInputType(required=True)
        
    def mutate(self, info, run_input=None):
        run = Run(
            date = run_input.date,
            time = run_input.time,
            distance = run_input.distance,
            user_id = run_input.user_id
        )

        run.calories_burned = run.calculate_calories(
            time=run.time,
            distance=run.distance,
            user_id=run.user_id
        )

        user = User.objects.get(pk=run_input.user_id)
        user.runs.append(run)
        user.save()

        return AddRunMutation(run=run)

class Query(ObjectType):
    user = Field(UserType, user_id=String(required=True))
    users = List(UserType)

    def resolve_user(self, info, user_id):
        return User.objects.get(pk=user_id)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

class Mutation(ObjectType):
    create_user = CreateUserMutation.Field()
    add_run = AddRunMutation.Field()

schema = Schema(query=Query, mutation=Mutation, types=[UserType])
