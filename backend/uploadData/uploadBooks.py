import csv
import pymysql
from uuid import uuid4
import random
import dotenv
import os

# Load environment variables from .env
dotenv.load_dotenv()

# List of publishers
publishers = [
    "Pearson", "McGraw Hill", "MIT Press", "Prentice Hall", "Wiley", "No Starch Press",
    "Oxford University Press", "Cambridge University Press", "O'Reilly Media", "Springer"
]

# MySQL connection parameters using PyMySQL
conn = pymysql.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USERNAME'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DB'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

# Read and insert books from CSV
with open("books_dataset.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        print(row)
        isbn = str(uuid4())
        title = row.get("Title")
        author = row.get("Author")
        published_year = int(row['Published Year']) if row.get('Published Year')!='N/A' else None
        publisher = random.choice(publishers)
        image_url = row.get("Cover URL")
        genre = row.get("Subject")
        language = row.get("Language")

        query = """
            INSERT INTO books (isbn, title, author, published_year, publisher, image_url, genre, language)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (isbn, title, author, published_year, publisher, image_url, genre, language)

        try:
            cursor.execute(query, data)
            conn.commit()
            count += 1
            print(f"{count}. Book added: {title}")
        except pymysql.MySQLError as e:
            conn.rollback()
            print(f"❌ Error: {e} - Skipped book: {title}")

cursor.close()
conn.close()

print(f"\n✅ Done: {count} books added successfully.")
