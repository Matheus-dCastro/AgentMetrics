from fastapi import APIRouter, Depends, HTTPException, dependencies
from sqlalchemy.orm import Session
from backend.src.leads.schemas import LeadValidation
from backend.src.leads.model import LeadDB
from backend.src.users.model import UserDB
from backend.src.leads.model import UserLeadAssociation
from backend.src.users.model import MetricasLeadInUser
from datetime import datetime
from backend.src.core.database import get_db
from backend.src.utils.validations import get_record, result_check, insert_db
import backend.src.utils.validations


def split_intencao(value):
    """ teste de commit
    Normaliza e limpa o valor da intenção, convertendo strings ou listas em um array limpo.

    Args:
        value (str | list | None): Valor bruto contendo as intenções.

    Returns:
        list[str]: Lista contendo strings limpas de espaços em branco.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if item is not None and str(item).strip()
        ]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    raise ValueError("intencao deve ser uma string ou lista de strings")


def validate_lead_intencao(existing_user, data_lead):
    """
    Valida se as intenções solicitadas pelo lead são permitidas para o usuário atribuído.

    Raises:
        HTTPException: Erro 400 se houver intenções inválidas em relação às permitidas no perfil.
    """
    if existing_user.intencao is None or data_lead.intencao is None:
        return

    allowed = [item.upper() for item in split_intencao(existing_user.intencao)]
    requested = [item for item in split_intencao(data_lead.intencao)]
    invalid = [item for item in requested if item.upper() not in allowed]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Intenção inválida para este usuário: {invalid}. Permitidas: {allowed}.",
        )


def modulo_lead(existing_user, existing_lead, data_lead):
    """
    Instancia e preenche o modelo de associação contendo os metadados do atendimento do lead.
    """
    validate_lead_intencao(existing_user, data_lead)
    intent_value = data_lead.intencao or existing_user.intencao

    return UserLeadAssociation(
        conversa_id=data_lead.conversa_id,
        user_id=existing_user.id,
        lead_id=existing_lead.id,
        lead_name=data_lead.name,
        lead_number=data_lead.numero_lead,
        categoria=data_lead.categoria,
        status=(data_lead.status.value if data_lead.status else None),
        fechado=False,
        resumo_conversa=data_lead.resumo_conversa,
        intencao=intent_value,
        data_hora_servico=data_lead.data_hora_servico,
        satisfacao=data_lead.satisfacao,
    )


def new_lead(data_lead: LeadValidation, db: Session = Depends(get_db)):
    """
    Cria um registro inédito de Lead e inicia sua primeira associação de conversa.
    """
    existing_user = get_record(db, UserDB, {"numero": data_lead.numero_user}, True)
    result_check(existing_user, "User não encontrado.", 404, False)

    new_lead_obj = LeadDB(
        name=data_lead.name,
        numero=data_lead.numero_lead,
        type="lead",
    )
    association = modulo_lead(existing_user, new_lead_obj, data_lead)

    new_lead_obj.associations.append(association)

    insert_db(db, new_lead_obj, True)
    return {
        "message": "Novo Cliente criado com sucesso",
        "cliente_id": new_lead_obj.id,
        "Status": association.status,
    }, aggregate_metricas(db)


def validation_lead_user(user, lead, db: Session, data_lead):
    """
    Busca se já existe um pareamento ativo de conversa para o trio específico (User, Lead, Conversa).
    """
    return (
        db.query(UserLeadAssociation)
        .filter(
            UserLeadAssociation.lead_id == lead.id,
            UserLeadAssociation.user_id == user.id,
            UserLeadAssociation.conversa_id == data_lead.conversa_id,
        )
        .first()
    )


def lead_update(data_lead, db: Session, user, lead):
    """
    Modifica os metadados de uma interação pré-existente e atualiza os contadores operacionais.
    """
    try:
        association = validation_lead_user(user, lead, db, data_lead)

        if association:
            validate_lead_intencao(user, data_lead)
            association.categoria = data_lead.categoria
            if data_lead.status.value == "FECHADO":
                association.fechado = True
            else:
                association.status = (
                    data_lead.status.value if data_lead.status else None
                )
            association.resumo_conversa = data_lead.resumo_conversa
            if data_lead.intencao is not None:
                association.intencao = data_lead.intencao
            association.satisfacao = data_lead.satisfacao

            db.commit()
            db.refresh(association)

            return {
                "message": "Pareamento atualizado com sucesso",
                "lead_id": lead.id,
                "usuario_vinculado": user.id,
                "Status": association.status,
            }, aggregate_metricas(db)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def aggregate_metrics_for_user(user: UserDB, db: Session):
    """
    Calcula, consolida e persiste as métricas de performance de atendimento de um usuário único.
    """
    associations = (
        db.query(UserLeadAssociation)
        .filter(UserLeadAssociation.user_id == user.id)
        .all()
    )

    total_leads = len(associations)
    pendentes = sum(1 for a in associations if a.status == "PENDENTE")
    aberto = sum(1 for a in associations if a.status == "ABERTO")
    leads_fechados = sum(1 for a in associations if a.fechado == True)

    satisfacoes = [a.satisfacao for a in associations if a.satisfacao is not None]
    avg_satisfacao = float(sum(satisfacoes) / len(satisfacoes)) if satisfacoes else None
    avg_response_time = None

    metric = (
        db.query(MetricasLeadInUser)
        .filter(MetricasLeadInUser.user_id == user.id)
        .first()
    )

    if metric:
        metric.total_leads = total_leads
        metric.leads_pendentes = pendentes
        metric.leads_abertos = aberto
        metric.leads_fechados = leads_fechados
        metric.avg_satisfacao = avg_satisfacao
        metric.avg_response_time = avg_response_time
        metric.last_aggregated = datetime.utcnow()
    else:
        metric = MetricasLeadInUser(
            user_id=user.id,
            total_leads=total_leads,
            leads_abertos=pendentes,
            leads_fechados=leads_fechados,
            avg_satisfacao=avg_satisfacao,
            avg_response_time=avg_response_time,
            last_aggregated=datetime.utcnow(),
        )
        db.add(metric)

    db.commit()
    db.refresh(metric)
    return metric


def aggregate_metricas(db: Session = Depends(get_db)):
    """
    Gera o relatório agregador macro de produtividade recalculando métricas para toda a base de usuários.
    """
    try:
        users = db.query(UserDB).all()
        results = []
        for u in users:
            m = aggregate_metrics_for_user(u, db)
            results.append(
                {
                    "user_id": u.id,
                    "total_leads": m.total_leads,
                    "leads_abertos": m.leads_abertos,
                    "leads_fechados": m.leads_fechados,
                    "avg_satisfacao": m.avg_satisfacao,
                    "last_aggregated": m.last_aggregated,
                }
            )
        return {"message": "Métricas agregadas com sucesso", "summary": results}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def edit_nome(data_lead, db: Session = Depends(get_db)):
    """
    Sincroniza e altera o nome cadastrado do lead caso haja divergências com os dados recebidos.
    """
    lead = get_record(db, LeadDB, {"numero": data_lead.numero_lead}, True)
    lead.name = data_lead.name
    db.commit()
    db.refresh(lead)
    return {"message": "Pareamento nome atualizado com sucesso", "User:": lead.id}
