import json

file_path = "notebooks/01_eda_and_modeling.ipynb"
with open(file_path, "r", encoding="utf-8") as f:
    notebook = json.load(f)

for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'ठीक है' in source or 'For Add student' in source:
            cell['cell_type'] = 'markdown'
            # Or we can just comment it out, or remove it entirely
            # Actually, looking at the IDE errors, it might be the very first cell.
            # I will just convert the cell to markdown if it contains these non-python texts.
            pass
        
        # Add imports if missing? The IDE errors might be coming from other cells missing imports.
        # Let's just prepend a new cell with all missing imports.

missing_imports = """import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
"""

notebook['cells'].insert(0, {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\n" for line in missing_imports.split("\n")[:-1]]
})

# Let's fix the first cell which has the Hindi text. 
# It seems someone pasted a chat completion directly. 
# Let's find it and turn it to markdown.
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        if len(cell['source']) > 0 and 'ठीक' in cell['source'][0]:
            cell['cell_type'] = 'markdown'

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("Notebook fixed.")
