"""
Execute the notebook from top to bottom and save with outputs.
"""
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

notebook_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'concrete_strength_analysis.ipynb'
)

print(f"Loading notebook: {notebook_path}")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Execute the notebook
ep = ExecutePreprocessor(timeout=120, kernel_name='python3')

# Set the working directory to the project root
cwd = os.path.dirname(os.path.abspath(__file__))
print(f"Execution directory: {cwd}")

try:
    ep.preprocess(nb, {'metadata': {'path': cwd}})
    print("Notebook executed successfully!")
except Exception as e:
    print(f"Execution failed: {e}")
    raise

# Save the notebook with outputs
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Notebook saved with outputs: {notebook_path}")
