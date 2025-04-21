import csv
from backend.config import db, app
from backend.models import Books

with app.app_context():
    with open("Books.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in list(reader)[1:]:
            book = Books(
                isbn=row[0],
                title=row[1],
                author=row[2],
                published_year=int(row[3]),
                publisher=row[4],
                image_url=row[5],
                genre=row[6]
            )
            db.session.add(book)
            print(row)

    db.session.commit()
    print("Books added successfully!")
