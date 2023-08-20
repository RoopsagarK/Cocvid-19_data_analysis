from tkinter import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from Covid_analysis1 import Country
from Covid_analysis1 import Country_names
from PIL import ImageTk, Image
from tkhtmlview import HTMLLabel
from worldGraph import *
#from worldGraph import *

# Creating a window named 'root'
root = Tk()
root.title('Covid-19 Data Analyzer') #Setting title for the Window
root.iconbitmap('tkinter/icon/covid-19.ico') #Setting Icon for the Window
root.configure(bg='#001C30') #Setting Background-color
covid_df = pd.read_csv('full_grouped.csv')
covid_df.drop(columns="WHO_Region", inplace=True)
sns.set_style('darkgrid')

cn_obj = Country_names()
CountryNames = cn_obj.getCountryNames()

#country = []

#for i in Country_names :
    #country.append(i)

#Dividing Root window into 'Three; different Frames

TopFrame = LabelFrame(root, width=100,height=50,bg='white') #Creating the frist frame to Render the Search Box
TopFrame.grid(row=0,column=0,columnspan=5,padx=10,pady=10)

IntroLabel = Label(TopFrame,text='Covid-19 Data Analyzer', width=120, height=2, bd=1, bg='#176B87',borderwidth=2,fg='#F6F4EB')
IntroLabel.grid(row=0,column=0,padx=5,pady=5)

DataFrame = LabelFrame(root,width=180,height=20,bg='#DAFFFB',borderwidth=5) #Creating the Third frame to rnder the 'Graph' and 'Info'
DataFrame.grid(row=2, column=0,padx=15,pady=15)

CategoryValue1 = StringVar()
CategoryValue2 = StringVar()
CategoryValue3 = StringVar()

Category1 = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'New-Cases', 'New-Death', 'New-Recovered']
Category2 = ['Deaths', 'Active', 'Recovered', 'Confirmed', 'Cases To Recovered']

DD1 = OptionMenu(DataFrame, CategoryValue1, *CountryNames)
DD1.grid(row=0 , column=0,padx=5, pady=5)
CategoryValue1.set('Select Country')

def Updater() :
    country = CategoryValue1.get()
    CountryObj = Country(country)
    country_wise_df = covid_df[covid_df["country"] == country]
    country_wise_df["month"] = pd.DatetimeIndex(country_wise_df.date).month 
    InfoDisplayer(list(CountryObj.confimed_cases())[-1], list(CountryObj.deaths())[-1], list(CountryObj.recovered())[-1], list(CountryObj.active())[-1], country)

def GraphPlotter() :
    #C,D,R,A,NC,ND,NR = 0
    country = CategoryValue1.get()
    cases = CategoryValue2.get()
    CountryObj = Country(country)
    country_wise_df = covid_df[covid_df["country"] == country]
    country_wise_df["month"] = pd.DatetimeIndex(country_wise_df.date).month

    if(cases == 'Confirmed'):
        # sns.scatterplot(country_wise_df.month,CountryObj.confimed_cases())
        ax = plt.axes()
        ax.set_facecolor("#241468")
        plt.plot(CountryObj.confimed_cases(),'m-', linewidth=5, alpha=0.75)
        plt.legend(["confirmed cases"])
        plt.show()
    elif(cases == 'Deaths'):
        ax = plt.axes()
        ax.set_facecolor("#0C356A")
        plt.plot(CountryObj.deaths(), color='#40F8FF', linewidth=5, alpha=0.75)
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

UpdateButton = Button(DataFrame, text='Update', padx=5, command=Updater, width=15)
UpdateButton.grid(row=0, column=5, padx=5, pady=5)

DD2 = OptionMenu(DataFrame, CategoryValue2, *Category1) 
DD2.grid(row=4, column=1, padx=10, pady=15)
CategoryValue2.set('Select Category For Graph View')

DD3 = OptionMenu(DataFrame, CategoryValue3, *Category2)
DD3.grid(row=4 , column=3)
CategoryValue3.set('Select Category For Map View')

def InfoDisplayer(confirmed, deaths, recovered, active, co) :
    print(confirmed)
    Values = "<p> Confrimed :  " + str(confirmed) + "</p><p> Deaths :  " + str(deaths) + "</p> <p> Recovered :  " + str(recovered) + "</p><p> Active :  " + str(active)  + "</p>"
    InfoHeader = HTMLLabel(DataFrame,html="<p>Country Selected :  " + co + "</p>",width=40, height=2,borderwidth=5,bg='#91C8E4')
    InfoHeader.grid(row=1,column=2)
    InfoLabel = HTMLLabel(DataFrame, html=Values, width=40, height=12, borderwidth=5)
    InfoLabel.grid(row=2, column=2,padx=40,pady=2)


def MapPlotter() :
    # 'Deaths', 'Active', 'Recovered', 'Confirmed', 'Cases To Recovered'
    val = CategoryValue3.get()

    if val == 'Deaths' :
        plot_map('Deaths', 'deaths_log')
    elif val == 'Active' :
        plot_map('Active', 'active_log')
    elif val == 'Recovered' :
        plot_map('Recovered' , 'recovered_log')
    elif val == 'Confirmed' :
        plot_map('Confirmed', 'confirmed_log')
    elif val == 'Cases To Recovered' :
        plot_map('Cases To Recovered' , 'cases_to_recovered')

InfoDisplayer("","","","","")

PlotLabel = Label(DataFrame, text='For Better Visualization Please Select a Category To Plot The \'Graph\' And \'Map\'')
PlotLabel.grid(row=3, column=2, padx=10,pady=(10,5))

PlotButton = Button(DataFrame, text='Plot on Graph', padx=5,pady=2, width=15, command=GraphPlotter)
PlotButton.grid(row=5, column=1,padx=10, pady=10)

MapButton = Button(DataFrame, text='Plot on Map', padx=5, pady=2, width=15, command=MapPlotter)
MapButton.grid(row=5, column=3,padx=10, pady=10)

root.mainloop()