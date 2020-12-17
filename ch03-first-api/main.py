from typing import Optional

import fastapi
import uvicorn

api = fastapi.FastAPI()


@api.get('/')
def index():
    body = "<html>" \
           "<body style='padding: 10px;'>" \
           "<h1>Welcome to the API</h1>" \
           "<div>" \
           "Try it: <a href='/api/calculate?x=7&y=11'>/api/calculate?x=7&y=11</a>" \
           "</div>" \
           "</body>" \
           "</html>"

    return fastapi.responses.HTMLResponse(content=body)


@api.get('/api/calculate')
def calculate_by_qs(x: int, y: int, z: Optional[int] = None): #pylint: disable=unsubscriptable-object
    if z == 0:
        return fastapi.responses.JSONResponse(
            content={"error": "ERROR: Z cannot be zero."},
            status_code=400)

    value = x + y

    if z is not None:
        value /= z

    return {
        'x': x,
        'y': y,
        'z': z,
        'operation': 'sum',
        'result': value,
    }

@api.get('/api/calculate/{x}/{y}')
def calculate_by_url(x: int, y: int, z: Optional[int] = None): #pylint: disable=unsubscriptable-object
    if z == 0:
        return fastapi.responses.JSONResponse(
            content={"error": "ERROR: Z cannot be zero."},
            status_code=400)

    value = x + y

    if z is not None:
        value /= z

    return {
        'x': x,
        'y': y,
        'z': z,
        'operation': 'sum',
        'result': value,
    }


uvicorn.run(api, port=8000, host="127.0.0.1")
