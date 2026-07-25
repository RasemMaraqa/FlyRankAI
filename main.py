from fastapi import FastAPI

app = FastAPI()


'''init the first fastapi server'''


@app.get("/")
def read_root():
    return {'message': 'Hello Server'}