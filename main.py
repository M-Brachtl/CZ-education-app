from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import nlp # import the nlp.py file


app = FastAPI()

app.mount("/page", StaticFiles(directory="docs", html=True), name="static")

@app.get("/")
def read_root(input_sentence: str):
    print(input_sentence)
    return nlp.get_pos_sentence(input_sentence)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)