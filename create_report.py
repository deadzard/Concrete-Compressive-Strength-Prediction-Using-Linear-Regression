"""
Generate the academic Word report using python-docx.
All values are from the executed model - nothing is fabricated.
"""
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

doc = Document()

# Page margins
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.15

# ===================== TITLE =====================
title = doc.add_heading('Concrete Compressive Strength Prediction\nUsing Linear Regression', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Artificial Intelligence and Machine Learning — Experiential Learning\n20 Marks | CO2 and CO3')
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(80, 80, 80)

# ===================== 1. OBJECTIVE =====================
doc.add_heading('1. Objective', level=1)
doc.add_paragraph(
    'The objective of this project is to explore a real-world dataset of concrete mixtures, '
    'perform exploratory data analysis (EDA), and build a Linear Regression model to predict '
    'the compressive strength of concrete based on its ingredients and age.'
)

# ===================== 2. DATASET =====================
doc.add_heading('2. Dataset Description', level=1)
doc.add_paragraph(
    'The dataset used is the Concrete Compressive Strength dataset from the UCI Machine Learning '
    'Repository (ID: 165), originally donated by Prof. I-Cheng Yeh (1998). The dataset contains '
    '1,030 samples of concrete with 8 input features and 1 target variable.'
)
p = doc.add_paragraph()
p.add_run('Source: ').bold = True
p.add_run('https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength')

# Input features table
doc.add_heading('Input Variables and Target', level=2)

table = doc.add_table(rows=10, cols=3)
table.style = 'Light Grid Accent 1'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ['#', 'Variable', 'Unit']
for i, h in enumerate(headers):
    table.rows[0].cells[i].text = h
    for paragraph in table.rows[0].cells[i].paragraphs:
        for run in paragraph.runs:
            run.bold = True

features = [
    ('1', 'Cement', 'kg/m³'),
    ('2', 'Blast Furnace Slag', 'kg/m³'),
    ('3', 'Fly Ash', 'kg/m³'),
    ('4', 'Water', 'kg/m³'),
    ('5', 'Superplasticizer', 'kg/m³'),
    ('6', 'Coarse Aggregate', 'kg/m³'),
    ('7', 'Fine Aggregate', 'kg/m³'),
    ('8', 'Age', 'days'),
    ('Target', 'Concrete Compressive Strength', 'MPa'),
]

for row_idx, (num, var, unit) in enumerate(features, 1):
    table.rows[row_idx].cells[0].text = num
    table.rows[row_idx].cells[1].text = var
    table.rows[row_idx].cells[2].text = unit

# ===================== 3. DATA CLEANING (Q1) =====================
doc.add_heading('3. Data Cleaning and Exploration (Question 1 — CO2)', level=1)

doc.add_heading('Missing Values', level=2)
doc.add_paragraph(
    'The dataset contains zero missing values across all 9 columns (1,030 records × 9 columns). '
    'No imputation or deletion was needed for missing data.'
)

doc.add_heading('Duplicate Records', level=2)
doc.add_paragraph(
    'A total of 25 duplicate records were identified — rows where all column values are identical '
    'to a previous row. These duplicates were removed to prevent the same data point from appearing '
    'in both training and testing sets, which would inflate model performance. After removing duplicates, '
    'the cleaned dataset contains 1,005 records.'
)

doc.add_heading('Descriptive Statistics (Selected Variables)', level=2)

stats_table = doc.add_table(rows=5, cols=5)
stats_table.style = 'Light Grid Accent 1'
stats_table.alignment = WD_TABLE_ALIGNMENT.CENTER

stats_headers = ['Variable', 'Mean', 'Std Dev', 'Min', 'Max']
for i, h in enumerate(stats_headers):
    stats_table.rows[0].cells[i].text = h
    for paragraph in stats_table.rows[0].cells[i].paragraphs:
        for run in paragraph.runs:
            run.bold = True

stats_data = [
    ('Cement (kg/m³)', '278.63', '104.34', '102.00', '540.00'),
    ('Water (kg/m³)', '181.49', '21.24', '121.75', '247.00'),
    ('Age (days)', '45.86', '63.73', '1', '365'),
    ('Strength (MPa)', '35.25', '16.28', '2.33', '82.60'),
]

for row_idx, (var, mean, std, mn, mx) in enumerate(stats_data, 1):
    stats_table.rows[row_idx].cells[0].text = var
    stats_table.rows[row_idx].cells[1].text = mean
    stats_table.rows[row_idx].cells[2].text = std
    stats_table.rows[row_idx].cells[3].text = mn
    stats_table.rows[row_idx].cells[4].text = mx

doc.add_paragraph()

# Scatter plot
doc.add_heading('Scatter Plot: Cement Content vs. Compressive Strength', level=2)
scatter_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scatter_plot.png')
if os.path.exists(scatter_path):
    doc.add_picture(scatter_path, width=Inches(4.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption = doc.add_paragraph('Figure 1: Cement Content (kg/m³) vs. Compressive Strength (MPa)')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.runs[0].font.size = Pt(9)
    caption.runs[0].font.italic = True
else:
    doc.add_paragraph('[Scatter plot image not found — see notebook for the generated plot.]')

doc.add_heading('Observations', level=2)

p1 = doc.add_paragraph(style='List Number')
p1.add_run('Positive trend between Cement and Strength: ').bold = True
p1.add_run(
    'The scatter plot shows a general upward trend — as cement content increases, compressive strength '
    'tends to increase. This is consistent with civil engineering knowledge, as cement is the primary '
    'binding agent. However, for any given cement content, strength varies widely due to the influence '
    'of other ingredients and curing age.'
)

p2 = doc.add_paragraph(style='List Number')
p2.add_run('Wide range of strength values: ').bold = True
p2.add_run(
    'Compressive strength ranges from 2.33 MPa to 82.60 MPa, with a mean of 35.25 MPa and a standard '
    'deviation of 16.28 MPa. The standard deviation is nearly half the mean, indicating high variability. '
    'This confirms that multiple features (not just cement alone) are needed to predict strength accurately.'
)

# ===================== 4. LINEAR REGRESSION (Q2) =====================
doc.add_heading('4. Linear Regression Model (Question 2 — CO3)', level=1)

doc.add_heading('Methodology', level=2)
doc.add_paragraph(
    'Linear Regression is a supervised machine learning algorithm that finds the best linear relationship '
    'between input features and a continuous target variable. It learns a coefficient (weight) for each '
    'feature and an intercept, minimising the sum of squared errors between predicted and actual values.'
)

doc.add_paragraph(
    'The dataset was split into 80% training data (804 records) and 20% testing data (201 records) using '
    'scikit-learn\'s train_test_split function with random_state=42 for reproducibility. The model was '
    'trained exclusively on the training set, and evaluated on the unseen test set to ensure no data leakage.'
)

# Five test records table
doc.add_heading('Actual vs. Predicted Strength (Five Test Records)', level=2)

pred_table = doc.add_table(rows=6, cols=4)
pred_table.style = 'Light Grid Accent 1'
pred_table.alignment = WD_TABLE_ALIGNMENT.CENTER

pred_headers = ['Test Record', 'Actual (MPa)', 'Predicted (MPa)', 'Absolute Error (MPa)']
for i, h in enumerate(pred_headers):
    pred_table.rows[0].cells[i].text = h
    for paragraph in pred_table.rows[0].cells[i].paragraphs:
        for run in paragraph.runs:
            run.bold = True

# Actual values from model execution
records = [
    ('1', '19.01', '23.46', '4.45'),
    ('2', '24.29', '16.70', '7.59'),
    ('3', '26.32', '22.45', '3.87'),
    ('4', '34.57', '37.40', '2.83'),
    ('5', '44.13', '42.89', '1.24'),
]

for row_idx, (num, actual, pred, err) in enumerate(records, 1):
    pred_table.rows[row_idx].cells[0].text = num
    pred_table.rows[row_idx].cells[1].text = actual
    pred_table.rows[row_idx].cells[2].text = pred
    pred_table.rows[row_idx].cells[3].text = err

doc.add_paragraph()

doc.add_heading('Model Performance', level=2)
p = doc.add_paragraph()
p.add_run('Mean Absolute Error (MAE): 8.90 MPa').bold = True
doc.add_paragraph(
    'On average, the model\'s predictions differ from the actual compressive strength by approximately '
    '8.90 MPa. Given that the test set strength values range from about 2 to 83 MPa, this indicates that '
    'the model captures the general trend but cannot precisely predict individual samples. The MAE is the '
    'average of all absolute differences between predicted and actual values.'
)
p2 = doc.add_paragraph()
p2.add_run('R² Score: 0.5802').bold = True
p2.add_run(
    ' — The model explains approximately 58.0% of the variance in compressive strength. '
    'The remaining 42% is due to non-linear relationships not captured by Linear Regression.'
)

# New sample
doc.add_heading('Prediction for a New Concrete Mix', level=2)
doc.add_paragraph(
    'A new concrete mix was defined using plausible values within the observed dataset ranges:'
)

new_table = doc.add_table(rows=9, cols=2)
new_table.style = 'Light Grid Accent 1'
new_table.alignment = WD_TABLE_ALIGNMENT.CENTER

new_headers = ['Input Feature', 'Value']
for i, h in enumerate(new_headers):
    new_table.rows[0].cells[i].text = h
    for paragraph in new_table.rows[0].cells[i].paragraphs:
        for run in paragraph.runs:
            run.bold = True

new_inputs = [
    ('Cement', '300.0 kg/m³'),
    ('Blast Furnace Slag', '100.0 kg/m³'),
    ('Fly Ash', '50.0 kg/m³'),
    ('Water', '180.0 kg/m³'),
    ('Superplasticizer', '6.0 kg/m³'),
    ('Coarse Aggregate', '1000.0 kg/m³'),
    ('Fine Aggregate', '750.0 kg/m³'),
    ('Age', '28 days'),
]

for row_idx, (feat, val) in enumerate(new_inputs, 1):
    new_table.rows[row_idx].cells[0].text = feat
    new_table.rows[row_idx].cells[1].text = val

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('Predicted Compressive Strength: 38.09 MPa').bold = True
doc.add_paragraph(
    'This is a model estimate, not a laboratory measurement. The predicted strength of 38.09 MPa '
    'is within the normal range for a concrete mix with 300 kg/m³ cement, moderate supplementary '
    'materials, and tested at 28 days. The actual strength in a real test may differ.'
)

# Limitation
doc.add_heading('Limitation', level=2)
doc.add_paragraph(
    'Linear Regression assumes that each input feature has a constant, additive effect on the target. '
    'In reality, concrete behaviour is non-linear — for instance, strength gain with age follows a '
    'logarithmic curve, and the effect of water depends on the water-to-cement ratio rather than the '
    'water content alone. Interaction effects between ingredients are also not captured. Non-linear '
    'models such as Random Forests or Neural Networks would likely achieve better accuracy.'
)

# ===================== 5. CONCLUSION =====================
doc.add_heading('5. Conclusion', level=1)
doc.add_paragraph(
    'This project demonstrated the complete machine learning workflow — from data acquisition and '
    'exploratory analysis to model training and evaluation. The UCI Concrete Compressive Strength '
    'dataset (1,030 records) was analysed, cleaned (25 duplicates removed), and used to train a '
    'Linear Regression model with an 80:20 train-test split. The model achieved a test MAE of '
    '8.90 MPa and an R² of 0.58, confirming that Linear Regression provides a reasonable baseline '
    'but is limited by the non-linear nature of concrete strength. The model successfully predicted '
    'a strength of 38.09 MPa for a new concrete mix, demonstrating its practical applicability as '
    'a first approximation.'
)

# Save
report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'concrete_strength_report.docx')
doc.save(report_path)
print(f"Report saved: {report_path}")
print(f"File size: {os.path.getsize(report_path)} bytes")
