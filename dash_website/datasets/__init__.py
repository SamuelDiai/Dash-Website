import numpy as np

# Shared
AGE_RANGES = np.arange(0, 100, 5)

# For scalars
TREE_SCALARS = {
    "Arterial": {
        "All": ["Scalars"],
        "BloodPressure": ["Scalars"],
        "Carotids": ["Scalars"],
        "PWA": ["Scalars"],
    },
    "Biochemistry": {"All": ["Scalars"], "Blood": ["Scalars"], "Urine": ["Scalars"]},
    "BloodCells": {"BloodCount": ["Scalars"]},
    "Brain": {
        "All": ["Scalars"],
        "Cognitive": [
            "AllScalars",
            "ReactionTime",
            "MatrixPatternCompletion",
            "TowerRearranging",
            "SymbolDigitSubstitution",
            "PairedAssociativeLearning",
            "ProspectiveMemory",
            "NumericMemory",
            "FluidIntelligence",
            "TrailMaking",
            "PairsMatching",
        ],
        "MRI": ["AllScalars", "dMRIWeightedMeans", "GreyMatterVolumes", "SubcorticalVolumes"],
    },
    "Demographics": {"All": ["Scalars"]},
    "Eyes": {
        "Acuity": ["Scalars"],
        "All": ["Scalars"],
        "Autorefraction": ["Scalars"],
        "IntraocularPressure": ["Scalars"],
    },
    "Hearing": {"HearingTest": ["Scalars"]},
    "Heart": {"All": ["Scalars"], "ECG": ["Scalars"], "MRI": ["Size", "PWA", "AllScalars"]},
    "Lungs": {"Spirometry": ["Scalars"]},
    "Musculoskeletal": {
        "Scalars": ["AllScalars", "Anthropometry", "Impedance", "HeelBoneDensitometry", "HandGripStrength"]
    },
    "PhysicalActivity": {"FullWeek": ["Scalars"]},
}

ETHNICITIES = [
    "Do_not_know",
    "Prefer_not_to_answer",
    "NA",
    "White",
    "British",
    "Irish",
    "White_Other",
    "Mixed",
    "White_and_Black_Caribbean",
    "White_and_Black_African",
    "White_and_Asian",
    "Mixed_Other",
    "Asian",
    "Indian",
    "Pakistani",
    "Bangladeshi",
    "Asian_Other",
    "Black",
    "Caribbean",
    "African",
    "Black_Other",
    "Chinese",
    "Other_ethnicity",
    "Other",
]

SEX_VALUE = {"female": 0, "male": 1}
SEX_COLOR = {"female": "Pink", "male": "Blue"}

# For time series
TREE_TIME_SERIES = {
    "Arterial": {"PulseWaveAnalysis": ["TimeSeries"]},
    "Heart": {"ECG": ["TimeSeries"]},
    "PhysicalActivity": {"FullWeek": ["Acceleration", "TimeSeriesFeatures"], "Walking": ["3D"]},
}

INFORMATION_TIME_SERIES = {
    "Arterial": {
        "PulseWaveAnalysis": {
            "TimeSeries": {
                "nb_channel": 1,
                "y_label": "blood pressure [normalized]",
                "x_label": "Time (10 min / unit)",
            }
        }
    },
    "Heart": {
        "ECG": {
            "TimeSeries": {
                "nb_channel": 15,
                "y_label": "5 uV / Lsb",
                "x_label": "Time (2 min / unit)",
            }
        }
    },
    "PhysicalActivity": {
        "FullWeek": {
            "Acceleration": {
                "nb_channel": 1,
                "y_label": "miligravity",
                "x_label": "Time (1 min / unit)",
            },
            "TimeSeriesFeatures": {
                "nb_channel": 113,
                "y_label": "Acceleration",
                "x_label": "Time (5 min / unit)",
            },
        },
        "Walking": {
            "3D": {
                "nb_channel": 3,
                "y_label": "Acceleration",
                "x_label": "Time (2 min / unit)",
            }
        },
    },
}

# For images
TREE_IMAGES = {
    "Abdomen": {"Liver": ["Raw", "Contrast"], "Pancreas": ["Raw", "Contrast"]},
    "Arterial": {"Carotids": ["CIMT120", "CIMT150", "LongAxis", "Mixed", "ShortAxis"]},
    "Brain": {
        "MRI": [
            "SagittalRaw",
            "SagittalReference",
            "CoronalRaw",
            "CoronalReference",
            "TransverseRaw",
            "TransverseReference",
        ]
    },
    "Eyes": {"Fundus": ["Raw"], "OCT": ["Raw"]},
    "Heart": {
        "MRI": [
            "2chambersRaw",
            "2chambersContrast",
            "3chambersRaw",
            "3chambersContrast",
            "4chambersRaw",
            "4chambersContrast",
        ]
    },
    "Musculoskeletal": {
        "FullBody": ["Figure", "Flesh", "Mixed", "Skeleton"],
        "Knees": ["DXA"],
        "Hips": ["DXA"],
        "Spine": ["Coronal", "Sagittal"],
    },
    "PhysicalActivity": {
        "FullWeek": [
            "GramianAngularField1minDifference",
            "GramianAngularField1minSummation",
            "MarkovTransitionField1min",
            "RecurrencePlots1min",
        ]
    },
}

SIDES_DIMENSION = ["Arterial", "Eyes", "Musculoskeletal"]
SIDES_SUBDIMENSION_EXCEPTION = ["FullBody", "Spine"]


# For videos
CHAMBERS_LEGEND = {"3": "3 chamber", "4": "4 chamber"}

SEX_LEGEND = {"male": "Male", "female": "Female"}

AGE_GROUP_LEGEND = {"young": "Young", "middle": "Middle", "old": "Old"}

SAMPLE_LEGEND = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}
