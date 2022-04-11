#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import cufflinks as cf
import tabula

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()


# In[2]:


# Reading the files
path="Higher-Education-Graduates-by-Discipline-Group 2006-2016.pdf"
rawd2=tabula.read_pdf(path, pages='1')[0]
rawd2=rawd2.drop(rawd2.columns[5:],axis=1)

rawd=pd.read_csv("Higher-Education-Graduates-by-Discipline-Group-AY-2010-11-to-2018-19.csv")
rawd=rawd.dropna(axis=0)


# In[3]:


#formatting the data
format={'Discipline Group':[x for x in rawd['Unnamed: 0'][1:] for _ in range(10)]+
                           [x for x in rawd['Unnamed: 0'][1:] for _ in range(4)], 
        
        'Pop':[x for d in rawd.iloc[1:,1:].values for x in d]+
                [x for d in rawd2.iloc[:,1:].values for x in d], 
        
        'Date':[x for _ in range(22) for x in rawd.iloc[0,1:]] +
                [x for _ in range(22) for x in rawd2.columns[1:]] }

#printing the values
df=pd.DataFrame(format)

# Converting the string to an int
df['Pop']=df['Pop'].replace(',', '', regex=True).astype(int)

# Stripping the date
Date1=pd.Series([pd.to_datetime(x.strip(),format='%Y-%y') for x in df['Date']]).dt.year-1
Date2=pd.Series([pd.to_datetime(x.strip(),format='%Y-%y') for x in df['Date']]).dt.year


df['Date']=["{}-{}".format(x,y) for x,y in zip(Date1, Date2)]

# Getting rid of the 'Grand Total'
df_GT= df.loc[df['Discipline Group']=='Grand Total']
df.drop(df[df['Discipline Group']=='Grand Total'].index, inplace = True)

# Sorting the values via Date
df=df.sort_values('Date').reset_index(drop=True)


# In[131]:


fig = px.bar(df,
           x='Pop', 
           y='Discipline Group',
           animation_frame='Date',
            width=500,
           color='Discipline Group')


fig.update_layout(
            margin_t=0,
            plot_bgcolor="#FFFFFF",
            sliders=[{"currentvalue": {"prefix": "Academic Year: "}}],
            showlegend=False,
            xaxis={'range':[0,250000], 'ticklen':3 },
            yaxis={'range':[15.5, 20.5],  
                   'categoryorder':'total ascending'})


# In[130]:


figb1 = px.bar(df,
               x='Pop', 
               y='Discipline Group',
               animation_frame='Date',
               width=500,
               color='Discipline Group')

figb1.update_layout(
                margin_t=0,
                plot_bgcolor="#FFFFFF",
                showlegend=False,
                margin_l=200,
                xaxis={'range':[0,4000]},
                yaxis={'range':[-0.5, 4.5],
                       'categoryorder':'total ascending'})

figb1.update_yaxes(automargin=False)


# In[116]:


# line plot with a drop down menu

figb2 = px.line(df, 
              x= 'Date',
              y= 'Pop',
              color='Discipline Group',
              markers=True)

figb2 = figb2.update_layout(margin_t=0,
                            plot_bgcolor="#FFFFFF",
                            legend_itemdoubleclick="toggleothers")


# In[25]:


import dash
import dash_html_components as html
import dash_core_components as dcc


app = dash.Dash( )


# In[ ]:


style_text={'font-family': 'Helvetica', 
                        'padding':'0em 4em', 
                        'color':'#737272'}
style_title={'font-family': 'Helvetica', 
                    'padding':'1.5em 1.5em  0em 1.5em', 
                    'color':'#737272',
                    'line-height': '1.25em'}
style_subtitle={'font-family': 'Helvetica', 
                    'padding':'1em 1em 0em 2em', 
                    'color':'#737272'}
style_box={'border-radius': '1em','box-shadow': '5px 5px 20px 1px #c3c7c4', 'grid-column': '1 / 2',
                      'grid-row': '1'}



app.layout = html.Div(
    
    children=[
        html.Div([html.H1([html.Br(),
            '''The Change of the Population of Higher Education Gradueation 
                of Discipline Groups in the Philippines 
                in the Academic Years 2005-2006 to 2018-2019'''],
                    style=style_title),
                  
                html.P('''Includes pre-baccalaureate up to doctoral programs''',
                       style=style_text),
                  
                html.P("References",
                       style=style_text),
                       
                html.P('''Commision on Higher Education. (2017, April 10). 
                    Table 4. Higher Education Graduates by Discipline Group: 
                    AY 2005-06 to AY 2015-16 (OPRKM-Knowledge Management Division, Compiler) ''',
                      style=style_text),
                       
                html.P('''Commission on Higher Education. (2020, October 8). 
                    Table 3. Higher Education Graduates by Discipline Group:
                    AY 2010-11 to 2018-19 (OPRKM-Knowledge Management Division, Compiler).''',
                      style=style_text)
                 ], 
                 style=style_box),
                  
        html.Div([
                html.H2('''Top 5 Most Popular to Graduate During the Academic Years''',
                style=style_title),
            
                dcc.Graph(figure=fig,style={'padding':'1em' }),
            
                html.H2('''Top 5 Least Popular to Graduate During the Academic Years''',
                style=style_subtitle),
            
                dcc.Graph(figure=figb1),html.Br()], 
                 style={'border-radius': '1em','box-shadow': '5px 5px 20px 1px #c3c7c4', 'grid-column': '2/ 2',
                      'grid-row': '1/span 2'}),
                  
        html.Div([html.H2('''The Trend of the Population of Graduate in the Discipline Groups''',
                style=style_subtitle),
                  
                dcc.Graph(figure=figb2),html.Br()], 
                style={'border-radius': '1em','box-shadow': '5px 5px 20px 1px #c3c7c4', 'grid-column': '1/ 2',
                      'grid-row': '2'})],

    style={'display': 'grid',
           'grid-template-columns': 'repeat(2,1fr)',
           'grid-auto-rows': 'minmax(450px, auto)',
           'flex-grow':'1',
           'grid-gap': '2em'
           }
        )
    

if __name__=="__main__":
    app.run_server()
                


# In[ ]:




