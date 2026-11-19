import glob
import pandas as pd

#Find the CSV in teh data folder
csv_path - glob.glob("data/*.csv")[0]
print("Loading:", csv_path)

df = pd.read_csv(csv_path, low_memory=False)
print("All US flights:", df.shape)

#ONLY flights for MCo
mco = df[(df["Origin"] == "MCO") | (df["Dest"] == "MCO")]
print("MCO flights:", mco.shape)


