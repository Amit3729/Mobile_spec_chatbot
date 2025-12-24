import pandas as pd
import re

from feature_engineering import (
    convert_price_to_npr,
    create_price_segment,
    calculate_gaming_score,
    create_battery_category,
    build_description,
)

DATA_PATH = '/Users/spkunwar/Desktop/untitled folder/Mobile_spec_chatbot/my-product-rag-app/data/Mobiles Dataset (2025).csv'

def load_csv(path)->pd.DataFrame:
    print('Loading data..........')
    df= pd.read_csv(path,encoding='latin1')
    print(f'Loaded : {df.shape[0]} rows and {df.shape[1]} columns')
    return df

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    print("Cleaning Data")
    #Remove duplicate rows
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f'Removed {before - after} duplicate rows')
    

    #standarized the columns
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(' ', '_')

    )
    df = df.rename(columns={
        "company_name": "brand",
        "model_name": "model"
    })

    #Handel missiog values
    missing_values = df.isnull().sum().sum()
    print(f'Misssing value is {missing_values}')
    if missing_values > 0:
        df = df.fillna({
            'company name':'Unknown',
            'model name' : 'Unknown',
            'processor':'Unknown',
            'ram' : '0 GB',
            'storage' : '0 GB',


        })
    else:
        pass
    return df

def extract_storage(model):
    matches = re.findall(r'(\d+)\s*(gb|tb|mb|g\s*b|t|m\s*b)',str(model),re.IGNORECASE)

    if matches:
        size, unit = matches[0]
        #clean unit
        unit = unit.lower().replace(' ','')
        if unit.startswith('g'):
            unit = 'GB'
        elif unit.startswith('t'):
            unit = 'TB'
        elif unit.startswith('m'):
            unit = 'MB'
        return f'{size} {unit}'
    return None

#Apply function



def save_clean_csv(df : pd.DataFrame, path:str):
    df.to_csv(path,index=False)
    print(f'Clean csv saved to {path}')



def main():
    df=load_csv(DATA_PATH)
    df = clean_data(df)
    df['storage'] = df['model'].apply(extract_storage)
    #remove storage from mode_name columns
    # df['model_name'] = df['model_name'].str.replace(r'\s*\d+\s*(?:GB|TB|MB).*','',flags=re.IGNORECASE).str.strip()
    df = convert_price_to_npr(df)
    df = create_price_segment(df)
    df = calculate_gaming_score(df)
    df = create_battery_category(df)
    df['description_text'] = df.apply(build_description, axis=1)



    print(df.head())
    save_clean_csv(df, 'data/clean_data.csv')

if __name__ == '__main__':
    main()