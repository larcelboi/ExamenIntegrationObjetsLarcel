from pydantic import BaseModel, ConfigDict, Field


class EtatLocal(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    numero: str
    occupation_actuelle: int = Field(ge=0)
    qualite_air_ppm: int = Field(ge=0, le=3000)
    purificateur_actif: bool = True


def niveau_qualite_air(ppm: int) -> str:
    """Détermine le niveau de qualité de l'air.

    Args:
        ppm (int): Concentration de particules dans l'air.

    Returns:
        str: Niveau de qualité correspondant à la concentration.
    """
    if ppm < 600:
        return "Bonne"
    elif ppm < 1200:
        return "Moyenne"
    else:
        return "Mauvaise"
