import pandas as pd


# def load_data(url):
#     """Load the dataset from a given URL"""
#     return pd.read_csv(url)


def standardize_column_names(df):
    """Standardize the column names by replacing 'ST' with 'state', converting to lower case, and replacing spaces with underscores"""
    df.columns = df.columns.str.replace('ST', 'state', regex=False)
    df.columns = df.columns.str.lower()   # Convert to lower case
    df.columns = df.columns.str.replace(' ', '_')   # Replace white spaces with underscores
    return df


def clean_gender_column(df):
    """Clean the 'gender' column by standardizing the values"""
    df['gender'] = df['gender'].replace({
        'Femal': 'F',
        'Male': 'M',
        'female': 'F'
    })
    return df


def clean_state_column(df):
    """Clean the 'state' column by replacing abbreviations with full names"""
    df['state'] = df['state'].replace({
        'Cali': 'California',
        'AZ': 'Arizona',
        'WA': 'Washington'
    })
    return df


def clean_education_column(df):
    """Clean the 'education' column by standardizing the values"""
    df['education'] = df['education'].replace({
        'Bachelors': 'Bachelor'
    })
    return df


# def clean_lifetime_value_column(df):
#     """Clean the 'lifetime_value' column by removing % character"""
#     df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%','')
#     return df


def clean_lifetime_value_column(df):
    """Clean the 'customer_lifetime_value' column by removing % character and converting to float"""
    # Ensure the column is of string type before replacing
    df['customer_lifetime_value'] = df['customer_lifetime_value'].astype(str).str.replace('%', '')
    
    # Optionally convert the cleaned column back to a numeric type
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')
    
    return df


def clean_vehicle_class_column(df):
    """Clean the 'vehicle_class' column by standardizing the values"""
    df['vehicle_class'] = df['vehicle_class'].replace({
        'Sports Car': 'Luxury',
        'Luxury SUV': 'Luxury',
        'Luxury Car': 'Luxury'
    })
    return df


def convert_customer_lifetime_value(df):
    """Convert 'Customer Lifetime Value' to numeric"""
    # errors='coerce': any value that cannot be converted to a numeric type will be replaced with NaN (Not a Number)
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')
    return df

def clean_number_of_open_complaints(df):
    """Clean 'Number of Open Complaints' by extracting the middle value and converting to numeric"""
    def extract_middle_value(complaint_string):
        if isinstance(complaint_string, str):
            parts = complaint_string.split('/')
            if len(parts) == 3:
                return int(parts[1])
        return None
        
    df['number_of_open_complaints'] = df['number_of_open_complaints'].apply(extract_middle_value)
    df['number_of_open_complaints'] = pd.to_numeric(df['number_of_open_complaints'], errors='coerce')
    return df


def handle_null_values(df):
    """Handle null values in the DataFrame"""
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = ['customer', 'state', 'education', 'policy_type', 'vehicle_class']  # all except 'gender'
    
    # Fill numeric columns with the median
    df[numeric_cols] = df[numeric_cols].apply(lambda col: col.fillna(col.median()))
    
    # Fill categorical columns with the mode
    for col in categorical_cols:
        if col in df.columns:  # Check if the column exists in the DataFrame
            df[col] = df[col].fillna(df[col].mode()[0])
    
    return df


def convert_numeric_to_integers(df):
    """Convert all numeric columns to integers"""
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].astype(int)
    return df


def remove_duplicates(df):
    """Remove duplicate rows from the DataFrame"""
    df_cleaned = df.drop_duplicates(keep='first')
    df_cleaned.reset_index(drop=True, inplace=True)
    return df_cleaned


def main(df):
    """Main function to perform all data cleaning and formatting."""
    # df = standardize_column_names(df)  # Standardize column names
    df = clean_gender_column(df)
    df = clean_state_column(df)
    df = clean_education_column(df)
    df = clean_lifetime_value_column(df)
    df = clean_vehicle_class_column(df)
    df = convert_customer_lifetime_value(df)
    df = clean_number_of_open_complaints(df)
    df = handle_null_values(df)
    df = convert_numeric_to_integers(df)
    df = remove_duplicates(df)

    # Save the cleaned DataFrame to a CSV file
    df.to_csv('cleaned_data.csv', index=False)
    
    return df