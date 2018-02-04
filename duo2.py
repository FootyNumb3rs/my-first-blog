import pandas as pd
import numpy as np
import pprint as pp
import plotly.graph_objs as go 
import plotly.plotly as py


def top_duo(player,primaryPlayer): # Taken in as pandas series
  temp_zip = zip(player.tolist(),primaryPlayer.tolist()) # Preparing for sorting
  temp_frame = pd.DataFrame([sorted(pzip) for pzip in temp_zip],columns =['p1','p2']) # Really inefficient
  temp_frame['count']= temp_frame['p1'] +'+'+ temp_frame['p2'] # Used for counting
  print(temp_frame['count'].value_counts()[0:9])
  return(temp_frame['count'].value_counts().index[0].split('+')) # Find the most frequent one, retrieve the names, 

def short_name(name):
  if len(name.split(' ')) == 1:
    return(name)
  else:
    return(name[0] +' ' + ' '.join(name.split(' ')[1:]))



def pull_league_data(league):
  league_map = {'Premier League': 'pl',
                    'La Liga':'liga',
                'CL':'CL',
                'Serie A':'SA'}
    

  df = pd.read_csv('{}_chances.csv'.format(league_map[league]),header=0) # So leagues can be inputted for easily 
  has_primary = df['primaryPlayer']!='-' # Has an assister
  df=df[has_primary] 
  df['player']=df['player'].apply(str.replace,args=('.',''))
  df['primaryPlayer']=df['primaryPlayer'].apply(str.replace,args=('.',''))
  df['player']=df['player'].apply(short_name)
  df['primaryPlayer']=df['primaryPlayer'].apply(short_name)
  df['relation']=df['player'] + ' > ' + df['primaryPlayer']
  return(df)

def get_duo_data(league):
  df = pull_league_data(league)
  name_array = []
  num_array = []

  for team,team_df in df.groupby('team'):
    partners = top_duo(team_df['player'],team_df['primaryPlayer']) # Gets name of partners that are the top duo
    #partners = list(team_df['relation'].value_counts().iloc[0:1].to_dict().keys())[0].split(' > ')
    part_df = df['player'].isin(partners) & df['primaryPlayer'].isin(partners)
    non_dup = df['player'] != df['primaryPlayer'] # There are cases when this is true, wierdly.
   # print(team,team_df.loc[:,'relation'].value_counts()[0:9])

    temp_data = team_df.loc[part_df&non_dup,'relation'].value_counts() # Subset by most frequent duo + count relations

    name_array.append(temp_data.index[0].split(' > ')) # The first value corresponds to the shot percentage of the first name in the first index 
    if len(temp_data.tolist()) < 2: # 
        num_array.append([temp_data[0],0]) # If only one name has accrued shots, then the value_counts contains one value, so the second must be zero
    else:
        num_array.append(temp_data.tolist()[0:2]) # If both have taken shots, just return the values


  num_array = np.array(num_array)
  name_array = np.array(name_array)
  #print(list(zip(name_array[:,0],name_array[:,1],num_array[:,0],num_array[:,1])))

  final_df = pd.DataFrame(list(zip(name_array[:,0],num_array[:,0],num_array[:,1],name_array[:,1])), columns = ['p1','abs1','abs2','p2'])

  print(final_df)
  final_df['total'] = final_df['abs1']+final_df['abs2']
  final_df.sort_values('total',inplace=True,ascending=True)
  final_df['perc1'] = final_df['abs1']/(final_df['total'])
  final_df['perc2'] = final_df['abs2']/(final_df['total'])
  final_df['league'] = league
  return(final_df)

def generate_data_layout(final_df):  

  ######################################## Beginning of Annotations
  annotations = []

  # Right Names
  annotations.extend([dict(x=1,
                      y=i,
                      text=name, 
                      font=dict(size=10),
                      yref='y', xref='x',
                      xanchor='left',
                      showarrow=False,
                      ) for i, name in enumerate(final_df['p2'].tolist())])    

  # 
  title_ = final_df['league'].unique()
  subtitle_ = ''#'All Chance Types Included'

  # Title 
  annotations.append(dict(x=.35,y=1.09,
                text='<b>{}<b>'.format(title_[0]),
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='center',
                font = dict(size=15,
                            family = 'Arial, bold')))

  # Subtitle 
  annotations.append(dict(x=-.2,y=1.06,
                text=subtitle_,
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='left',
                font = dict(size=10,
                            family = 'Arial')))


  stext = ['Each chance',
           'involves one player',
           'shooting and the',
           'other creating the',
           'chance. <br>',
           'Each number represents',
           'the times that',
           'player was the',
           'one to shoot.',
           '<br>Each duo is',
           'the most frequent one',
           'for that team.<br>',
           'Example:<br> Together, Kane &',
           'Eriksen were involved in',
           '34 chances. Kane shot',
           '28 of those and',
           'Eriksen did 6.',
           'Hence, Kane created 6',
           'and Eriksen did 28.',
              ]

  # Side Text
  annotations.append(dict(x = 1.45,
                    y = .995,
                   font=dict(size=10,
                             color='grey'),
                   showarrow=False,
                   xref ='paper',
                   yref ='paper',
                   text ='<br>'.join(stext) if final_df['league'].unique()[0] == 'Serie A' else '',
                   align='right'))

  # Left Number
  annotations.extend([dict(x = final_df['perc1'].tolist()[i]-.01,
                   y = i,
                   text = num,
                   xref = 'x', yref = 'y',
                   font=dict(size=10),
                   showarrow=False,
                   xanchor='right'
                   ) for i, num in enumerate(final_df['abs1'].tolist())])

             
  # Right Number               
  annotations.extend([dict(x = final_df['perc1'].tolist()[i]+.01,
                   y = i,
                   text = num,
                   xref='x',yref='y',
                   font=dict(size=10),
                   xanchor='left',
                   opacity = 0 if final_df['perc2'].tolist()[i] == 0 else 1,
                   showarrow=False,
                   ) for i, num in enumerate(final_df['abs2'].tolist())])

  # DRAFT 
  annotations.append(dict(text="DRAFT" if final_df['league'].unique()[0] == 'Serie A' else '',
                        xref="paper", yref="paper",
                        x=1.4, y=0,
                        showarrow=False,
                        font=dict(family='Arial',size=20,color='red')))

  ##################### End of Annotations


  ##################### Preparing Data Bars       
  data = [go.Bar(x = final_df['perc1'].tolist(), y = final_df['p1'].tolist(),
                    orientation='h',
                    marker=dict(color='#6fcb9f',
                                line=dict(width=.7)),
                    hovertext=round(final_df['perc1']*100,1).astype(str)+'%',
                    hoverinfo='text'),
             go.Bar(x = final_df['perc2'].tolist(),
                    y = final_df['p1'].tolist(),
                    orientation='h',
                    marker=dict(color='#ffe28a',
                                line=dict(width=.7)),
                    hovertext=round(final_df['perc2']*100,1).astype(str)+'%',
                    hoverinfo='text')]
  ##################### Done Preparing Data



  images=[dict(
              source="https://i.imgur.com/4tJcdMZ.png"if final_df['league'].unique()[0] == 'Serie A' else '',
              xref="paper", yref="paper",
              x=1.3, y=1.11,
              sizex=0.7, sizey=0.7,
              xanchor="right", yanchor="bottom"
                    )]


  layout = go.Layout(width = 500,
                     height = 500,
                     font=dict(family='Arial'),
                     yaxis = dict(showgrid=False,
                                 tickfont = dict(
                                     family='Arial',
                                     size=10
                                     )),
                     paper_bgcolor='#f1f1f1',
                     plot_bgcolor='#f1f1f1',
                     margin = go.Margin(
                            l=100,
                              r=140,
                              b=20,
                              t=100,
                              pad=4),
                     barmode='stack',  
                     annotations = annotations,
                     images=images,
                     showlegend=False)


  return(data,layout)

