# Exploring Posture as a Marker of Clinical Vulnerability: Natural Language Processing of Discharge Notes in MIMIC-IV

## Setup

1. Install the following
   - [Python 3.13](https://www.python.org/downloads/release/python-3139/)
   - [uv](https://docs.astral.sh/uv/) 

2. Clone the repository.

``` sh
git clone https://github.com/khelmr/posture_mddatathon_2025.git
```
3. Run the following command in the repo to setup environment.

``` sh
uv sync
```

## Files
- `output` generated data from `scripts`
    - `labeled_posture.csv` - MIMIC-IV-Notes data with posture information labeled for matched entries
    - `posture_data_preprocessed.csv` - compiled and pre-processed MIMIC-IV data for entry into Random Forest Model
    - `posture_data_preprocessed_abridged.csv`- compiled and pre-processed MIMIC-IV data for entry into Random Forest Model (excluding experimental columns)
    - `posture_mention_notes.csv` - MIMIC-IV-Notes entries that contain the word "posture"
    - 
- `scripts` scripts and Jupyter notebooks used to process data
    - `explore.ipynb` - draft notebook for exploring the MIMIC-IV data
    - `filter_scoliosis_icd.py` - script for finding scoliosis instances in the icd table (unused)
    - `nlp.ipynb` - Performing NLP/regex searching, filtering, and labeling of MIMIC-IV-Notes data; also compiling and preprocessing of data for entry into the Random Forest Model
    - `posture_random_forest_age_cohorts.ipynb` - Train Random Forest regressors that model hospital stay duration and surface feature importance overall and within age cohorts.
    - `posture_random_forest.ipynb` - Train a Random Forest classifier that predicts 90-day mortality from posture-derived labels plus basic demographics.
    - `posture_random_forest.ipynb` - Train a Random Forest regressor that predicts hospital stay duration from posture-derived labels and patient metadata.

