from fastapi import FastAPI, Body,  Form, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import SessionLocal, User
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPEN_API_KEY")
) 
app = FastAPI()
app.mount("/static", StaticFiles(directory="public"), name="static")
app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")




@app.get("/")
def root():
    return FileResponse("public/index.html")


@app.get("/mainpage")
def signup():
    return FileResponse("public/mainpage.html")


def get_db():      
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/hello")
def hello(name = Body(embed=True), email = Body(embed=True), password = Body(embed=True), confirm_password= Body(embed=True), db: Session = Depends(get_db)):
    print(name, email)
    
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Пароли не совпадают!")
    
    existing_user = db.query(User).filter(User.username == name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Такой Email уже существует")

    
    new_user = User(username=name,email = email, password = password, )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Регистрация успешна!"}


@app.post("/login")
def login(email = Body(embed=True), password = Body(embed=True), db: Session = Depends(get_db)):
    print(email, password)

   
    user = db.query(User).filter(User.email == email).first()

    
    if not user:
        raise HTTPException(status_code=400, detail="Неправильный email или пароль")

    
    if user.password != password:
        raise HTTPException(status_code=400, detail="Неправильный email или пароль")

    return {"message": "Вы успешно вошли в аккаунт!"}



@app.post("/response")
async def response(userMessage= Body(embed=True)):
    the_response_from_ai = await ai_integration(userMessage)
    print(the_response_from_ai)
    return {"response": the_response_from_ai}


    

async def ai_integration(ai_response):
    if ai_response.lower() == "привет":
        return "**Привет!** 👋\n\nЯ твой AI-репетитор. Напиши, какой курс хочешь пройти. Например:\n\n- Python\n- Веб-разработка\n- Математика"
    else:
        return "🔍 *Я пока не знаю, что это значит, но скоро научусь!*"

    
    
    

async def ai_integrations(ai_response):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system","content":"You are kind helpful assintant"}, 
        
        {
            "role":"user",
            "content": f"{ai_response}"
        }
    ]
)

    return completion.choices[0].message.content
    print("саксесс")