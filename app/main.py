from fastapi import FastAPI
from ariadne.asgi import GraphQL
from app.server.graphql.schema import schema
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

middleware = [
    Middleware(
        ContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
    )
]

app = FastAPI(middleware=middleware)

app.add_route("/graphql", GraphQL(schema, debug=True))
