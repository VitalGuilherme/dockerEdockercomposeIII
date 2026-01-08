from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./tarefa.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

MY_USERNAME = "admin"
MY_PASSWORD = "admin"

security = HTTPBasic()

class TarefaDB(Base):
    __tablename__="tarefa"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)


class Tarefa(BaseModel):
    #id: int
    nome: str
    descricao: str

listar_tarefas = []

Base.metadata.create_all(bind=engine)

def autenticar_my_username(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MY_USERNAME)
    is_password_correct = secrets.compare_digest(credentials.password, MY_PASSWORD)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário e senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )
    
def listar(listar_tarefas, order_by='nome', direction='asc'):
    reverse = (direction == 'desc')
    return sorted(listar_tarefas,key=lambda tarefa: getattr(tarefa, order_by), reverse=reverse)


@app.get("/tarefa")
def get_tarefas(page: int = 1, limit: int = 5, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_my_username)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit inválidos.")
    
    tarefa = db.query(TarefaDB).offset((page - 1) * limit).limit(limit).all()
    
    if not tarefa:
        return {"message": "Não existe nenhuma tarefa registrada."}
    
    #ordenar_tarefas = listar(listar_tarefas, order_by='nome', direction='asc')


    #start = (page - 1) * limit
    #end = start + limit

    #tarefas_paginadas = ordenar_tarefas[start:end]

    total_tarefas = db.query(TarefaDB).count()

    return {
        "page": page,
        "limit": limit,
        "total": (total_tarefas),
        "tarefas": [{"id": tarefa.id, "nome": tarefa.nome, "descricao": tarefa.descricao} for tarefa in tarefa]
    }


@app.post("/tarefa", status_code=201)
def add_tarefas(tarefa: Tarefa, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_my_username)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome == tarefa.nome, TarefaDB.descricao == tarefa.descricao).first()
    #for t in listar_tarefas:
    #    if t.nome == tarefa.nome:
    if db_tarefa:
        raise HTTPException(status_code=400, detail= "Essa tarefa já foi registrada.")

    nova_tarefa = TarefaDB(nome=tarefa.nome, descricao=tarefa.descricao)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    #listar_tarefas.append(tarefa)
    return {"message": "Tarefa adicionada com sucesso!"}

#@app.put("/tarefa/atualizar/{nome}")
@app.put("/tarefa/atualizar/{id}")
def atualizar_tarefa(id: int, nova_tarefa: Tarefa, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_my_username)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id == id).first()
    if not db_tarefa:
#    for atu, tarefa in enumerate(listar_tarefas):
#        if tarefa.nome == nome:
#            listar_tarefas[atu] = nova_tarefa
#            return {"message": f"Tarefa '{nome}' concluída com sucesso.", "Tarefa": nova_tarefa}
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    db_tarefa.nome = nova_tarefa.nome
    db_tarefa.descricao = nova_tarefa.descricao
    db.commit()
    db.refresh(db_tarefa)

    return {"message": "Tarefa atualizado com sucesso!"}


@app.delete("/tarefa/{id}")
def remover_tarefa(id: int, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_my_username)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id == id).first()
    if not db_tarefa:
    #for tarefa in listar_tarefas:
    #    if tarefa.nome == nome:
    #        listar_tarefas.remove(tarefa)
    #        return {"message": "Tarefa removida com sucesso"}
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(db_tarefa)
    db.commit()
    return {"message": "Tarefa deletado com sucesso!"}
