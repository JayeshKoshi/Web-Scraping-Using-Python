import bs4
import urllib.request
import smtplib
import time
import datetime
import csv
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import PhotoImage
import tkinter.messagebox

# Create the main window
top = Tk()
top.geometry("612x408")
top.config(bg="black")
top.minsize(612, 408)
top.maxsize(612, 408)
top.title("Web Scraping")

# Load the background image
image = PhotoImage(file='black.png')
label = Label(top, image=image)
label.place(x=0, y=0, relwidth=1, relheight=1)

# Create the title label
title = Label(top, text="PRICE SCRAPER", font="comicsansms 30 bold underline", bg="black", fg="yellow")
title.place(x=155, y=10)

# Create the URL input label and entry
input_url = Label(top, text="ENTER THE URL", font="Arial 15", bg="black", fg="yellow")
input_url.place(x=240, y=100)
input_url_value = StringVar()
url_entry = Entry(top, textvariable=input_url_value, bg="black", fg="yellow", borderwidth=14, relief=SUNKEN)
url_entry.place(x=70, y=140, height=40, width=500)

# Create the desired price input label and entry
desire_price = Label(top, text="ENTER THE DESIRED PRICE ", font="Arial 15", bg="black", fg="yellow")
desire_price.place(x=185, y=190)
input_desire_price = StringVar()
inp_dp = Entry(top, textvariable=input_desire_price, bg="black", fg="yellow", borderwidth=14, relief=SUNKEN)
inp_dp.place(x=240, y=230, height=40, width=150)

# Function to check the price
def check_price():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        req = urllib.request.Request(input_url_value.get(), headers=headers)
        read_url = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code)
        return None

    parse = bs4.BeautifulSoup(read_url, 'html.parser')
    price_element = parse.find('span', {'class': ['a-offscreen', 'a-price-whole']})
    if price_element is not None:
        prices = price_element.get_text()
        prices = float(prices.replace(",", "").replace("₹", ""))
        title = parse.find('span', id="productTitle").get_text()
        date = datetime.date.today()
        prices_list.append(prices)
        price_label = Label(top, text=prices, bg="black", fg="yellow")
        price_label.place(x=320, y=300)
        print(prices, title, date)
        with open('prices.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Price', 'Date'])
            writer.writerow([title, prices, date])
    else:
        tkinter.messagebox.showerror("Error", "Price not found on the page")


def send_email(message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('jayeshtesting2405@gmail.com', 'pedehuczfozfeiwg')
    s.sendmail('jayeshtesting2405@gmail.com', 'jayeshkoshi@gmail.com', message)
    s.quit()


def price_decrease(prices_list):
    if prices_list[-1] < prices_list[-2]:
        return True
    else:
        return False


def button_clicked():
    url = url_entry.get()
    if not url:
        tkinter.messagebox.showerror("Error", "URL field is empty")
        return
    else:
        print(url)
        plot()

    count = 1

    while True:
        check_price()
        if count > 1:
            flag = price_decrease(prices_list)
            if flag:
                decrease = prices_list[-1] - prices_list[-2]
                message = f"The price has decreased by ₹{decrease}"
                send_email(message)
        time.sleep(2)
        count = count + 1


b1 = Button(fg="red", text="ENTER", command=button_clicked, bg="black", foreground="yellow")
b1.place(x=258, y=305, height=35, width=120)

prices_list = []

def plot():
    with open('prices.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(plots)
        x = []
        y = []
        for row in plots:
            x.append(row[2])
            y.append(row[1])
    plt.scatter(x, y)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price Scatter Plot')
    plt.show()

top.mainloop()
