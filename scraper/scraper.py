import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, jsonify

# URL of the Anayasa Mahkemesi üyeleri page
members_url = "https://www.anayasa.gov.tr/tr/baskanvekilleri-ve-uyeler/uyeler/"
source_url = "https://www.anayasa.gov.tr"
subsource_url = members_url

# Fetch the page content, ignoring SSL verification
response = requests.get(members_url, verify=False)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all divs containing the members
members = soup.find_all('div', class_='col-lg-2 col-md-2 col-sm-4 col-6')

# Initialize a list to hold the member data
member_data = []

# Loop through each member div and extract the name
for member in members:
    name = member.find('h3').get_text(strip=True)
   
    # Split the name into first name and last name
    name_parts = name.split()
    first_name = " ".join(name_parts[:-1])
    last_name = name_parts[-1]
   
    # Append the extracted data to the list
    member_data.append([first_name, last_name, 'Anayasa Mahkemesi Üyesi'])

# Convert the list to a DataFrame
members_df = pd.DataFrame(member_data, columns=['İsim', 'Soyisim', 'Ünvan'])

# Add additional columns to match the existing CSV structure
members_df['ID'] = range(1, len(members_df) + 1)
members_df['Sektör'] = 'Siyaset'
members_df['Source'] = source_url
members_df['Subsource'] = subsource_url

# Reorder the columns to match the final CSV structure
members_df = members_df[['ID', 'İsim', 'Soyisim', 'Ünvan', 'Sektör', 'Source', 'Subsource']]

# Save the DataFrame to a new CSV file
final_csv_path = 'data3.csv'
members_df.to_csv(final_csv_path, index=False)

# Flask API to serve the CSV data
app = Flask(__name__)

@app.route('/get-data', methods=['GET'])
def get_data():
    data = members_df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

print("Yeni CSV dosyası 'data3.csv' olarak kaydedildi.")
