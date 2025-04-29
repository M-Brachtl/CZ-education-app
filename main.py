from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import UploadFile, File, Form
import json
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

def profile_exists(username: str) -> bool:
    try:
        data = json.load(open("docs/profile/users.json", "r"))
        for user in data:
            if user["username"] == username:
                return True
        return False
    except FileNotFoundError:
        return False

# testování NLP funkcí
@app.get("/test/test.html", response_class=HTMLResponse)
def read_root():
    return open("test.html", "r").read()
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
    profile_data = json.load(open("docs/profile/users.json", "r"))
    if profile_exists(username):
        if profile_data[username]["password"] == password:
            profile_data[username]["logged-in"] = True
            return profile_data[username]
        else:
            return {"error": "Špatné heslo"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
@app.get("/profile/register/{username}/{password}") # registrace uživatele
def read_root(username: str, password: str):
    profile_data: list[dict] = json.load(open("docs/profile/users.json", "r"))
    if profile_exists(username):
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
        json.dump(profile_data, open("docs/profile/users.json", "w"))
        return {"success": "Uživatelské jméno bylo úspěšně vytvořeno"}
@app.get("/profile/add-friend/{username}/{friend}") # přidat přítele
def read_root(username: str, friend: str):
    profile_data: list[dict] = json.load(open("docs/profile/users.json", "r"))
    if profile_exists(username):
        if profile_data[username]["logged-in"] == False:
            return {"error": "Nejste přihlášeni"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    if profile_exists(friend):
        if friend not in profile_data[username]["friends"]:
            profile_data[username]["friends"].append(friend)
            json.dump(profile_data, open("docs/profile/users.json", "w"))
            return {"success": "Přítel byl úspěšně přidán"}
        else:
            return {"error": "Uživatel již je ve vašich přátelích"}
    else:
        return {"error": "Uživatelské jméno přítele neexistuje"}
@app.get("/profile/remove-friend/{username}/{friend}") # odstranění přítele
def read_root(username: str, friend: str):
    profile_data: list[dict] = json.load(open("docs/profile/users.json", "r"))
    if profile_exists(username):
        if profile_data[username]["logged-in"] == False:
            return {"error": "Nejste přihlášeni"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    if profile_exists(friend) and friend in profile_data[username]["friends"]:
        profile_data[username]["friends"].remove(friend)
        json.dump(profile_data, open("docs/profile/users.json", "w"))
        return {"success": "Přítel byl úspěšně odstraněn"}
    else:
        return {"error": "Uživatel není ve vašich přátelích"}
@app.post("/profile/change-profile-picture") # změna profilového obrázku
def change_profile_picture(username: str = Form(...), file: UploadFile = File(...)):
    profile_data: list[dict] = json.load(open("docs/profile/users.json", "r"))
    if profile_exists(username):
        if profile_data[username]["logged-in"] == False:
            return {"error": "Nejste přihlášeni"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        return {"error": "Neplatný formát souboru"}
    # file ending in f string
    file.filename = f"{username}.{file.content_type.split('/')[1]}"
    with open(f"docs/profile/images/{file.filename}", "wb") as f:
        f.write(file.file.read())
    profile_data[username]["profile_picture"] = file.filename
    json.dump(profile_data, open("docs/profile/users.json", "w"))
    return {"success": "Profilový obrázek byl úspěšně změněn"}
@app.get("/profile/update_progress/{username}/{xp}/{level}") # aktualizace postupu uživatele
def read_root(username: str, xp: int, level: int):
    profile_data: list[dict] = json.load(open("docs/profile/users.json", "r"))
    if profile_exists(username):
        if profile_data[username]["logged-in"] == False:
            return {"error": "Nejste přihlášeni"}
    else:
        return {"error": "Uživatelské jméno neexistuje"}
    profile_data[username]["xp"] = xp
    profile_data[username]["level"] = level
    json.dump(profile_data, open("docs/profile/users.json", "w"))
    return {"success": "Postup byl úspěšně aktualizován"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)

# spustit příkazem: uvicorn main:app (--reload: pro automatické reloadování) (--host=: pro přístup z jiného zařízení) (--port=8000: pro změnu portu)