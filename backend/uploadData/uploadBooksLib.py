import requests
import csv
import time

subjects = ['Algorithms', 'Artificial Intelligence', 'C Programming', 'Chemistry', 'Civil Engineering',
            'Compiler Design', 'Computer Networks', 'Computer Science', 'Control Systems', 'Data Structures',
            'Database Systems', 'Digital Logic', 'Electronics', 'Java Programming', 'Machine Learning', 'Mathematics',
            'Mechanical Engineering', 'Networking', 'Operating Systems', 'Physics', 'Programming', 'Python Programming',
            'Software Engineering']


def fetch_books_for_subject(subject, limit=10):
    url = "https://openlibrary.org/search.json"
    params = {"q": subject, "limit": limit}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch data for {subject}")
        return []

    data = response.json()
    books = []

    for book in data.get("docs", []):
        author = book.get("author_name", ["Unknown"])[0]
        cover_id = book.get("cover_i")
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else ""

        book_info = {
            "Subject": subject,
            "Title": book.get("title", "No Title"),
            "Author": author,
            "Language": ', '.join(book.get("language", ["Unknown"])),
            "Published Year": book.get("first_publish_year", "N/A"),
            "Cover URL": cover_url,
        }

        books.append(book_info)

    print(f"✅ {len(books)} books fetched for {subject}")
    return books


def generate_books_csv(filename="all_subject_books.csv", limit_per_subject=10):
    all_books = []

    for subject in subjects:
        books = fetch_books_for_subject(subject, limit=limit_per_subject)
        all_books.extend(books)
        time.sleep(0.5)  # Respectful delay to not hammer the API

    if not all_books:
        print("No books found at all.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=all_books[0].keys())
        writer.writeheader()
        writer.writerows(all_books)

    print(f"\n📘 Done! {len(all_books)} books saved to '{filename}' 🎉")


# Launch the book hunt
generate_books_csv("books_dataset.csv", limit_per_subject=10)
