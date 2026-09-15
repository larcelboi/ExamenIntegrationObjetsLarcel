from pydantic import BaseModel, ConfigDict, Field


class EtatLocal(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    numero: str
    occupation_actuelle: int = Field(ge=0)
    qualite_air_ppm: int = Field(ge=0, le=3000)
    purificateur_actif: bool = True


class ModificationPurificateur(BaseModel):
    """Corps de requête pour allumer ou éteindre le purificateur d'un local."""

    actif: bool


def niveau_qualite_air(ppm: int) -> str:
    if ppm < 600:
        return "Bonne"
    elif ppm < 1200:
        return "Moyenne"
    else:
        return "Mauvaise"
