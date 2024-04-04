import pandas as pd
from datacleaner import autoclean
import numpy as np

file1_path = '/Users/kavinjindel2004/Desktop/file_3_Mar18_Output_1.csv'
file2_path = '/Users/kavinjindel2004/Desktop/file_4_Mar18_Output_1.csv'
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

df = pd.concat([df1, df2])
# df = autoclean(merged_df, drop_nans=False)
# Convert date columns to datetime and extract relevant time-related features
date_columns = ['account_open_date_13_march', 'account_open_date_18_march']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce', format='%m/%d/%Y')

# Check for duplicate rows and remove them
df.drop_duplicates(inplace=True)

# Handle missing values
# For categorical variables: Replace missing values with 'UNKNOWN' or the most frequent value
categorical_cols = ['account_status_13_march', 'card_activation_status_13_march', 'ebill_enrolled_status_13_march',
                    'auto_pay_enrolled_status_13_march', 'account_status_18_march', 'card_activation_status_18_march', 
                    'ebill_enrolled_status_18_march', 'auto_pay_enrolled_status_18_march']
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# For numerical variables: Replace missing values with the median
numeric_cols = ['no_of_accounts_with_syf_13_march', 'account_balance_13_march', 'account_balance_18_march']
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Outlier detection and handling for 'account_balance' columns
# Define a function to detect outliers using IQR
def detect_outliers_iqr(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data < lower_bound) | (data > upper_bound)]

# Apply the function to 'account_balance' columns
for col in ['account_balance_13_march', 'account_balance_18_march']:
    outliers_indices = detect_outliers_iqr(df[col]).index
    df.loc[outliers_indices, col] = np.nan  # replace outliers with NaN
    df[col].fillna(df[col].median(), inplace=True)  # replace NaN with median

# Encode categorical variables if needed (e.g., Label Encoding, One-Hot Encoding)
# ...
# Create new feature 'tenure_days' as the number of days since the account was opened
current_date = pd.to_datetime('today')
df['tenure_days_13_march'] = (current_date - df['account_open_date_13_march']).dt.days
df['tenure_days_18_march'] = (current_date - df['account_open_date_18_march']).dt.days

# Delinquency history: Convert to a binary variable (0 for current, 1 for past due)
df['delinquency_binary_13_march'] = df['delinquency_history_13_march'].apply(lambda x: 0 if '[00]' in str(x) else 1)
df['delinquency_binary_18_march'] = df['delinquency_history_18_march'].apply(lambda x: 0 if '[00]' in str(x) else 1)

# Ensure 'eservice_ind' is binary as per the problem statement
df['eservice_ind_13_march'] = df['eservice_ind_13_march'].apply(lambda x: 1 if x == 1 else 0)
df['eservice_ind_18_march'] = df['eservice_ind_18_march'].apply(lambda x: 1 if x == 1 else 0)

# Drop columns not needed for analysis or columns with excessive missing values
# df.drop(columns=['column_to_drop'], inplace=True)

# Final check for missing values and types
print(df.info())
print(df.isnull().sum())
print(df)
df = autoclean(df, drop_nans=False)
# Save the cleaned dataset to a new CSV file
cleaned_file_path = '/Users/kavinjindel2004/Desktop/cleaned_datasetfinal.csv'
df.to_csv(cleaned_file_path, index=False)

print(f"The cleaned dataset has been saved to {cleaned_file_path}.")