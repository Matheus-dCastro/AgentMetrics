from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
import backend.src.utils.models as models
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from backend.src.core.database import Base


class LeadDB(models.IdentityDB):
    """
    Modelo ORM que representa um Lead no sistema.

    Utiliza herança polimórfica baseada na tabela global de Identidades.
    Gerencia o relacionamento de muitos-para-muitos com os usuários (atendentes)
    tanto de forma direta quanto enriquecida através de metadados de associação.

    Attributes:
        id (int): Chave primária e estrangeira referenciando a tabela Identity.
        users (list[UserDB]): Lista de usuários associados diretamente ao lead.
        associations (list[UserLeadAssociation]): Lista contendo o histórico e metadados
            detalhados das conversões do lead.
    """

    __tablename__ = "Leads"

    id = Column("ID", Integer, ForeignKey("Identity.ID"), primary_key=True)

    users = relationship(
        "UserDB",
        secondary="user_lead_association",
        back_populates="clientes",
    )

    associations = relationship(
        "UserLeadAssociation",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    __mapper_args__ = {"polymorphic_identity": "lead"}


class UserLeadAssociation(Base):
    """
    Modelo ORM intermediário para a relação entre Usuários e Leads.

    Funciona como uma tabela de associação estendida que, além de unir as chaves
    estrangeiras de ambas as entidades, armazena informações cruciais sobre
    o atendimento/conversão realizada (histórico, satisfação, resumo, etc).

    Attributes:
        conversa_id (int): Identificador único e chave primária da conversão.
        lead_id (int): Chave estrangeira que aponta para o Lead correspondente.
        user_id (int): Chave estrangeira que aponta para o Usuário atendente.
        lead_name (str): Nome do lead capturado no atendimento.
        lead_number (str): Número telefônico ou identificador de contato do lead.
        status (str): Estado atual da conversão/atendimento.
        categoria (str): Classificação temática da interação.
        intencao (str): Objetivo ou intenção detectada no lead.
        satisfacao (int): Avaliação numérica de satisfação do atendimento.
        resumo_conversa (str): Texto descritivo sintetizando o diálogo.
        data_hora_servico (Date): Registro cronológico do serviço prestado.
        user (UserDB): Referência direta à instância do usuário associado.
        lead (LeadDB): Referência direta à instância do lead associado.
    """

    __tablename__ = "user_lead_association"

    conversa_id = Column("ID da conversao", Integer, primary_key=True)
    lead_id = Column("lead_id", Integer, ForeignKey("Leads.ID"))
    user_id = Column("user_id", Integer, ForeignKey("Users.ID"))

    lead_name = Column("lead_name", String)
    lead_number = Column("lead_number", String)

    status = Column("status", String)
    fechado = Column("fechado", Boolean)
    categoria = Column("categoria", String)
    intencao = Column("intencao", String)
    satisfacao = Column("satisfacao", Integer)
    resumo_conversa = Column("resumo_conversa", String)
    data_hora_servico = Column("data_hora_servico", Date)

    user = relationship("UserDB", back_populates="associations")
    lead = relationship("LeadDB", back_populates="associations")
