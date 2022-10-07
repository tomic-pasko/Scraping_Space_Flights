from bs4 import BeautifulSoup
import requests  # Importing the HTTP library
from spaceFlights import SpaceFlights
import csv

url = 'https://nextspaceflight.com/launches/past/?search='
# XPATH of button element LAST >>
xpath = "/html/body/div/div/main/div/div[2]/div[2]/span/div/button[2]"


# Example of page with number, https://nextspaceflight.com/launches/past/?page=2&search=

# Get number of pages from new_url
Webpage = SpaceFlights(url, xpath)
new_url = Webpage.get_new_url()
num_pages = int(new_url.split("=")[1][:3])

organisations = []
locations = []
dates = []
details = []
mission_status = []
rocket_status = []
price = []

for i in range(num_pages):
    url = "https://nextspaceflight.com/launches/past/?page=" + f"{i+1}" + "&search="

    # Requesting for the website
    Web = requests.get(url)
    # Creating a BeautifulSoup object and specifying the parser
    soup = BeautifulSoup(Web.text, 'html.parser')

    # Get Organisation names from prepared soup
    organisation = soup.select(".mdl-card__title-text")
    # nested divs with same class --> .mdl-card__title-text, everything is duplicated, take every second element
    organisation_v2 = organisation[::2]
    for org in organisation_v2:
        organisations.append(org.find_all("span")[0].getText().strip())

    # Get Location and Date from prepared soup
    locations_dates = soup.select(".mdl-card__supporting-text")
    for tag in locations_dates:
        dates.append(tag.getText().strip().split("\n")[0])
        if len(tag.getText().strip().split("\n")) > 2:
            locations.append(tag.getText().strip().split("\n")[3].strip())
        else:
            locations.append(tag.getText().strip().split("\n")[1])
        #locations.append(tag.getText().strip().split("\n")[1])

    # Get Detail from prepared soup
    detail = soup.find_all("h5")
    for tag in detail:
        details.append(tag.getText().replace("\n", '').strip())

    #Get Rocket Status, Price and Mission Status from details button on every card
    missions_in_page = soup.select('h5')
    mission_details_link_soup = soup.select('.mdc-button:first-child')
    for i in range(len(missions_in_page)):

        # onclick="location.href = '/launches/details/4337'"
        # to construct link (about launch details) number at the end is needed (4337)

        mission_details_link_num = mission_details_link_soup[i].get('onclick')[35:-1]
        response = requests.get(f"https://nextspaceflight.com/launches/details/{mission_details_link_num}")
        soup = BeautifulSoup(response.text, 'html.parser')

        rocket_status.append(
            soup.select_one('.a:first-child .mdl-cell:nth-of-type(2)').getText(strip=True).split(": ")[1])
        mission_status.append(soup.select_one(".status").getText(strip=True))
        price_value = soup.select_one('.a:first-child .mdl-cell:nth-of-type(3)').getText(strip=True)[8:-8]
        try:
            price_val = float(price_value)
            price.append(price_val)
        except ValueError:
            price.append('')

# Create csv file from gathered data

header = ['Unnamed: 0', 'Organisation', 'Location', 'Date', 'Detail', 'Rocket_Status', 'Price', 'Mission_Status']
rows = []

for i in range(len(details)):
    rows.append([i, organisations[i], locations[i], dates[i], details[i], rocket_status[i], price[i], mission_status[i]])

with open('mission_launches.csv', 'w', newline='', encoding="utf-8") as f:
    csv_writer = csv.writer(f)

    # write header
    csv_writer.writerow(header)
    # write rows
    csv_writer.writerows(rows)





