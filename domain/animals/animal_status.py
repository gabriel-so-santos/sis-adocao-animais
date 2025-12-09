from enum import Enum, auto

class AnimalStatus(Enum):
    """Enumeração que representa os estados possíveis de um animal no sistema.

    Estados:
        AVAILABLE: Animal disponível para adoção.
        RESERVED: Animal reservado por um adotante.
        ADOPTED: Animal já adotado.
        RETURNED: Animal devolvido após adoção.
        QUARANTINE: Animal em quarentena por saúde ou comportamento.
        UNADOPTABLE: Animal não pode ser adotado.
    """
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    ADOPTED = "ADOPTED"
    RETURNED = "RETURNED"
    QUARANTINE = "QUARANTINE"
    UNADOPTABLE = "UNADOPTABLE"

    @staticmethod
    def is_valid_transition(current_status: 'AnimalStatus', new_status: 'AnimalStatus') -> bool:
        """Verifica se uma transição de estado é permitida.

        Transições possíveis:
            - AVAILABLE → RESERVED → ADOPTED
            - AVAILABLE → UNADOPTABLE
            - ADOPTED → RETURNED → (QUARANTINE | AVAILABLE | UNADOPTABLE)
            - QUARANTINE → (AVAILABLE | UNADOPTABLE)

        Args:
            current_status (AnimalStatus): Estado atual do animal.
            new_status (AnimalStatus): Novo estado pretendido.

        Returns:
            bool: True se a transição for permitida, False caso contrário.
        """
        transitions = {
            AnimalStatus.AVAILABLE: {
                AnimalStatus.RESERVED,
                AnimalStatus.UNADOPTABLE,
            },
            AnimalStatus.RESERVED: {
                AnimalStatus.ADOPTED,
            },
            AnimalStatus.ADOPTED: {
                AnimalStatus.RETURNED,
            },
            AnimalStatus.RETURNED: {
                AnimalStatus.QUARANTINE,
                AnimalStatus.AVAILABLE,
                AnimalStatus.UNADOPTABLE,
            },
            AnimalStatus.QUARANTINE: {
                AnimalStatus.AVAILABLE,
                AnimalStatus.UNADOPTABLE,
            },
            AnimalStatus.UNADOPTABLE: set(),
        }

        allowed = transitions.get(current_status, set())
        return new_status in allowed