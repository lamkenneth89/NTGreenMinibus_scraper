from flask import Flask, render_template, send_file
import os
from scraper import generate_output  # Import the generate_output function

app = Flask(__name__)

# Define the URLs and output file
urls_to_scrape = [
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A",
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A?from=087K%0A%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B487K%E7%B7%9A",
    "https://hkbus.fandom.com/wiki/%E5%88%86%E9%A1%9E:%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4%E8%B7%AF%E7%B7%9A?from=812%0A%E6%96%B0%E7%95%8C%E5%B0%88%E7%B6%AB%E5%B0%8F%E5%B7%B4812%E7%B7%9A"
]
output_file = "minibus_vehicle_info.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download_csv():
    generate_output(urls_to_scrape, output_file)
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!DOCTYPE html>
<html>
<head>
    <title>Minibus Data Downloader</title>
</head>
<body>
    <h1>Download Minibus Vehicle Information</h1>
    <p>Click the button below to scrape the data and download the CSV file.</p>
    <a href="/download">
        <button>Download CSV</button>
    </a>
</body>
</html>