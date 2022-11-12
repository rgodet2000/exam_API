from pydantic import BaseModel
from typing import Optional, List
import pandas as pd

df = pd.read_csv("../data/questions.csv")
df = df.drop(["remark"], axis = 1)
subjects = list(df["subject"].unique())

class Test(BaseModel):
    nombre:Optional[int]=20
    subjects:Optional[List[str]]=subjects
    use:Optional[str]="Test de positionnement"