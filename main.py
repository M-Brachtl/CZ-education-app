from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import nlp_stanza # import the nlp_stanza.py file

from pydantic import BaseModel


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

app.mount("/profile/images", StaticFiles(directory="profile-images"), name="profile-images")
# přístup k homepage: http://localhost:8000/Czech-Education-App/home

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def profile_exists(username: str) -> int:
    try:
        data = json.load(open("profiles.json", "r"))
        for i, user in enumerate(data):
            if user["username"] == username:
                return i
        return -1
    except FileNotFoundError:
        return -1
    
class ProfilePicture(BaseModel):
    username: str
    file: list[int]
    filetype: str

# testování NLP funkcí
@app.get("/test/test.html", response_class=HTMLResponse)
def read_root():
    return open("test.html", "r",encoding="utf-8").read()
# POS tagging = Slovní druhy
@app.get("/pos/{input_sentence}")
def read_root(input_sentence: str):
    print(input_sentence)
    return nlp_stanza.get_xpos_sentence(input_sentence)
# Morphology = Mluvnické kategorie
@app.get("/morph/{input_sentence}")
def read_root(input_sentence: str):
    print(input_sentence)
    return nlp_stanza.get_morphology_sentence(input_sentence)

# User profile functions
@app.get("/profile/login/{username}/{password}") # přihlášení uživatele
def read_root(username: str, password: str):
    profile_data = json.load(open("profiles.json", "r"))
    profile_index = profile_exists(username)
    if profile_index > -1:
        if profile_data[profile_index]["password"] == password:
            profile_data[profile_index]["logged-in"] = True
            json.dump(profile_data, open("profiles.json", "w"),indent=4)
            return profile_data[profile_index]
        else:
            return {"error": "Špatné heslo"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    
@app.get("/profile/register/{username}/{password}") # registrace uživatele
def read_root(username: str, password: str):
    profile_data = json.load(open("profiles.json", "r"))
    profile_index = profile_exists(username)
    if profile_index > -1:
        return {"error": "Uživatelské jméno již existuje"}
    else:
        profile_data.append({
            "username": username,
            "password": password,
            "darkmode": False,
            "friends": [],
            "level": 1,
            "profile_picture": "default.png",
            "xp": 0,
            "logged-in": True
        })
        json.dump(profile_data, open("profiles.json", "w"),indent=4)
        return profile_data[-1]
    
@app.get("/profile/add-friend/{username}/{friend}") # přidat přítele
def read_root(username: str, friend: str):
    profile_data = json.load(open("profiles.json", "r"))
    profile_index = profile_exists(username)
    if profile_index > -1:
        if profile_data[profile_index]["logged-in"] == False:
            return {"error": "Nejste přihlášeni"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    if profile_exists(friend) > -1:
        if friend not in profile_data[profile_index]["friends"]:
            profile_data[profile_index]["friends"].append(friend)
            for user in profile_data:
                if user["username"] == friend:
                    user["friends"].append(username)
                    break
            json.dump(profile_data, open("profiles.json", "w"),indent=4)
            return {"success": "Přítel byl úspěšně přidán"}
        else:
            return {"error": "Uživatel již je ve vašich přátelích"}
    else:
        return {"error": "Uživatelské jméno přítele neexistuje"}
    
@app.get("/profile/remove-friend/{username}/{friend}") # odstranění přítele
def read_root(username: str, friend: str):
    profile_data = json.load(open("profiles.json", "r"))
    profile_index = profile_exists(username)
    if profile_index > -1:
        if profile_data[profile_index]["logged-in"] == False:
            return {"error": "Nejste přihlášeni"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    if profile_exists(friend) > -1 and friend in profile_data[profile_index]["friends"]:
        profile_data[profile_index]["friends"].remove(friend)
        json.dump(profile_data, open("profiles.json", "w"),indent=4)
        return {"success": "Přítel byl úspěšně odstraněn"}
    else:
        return {"error": "Uživatel není ve vašich přátelích"}
    
@app.post("/profile/change-profile-picture") # změna profilového obrázku
def change_profile_picture(request: ProfilePicture):
    username = request.username
    file = request.file
    filetype = request.filetype
    profile_data: list[dict] = json.load(open("profiles.json", "r"))
    profile_index = profile_exists(username)
    if profile_index > -1:
        if profile_data[profile_index]["logged-in"] == False:
            return {"error": "Nejste přihlášeni"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    if filetype not in [".png", ".jpg", ".jpeg"]:
        return {"error": "Neplatný typ souboru"}
    
    file_bytes = bytes(file) # převod na bytes
    # uložení souboru z bytes do složky profile-images
    with open(f"profile-images/{username + filetype}", "wb") as f:
        f.write(file_bytes)
    profile_data[profile_index]["profile_picture"] = username + filetype
    json.dump(profile_data, open("profiles.json", "w"),indent=4)
    return {"success": "Profilový obrázek byl úspěšně změněn"}

@app.get("/profile/update_progress/{username}/{xp}/{level}") # aktualizace postupu uživatele
def read_root(username: str, xp: int, level: int):
    profile_data = json.load(open("profiles.json", "r"))
    profile_index = profile_exists(username)
    if profile_index > -1:
        if profile_data[profile_index]["logged-in"] == False:
            return {"error": "Nejste přihlášeni"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    profile_data[profile_index]["xp"] = xp
    profile_data[profile_index]["level"] = level
    json.dump(profile_data, open("profiles.json", "w"),indent=4)
    return {"success": "Postup byl úspěšně aktualizován"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)

# spustit příkazem: uvicorn main:app (--reload: pro automatické reloadování) (--host=: pro přístup z jiného zařízení) (--port=8000: pro změnu portu)