# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect

#from deployment.settings import MEDIA_ROOT
#from django.views.generic import TemplateView

import numpy as np
import pandas as pd
#import matplotlib as pl
#pl.use('Agg') #Agg is a non-interactive backend, only save to files
#import matplotlib.pyplot as plt
#import seaborn as sb

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index', 
                'selectedState':'',
                'level':"country",
                'districts':statesList, 
                'numberOfDistricts': len(statesList),
                'rainfallAcrossDistricts':rainfallList, 
                'dates':daysList, 
                'rainfallAcrossDaysList':rainfallAcrossWeekList,
                'states':statesList,
                'datesRained' : datesRainedCountry
                }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url = "/login/")
def states(request):
    state = request.GET.get('state','')
    if(state == ''):
        return redirect('home')

    stateData = groupedRainfallByState.get_group(state)
    rainfallList = []
    daysList = []
    datesRained = []
    for date in stateData.index:
        #weeklyRainfallData.append(stateData.loc[date]['rainfall'])
        rainfallList.append(stateData.loc[date]['rainfall'])
        daysList.append(str(date))
        datesRained.append([str(date),round(stateData.loc[date]['rainfall'],2)])

    districts = DFDistrict[DFDistrict['state'] == state]['district'].unique()
    districtRainfall = {}
    districtList = []
    rainfallAcrossDistrict = []
    for district in districts:
        rainfallAcrossDistrict.append(DFDistrict[DFDistrict['district'] == district]['rainfall'].values[0])
    #districtRainfall[district] = DFDistrict[DFDistrict['district'] == district]['rainfall'].values[0]
    
    context = {'selectedState':state,
                'states' :statesList,
                #'rainfallAcrossDaysList': [1,2,3],
                'rainfallAcrossDaysList': rainfallList,
                'dates': daysList,
                #'dates' : [1,2,3],
                'districts': list(districts),
                'numberOfDistricts':len(districts),
                'rainfallAcrossDistricts': rainfallAcrossDistrict,
                'datesRained' : datesRained
                 }

    html_template = loader.get_template('home/state.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))




#get the data upon loading

# rainfaillAvgPath = r"C:\Users\ryeoh\Project\RainFallAnalysis\data\rainFallavg_bystate_Data.csv"
# DFRainfallByState = pd.read_csv(rainfaillAvgPath)
# RainFallByStateDict = {}
# statesList = []
# rainfallList = []
# for state in DFRainfallByState['state']:
#     #RainFallByStateDict[state] = DFRainfallByState[DFRainfallByState['state'] == state]['rainfall'].values[0]
#     statesList.append(state)
#     rainfallList.append(DFRainfallByState[DFRainfallByState['state'] == state]['rainfall'].values[0])

# rainfallAcrossWeekPath = r"C:\Users\ryeoh\Project\RainFallAnalysis\data\rainFall_acrossweek_Data.csv"
# DFDayTrend = pd.read_csv(rainfallAcrossWeekPath)
# #rainfallAcrossWeek = {}
# rainfallAcrossWeekList = []
# daysList = []
# groupedRainfallByState = DFDayTrend.groupby('state')

# for state in groupedRainfallByState.groups:
#     weeklyRainfallData = []
#     #print(groupedRainfallByState.get_group(state))
#     stateData = groupedRainfallByState.get_group(state)
#     for date in stateData.index:
#         weeklyRainfallData.append(stateData.loc[date]['rainfall'])
#     rainfallAcrossWeek[state] = weeklyRainfallData


# state = "Johor"
# stateData = groupedRainfallByState.get_group(state)
# for date in stateData.index:
#     #weeklyRainfallData.append(stateData.loc[date]['rainfall'])
#     rainfallAcrossWeekList.append(stateData.loc[date]['rainfall'])
#     daysList.append(stateData.loc[date]['date'])



filePath = r"C:\Users\ryeoh\Project\RainFallAnalysis\data\rainFallData.csv"
rainfallDF = pd.read_csv(filePath)

#remove negative numbers from rainfall
rainfallDF['rainfall'] = rainfallDF['rainfall'].replace('-', 0)
rainfallDF['rainfall'] = rainfallDF['rainfall'].astype(float)
rainfallDF['rainfall'].loc[rainfallDF['rainfall']<0] = 0


#get rainfall by state
DFRainfallByState = rainfallDF.groupby('state')['rainfall'].mean().reset_index()

statesList = []
rainfallList = []
for state in DFRainfallByState['state']:
    #RainFallByStateDict[state] = DFRainfallByState[DFRainfallByState['state'] == state]['rainfall'].values[0]
    statesList.append(state)
    rainfallList.append(DFRainfallByState[DFRainfallByState['state'] == state]['rainfall'].values[0])


#get rainfall across days
DFDayTrend = rainfallDF.groupby(['state', 'date'])['rainfall'].mean().reset_index()
DFDayTrend.set_index('date', inplace=True)


DFCountryAverageDays = rainfallDF.groupby(['date'])['rainfall'].mean().reset_index()
#DFCountryAverageDays.set_index('date')
rainfallAcrossWeekList = [round(DFCountryAverageDays.loc[date]['rainfall'],2) for date in DFCountryAverageDays.index]
daysList = [ str(DFCountryAverageDays.iloc[date]['date']) for date in DFCountryAverageDays.index]
datesRainedCountry = list(zip(daysList,rainfallAcrossWeekList))

groupedRainfallByState = DFDayTrend.groupby('state')


#get rainfall by districts
DFDistrict = rainfallDF.groupby(['state', 'district']).mean().reset_index()

#statesDistrictRainfall[state] = districtRainfall