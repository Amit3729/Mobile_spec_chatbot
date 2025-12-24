import pandas as pd
import numpy as np
import re

#Exchnage rate
INR_TO_NPR = 1.6

def extract_amount(text): #Extract numeric value from price string
    cleaned = re.sub(r'[^\d.,]', '',str(text))
    cleaned = cleaned.replace(',','')

    try:
        return float(cleaned)
    except ValueError:
        return None
    
def convert_price_to_npr(df:pd.DataFrame)->pd.DataFrame:
    df['amount_inr'] = df['launched_price_(india)'].apply(extract_amount)
    df['amount_npr'] = df['amount_inr'] * INR_TO_NPR
    df['launched_price_(nepal)'] = df['amount_npr'].apply(
        lambda x : f'NPR {x:,.1f}' if pd.notna(x) and x > 0 else 'NPR N/A'
    )
    return df

def create_price_segment(df:pd.DataFrame)->pd.DataFrame:
    print('PRICE SEGMENTATION')
    print('-'*50)
    def get_segment(price):
        if pd.isna(price) or price == 0:
            return "Unknow"
        elif price < 20000:
            return 'Budget'
        elif price < 50000:
            return 'Mid-Range'
        else:
            return 'Premium'
    
    df['price_segment'] = df['amount_npr'].apply(get_segment)
    print('\nPrice Segment Distribution')
    print(df['price_segment'].value_counts())
    return df

def extract_ram_gb(ram_text):
    if pd.isna(ram_text): 
        return None
    
    #find number
    match = re.search(r'(\d+)', str(ram_text))
    if match:
        return int(match.group(1))
    return None

def calculate_gaming_score(df : pd.DataFrame)-> pd.DataFrame:
    print("Gaming Score")

    df['ram_gb'] = df['ram'].apply(extract_ram_gb)
    def get_gaming_score(ram_gb):
        if ram_gb <= 2:
            return 3
        elif ram_gb <= 4:
            return 5
        elif ram_gb == 6:
            return 7
        elif ram_gb == 8:
            return 9
        else:
            return 10
    
    df['gaming_score'] = df['ram_gb'].apply(get_gaming_score)
    return df

#Create Battery Category:
def extract_battery_mah(battery_text):
    if pd.isna(battery_text):
        return None
    
    #Find numbers(usally in format'4000mah' or '4000 mah')
    match = re.search(r'(\d+)',str(battery_text))
    if match:
        return int(match.group(1))
    return 0

def create_battery_category(df : pd.DataFrame)->pd.DataFrame:
    print('BATTERY CATEGORY')
    #Extract battery capacity
    df['battery_mah'] = df['battery_capacity'].apply(extract_battery_mah)

    def get_battery_category(mah):
        if mah == 0:
            return 'Unknown'
        elif mah < 4000:
            return 'Low'
        elif mah <=5000:
            return 'Medium'
        else:
            return 'High'
    df['battery_category'] = df['battery_mah'].apply(get_battery_category)
    return df

def build_description(row):
    return (
        f"{row['brand']} {row['model']} smartphone with "
        f"{row['ram_gb']}GB RAM, "
        f"{row['battery_mah']}mAh battery, "
        f"price category {row['price_segment']}. "
        f"Gaming score {row['gaming_score']} out of 10."
    )

    

    
