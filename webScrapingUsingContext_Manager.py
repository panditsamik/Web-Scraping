import ssl
import time
import requests
import selectorlib
import smtplib

url = "https://programmer100.pythonanywhere.com/tours/"


def scrape():
    response = requests.get(url)
    data = response.text
    return data


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    extract = extractor.extract(source)["tours"]
    return extract


def read():
    with open("data.txt", "r") as file:
        return file.read()


def store(extracted):
    with open("data.txt", "w") as file:
        file.write(extracted + "\n")


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
        content = read()
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(f"Hey! New event was found.\n{extracted}")
        time.sleep(60)
