import os, secrets, random
from datetime import timedelta, datetime
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from jose import JWTError, jwt
from passlib.context import CryptContext
from authflowapp import runner, templates
from authflowapp.models import User, ALGORITHM
from authflowapp.database import get_db
from passlib.context import CryptContext
from authflowapp.config import SECRET_KEY
from pydantic import BaseModel


router = APIRouter()
csrf_protect = CsrfProtect()

#  --  C L A S S E S  --

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class CsrfSettings(BaseModel):
    secret_key: str = SECRET_KEY

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
expiration_time = datetime.utcnow() + timedelta(minutes=15)
token = jwt.encode({'exp': expiration_time, 'sub': 'user_id'}, 'secret_key', algorithm='HS256')


#  --  B A S E   F U N C T I O N S  --

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validateMail(email):
    email_pattern = r"^\S+@\S+\.\S+$"
    if not re.match(email_pattern, email):
        return ["Please enter a valid email address"]

    else:
        return [""] 

def validatePasswordMatch(x, y):
    if x != y:
            return ["The passwords must match!", "danger"]
    else:
        return [""]

def generate_password_hash(password):
    return crypt_context.hash(password)

def check_password_hash(hashed_password, plain_password):
    return crypt_context.verify(plain_password, hashed_password)

def decode_token(token):
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None

blacklist = set()

def is_token_blacklisted(token):
    return token in blacklist

def blacklist_token(token):
    blacklist.add(token)


@runner.get("/set-cookie")
def set_cookie(response: Response):
    access_token = "authflow" 
    response.set_cookie(
        key="auth_token",
        value=access_token,
        max_age=0,
        httponly=True,
    )
    return {"message": "Cookie set successfully"}


#  --  R O U T E S  --

@runner.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "AuthFlow"})

@runner.route("/register", methods=["GET", "POST"])
async def register(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    referer = request.headers.get("Referer")
    if request.method == "POST":
        fname = form_data.get("fname")
        lname = form_data.get("lname")
        mail = form_data.get("mail")
        pwd = form_data.get("pwd")
        cpwd = form_data.get("cpwd")
        hashedpwd = generate_password_hash(pwd)
        csrf_protect.verify_csrf_token(request)
        userDeets = db.query(User).filter(User.user_email == mail).first()
        if fname != "" and lname != "" and mail != "" and pwd != "":
            if not validateMail(mail) and validatePasswordMatch(pwd, cpwd):
                return {"referer": referer}
            if userDetails:
                messages = ["This email is taken! Use another email instead.", "warning"]
                return {"referer": referer}
            else:
                new_user = User(user_fname = fname, user_lname = lname, user_email = mail, user_password = hashedpwd, confirmation_token = confirmation_token,)         
                db.session.add(new_user)
                db.session.commit()
                userId = new_user.user_id
                request.session["user"] = userId
                send_confirmation_email_task.apply_async(args=[mail, fname, confirmation_token])
                messages = [(f"Account created for you, {fname}! Please proceed to LOGIN ", "success")]
                return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        else:
            messages = ["Kindly fill all fields", "alert"]
            return {"referer": referer}
    else:
        return templates.TemplateResponse("register.html", {"request": request, "messages": messages})
    
@runner.route("/login", methods=["GET", "POST"])
async def login(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    referer = request.headers.get("Referer")
    mail = form_data.get("mail")
    pwd = form_data.get("pwd")
    if request.method == "POST":
        csrf_protect.verify_csrf_token(request)
        userDeets = db.query(User).filter(User.user_email == mail).first()
        pwdInDb = userDetails.user_password
        if check_password_hash(pwdInDb, pwd):
            userId = userDetails.user_id
            request.session["user"] = userId
            message = [(f"Welcome back, {userDetails.user_fname}")]
            response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(
                key="auth_token",
                value=access_token,
                max_age=1800,  # Set an appropriate expiration time
                httponly=True,
            )
            return response
        else:
            message = ["Incorrect username or password"]
            return {"referer": referer}
    else:
        return templates.TemplateResponse("login.html", {"request": request, "messages": messages})

@runner.route("/reset", methods=["GET", "POST"])
async def reset(request: Request):
    pass
    return templates.TemplateResponse("reset.html", {"request": request})

@runner.route("/confirm-registration", methods = (["POST", "GET"]))
def confirm(request: Request, db: Session = Depends(get_db)):
    user = User.query.filter_by(confirmation_token=token).first()
    if user and not user.confirmed:
        user.confirmed = True
        user.confirmation_token = None
        db.session.commit()
        message=["Your registration has been confirmed. You can now log in.", "success"]
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    elif user.confirmed:
        message = ["Your account is already confirmed. Please log in.", "info"]
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    else:
        abort(404)
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)



@runner.get("/logout", response_class=HTMLResponse)
def logout(request: Request, response: Response):
    del request.session["user"]
    response.delete_cookie("auth_token")  # Specify the cookie name you want to delete
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
