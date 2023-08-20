#%config Completer.use_jedi = False
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

world_geojson = json.load(open('countries.geojson', 'r'))
covid_df = pd.read_csv('full_grouped.csv') 

# Drop the 'useless columns

covid_df.drop(columns=['WHO_Region', 'new_cases', 'new_deaths', 'new_recovered'], inplace=True)

geojson_name_changes = {
    "United States of America": "US",
    "Democratic Republic of the Congo": "Congo (Kinshasa)" ,
    "Republic of Congo": "Congo (Brazzaville)",
    "United Republic of Tanzania":"Tanzania",
}
for feature in world_geojson['features']:
    old_name = feature['properties']['ADMIN']
    new_name = geojson_name_changes.get(old_name, old_name)
    feature['properties']['ADMIN'] = new_name
csv_name_changes = {
    "Burma" : "Myanmar",
    "Cote d'Ivoire" : "Ivory Coast"
}
covid_df['country'] = covid_df['country'].replace(csv_name_changes)

#picking out the country names from the geojson
geojson_country_names = [feature['properties']['ADMIN'] for feature in world_geojson['features']]
# print(geojson_country_names)
# converting the csv and geojson country names in sets to compare
geojson_country_set = set(geojson_country_names)
csv_country_set = set(covid_df['country'])
#print(csv_country_set)
# making a set of common countries
common_countries = geojson_country_set.intersection(csv_country_set)

#filtering out the features list from the world_geojson 
filtered_geojson_features =  [feature for feature in world_geojson['features'] if feature['properties']['ADMIN'] in common_countries]

#making a new geojson to use
filtered_geojson = {'type' : 'FeatureCollection', 'features' : filtered_geojson_features}
# temp = set([feature['properties']['ADMIN'] for feature in filtered_geojson['features']])
# print(temp)

#making a new csv of countries
filtered_csv_countries = covid_df[covid_df['country'].isin(common_countries)]

#verifyling the equality of the 2 sets of data
# print( set(temp) - set(filtered_csv_countries['country'].unique()))

#assigning unique ids to each geojson country
country_id_map = {}
for feature in filtered_geojson['features']:
    feature['id'] = feature['properties']['ISO_A3']
    country_id_map[feature['properties']['ADMIN']] = feature['id']
#adding that id to csv, while supressing settingWithCopyWarning
with pd.option_context('mode.chained_assignment', None):
    filtered_csv_countries.loc[:, 'id'] = filtered_csv_countries['country'].apply(lambda x:country_id_map[x])

# country = 'Andorra'
# country_data = filtered_csv_countries[filtered_csv_countries['country'] == country]
# country_data
date_to_check = '2020-07-27'
date_data = filtered_csv_countries[filtered_csv_countries['date'] == date_to_check]


with pd.option_context('mode.chained_assignment', None):
    date_data['deaths_log'] = np.log10(date_data['deaths'] + 1e-10)
    date_data['active_log'] = np.log10(date_data['active'] + 1e-10)
    date_data['recovered_log'] = np.log10(date_data['recovered'] + 1e-10)
    date_data['confirmed_log'] = np.log10(date_data['confirmed'] + 1e-10)
    date_data['cases_to_recovered'] = round((date_data['recovered'] / date_data['confirmed']), 4) 

def plot_map(title_string='Confirmed cases',data_to_plot = 'confirmed_log'):
    '''Plots maps
    title_string can be anything
    data_to_plot must be among the following 
    ['recovered_log', 'confirmed_log', 'active_log', 'deaths_log', 'cases_to_recovered']'''
    color_scale_custom = 'RdYlGn_r' if data_to_plot not in ['recovered_log', 'cases_to_recovered'] else 'RdYlGn'

    fig = px.choropleth_mapbox(date_data,
                        locations="id",
                        geojson=filtered_geojson, 
                        color=data_to_plot,
                        hover_name='country',
                        hover_data=['confirmed', 'deaths','recovered', 'active','cases_to_recovered','id'],
                        mapbox_style='carto-positron',
                        color_continuous_scale=color_scale_custom,
                        zoom = 1.5,
                        opacity = 0.7)
    fig.update_traces(hovertemplate='<b>%{hovertext}(%{customdata[5]})</b><br>' +
                                     'Confirmed: %{customdata[0]}<br>' +
                                     'Deaths: %{customdata[1]}<br>' +
                                     'Recovered: %{customdata[2]}<br>' +
                                     'Active: %{customdata[3]}<br>'+
                      'Recovered/Cases: %{customdata[4]}<extra></extra>')
    fig.update_layout(
        coloraxis_colorbar=dict(title=title_string,tickvals=[], ticktext=[]),
         title=f'COVID-19 {title_string} by Country as of 27-7-2020'
    )
    fig.show()
plot_map('Deaths', 'cases_to_recovered')
