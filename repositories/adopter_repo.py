from models.adopter_model import AdopterModel
from domain.people.adopter import Adopter, HousingType
        

class AdopterRepository:
   
    def __init__(self, session):
        self.session = session
    
    def to_domain(self, adopter_model: AdopterModel) -> Adopter:
        """Converte o Model (SQL) em uma entidade de domínio"""
        
        return Adopter(
            id = adopter_model.id,
            name = adopter_model.name,
            age = adopter_model.age,
            housing_type = HousingType[adopter_model.housing_type],    
            usable_area = adopter_model.usable_area,
            has_pet_experience = adopter_model.has_pet_experience,
            has_children_at_home = adopter_model.has_children_at_home,
            has_other_animals = adopter_model.has_other_animals
        )

    # ---- Create ----
    def save(self, adopter) -> AdopterModel:
        """Salva uma entidade Adopter no banco"""

        adopter_db = AdopterModel(
            id = adopter.id,
            name = adopter.name,
            age = adopter.age,
            housing_type = adopter.housing_type.name,           # Enum -> str
            usable_area = adopter.usable_area,
            has_pet_experience = adopter.has_pet_experience,
            has_children_at_home = adopter.has_children_at_home,
            has_other_animals = adopter.has_other_animals
        )

        self.session.add(adopter_db)
        self.session.commit()
        self.session.refresh(adopter_db)
        return adopter_db

    # ---- Read ----
    def list_all(self) -> list[AdopterModel]:
        """Retorna uma lista de todos os adotates cadastrados no banco"""
        return self.session.query(AdopterModel).all()

    def get_by_id(self, id: int) -> AdopterModel:
        """Retorna um adotante cadastrado no banco"""
        return self.session.get(AdopterModel, id)

    # ---- Update ----
    def update(self, adopter) -> AdopterModel|None:
        """Atualiza um registro existente no banco a partir de um objeto de domínio"""
        adopter_db = self.session.get(AdopterModel, adopter.id)

        if not adopter_db:
            return None

        adopter_db.name = adopter.name
        adopter_db.age = adopter.age
        adopter_db.housing_type = adopter.housing_type.name        # Enum -> str
        adopter_db.usable_area = adopter.usable_area
        adopter_db.has_pet_experience = adopter.has_pet_experience
        adopter_db.has_children_at_home = adopter.has_children_at_home
        adopter_db.has_other_animals = adopter.has_other_animals

        self.session.commit()
        self.session.refresh(adopter_db)
        return adopter_db

    # ---- Delete ----
    def delete_by_id(self, id: int) -> bool:
        adopter_db = self.session.get(AdopterModel, id)

        if not adopter_db:
            return False

        self.session.delete(adopter_db)
        self.session.commit()
        return True