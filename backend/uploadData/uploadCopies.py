import random
import pymysql
from dotenv import load_dotenv
import os
from uuid import uuid4


# Load .env file
load_dotenv()

# MySQL config
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USERNAME'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.Cursor  # or DictCursor if you need dicts
}

# Connect to the MySQL database
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# Fetch books
cursor.execute("SELECT * FROM books")
books = cursor.fetchall()

copies = []
for book in books:
    num_copies = random.randint(1, 5)
    for i in range(num_copies):
        book_isbn = book[0]  # Assuming first column is ISBN
        copy_number = i + 1
        bookcopy_id = str(uuid4())
        copies.append((bookcopy_id, book_isbn, copy_number))
        print(f"Book ISBN: {book_isbn}, Copy Number: {copy_number}")

# Insert into book_copies table
query = """
    INSERT INTO bookcopies (id, book_id, copy_number)
    VALUES (%s, %s, %s)
"""
try:
    cursor.executemany(query, copies)
    conn.commit()
    print(f"✅ Finished adding {len(copies)} copies.")
except pymysql.MySQLError as e:
    conn.rollback()
    print(f"❌ Error occurred: {e}")

# Clean up
cursor.close()
conn.close()
