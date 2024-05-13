from pydantic import BaseModel

class ChoiceBase(BaseModel):
    choice_text : str
    isTrue: bool
    
class QuestionBase(BaseModel):
    question_text : str
    choices : List[ChoiceBase]
    