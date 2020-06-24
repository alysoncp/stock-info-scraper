# Webscraper experiments

#2020 June 20th


import csv
from pprint import pprint
import requests
import bs4
from bs4 import BeautifulSoup

def getSummary(ticker):
    #Fancy soup scraping stuff
    pr = requests.get('https://ca.finance.yahoo.com/quote/'+str(ticker))
    soup=bs4.BeautifulSoup(pr.text, features="html.parser" )
    #Specific data pulled
    price=soup.find('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    sumData = {
        "Price" : price
        }
    return sumData

def getStats(ticker):
    pull = requests.get('https://ca.finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker)
    soup=bs4.BeautifulSoup(pull.text, features="html.parser" )
    tablepath = 'table',{'class':"W(100%) Bdcl(c)"}
    rowpath = 'tr',{'class':"Bxz(bb) H(36px) BdB Bdbc($seperatorColor) fi-row Bgc($hoverBgColor):h"}
    tdPath = 'td',{'class':"Fw(500) Ta(end) Pstart(10px) Miw(60px)"}
    
    tPE = soup.find_all(tablepath)[0].find_all(rowpath)[2].find('td',{'class':"Fw(500) Ta(end) Pstart(10px) Miw(60px)"}).text
    priceBook = soup.find_all(tablepath)[0].find_all(rowpath)[6].find_all(tdPath)[1].text
    beta = soup.find_all(tablepath)[1].find_all(rowpath)[0].find_all(tdPath)[1].text
    m50Day = soup.find_all(tablepath)[1].find_all(rowpath)[5].find_all(tdPath)[1].text
    m200Day = soup.find_all(tablepath)[1].find_all(rowpath)[6].find_all(tdPath)[1].text
    statData = {
        "Beta" : beta,
        "P/E" : float(tPE),
        "P/B" : float(priceBook),
        "50Day" : m50Day,
        "200Day" : m200Day
        }
    return statData

def getRevenue(ticker):

    pull = requests.get('https://finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker)
    soup=bs4.BeautifulSoup(pull.text, features="html.parser" )
    tablePath = 'div',{'data-reactid':"31"}
    
    titleID = 59
    revList = []
    #print("Title ID: "+str(titleID))
    
    revTitle= soup.find(tablePath).find('span',{'data-reactid':titleID}).text
    if revTitle == "Total Revenue":
    
        reactID = titleID + 5
        endOfRow = reactID + 6
      
        while reactID <= endOfRow:
            revenue= soup.find(tablePath).find('span',{'data-reactid':reactID}).text
            reactID += 2
            revenue = float(revenue.replace(",", ""))
            revList.append(revenue)

                
    return revList

    


def getAnalysis(ticker):
    pull = requests.get('https://ca.finance.yahoo.com/quote/'+ticker+'/analysis?p='+ticker)
    soup=bs4.BeautifulSoup(pull.text, features="html.parser" )
    tablepath = 'table',{'class':"W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)"}
    rowpath = 'tr',{'class':"BdT Bdc($seperatorColor)"}
    
    EPS = float(soup.find_all(tablepath)[2].find_all(rowpath)[2].find('span',{'class':"Trsdu(0.3s)"}).text)
    growth = soup.find_all(tablepath)[5].find_all(rowpath)[3].find('td',{'class':"Ta(end) Py(10px)"}).text
    growth = growth.replace('%', '')
    analData = {
        "EPS" : float(EPS),
        "Growth" : float(growth)
        }
    return analData

ticker = "V"

dataSummary = getSummary(ticker)
dataAnalysis = getAnalysis(ticker)
dataStats = getStats(ticker)

dataSummary.update(dataAnalysis)
dataSummary.update(dataStats)
revenueList = getRevenue(ticker)

revGrowOneYear = revenueList[0]/revenueList[1]*100-100
revGrowThreeYear = revenueList[0]/revenueList[3]*100-100

pprint("Data for: "+ticker)
pprint(dataSummary)
    

pprint("One year revenue growth: "+str(revGrowOneYear)+"%")
pprint("Three year revenue growth: "+str(revGrowThreeYear)+"%")

















#-------------------------------------------
#Discarded code




#def marketBeat(ticker):
 #   pull = requests.get('https://www.marketbeat.com/stocks/NYSE/MA/financials/')
  #  soup=bs4.BeautifulSoup(pull.content, features="html.parser" )
   # iframe_src = soup.find('iframe',{'style':"height:2000px;width:100%;"}).attrs["src"]
 #   pull = requests.get(iframe_src)
  #  soup=bs4.BeautifulSoup(pull.text, features="html.parser" )
    #bEPS = soup.find('div',{'class':"fundamentals embedded"})

   # return soup