from pydantic import BaseModel


class Critique(BaseModel):
    class Feedback(BaseModel):
        response: str
        correction: str

    query: str
    feedback: list[Feedback] | None = None
    response: str | None = None


class CritiqueWithSituation(Critique):
    situation: str
