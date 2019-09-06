import graphene
from graphene import Field, ObjectType, InputObjectType, String, Schema, Int, Float, DateTime, ID
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
    time = Int(required=True)
    distance = Float(required=True)
    date = DateTime()

class CreateUserMutation(graphene.Mutation):

    class Arguments:
        user_input = CreateUserInputType(required=True)

    user = Field(lambda: UserType)
    success = graphene.Boolean()
        
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

class AddRunMutation(graphene.Mutation):
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
            time=run_input.time,
            distance=run_input.distance,
            user_id=run_input.user_id
        )

        user = User.objects.first()
        user.runs.append(run)
        user.save()
        return AddRunMutation(run=run)

class Query(ObjectType):
    user = graphene.Field(UserType, user_id=graphene.String(required=True))
    users = graphene.List(UserType)

    def resolve_user(self, info, user_id):
        return User.objects.get(pk=user_id)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

class Mutation(ObjectType):
    create_user = CreateUserMutation.Field()
    add_run = AddRunMutation.Field()

schema = Schema(query=Query, mutation=Mutation, types=[UserType])
