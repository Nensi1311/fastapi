from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello():
    return {'message': 'Hello World'}

@app.get('/about')
def about():
    return {'message': 'I am Nensi Pansuriya'}

# def index():
#     return {'data': 'blog list'}

# @app.get('/blog/unpublished')
# def unpublished():
#     return {'data': 'all unpublished blogs'}

# # dynamic route
# @app.get('/blog/{id}')
# def show(id: int):
#     return {'data': id}


# @app.get('/blog/{id}/comments')
# def comments(id):
#     return {'data': {'1', '2'}}