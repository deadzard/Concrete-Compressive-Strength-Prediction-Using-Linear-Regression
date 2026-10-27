# Concrete Compressive Strength Prediction Using Linear Regression

## Project Purpose

This project predicts the compressive strength of concrete using a Multiple Linear Regression model. It is part of an Artificial Intelligence and Machine Learning Experiential Learning assignment (20 marks — CO2 and CO3).

## Dataset Source

- **Name:** Concrete Compressive Strength
- **Source:** UCI Machine Learning Repository
- **URL:** https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength
- **Original Donor:** Prof. I-Cheng Yeh, Department of Information Management, Chung-Hua University, Taiwan
- **Publication:** Yeh, I-C. (1998). "Modeling of strength of high-performance concrete using artificial neural networks." *Cement and Concrete Research*, 28(12), 1797–1808.
- **Records:** 1,030 samples (1,005 after removing 25 duplicates)
- **Features:** 8 input variables + 1 target variable
- **Retrieved on:** 2026-10-27

### Citation

```
Yeh, I-Cheng. (2007). Concrete Compressive Strength. UCI Machine Learning Repository.
https://doi.org/10.24432/C5PK67.
```

## Folder Structure

```
concrete-strength-ml/
├── dataset/
│   └── concrete_data.csv          # Genuine UCI dataset (1,030 records)
├── concrete_strength_analysis.ipynb   # Complete Jupyter notebook with outputs
├── concrete_strength_report.docx      # 2–3 page academic report
├── scatter_plot.png                   # Scatter plot (Cement vs. Strength)
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── download_dataset.py                # Script to download the dataset
├── extract_results.py                 # Script to extract model results
├── create_report.py                   # Script to generate the Word report
└── run_notebook.py                    # Script to execute the notebook
```

## Python Environment Setup

### Prerequisites

- Python 3.10 or later
- pip (Python package installer)

### Installation

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
```

2. Activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run the Notebook

1. Start Jupyter Notebook or JupyterLab:

```bash
jupyter notebook
```

2. Open `concrete_strength_analysis.ipynb`.

3. Run all cells from top to bottom: **Kernel → Restart & Run All**.

4. The dataset is loaded from `dataset/concrete_data.csv`. If the file is missing, run:

```bash
python download_dataset.py
```

## How to Reproduce the Analysis

1. Install dependencies as described above.
2. Ensure `dataset/concrete_data.csv` exists (download if needed).
3. Open and run all cells in `concrete_strength_analysis.ipynb`.
4. The notebook produces all outputs, statistics, plots, and predictions.
5. The train-test split uses `random_state=42` for full reproducibility.

## Key Results

| Metric | Value |
|--------|-------|
| Training Records | 804 (80%) |
| Testing Records | 201 (20%) |
| Test MAE | 8.90 MPa |
| Test R² | 0.5802 |
| New Sample Prediction | 38.09 MPa |
