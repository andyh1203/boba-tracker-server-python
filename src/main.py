from fastapi import FastAPI
from resolvers.hello import Query
from starlette.graphql import GraphQLApp
import graphene

app = FastAPI()

app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))
