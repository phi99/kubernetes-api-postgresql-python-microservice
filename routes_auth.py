from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import db_sqlalchemy, model_schemas, db_models, tools, auth_token
from typing_extensions import Annotated

router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=model_schemas.Token)
async def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(db_sqlalchemy.get_db)):
    user=db.query(db_models.User).filter(db_models.User.username==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not tools.passwcheck(user_credentials.password,user.passw):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token=auth_token.create_access_token(data={"user_id":user.id})
    return {"access_token" : access_token, "token_type":"bearer"}
