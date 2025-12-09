class PolicyNotMetError(Exception):
    """Raised when adopter does not meet policy requirements."""
    pass

class InvalidStatusTransitionError(Exception):
    """
    "Raised when the animal status transition is invalid.
    """