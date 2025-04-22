import streamlit as st
import pandas as pd
from scraper import generate_output  # Import the generate_output function
import tempfile
import os


DEFAULT_URLS = """https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A
https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A?from=087K%0A%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B487K%E7%B7%9A
https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A?from=812%0A%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4812%E7%B7%9A"""

st.title("Minibus Data Downloader")

urls_input = st.text_area(
    "Enter URLs to scrape (one per line, max 3):",
    value=DEFAULT_URLS,
    height=150,
)

urls_to_scrape = [url.strip() for url in urls_input.split("\n") if url.strip()]

if len(urls_to_scrape) > 3:
    st.warning("You have entered more than 3 URLs. Only the first 3 will be used.")
    urls_to_scrape = urls_to_scrape[:3]

output_format = st.radio("Select output format:", ["CSV", "Excel"], index=0)

if st.button("Scrape and Download"):
    if not urls_to_scrape:
      st.warning("Please enter at least one url!")
    else:
      with st.spinner("Scraping data and generating file..."):
        file_extension = "csv" if output_format == "CSV" else "xlsx"
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmpfile:
            df_final = generate_output(urls_to_scrape, tmpfile.name)
            if df_final is not None:
                
                if output_format == "CSV":                    
                    file_name = "minibus_vehicle_info.csv"
                    mime = "text/csv"
                    tmpfile.close()
                    with open(tmpfile.name, "rb") as file:
                        data_to_download = file.read()
                else:                    
                    for col in df_final.columns:
                      if df_final[col].dtype == 'object':
                        df_final[col] = df_final[col].str.encode('utf-8', errors='ignore').str.decode('utf-8')
                    df_final.to_excel(tmpfile, index=False, engine='openpyxl')
                    tmpfile.seek(0)
                    file_name = "minibus_vehicle_info.xlsx"
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" 
                    data_to_download = tmpfile.read()             
                st.success(f"Data scraped and saved as {file_name}. Click below to download.")
                btn = st.download_button(
                    label=f"Download {output_format}",
                    data=data_to_download,
                    file_name=file_name,
                    mime=mime,
                )
                os.remove(tmpfile.name)