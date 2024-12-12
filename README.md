# SteroidXtract&ndash;MS-DIAL Matcher

This repository contains a Python script to match SteroidXtract predictions to features identified in MS-DIAL.

## Overview
The script processes:
- A **processed MS-DIAL feature table** (CSV format).
- **SteroidXtract predictions** (CSV format) located in a specified directory.

It identifies matching features based on:
- **Retention time (RT)** tolerance.
- **Precursor m/z** tolerance.

**Outputs:**
1. An updated MS-DIAL feature table with added prediction scores and source file tracking.
2. A filtered feature table containing positive predictions only.

## Data

The `Data` folder contains demo data for testing the script:
- **Output**: Output directory with results.
- **SteroidXtract_prediction**: SteroidXtract prediction files.
- **MS-DIAL.csv**: Sample processed MS-DIAL feature table.

In the processed MS-DIAL feature table:
- **MB = GOOD** means that the maximum intensity across all samples for a feature is greater than three times the intensity of the method blank.
- **RT = GOOD** means that the feature elutes before 23 minutes, which is when the gradient ends.

## Usage
### Input Parameters
- **`msdial_file`**: File path to the processed MS-DIAL feature table (CSV format).
- **`input_dir`**: Directory containing SteroidXtract prediction files (CSV format).
- **`output_dir`**: Directory where output files will be saved.
- **`rt_tol`**: Retention time tolerance in minutes.
- **`mz_tol`**: Precursor m/z tolerance.

### How the Script Works
1. Loads the MS-DIAL feature table and ensures the necessary columns exist.
2. Iterates through all SteroidXtract prediction files in the input directory.
3. Matches predictions with MS-DIAL features based on RT and precursor m/z tolerances.
4. Updates the MS-DIAL feature table with the highest prediction score and source file tracking.
5. Saves:
   - An updated MS-DIAL feature table.
   - A filtered table containing features with positive predictions.

### Example Input Parameters
```python
msdial_file = r'E:\SteroidXtract_MSDIAL\MS_DIAL.csv'
input_dir = r'E:\SteroidXtract_MSDIAL\SteroidXtract_predictions'
output_dir = r'E:\SteroidXtract_MSDIAL\Output'

rt_tol = 0.3  # RT tolerance in minutes
mz_tol = 0.01 # Precursor m/z tolerance
```

## Outputs
1. **`updated_msdial_file.csv`**: Updated MS-DIAL feature table.
2. **`positive_predictions.csv`**: Table of features with positive predictions only.

## Dependencies
- **Python 3.x**
- Libraries: `os`, `pandas`, `glob`

Install dependencies using:
```bash
pip install pandas
```

## Running the Script
Run the script in your terminal or IDE:
```bash
python steroidxtract_msdial_matcher.py
```
