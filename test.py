import requests
import json

# Define the URL of your FastAPI server
url = "https://nextjs-fastapi-framework-dp-auto.vercel.app/api/ahref/kd/"
# url = "https://next-fastapi-starter-demo.vercel.app/api/ahref/kd/"
# The keyword you want to send in the JSON body
keyword = "luma ai"

# The headers specify the content type of the request body
headers = {"Content-Type": "application/json"}

# The data to be sent in the body of the POST request
# It's a JSON string with a 'keywords' field that contains the keyword
data = json.dumps({"keywords": keyword})

# Define the proxy server URL (SOCKS5 in this case)
proxy_url = "socks5h://127.0.0.1:1080"

# Create the proxies dictionary
proxies = {
    "http": proxy_url,
    "https": proxy_url,
}

response = requests.post(
    url,
    headers=headers,
    data=data,
    proxies=proxies,
    #  sss, verify=False
)

# Check if the request was successful
if response.ok:
    # Parse the JSON response
    result = response.json()
    print("Success:", result)
else:
    # Print the status code and error message if the request failed
    print("Failed to fetch data:", response.status_code, response.text)
