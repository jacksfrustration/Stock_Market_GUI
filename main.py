import requests
from tkinter import messagebox
import pyperclip
from tkinter import *
import json


data_dict=[]

#read json file and save the data in a list of dictionaries
with open("company_id.json","r")as file:
    data=json.load(file)['data']
#save the data in a new list of dictionaries saving only name and symbol of companies
data_dict=[{"name":datum[1],
            "symbol":datum[2]
            } for datum in data]
#api keys have been removed because they are sensitive information
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY="#################################"
NEWS_API_KEY="############################"

def get_news():
    '''Uses the news api to search for articles with titles that have the company name in them
    creates a new list of article titles and URLs and asks the user which article he/she would like to read
    copies the url link to clipboard when the article gets chosen and stops the iteration through the article list'''
    news_params = {

        "apiKey": NEWS_API_KEY,
        "q": company_name_ent.get(),
        "searchIn": "title"
    }
    new_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles=new_response.json()["articles"]

    new_list=[{"title":article['title'],"url":article['url']} for article in articles]
    for el in new_list:
        if messagebox.askokcancel(title="Retrieve article URL link",message=f"Article Title: {el['title']}\nWould you like to copy this URL in order to read the article?"):
            pyperclip.copy(el['url'])
            return None


def check_stock_prices():
    '''checks if company name exists in the company_id json file
    if it exists it grabs the corresponding symbol and uses that symbol to access the information available
    gets the latest 2 dates from the api call into a list and uses the dates to retrieve the closing prices for those dates
    finally outputs the closing prices of the company in the stock market for the 2 chosen dates and also outputs the percentage
    difference between the two dates. if the company name does not exist an appropriate error message is generated'''
    found=False
    for data in data_dict:
        if data["name"]==company_name_ent.get().title():
            cur_sym=data["symbol"]
            found=True
    if found:
        stock_params={
            "function":"TIME_SERIES_DAILY",
            "symbol":cur_sym,
            "apikey":STOCK_API_KEY
        }
        response=requests.get(STOCK_ENDPOINT,params=stock_params)
        dates=list(response.json()["Time Series (Daily)"].keys())
        yesterdays_data=response.json()["Time Series (Daily)"][dates[0]]
        day_before_data=response.json()["Time Series (Daily)"][dates[1]]
        diff_percentage=round((float(yesterdays_data['4. close']) / float(day_before_data['4. close'])) * 100,2)
        messagebox.showinfo(title=f"{dates[0]} - {dates[1]} Data",message=f"Yesterday's closing price was ${round(float(yesterdays_data['4. close']),2)}\n"
                                                                 f"Day before's closing price was ${round(float(day_before_data['4. close']),2)}\n"
                                                                          f"There was a {round(diff_percentage,2)}% difference between the two dates")
    else:
        messagebox.showerror(title="Ooops",message="Company name not found")


window=Tk()
window.title("Stock Market App")
canvas=Canvas(window,width=529,height=355)
bg_pic=PhotoImage(file="getty-stock-market-data-3742641520.png")
bg=canvas.create_image(265,178,image=bg_pic)
canvas.grid(row=0,column=0,columnspan=3)
company_name_lbl=Label(text="Enter Company Name: ")
company_name_lbl.grid(row=1,column=0)

company_name_ent=Entry()
company_name_ent.grid(row=1,column=1)

yesterdays_data_but=Button(text="Get Yesterdays data",command=check_stock_prices)
yesterdays_data_but.grid(row=1,column=2)
news_articles_but=Button(text="Get news articles",command=get_news)
news_articles_but.grid(row=2,column=1)
window.mainloop()

