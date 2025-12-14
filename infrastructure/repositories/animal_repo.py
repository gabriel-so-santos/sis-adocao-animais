import json

from .base_repo import BaseRepository
from typing import override

from domain.animals.animal import Species, Gender, Size
from domain.animals.animal_status import AnimalStatus

from infrastructure.db_models.animal_model import AnimalModel
from domain.animals.cat import Cat
from domain.animals.dog import Dog

from domain.exceptions import InvalidStatusTransitionError

class AnimalRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session, AnimalModel)

    @override
    def _to_domain(self, animal_model: AnimalModel) -> Cat | Dog:
        """
        Converte um objeto AnimalModel (SQLAlchemy) em uma entidade de domínio
        correspondente (Cat ou Dog).

        Args:
            animal_model (AnimalModel): Instância do modelo persistido no banco.

        Returns:
            animal (Cat | Dog): Entidade de domínio reconstruída a partir dos dados
            armazenados no banco de dados.
        """
        
        species = Species[animal_model.species]         
        extra_data = animal_model.extra_data or {}

        common_args = dict(
            id=animal_model.id,
            species=species,                            # Enum
            breed=animal_model.breed,
            name=animal_model.name,
            gender=Gender[animal_model.gender],         # Enum
            age_months=animal_model.age_months,
            size=Size[animal_model.size],               # Enum
            temperament=json.loads(animal_model.temperament),
            status=AnimalStatus[animal_model.status],   # Enum
            timestamp=animal_model.timestamp,
        )

        if species == Species.CAT:   
            animal = Cat(
                **common_args,
                is_hypoallergenic=extra_data.get("is_hypoallergenic", False)
            )
        else:
            animal = Dog(
                **common_args,
                needs_walk=extra_data.get("needs_walk", False)
            )
        return animal
    
    @override
    def _to_model(self, animal: Cat | Dog) -> AnimalModel:
        """
        Converte uma entidade de domínio (Cat ou Dog) em um objeto AnimalModel
        para persistência no banco de dados.

        Args:
            animal (Cat | Dog): Entidade de domínio contendo os dados
            a serem convertidos.

        Returns:
            AnimalModel: Instância correspondente ao modelo de dados pronto
            para inserção ou atualização no banco.
        """
        extra_data = {}

        if isinstance(animal, Dog):
            extra_data["needs_walk"] = animal.needs_walk

        if isinstance(animal, Cat):
            extra_data["is_hypoallergenic"] = animal.is_hypoallergenic

        animal_model = AnimalModel(
            id=animal.id, 
            species=animal.species.value,               # Enum
            breed=animal.breed,
            name=animal.name,
            gender=animal.gender.value,                 # Enum   
            age_months=animal.age_months,
            size=animal.size.value,                     # Enum       
            temperament=json.dumps(animal.temperament),   
            status=animal.status.value,                 # Enum
            timestamp = animal.timestamp,

            extra_data=extra_data
        )
        return animal_model
    
    def list_reservable_animals(self) -> list[Cat | Dog]:
        """
        Retorna todos os animais que podem participar do processo de reserva,
        ou seja, aqueles com status AVAILABLE ou RESERVED.
        """
        reservable = [
            AnimalStatus.AVAILABLE.value,
            AnimalStatus.RESERVED.value,
        ]
        models = self.session.query(AnimalModel).filter(AnimalModel.status.in_(reservable)).all()

        return [self._to_domain(model) for model in models]
    
    @override  
    def update(self, animal: Cat | Dog) -> bool:
        """
        Atualiza um registro existente no banco com base nos dados
        fornecidos pela entidade de domínio (com execeção do stuatus do animal).

        Args:
            animal (Cat | Dog): Entidade contendo os dados atualizados.

        Returns:
            bool: True se a atualização foi bem-sucedida, False se o registro não existir.
        """
        animal_model = self._to_model(animal)

        if not animal_model:
            return False
        
        animal_model.breed = animal.breed
        animal_model.name = animal.name
        animal_model.gender = animal.gender.value
        animal_model.age_months = animal.age_months
        animal_model.size = animal.size.value
        animal_model.temperament = json.dumps(animal.temperament)

        self.session.commit()
        self.session.refresh(animal_model)
        return True

    def update_status(self, id: int, new_status: AnimalStatus) -> None:
        """
        Atualiza apenas o status de um animal, garantindo que a transição de estado
        seja válida conforme as regras definidas em AnimalStatus.

        Args:
            id (int): Identificador do animal.
            new_status (AnimalStatus): Novo status a ser aplicado.

        Raises:
            InvalidStatusTransitionError: Caso a transição seja inválida.
        """
        animal_model = self.session.get(AnimalModel, id)

        current = AnimalStatus[animal_model.status]

        if AnimalStatus.is_valid_transition(current, new_status):
            animal_model.status = new_status.value

        else:
            raise InvalidStatusTransitionError(f"Transição inválida! {current} -> {new_status}")