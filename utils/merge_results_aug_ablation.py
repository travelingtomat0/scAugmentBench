import os
from glob import glob
import pandas as pd
import csv
import numpy as np
from sklearn.preprocessing import MinMaxScaler

experiment = 'ablation-db-2/augmentation-combi'
# data = ['ImmHuman', 'MCA', 'PBMC']
data = ['MCA']
augmentations = ["bbknn", "gauss", "mask", "swap", "crossover", "mnn"]
# models_list = ['SimCLR', 'MoCo']
models_list = ['SimCLR']
pipeline = 'base'
seed = '20'

metrics = ['Isolated labels', 'Leiden NMI', 'Leiden ARI', 'Silhouette label', 'cLISI', 'Silhouette batch', 'iLISI', 'KBET', 'Graph connectivity', 'PCR comparison']

def compare_model_architectures(data):

    cols = metrics + ["data", "model", "seed", "aug1", "aug2"]
                    
    df_list = []
    for model in models_list:
        for aug1 in augmentations:
            for d in data:
                if aug1 == 'bbknn':
                    aug2_list = ["bbknn", "gauss", "innerswap", "mask", "crossover"]
                elif aug1 == 'gauss':
                    aug2_list = ["gauss", "innerswap", "mask"]
                elif aug1 == 'mask':
                    aug2_list = ["innerswap", "mask"]
                elif aug1 == 'swap':
                    aug2_list = ["innerswap"]
                elif aug1 == 'crossover':
                    aug2_list = ["crossover", "gauss", "innerswap", "mask"]
                elif aug1 == 'mnn':
                    aug2_list = ["mnn", "gauss", "innerswap", "mask"]

                for aug2 in aug2_list:
                    PATH = experiment + '/' + d + '/' + aug1 + '/' + aug2 + '/' + model + '/' + seed
                    result_paths = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.csv'))]
                    for i, seed_path in enumerate(result_paths):
                        with open(seed_path, newline='') as csvfile:
                            reader = csv.DictReader(csvfile)
                            for row in reader:
                                row.pop('Bio conservation')
                                row.pop('Batch correction')
                                row.pop('Total')
                                
                                values = row
                                values["data"] = d
                                values["model"] = model
                                values["seed"] = seed
                                values["aug1"] = aug1
                                values["aug2"] = aug2

                                df_list.append(values)
    
    df = pd.DataFrame(df_list, columns=cols)
    df_scaled_metrics = scale_result(df[metrics])
    df.loc[:, "Total"] = df_scaled_metrics["Total"]
    df.loc[:, "Bio conservation"] = df_scaled_metrics["Bio conservation"]
    df.loc[:, "Batch correction"] = df_scaled_metrics["Batch correction"]

    # remove_cols = list(filter(lambda x: ("Bio conservation" not in x) and ("Batch correction" not in x) and ("Total" not in x), list(df.columns)))
    remove_cols = list(filter(lambda x: x not in ["Total", "data", "model", "seed", "aug1", "aug2"], list(df.columns)))
    df = df.drop(remove_cols, axis=1).round(3)

    
    # Parse into the format
    cols_final = ["Gaussian Noise", "InnerSwap", "Masking", "BBKNN", "MNN", "CrossOver"]
    final_df = pd.DataFrame(index=cols_final, columns=[c + f"_{data[0]}" for c in cols_final])

    df.loc[df["aug1"] == "bbknn", "aug1"] = "BBKNN"
    df.loc[df["aug2"] == "bbknn", "aug2"] = "BBKNN"

    df.loc[df["aug1"] == "gauss", "aug1"] = "Gaussian Noise"
    df.loc[df["aug2"] == "gauss", "aug2"] = "Gaussian Noise"

    df.loc[df["aug1"] == "innerswap", "aug1"] = "InnerSwap"
    df.loc[df["aug2"] == "innerswap", "aug2"] = "InnerSwap"

    df.loc[df["aug1"] == "swap", "aug1"] = "InnerSwap"
    df.loc[df["aug2"] == "swap", "aug2"] = "InnerSwap"

    df.loc[df["aug1"] == "mask", "aug1"] = "Masking"
    df.loc[df["aug2"] == "mask", "aug2"] = "Masking"

    df.loc[df["aug1"] == "crossover", "aug1"] = "CrossOver"
    df.loc[df["aug2"] == "crossover", "aug2"] = "CrossOver"

    df.loc[df["aug1"] == "mnn", "aug1"] = "MNN"
    df.loc[df["aug2"] == "mnn", "aug2"] = "MNN"
    
    print(final_df)

    for index, row in df.iterrows():
        print(row["aug1"], row["aug2"]+f"_{data[0]}")
        final_df.loc[row["aug1"], row["aug2"]+f"_{data[0]}"] = row["Total"]
        final_df.loc[row["aug2"], row["aug1"]+f"_{data[0]}"] = row["Total"]
    print(final_df)
    return final_df

def scale_result(df):
    scaled= pd.DataFrame(MinMaxScaler().fit_transform(df), columns=df.columns, index=df.index)
    biometrics = ['Isolated labels', 'Leiden NMI', 'Leiden ARI', 'Silhouette label', 'cLISI']
    batchmetrics = ['Silhouette batch', 'iLISI', 'KBET', 'Graph connectivity', 'PCR comparison']
    scaled[f"Batch correction"] = scaled[batchmetrics].mean(1)
    scaled[f"Bio conservation"] = scaled[biometrics].mean(1)
    scaled[f"Total"] = 0.6 * scaled[f"Bio conservation"] + 0.4 * scaled[f"Batch correction"]
    df[f"Bio conservation"] = scaled[f"Bio conservation"].copy()
    df[f"Batch correction"] = scaled[f"Batch correction"].copy()
    df.loc[:,"Total"] = scaled["Total"].copy()
    return df


averages = compare_model_architectures(data=data)
dir_path = "aug_abl/"
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
    print("Directory created successfully!")
else:
    print("Directory already exists!")
averages.to_csv(f"{dir_path}{models_list[0]}_{data[0]}_avg.csv")
