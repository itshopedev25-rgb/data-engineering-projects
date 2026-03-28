import requests
from bs4 import BeautifulSoup
import boto3
import csv

# Step 1 — Open the webpage
url = "https://books.toscrape.com"
response = requests.get(url)

# Step 2 — Read the HTML
soup = BeautifulSoup(response.content, "lxml")

# Step 3 — Find all books
books = soup.find_all("article", class_="product_pod")

print(f"Found {len(books)} books\n")

# Step 4 — Save to CSV and print
with open('books.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Rating'])

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]

        # Print to screen
        print(f"Title:  {title}")
        print(f"Price:  {price}")
        print(f"Rating: {rating}")
        print("─" * 40)

        # Save to CSV at same time
        writer.writerow([title, price, rating])

# Step 5 — Upload CSV to S3
s3 = boto3.client('s3')
s3.upload_file(
    'books.csv',
    'my-app-photos-467117757131-us-east-1-an',
    'raw/books.csv'
)

print("Data uploaded to S3 successfully!")