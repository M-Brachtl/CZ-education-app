from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import uvicorn
import nlp_stanza # import the nlp_stanza.py file


app = FastAPI()

# složky v docs: home, friends, images, profile, kategorie, slovni-druhy, leaderboard
app.mount("/Czech-Education-App/home", StaticFiles(directory="docs/home", html=True), name="home")
app.mount("/Czech-Education-App/friends", StaticFiles(directory="docs/friends", html=True), name="friends")
app.mount("/Czech-Education-App/images", StaticFiles(directory="docs/images"), name="images")
app.mount("/Czech-Education-App/profile", StaticFiles(directory="docs/profile", html=True), name="profile")
app.mount("/Czech-Education-App/kategorie", StaticFiles(directory="docs/kategorie", html=True), name="kategorie")
app.mount("/Czech-Education-App/slovni-druhy", StaticFiles(directory="docs/slovni-druhy", html=True), name="slovni-druhy")
app.mount("/Czech-Education-App/leaderboard", StaticFiles(directory="docs/leaderboard", html=True), name="leaderboard")

app.mount("/Czech-Education-App/", StaticFiles(directory="docs", html=True), name="static")

# přístup k homepage: http://localhost:8000/Czech-Education-App/home

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

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)

# spustit příkazem: uvicorn main:app (--reload: pro automatické reloadování) (--host=: pro přístup z jiného zařízení) (--port=8000: pro změnu portu)