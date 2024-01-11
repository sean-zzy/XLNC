from fastapi import FastAPI
from pypox import Pypox
from os.path import dirname
from pypox.middleware import VanguardMiddleware
from starlette.staticfiles import StaticFiles

app: FastAPI = Pypox(dirname(__file__))()
app.add_middleware(
    VanguardMiddleware,
    route_dir=dirname(__file__) + "/routes",
    static_dir=dirname(__file__) + "/static",
    pyodide_dir=dirname(__file__) + "/pyodide",
    enable_pyodide=False,
    base_html="index.html",
    error_html="error.html",
)
app.mount(
    "/static", StaticFiles(directory=dirname(__file__) + "/static"), name="static"
)
