import aiohttp_cors
from aiohttp import web

from .middlewares.exception import error_middleware
from .model import ModelApi
from .prediction import PredictionApi, VideoPredictionApi
from .webhook import WebHook

app = web.Application(middlewares=[error_middleware])

app.router.add_view('/predictions', PredictionApi)
app.router.add_view('/predictions/video', VideoPredictionApi)
app.router.add_view('/model', ModelApi)
app.router.add_view('/webhook', WebHook)

# cors
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(),
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route, webview=True)
