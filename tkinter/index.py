from tkinter import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from Covid_analysis1 import Country
from Covid_analysis1 import Country_names
from PIL import ImageTk, Image
from tkhtmlview import HTMLLabel

# Creating a window named 'root'
root = Tk()
root.title('Covid-19 Data Analyzer') #Setting title for the Window
root.iconbitmap('tkinter/icon/covid-19.ico') #Setting Icon for the Window
root.configure(bg='#272829') #Setting Background-color
covid_df = pd.read_csv('full_grouped.csv')
covid_df.drop(columns="WHO_Region", inplace=True)
sns.set_style('darkgrid')


cn_obj = Country_names()
CountryNames = cn_obj.getCountryNames()

#country = []

#for i in Country_names :
    #country.append(i)

#Dividing Root window into 'Three; different Frames

SearchFrame = LabelFrame(root, width=100,height=50) #Creating the frist frame to Render the Search Box
SearchFrame.grid(row=0,column=0,columnspan=3,padx=5,pady=5)

SearchEntry = Entry(SearchFrame,width=100,bd=1,borderwidth=2,bg='#D8D9DA',fg='#272829')
SearchEntry.grid(row=0,column=0)

MapFrame = LabelFrame(root,width=172,height=40,bg='#FFF6E0' , borderwidth=5) #Creating the Second frame to render 'Glabal Map'
MapFrame.grid(row=1,column=0,padx=15,pady=15)

MapLabel = Label(MapFrame, text='Map Will Be displayed here !',width=172, height=20, bg='#D8D9DA') #Dispalying the World Map
MapLabel.grid(row=0, column=0,padx=10,pady=10)

DataFrame = LabelFrame(root,width=180,height=20,bg='#D8D9DA',borderwidth=5) #Creating the Third frame to rnder the 'Graph' and 'Info'
DataFrame.grid(row=2, column=0,padx=15,pady=15)

DataMapLabel = Label(DataFrame,text='Map',width=45,height=15,bg='lightblue',borderwidth=5)
DataMapLabel.grid(row=0,column=0,rowspan=2,padx=40)

CategoryValue1 = StringVar()
CategoryValue2 = StringVar()

Category = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'New-Cases', 'New-Deaths', 'New-Recovered']

Cases1 = OptionMenu(DataFrame, CategoryValue1, *CountryNames)
Cases1.grid(row=0 , column=1,padx=5, pady=5)
CategoryValue1.set('Select Country')

Cases2 = OptionMenu(DataFrame, CategoryValue2, *Category) 
Cases2.grid(row=0, column=2, padx=5, pady=5)
CategoryValue2.set('Select Category')


def Updater() :
    #C,D,R,A,NC,ND,NR = 0
    country = CategoryValue1.get()
    cases = CategoryValue2.get()
    CountryObj = Country(country)
    country_wise_df = covid_df[covid_df["country"] == country]
    country_wise_df["month"] = pd.DatetimeIndex(country_wise_df.date).month
    
    InfoDisplayer(sum(CountryObj.confimed_cases()), sum(CountryObj.deaths()),sum(CountryObj.recovered()), sum(CountryObj.active()), sum(CountryObj.new_cases()), sum(CountryObj.new_deaths()), sum(CountryObj.new_recovered()))


    if(cases == 'Confirmed'):
        # sns.scatterplot(country_wise_df.month,CountryObj.confimed_cases())
        ax = plt.axes()
        ax.set_facecolor("#241468")
        plt.plot(CountryObj.confimed_cases(), "m-", linewidth=5, alpha=0.75)
        plt.legend(['confirmed cases'])
        plt.show()
    elif(cases == 'Deaths'):
        ax = plt.axes()
        ax.set_facecolor("#0C356A")
        plt.plot(CountryObj.confimed_cases(), color='#40F8FF', linewidth=5, alpha=0.75)
        plt.legend(["Deaths"])
        plt.show()
    elif(cases == 'Recovered') :
        ax = plt.axes()
        ax.set_facecolor("#FFF5E0")
        plt.plot(CountryObj.recovered(), color='#FF6969', linewidth=5, alpha=0.75)
        plt.legend(["Recovered"])
        plt.show()
    elif(cases == 'Active') :
        ax = plt.axes()
        ax.set_facecolor("#0D1282")
        plt.plot(CountryObj.active(), color='#EEEDED', linewidth=5, alpha=0.75)
        plt.legend(["Active"])
        plt.show()
    elif(cases == 'New-Cases') :
        ax = plt.axes()
        ax.set_facecolor("#ECF8F9")
        plt.plot(CountryObj.new_cases(), color='#068DA9', linewidth=5, alpha=0.75)
        plt.legend(["New cases"])
        plt.show()
    elif(cases == 'New-Deaths'):
        ax = plt.axes()
        ax.set_facecolor("#900C3F")
        plt.plot(CountryObj.new_deaths(), color='#F8DE22', linewidth=5, alpha=0.75)
        plt.legend(["New Deaths"])
        plt.show()
    elif(cases == 'New-Recovered'):
        ax = plt.axes()
        ax.set_facecolor("#EDF1D6")
        plt.plot(CountryObj.new_recovered(), color='#609966', linewidth=5, alpha=0.75)
        plt.legend(["New Recovered"])
        plt.show()

    

    

UpdateButton = Button(DataFrame, text='Update', padx=2, command=Updater)
UpdateButton.grid(row=0, column=3, padx=5, pady=5)

Graph = Label(DataFrame, text="Graph", width=55,height=13,bg='pink',borderwidth=5)
Graph.grid(row=1,column=1,columnspan=3,padx=15,pady=12)


def InfoDisplayer(confirmed, deaths, recovered, active, newCases, newDeaths, newRecovered) :
    print(confirmed)
    Values = "<p> Confrimed : " + str(confirmed) + "</p><p> Deaths : " + str(deaths) + "</p> <p> Recovered : " + str(recovered) + "</p><p> Active : " + str(active) + "</p><p> New Cases : " + str(newCases) + "</p><p> New Deaths : " + str(newDeaths) + "</p><p> New Recovered : " + str(newRecovered) + "</p>"
    InfoLabel = HTMLLabel(DataFrame, html=Values, width=45, height=15, bg='lightblue',borderwidth=5)
    InfoLabel.grid(row=0, column=4,rowspan=2,padx=40)

InfoDisplayer("","","","","","","")

root.mainloop()