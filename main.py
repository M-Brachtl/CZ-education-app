from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import uvicorn
import nlp_stanza # import the nlp_stanza.py file


app = FastAPI()

app.mount("/Czech-Education-App/home", StaticFiles(directory="docs/home", html=True), name="home")
app.mount("/Czech-Education-App/test", StaticFiles(directory="docs/test", html=True), name="test")
app.mount("/Czech-Education-App/images", StaticFiles(directory="docs/images"), name="images")
app.mount("/Czech-Education-App/profile", StaticFiles(directory="docs/profile", html=True), name="profile")
app.mount("/Czech-Education-App/settings", StaticFiles(directory="docs/settings", html=True), name="settings")
app.mount("/Czech-Education-App/", StaticFiles(directory="docs", html=True), name="static")

# @app.get("/page/", response_class=HTMLResponse)
# def serve_index():
#     return open("docs/home/index.html", "r").read()

@app.get("/test/test.html", response_class=HTMLResponse)
def read_root():
    return open("test.html", "r").read()

@app.get("/pos/{input_sentence}")
def read_root(input_sentence: str):
    print(input_sentence)
    return nlp_stanza.get_xpos_sentence(input_sentence)

@app.get("/morph/{input_sentence}")
def read_root(input_sentence: str):
    print(input_sentence)
    return nlp_stanza.get_morphology_sentence(input_sentence)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)