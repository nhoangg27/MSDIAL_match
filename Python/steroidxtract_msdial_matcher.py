#########################################
# This script is to match SteroidXtract predictions to MS-DIAL feature table in csv format.
# Nhi Hoang, Dec 12, 2024
# Copyright @ The University of British Columbia
#########################################

# Working directories
msdial_file = r'E:\SteroidXtract_MSDIAL\MS_DIAL.csv' # Processed feature table from MS-DIAL
input_dir = r'E:\SteroidXtract_MSDIAL\SteroidXtract_predictions' # Path to SteroidXtract predictions
output_dir = r'E:\SteroidXtract_MSDIAL\Output' # Output data path

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Parameter settings
rt_tol = 0.3 # RT tolerance in minutes
mz_tol = 0.01 # Precursor m/z tolerance

#########################################
# Libraries
import os
import pandas as pd
import glob
print('Libraries loaded')

# Load SteroidXtract predictions
os.chdir(input_dir)
files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

# Load MS-DIAL feature table
msdial_df = pd.read_csv(msdial_file)

# Ensure necessary columns exist in MS-DIAL file
if 'Prediction' not in msdial_df.columns:
    msdial_df['Prediction'] = 0
if 'Source Files' not in msdial_df.columns:
    msdial_df['Source Files'] = ''

# Process files and match predictions
for l in range(len(files)):
    print(l)
    print('New file loaded')
    
    # Read csv file
    os.chdir(input_dir)
    xtract_file = files[l]
    print(files[l])
    xtract_df = pd.read_csv(xtract_file)

    # Filter for predictions > 0.5
    filtered_pred = xtract_df[xtract_df['prediction'] > 0.5]

    # Iterate through each row in the filtered output
    for _, row in filtered_pred.iterrows():
        rt, precursor_mz, prediction = row['rt'], row['precursor_MZ'], row['prediction']

        # Find matching features in MS-DIAL feature table based on tolerances
        matches = msdial_df[
            (msdial_df['Average Rt(min)'].between(rt - rt_tol, rt + rt_tol)) &
            (msdial_df['Average Mz'].between(precursor_mz - mz_tol, precursor_mz + mz_tol))
        ]

        # Update the 'Prediction' column and track source files
        for match_index in matches.index:
            current_prediction = msdial_df.at[match_index, 'Prediction']
            current_sources = msdial_df.at[match_index, 'Source Files']
            msdial_df.at[match_index, 'Prediction'] = max(current_prediction, prediction)
            updated_sources = set(current_sources.split('; ') if current_sources else [])
            updated_sources.add(xtract_file[0:-4])
            msdial_df.at[match_index, 'Source Files'] = '; '.join(sorted(updated_sources))

# Save the updated MS-DIAL file
os.chdir(output_dir)
updated_file_path = "updated_msdial_file.csv"
msdial_df.to_csv(updated_file_path, index=False)

# Create and save a file with positive predictions only
positive_predictions_df = msdial_df[msdial_df['Prediction'] > 0]
positive_file_path = "positive_predictions.csv"
positive_predictions_df.to_csv(positive_file_path, index=False)

print(f"MS-DIAL file updated successfully: {updated_file_path}")
print(f"Positive predictions file created: {positive_file_path}")
