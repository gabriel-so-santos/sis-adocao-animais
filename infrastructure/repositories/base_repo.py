from abc import ABC
from typing import Any
from sqlalchemy.exc import IntegrityError

class BaseRepository(ABC):
    """
    Classe base abstrata para repositórios que utilizam SQLAlchemy.

    Esta classe define um contrato padrão para a implementação de repositórios
    responsáveis pela persistência de entidades de domínio. Ela fornece métodos
    CRUD básicos e conversões genéricas entre modelos SQLAlchemy e
    entidades de domínio. Subclasses que exigem conversões específicas ou comportamentos adicionais
    devem sobrescrever os métodos apropriados para garantir a correta
    equivalência entre modelo persistido e entidade de domínio.

    Por padrão, assume-se que o modelo e a entidade de domínio possuem atributos
    com os mesmos nomes e tipos diretamente compatíveis, não sendo necessária
    lógica adicional de conversão.

    Os métodos devem ser sobrescritos em subclasses quando houver:
        - conversão de enums ou value objects
        - aplicação de regras de negócio na criação da entidade
        - composição ou agregação de objetos
        - comportamentos e/ou argumentos específicos
        - tratamento específico de relacionamentos

    Attributes:
        session (Session): Instância da sessão SQLAlchemy utilizada para operações no banco de dados.
        model_class (type): Classe do modelo SQLAlchemy gerenciado pelo repositório.
        domain_class (type): Classe da entidade de domínio correspondente ao modelo.
    """

    domain_class = None
    
    def __init__(self, session, model_class):
        self.session = session
        self.model_class = model_class
        
    # -------------------------- STANDART MAPPING --------------------------

    def _to_domain(self, model_obj: Any) -> Any | None:
        """
        Converte um modelo SQLAlchemy em uma entidade de domínio utilizando
        mapeamento automático baseado em atributos públicos.

        Este é o comportamento padrão do repositório e pode ser sobrescrito em
        subclasses quando houver:
            - conversão de enums ou value objects
            - aplicação de regras de negócio na criação da entidade
            - composição ou agregação de objetos
            - comportamentos e/ou argumentos específicos
            - tratamento específico de relacionamentos

        Este método pressupõe que o construtor da entidade de domínio aceite
        apenas atributos públicos presentes no modelo SQLAlchemy.

        Args:
            model_obj (Any): Instância do modelo SQLAlchemy persistido no banco
            de dados.

        Returns:
            Any | None: Entidade de domínio correspondente ao modelo informado
            ou None, caso o modelo seja None.
        """
        if model_obj is None:
            return None

        data_args = {
            column.name: getattr(model_obj, column.name)
            for column in model_obj.__table__.columns
        }
        return self.domain_class(**data_args)

    def _to_model(self, domain_obj: Any) -> Any | None:
        """
        Converte uma entidade de domínio em um modelo SQLAlchemy utilizando
        mapeamento automático baseado em atributos públicos.

        Este é o comportamento padrão do repositório e pode ser sobrescrito em
        subclasses quando houver:
            - conversão de enums ou value objects
            - aplicação de regras de negócio na criação da entidade
            - composição ou agregação de objetos
            - comportamentos e/ou argumentos específicos
            - tratamento específico de relacionamentos

        Args:
            domain_obj (Any): Entidade de domínio a ser convertida em modelo persistente.

        Returns:
            Any | None: Instância do modelo SQLAlchemy pronta para ser
                persistida ou None, caso a entidade seja nula.
        """
        if domain_obj is None:
            return None

        data_args = {
            column.name: getattr(domain_obj, column.name)
            for column in self.model_class.__table__.columns
            if hasattr(domain_obj, column.name)
        }
        return self.model_class(**data_args)

    # -------------------------- CRUD --------------------------

    # ---- Create ----
    def save(self, domain_obj) -> bool:
        """
        Insere uma nova entidade no banco de dados.

        Converte a entidade de domínio em um modelo SQLAlchemy, persiste o
        registro no banco de dados e confirma a transação. Caso ocorra um erro
        de integridade do banco (IntegrityError), como violação de chave e/ou atributos únicos,
        a operação será revertida (rollback).

        Args:
            domain_obj (Any): Entidade de domínio a ser persistida.


        Returns:
            bool: True se a operação for bem-sucedida;
            False caso ocorra um erro de integridade durante a persistência.
        """
        try:
            model_obj = self._to_model(domain_obj)
            self.session.add(model_obj)
            self.session.commit()
            self.session.refresh(model_obj)
            return True
        except IntegrityError:
            self.session.rollback()
            return False
          
    # ---- Read ----
    def list_all(self) -> list:
        """
        Retorna todos os registros pertencentes ao modelo gerenciado.

        Recupera todos os modelos do banco de dados e converte cada um deles
        para sua respectiva entidade de domínio.

        Returns:
            list[Any]: Lista contendo todas as entidades de domínio encontradas.
        """
        models = self.session.query(self.model_class).all()

        return [self._to_domain(model_obj) for model_obj in models]

    def get_by(self, id: int) -> Any | None:
        """
        Obtém um único registro com base no seu identificador único.

        Busca o modelo correspondente no banco e, caso encontrado, converte-o
        para uma entidade de domínio.

        Este método deve ser sobrescrito em entidades que não possuem
        chaves únicas próprias (entidades fracas) ou para adição de filtros adicionais.

        Args:
            id (int): Identificador único do registro desejado.

        Returns:
            (Any | None): Entidade de domínio se encontrada; caso contrário, None.
        """
        model_obj = self.session.get(self.model_class, id)

        if not model_obj:
            return None

        return self._to_domain(model_obj)

    # ---- Update ----
    def update(self, domain_obj) -> bool:
        """
        Atualiza um registro existente no banco de dados.

        Converte a entidade de domínio em um modelo SQLAlchemy e realiza
        a operação de merge, garantindo que os dados sejam atualizados de forma
        transacional.

        Args:
            domain_obj (Any): Entidade de domínio contendo os dados atualizados.

        Returns:
            bool: True se a atualização for concluída com sucesso;
            False caso o modelo não possa ser processado.
        """
        model_obj = self._to_model(domain_obj)

        if not model_obj:
            return False

        updated_obj = self.session.merge(model_obj)
        self.session.commit()
        self.session.refresh(updated_obj)
        return True

    # ---- Delete ----
    def delete_by(self, id: int) -> bool:
        """
        Remove um registro do banco com base no seu identificador.

        A operação remove o modelo correspondente e confirma a transação.
        Caso o registro não exista, nenhuma modificação é realizada.

        Este método deve ser sobrescrito em entidades que não possuem
        chaves únicas próprias (entidades fracas) ou para adição de filtros adicionais.

        Args:
            id (int): Identificador único do registro a ser removido.

        Returns:
            bool: True se a remoção for realizada; False se o registro não existir.
        """
        model_obj = self.session.get(self.model_class, id)
        if not model_obj:
            return False

        self.session.delete(model_obj)
        self.session.commit()
        return True