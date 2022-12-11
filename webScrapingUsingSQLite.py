import ssl
import time
import requests
import selectorlib
import smtplib
import sqlite3

url = "https://programmer100.pythonanywhere.com/tours/"
connection = sqlite3.connect("data.db")


def scrape():
    response = requests.get(url)
    data = response.text
    return data


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    extract = extractor.extract(source)["tours"]
    return extract


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "samikpandit02@gmail.com"
    password = "vdjycfiezbrnonlz"

    receiver = "samikpandit02@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


if __name__ == "__main__":
    while True:
        scraped = scrape()
        extracted = extract(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(f"Hey! New Event was found.\n{extracted}")
        time.sleep(1)
