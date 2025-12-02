from database import init_db, SessionLocal

# Domain
from domain.animals.animal import Animal, Gender, Size, AnimalStatus
from domain.people.adopter import Adopter, HousingType
from domain.adoption.adoption import Adoption

# Repositories
from repositories.animal_repo import AnimalRepository
from repositories.adopter_repo import AdopterRepository
from repositories.adoption_repo import AdoptionRepository

# Inicializa o BD
init_db()

# Cria sessão
session = SessionLocal()

# Repositórios
animal_repo = AnimalRepository(session)
adopter_repo = AdopterRepository(session)
adoption_repo = AdoptionRepository(session)

print("\n--- CADASTRANDO ANIMAL ---")
animal = Animal(
    id=None,
    species="Cachorro",
    breed="Pastor Alemão",
    name="Jeeb",
    gender=Gender.MALE,
    age_months=20,
    size=Size.LARGE,
    temperament=["brincalhão", "obediente"],
    status=AnimalStatus.AVAILABLE
)
animal_db = animal_repo.save(animal)
print("Animal criado:", animal_db.id, animal_db.name)

print("\n--- CADASTRANDO ADOTANTE ---")
adopter = Adopter(
    id=None,
    name="Maria Silva",
    age=34,
    housing_type=HousingType.HOUSE,
    usable_area=120.0,
    has_pet_experience=True,
    has_children_at_home=False,
    has_other_animals=False
)
adopter_db = adopter_repo.save(adopter)
print("Adotante criado:", adopter_db.id, adopter_db.name)

print("\n--- REGISTRANDO ADOÇÃO ---")
adoption = Adoption(
    id=None,
    adopter_id=adopter_db.id,
    animal_id=animal_db.id,
    fee=90.0,
    created_at=None  # repo deve preencher automaticamente
)
adoption_db = adoption_repo.save(adoption)
print("Adoção criada. ID:", adoption_db.id)

print("\n--- LISTANDO TODAS AS ADOÇÕES ---")
for ad in adoption_repo.list_all():
    print(f"Adocao #{ad.id} | Adotante={ad.adopter_id} | Animal={ad.animal_id} | Taxa={ad.fee}")

print("\n--- TESTANDO DELETE ---")
deleted = animal_repo.delete_by_id(animal_db.id)
print("Animal deletado?", deleted)

print("\n--- LISTANDO TODOS OS ANIMAIS ---")
for a in animal_repo.list_all():
    print(a.id, a.name, a.species)