from datetime import date
from typing import Optional
from pydantic import BaseModel
from backend.src.utils.enum import StatusEnum


class user_lead_association(BaseModel):
    """
    Schema Pydantic representativo dos metadados de um acoplamento User-Lead.

    Utilizado principalmente para estruturar a resposta (output) do histórico de
    conversões e interações ativas de um atendente, abstraindo chaves estrangeiras complexas.

    Attributes:
        conversa_id (int): Identificador sequencial da conversão de chat.
        categoria (str, optional): Tag qualificadora de temperatura ou escopo do lead.
        status (StatusEnum, optional): Status do fluxo de atendimento. Padrão: StatusEnum.ABERTO.
        resumo_conversa (str, optional): Memorando ou síntese textual do atendimento.
        intencao (str, optional): Objetivo mapeado na mensagem do cliente.
        data_hora_servico (date, optional): Data civil de execução ou agendamento.
        satisfacao (int, optional): Métrica de avaliação de qualidade dada à conversa.
    """

    conversa_id: int
    categoria: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.ABERTO
    fechado: bool = False
    resumo_conversa: Optional[str] = None
    intencao: Optional[str] = None
    data_hora_servico: Optional[date] = None
    satisfacao: Optional[int] = None
