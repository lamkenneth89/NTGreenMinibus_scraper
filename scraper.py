import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_minibus_routes(urls):
    route_list = []
    for url in urls:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', class_='category-page__member-link'):
            route_code = link.get_text(strip=True)
            route_url = 'https://hkbus.fandom.com' + link['href']
            route_list.append([route_code, route_url])
    df_routes = pd.DataFrame(route_list, columns=['Route Code', 'URL'])
    return df_routes

def scrape_vehicle_info(route_code, route_url):
    response = requests.get(route_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    target_section = soup.find('span', id='用車')
    if target_section:
        vehicle_table = target_section.find_next('table', class_='wikitable')
        if vehicle_table:
            rows = vehicle_table.find_all('tr')
            vehicle_data = []
            previous_seats = ""
            for row in rows[1:]:
                columns = row.find_all('td')
                if len(columns) >= 3:
                    vehicle_number = columns[0].get_text(strip=True)
                    seats = columns[2].get_text(strip=True) if len(columns) >= 3 and columns[2].get_text(strip=True) else previous_seats
                    vehicle_data.append([route_code, vehicle_number, seats])
                    previous_seats = seats
                elif len(columns) >= 2:
                    vehicle_number = columns[0].get_text(strip=True)
                    seats = previous_seats
                    vehicle_data.append([route_code, vehicle_number, seats])
            df_vehicle = pd.DataFrame(vehicle_data, columns=['Route Code', 'Vehicle Number', 'Seats'])
            return df_vehicle
    return pd.DataFrame(columns=['Route Code', 'Vehicle Number', 'Seats']) # Return empty DataFrame if no data found

def process_route_details(df_routes):
    all_vehicle_data = []
    for _, row in df_routes.iterrows():
        route_code, route_url = row['Route Code'], row['URL']
        df_vehicle = scrape_vehicle_info(route_code, route_url)
        if not df_vehicle.empty:
            all_vehicle_data.append(df_vehicle)
    df_all_vehicles = pd.concat(all_vehicle_data, ignore_index=True)
    return df_all_vehicles

def clean_and_extract_seats(df_vehicles):
    previous_seats = ""
    for index, row in df_vehicles.iterrows():
        if "座椅" not in row["Seats"]:
            df_vehicles.loc[index, "Seats"] = previous_seats
        previous_seats = row["Seats"]
    df_vehicles["Seats_edited"] = df_vehicles["Seats"].str.extract(r"(\d{2})")

    # Filter rows based on Vehicle Number format
    pattern = r"^[A-Z]{2}\d{3,4}$"  # Define the regex pattern
    df_vehicles = df_vehicles[df_vehicles["Vehicle Number"].str.match(pattern)]
    return df_vehicles

def generate_output(urls, output_file):
    df_routes = scrape_minibus_routes(urls)
    df_vehicles = process_route_details(df_routes)
    df_cleaned = clean_and_extract_seats(df_vehicles)
    df_final = pd.merge(df_cleaned, df_routes[['Route Code', 'URL']], on='Route Code', how='left')
    df_final.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Processed data saved to {output_file}")
    return df_final

# Example Usage
urls_to_scrape = [
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A",
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A?from=087K%0A%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B487K%E7%B7%9A",
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A?from=812%0A%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4812%E7%B7%9A"
]

output_file = "minibus_vehicle_info.csv"

df_final = generate_output(urls_to_scrape, output_file)