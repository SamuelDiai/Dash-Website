import pandas as pd

ORDER_DIMENSIONS = pd.MultiIndex.from_tuples(
    [
        ("*", "*"),
        ("*instances01", "*"),
        ("*instances1.5x", "*"),
        ("*instances23", "*"),
        ("Abdomen", "*"),
        ("Abdomen", "Liver"),
        ("Abdomen", "Pancreas"),
        ("Arterial", "*"),
        ("Arterial", "Carotids"),
        ("Arterial", "PulseWaveAnalysis"),
        ("Biochemistry", "*"),
        ("Biochemistry", "Blood"),
        ("Biochemistry", "Urine"),
        ("BloodCells", "*"),
        ("Brain", "*"),
        ("Brain", "Cognitive"),
        ("Brain", "MRI"),
        ("Eyes", "*"),
        ("Eyes", "All"),
        ("Eyes", "Fundus"),
        ("Eyes", "OCT"),
        ("Hearing", "*"),
        ("Heart", "*"),
        ("Heart", "ECG"),
        ("Heart", "MRI"),
        ("Lungs", "*"),
        ("Musculoskeletal", "*"),
        ("Musculoskeletal", "FullBody"),
        ("Musculoskeletal", "Hips"),
        ("Musculoskeletal", "Knees"),
        ("Musculoskeletal", "Scalars"),
        ("Musculoskeletal", "Spine"),
        ("PhysicalActivity", "*"),
    ]
)
