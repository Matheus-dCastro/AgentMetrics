from dns import query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.src.core.database import get_db
from backend.src.core.security import (
    get_password_hash,
    verify_password,
    verificar_token,
)
from backend.src.leads.model import LeadDB
from backend.src.utils.schemas import user_lead_association
from backend.src.utils.validations import get_record, result_check, insert_db
from backend.src.users.model import UserDB
from backend.src.users.schemas import Creat_new_user, login_user, intenso
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from backend.src.core.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from fastapi.security import OAuth2PasswordRequestForm
from backend.src.leads.model import UserLeadAssociation
from backend.src.users.service import token, serialize_intencao

user_routers = APIRouter(prefix="/user", tags=["User"])


@user_routers.post("/register")
def add_new_user(user_data: Creat_new_user, db: Session = Depends(get_db)):
    """
    Cadastra um novo usuário atendente no sistema após validação de dados únicos.
    """
    existing_user = get_record(db, UserDB, {"email": user_data.email}, True)
    result_check(existing_user, "O email já está cadastrado.", 404)

    existing_user_numero = get_record(db, UserDB, {"numero": user_data.numero}, True)
    result_check(existing_user_numero, "O Número já está cadastrado.", 404)

    novo_user = UserDB(
        name=user_data.name,
        numero=user_data.numero,
        email=user_data.email,
        senha=get_password_hash(user_data.senha),
    )
    insert_db(db, novo_user, True)
    return {"message": "Sucesso", "user_id": novo_user.id}


@user_routers.post("/login")
async def login(login: login_user, db: Session = Depends(get_db)):
    """
    Autentica um usuário via payload JSON padrão e emite tokens de acesso e renovação.
    """
    user = get_record(db, UserDB, {"email": login.email}, True)
    result_check(user, "Senha ou Login errados", 400, False)

    if not verify_password(login.senha, user.senha):
        raise HTTPException(status_code=400, detail="Senha ou Login errados")

    access_token = token(user.id)
    refresh_token = token(user.id, timedelta(days=1))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "message": "Autenticação bem-sucedida",
    }


# @user_routers.post("/login-forms") # serve para ter o login na documentação interativa
# async def login_forms(
#     login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):
#     """
#     Autentica um usuário usando o formato de formulário padrão OAuth2 (utilizado pelo Swagger).
#     """
#     user = get_record(db, UserDB, {"email": login.username}, True)
#     result_check(user, "Senha ou Login errados", 400, False)

#     if not verify_password(login.password, user.senha):
#         raise HTTPException(status_code=400, detail="Senha ou Login errados")

#     access_token = token(user.id)
#     return {
#         "access_token": access_token,
#         "token_type": "Bearer",
#         "message": "Autenticação bem-sucedida",
#     }


@user_routers.get("/refresh")  # refatorar esse metodo para virar um def simples
async def use_refresh_token(user: UserDB = Depends(verificar_token)):
    """
    Gera e retorna um novo token de acesso válido a partir de uma sessão de usuário ativa.
    """
    acces_token = token(user.id)
    return {
        "access_token": acces_token,
        "token_type": "Bearer",
        "message": "Autenticação bem-sucedida",
    }


@user_routers.get("/list-leads")
async def list_leads(
    user: UserDB = Depends(verificar_token),
    db: Session = Depends(get_db),
):
    """
    Recupera e lista de forma serializada todas as interações e leads vinculados ao usuário autenticado.
    """
    user_login = (
        db.query(UserLeadAssociation)
        .filter(UserLeadAssociation.user_id == user.id)
        .all()
    )
    return [
        {
            "id": item.lead_id,
            "nome": item.lead_name,
            "numero": item.lead_number,
            "Status": item.status,
            "Fechada": item.fechado,
            "intencao": item.intencao,
            "satisfação": item.satisfacao,
            "resumo": item.resumo_conversa,
            "data": item.data_hora_servico,
        }
        for item in user_login
    ]


@user_routers.post("/intesao")
async def def_intesao(
    data_user: intenso,
    db: Session = Depends(get_db),
    user: UserDB = Depends(verificar_token),
):
    """
    Atualiza as intenções de segmentação de leads associadas ao perfil operacional do atendente.
    """
    user_intesao = get_record(db, UserDB, {"id": user.id}, True)

    if user_intesao:
        user_update = db.query(UserDB).filter(UserDB.id == user_intesao.id).first()
        if user_update:
            user_update.intencao = serialize_intencao(data_user.intencao)
            db.commit()
            db.refresh(user_intesao)

    return {
        "message": "Pareamento intensao atualizado com sucesso",
        "User:": user_intesao.id,
    }


# @user_routers.post("/novo-nome") # modelo de edição do user -> tem q passar para pedir o token
# def edit_nome(dados: edit_user, db: Session = Depends(get_db)):
#     user = get_record(db, UserDB, {"email": dados.email}, True)
#     if user:
#         user_update = db.query(UserDB).filter(UserDB.id == user.id).first()
#         if user_update:
#             user_update.nome = dados.nome
#             db.commit()
#             db.refresh(user)
#     return {
#         "message": "Pareamento nome atualizado com sucesso",
#         "User:": user.id,
#     }
