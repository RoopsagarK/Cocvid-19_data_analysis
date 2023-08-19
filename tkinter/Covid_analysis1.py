import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

covid_df = pd.read_csv('full_grouped.csv')
covid_df.drop(columns="WHO_Region", inplace=True)

csv_name_changes = {
    "Burma" : "Myanmar",
    "Cote d'Ivoire" : "Ivory Coast"
}

covid_df['country'] = covid_df['country'].replace(csv_name_changes)

def calculate_death_rate(total_cases, total_deaths):
    death_rate = (total_deaths/total_cases)*100
    return death_rate

class Country_names:
    covid_df = pd.read_csv('full_grouped.csv')
    covid_df.drop(columns="WHO_Region", inplace=True)
    csv_name_changes = {
        "Burma" : "Myanmar",
        "Cote d'Ivoire" : "Ivory Coast"
    }

    covid_df['country'] = covid_df['country'].replace(csv_name_changes)
    def getCountryNames(self):
        return self.covid_df["country"].tolist()

class Country:
    header_list = covid_df.columns.values.tolist()
    header_list.remove('date')
    header_list.remove('country')
    # country_wise_df = covid_df.groupby("country")[header_list]
    def __init__(self, name):
        self.name = name

    def new_cases(self):
        country_wise_df = covid_df[covid_df["country"] == self.name]
        return country_wise_df['new_cases'].tolist()
    
    def confimed_cases(self):
        country_wise_df = covid_df[covid_df["country"] == self.name]
        return country_wise_df['confirmed'].tolist()
    
    def recovered(self):
        country_wise_df = covid_df[covid_df["country"] == self.name]
        return country_wise_df['recovered'].tolist()
    
    def deaths(self):
        country_wise_df = covid_df[covid_df["country"] == self.name]
        return country_wise_df['deaths'].tolist()

    def active(self):
        country_wise_df = covid_df[covid_df["country"] == self.name]
        return country_wise_df['active'].tolist()
    
    def new_deaths(self):
        country_wise_df = covid_df[covid_df["country"] == self.name]
        return country_wise_df['new_deaths'].tolist()
    
    def new_recovered(self):
        country_wise_df = covid_df[covid_df["country"] == self.name]
        return country_wise_df['new_recovered'].tolist()
    
covid_df['date'] = pd.to_datetime(covid_df.date)
covid_dt_df = covid_df.copy()
covid_dt_df["month"] = pd.DatetimeIndex(covid_dt_df.date).month
covid_dt_df["day"] = pd.DatetimeIndex(covid_dt_df.date).day

covid_dt_df.drop(columns='date', inplace=True)

class Period:
    
    def __init__(self, country_name):
        self.country_name = country_name
    

    def month(self, month_number):

        country_dt_df = covid_dt_df.loc[covid_dt_df['country'] == self.country_name]
        country_dt_df.drop(columns=['day', 'country'], inplace=True)
        header_list = country_dt_df.columns.values.tolist()
        header_list.remove('month')
        month_wise_df = country_dt_df.groupby("month")[header_list].sum()
    
        case_list = month_wise_df.loc[month_number]
        result = {}
        for header_list,case in zip(header_list, case_list):
            result[header_list] = case
        
        return result

    def day(self, month_number, day_number): 
        country_dt_df = covid_dt_df.loc[covid_dt_df['country'] == self.country_name]
        country_dt_df.drop(columns=['country'], inplace=True)
        header_list = country_dt_df.columns.values.tolist()
        header_list.remove('month')
        header_list.remove('day')
        
        day_wise_df = country_dt_df.loc[country_dt_df['month'] == month_number]
        day_wise_df = day_wise_df[day_wise_df['day'] == day_number]
        day_wise_df.drop(columns=['month'], inplace=True)
        day_wise_df = day_wise_df.groupby("day")[header_list].sum()
        
        case_list = day_wise_df.loc[day_number]
          
        result = {}
        for header_list,case in zip(header_list, case_list):
            result[header_list] = case
        
        return result