from tkinter import *
import matplotlib.pyplot as plt
import pandas as pd
from PIL import ImageTk, Image

root = Tk()
root.title('Covid-19 Data Analyzer')
root.iconbitmap('tkinter/icon/covid-19.ico')
root.configure(bg='#272829')

MyDateList = []
for i in range(32) :
    MyDateList.append(i)

SearchFrame = LabelFrame(root, width=100,height=50)
SearchFrame.grid(row=0,column=0,columnspan=3,padx=5,pady=5)

SearchEntry = Entry(SearchFrame,width=100,bd=1,borderwidth=2,bg='#D8D9DA',fg='#272829')
SearchEntry.grid(row=0,column=0)

MapFrame = LabelFrame(root,width=172,height=40,bg='#FFF6E0' , borderwidth=5)
MapFrame.grid(row=1,column=0,padx=15,pady=15)

MapLabel = Label(MapFrame, text='Map Will Be displayed here !',width=172, height=20, bg='#D8D9DA')
MapLabel.grid(row=0, column=0,padx=10,pady=10)

DataFrame = LabelFrame(root,width=180,height=20,bg='#D8D9DA',borderwidth=5)
DataFrame.grid(row=2, column=0,padx=15,pady=15)

DataMapLabel = Label(DataFrame,text='Map',width=45,height=15,bg='lightblue',borderwidth=5)
DataMapLabel.grid(row=0,column=0,rowspan=2,padx=40)

CaseValue = StringVar()
MonthValue = StringVar()
DateValue = IntVar()

Cases = OptionMenu(DataFrame, CaseValue, 'Death Rate', 'Mortality Rate', 'Incident Rate', 'Daily Change Rate')
Cases.grid(row=0 , column=1,padx=5, pady=5)
CaseValue.set('Select Category')

Months = ['January', 'Febrauary', 'March', 'April', 'May', 'June', 'July']


MonthValue.set('Select Month')
Month = OptionMenu(DataFrame,MonthValue, *Months) 
Month.grid(row=0, column=2, padx=5,pady=5)

DateValue.set('Select Date')
Date = OptionMenu(DataFrame, DateValue, *MyDateList) 
Date.grid(row=0, column=3, padx=5, pady=5)

Graph = Label(DataFrame, text='Graph', width=55,height=13,bg='pink',borderwidth=5)
Graph.grid(row=1,column=1,columnspan=3,padx=15,pady=12)

InfoLabel = Label(DataFrame, text='Info', width=45, height=15, bg='lightblue',borderwidth=5)
InfoLabel.grid(row=0, column=4,rowspan=2,padx=40)

root.mainloop()