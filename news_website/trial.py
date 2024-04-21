import requests

# URL of the BBC News website
url = 'https://www.bbc.com/news'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the HTML content of the webpage
    print(response.text)
else:
    print('Failed to retrieve data from the BBC News website. Status code:', response.status_code)
