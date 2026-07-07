from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional, Union
from backend.src.utils.enum import Categoria, StatusEnum
from pydantic import ConfigDict
from backend.src.utils.validations import normalize_intencao_value


class LeadValidation(BaseModel):
    """
    Schema Pydantic para validação e normalização de dados de entrada de Leads.

    Utilizado para interceptar requisições de interações de chat, garantindo que
    as propriedades obrigatórias existam e que os campos opcionais recebam seus
    valores padrão adequados. Possui suporte para conversão direta de objetos ORM.

    Attributes:
        name (str, optional): Nome de exibição do Lead.
        conversa_id (int): ID identificador do fluxo de conversão.
        numero_lead (str): Identificador (ex: telefone) do lead.
        numero_user (str): Identificador (ex: telefone) do usuário atendente.
        categoria (str, optional): Classificação do lead. Padrão: Categoria.MEDIA.
        status (StatusEnum, optional): Status atual do lead. Padrão: StatusEnum.PENDENTE.
        resumo_conversa (str, optional): Sumário do histórico recente do chat.
        intencao (str | list[str], optional): Intenções identificadas. Passa por normalização.
        data_hora_servico (date, optional): Data relacionada ao serviço prestado.
        satisfacao (int, optional): Nota de satisfação atribuída à interação.
    """

    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    conversa_id: int
    numero_lead: str
    numero_user: str
    categoria: Optional[str] = Categoria.BAIXA
    status: Optional[StatusEnum] = StatusEnum.PENDENTE
    resumo_conversa: Optional[str] = None
    intencao: Optional[Union[str, list[str]]] = None
    data_hora_servico: Optional[date] = None
    satisfacao: Optional[int] = None

    @field_validator("intencao", mode="before")
    @classmethod
    def normalize_intencao(cls, value):
        """
        Interfere no ciclo de validação para normalizar o formato da intenção informada.

        Garante consistência caso os dados cheguem mal formatados ou mistos.
        """
        return normalize_intencao_value(value)
