# Define the range for the IDs
start_id = 12312
end_id = 1012311

# Define the base URL
base_url = "http://localhost:8000/api/orders/"

# Generate the list of URLs
urls = [f"{base_url}{id}/" for id in range(start_id, end_id + 1)]

# If you want to save the URLs to a file:
with open("urls.txt", "w") as file:
    for url in urls:
        file.write(url + "\n")
