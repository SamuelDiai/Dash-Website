import pandas as pd

from dash_website.utils.aws_loader import load_csv
from dash_website.datasets import TREE_IMAGES


columns_to_take = [
    "id",
    "sex",
    "age_category",
    "aging_rate",
    "sample",
    "Age",
    "Biological_Age",
    "Ethnicity.White",
    "Ethnicity.British",
    "Ethnicity.Irish",
    "Ethnicity.White_Other",
    "Ethnicity.Mixed",
    "Ethnicity.White_and_Black_Caribbean",
    "Ethnicity.White_and_Black_African",
    "Ethnicity.White_and_Asian",
    "Ethnicity.Mixed_Other",
    "Ethnicity.Asian",
    "Ethnicity.Indian",
    "Ethnicity.Pakistani",
    "Ethnicity.Bangladeshi",
    "Ethnicity.Asian_Other",
    "Ethnicity.Black",
    "Ethnicity.Caribbean",
    "Ethnicity.African",
    "Ethnicity.Black_Other",
    "Ethnicity.Chinese",
    "Ethnicity.Other",
    "Ethnicity.Other_ethnicity",
    "Ethnicity.Do_not_know",
    "Ethnicity.Prefer_not_to_answer",
    "Ethnicity.NA",
]


if __name__ == "__main__":
    list_information = []

    for DIMENSION in list(TREE_IMAGES.keys()):
        for SUBDIMENSION in list(TREE_IMAGES[DIMENSION].keys()):
            for SUB_SUBDIMENSION in TREE_IMAGES[DIMENSION][SUBDIMENSION]:
                if DIMENSION == "Musculoskeletal" and SUB_SUBDIMENSION == "DXA":
                    SUB_SUBDIMENSION_OLD = "MRI"
                else:
                    SUB_SUBDIMENSION_OLD = SUB_SUBDIMENSION
                information_raw = load_csv(
                    f"page9_AttentionMaps/Attention_maps_infos/AttentionMaps-samples_Age_{DIMENSION}_{SUBDIMENSION}_{SUB_SUBDIMENSION_OLD}.csv",
                    usecols=columns_to_take,
                )[columns_to_take].set_index("id")

                information = pd.DataFrame(
                    None,
                    columns=[
                        "dimension",
                        "subdimension",
                        "sub_subdimension",
                        "sex",
                        "age_group",
                        "aging_rate",
                        "sample",
                        "chronological_age",
                        "biological_age",
                        "ethnicity",
                    ],
                    index=information_raw.index,
                )
                information["dimension"] = DIMENSION
                information["subdimension"] = SUBDIMENSION
                information["sub_subdimension"] = SUB_SUBDIMENSION
                information["sex"] = information_raw["sex"].str.lower()
                information["age_group"] = information_raw["age_category"]
                information["aging_rate"] = information_raw["aging_rate"]
                information["sample"] = information_raw["sample"]
                information["chronological_age"] = information_raw["Age"].round(1)
                information["biological_age"] = information_raw["Biological_Age"]

                for id_participant in information_raw.index:
                    ethnicities = information_raw.loc[
                        id_participant, information_raw.columns[information_raw.columns.str.startswith("Ethnicity")]
                    ]

                    information.loc[id_participant, "ethnicity"] = " ".join(
                        list(map(lambda list_ethni: list_ethni.split(".")[1], ethnicities[ethnicities == 1].index))
                    )

                list_information.append(information.reset_index())

    pd.concat(list_information).reset_index(drop=True).to_feather("all_data/datasets/images/information.feather")