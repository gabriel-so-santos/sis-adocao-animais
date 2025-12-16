from datetime import datetime
from domain.adoptions.adoption import Adoption

class AdoptionContractService:
    """
    Serviço responsável por gerar o contrato textual de adoção.
    """
    def __init__(
        self,
        adoption_repo,
        animal_repo,
        adopter_repo
    ):
        self.adoption_repo = adoption_repo
        self.animal_repo = animal_repo
        self.adopter_repo = adopter_repo

    def generate_contract(self, adoption_id: int) -> str:
        """
        Gera o texto do contrato de adoção com base nos dados da adoção.

        Args:
            adoption (Adoption): Adoção registrada no sistema.

        Returns:
            str: Texto completo do contrato de adoção.
        """
        adoption = self.adoption_repo.get_by_id(adoption_id)
        animal = self.animal_repo.get_by_id(adoption.animal_id)
        adopter = self.adopter_repo.get_by_id(adoption.adopter_id)

        contract = f"""
CONTRATO DE ADOÇÃO DE ANIMAL

Data da Adoção: {adoption.timestamp.strftime("%d/%m/%Y %H:%M")}

ADOTANTE
Nome: {adopter.name}
Idade: {adopter.age} anos
Tipo de moradia: {adopter.housing_type_format()}
Área útil: {adopter.usable_area} m²
Possui crianças na residência?: {adopter.has_children_at_home_format()}
Possui algum outro animal?: {adopter.has_pet_experience_format()}
Possui experiência com pets?: {adopter.has_pet_experience_format()}

ANIMAL
Nome: {animal.name}
Espécie: {animal.species_format()}
Sexo: {animal.gender_format()}
Raça: {animal.breed}
Porte: {animal.size_format()}
Idade: {animal.age_months} meses
{animal.extra_info_str()}
É arisco?: {animal.has_wary_temperament_format()}
Temperamento: {animal.temperament_format()}

TAXA DE ADOÇÃO
Valor pago: R$ {adoption.fee:.2f}

TERMOS
1. O adotante compromete-se a fornecer cuidados adequados ao animal.
2. O animal não poderá ser abandonado ou repassado a terceiros.
3. Em caso de impossibilidade de permanência, o animal deverá ser devolvido à instituição.
4. A instituição não se responsabiliza por custos futuros com saúde ou manutenção.



Assinatura do adotante: ______________________________________________________________

Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""

        return contract.strip()