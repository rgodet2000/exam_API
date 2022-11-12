from pydantic import BaseModel
from typing import Optional, List
import pandas as pd

df = pd.read_csv("../data/questions.csv")
df = df.drop(["remark"], axis = 1)
subjects = list(df["subject"].unique())

class AdminTest(BaseModel):
    question:str
    subject:str
    use:str
    correct:str
    responseA:str
    responseB:str
    responseC:Optional[str] = "null"
    responseD:Optional[str] = "null"
    remark:Optional[str] = "null"