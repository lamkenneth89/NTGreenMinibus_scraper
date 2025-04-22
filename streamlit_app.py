import streamlit as st
import pandas as pd
from scraper import generate_output  # Import the generate_output function

# Define the URLs and output file
urls_to_scrape = [
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A",
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A?from=087K%0A%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B487K%E7%B7%9A",
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A?from=812%0A%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4812%E7%B7%9A"
]
output_file = "minibus_vehicle_info.csv"

st.title("Minibus Data Downloader")

if st.button("Scrape and Download CSV"):
    with st.spinner("Scraping data and generating CSV..."):
        df_final = generate_output(urls_to_scrape, output_file)

        # Provide download button
        with open(output_file, "rb") as file:
            btn = st.download_button(
                label="Download CSV",
                data=file,
                file_name=output_file,
                mime="text/csv",
            )
    if btn:
        st.success(f"Data scraped and saved to {output_file}. Click above to download.")