import pandas as pd
from collections import Counter
from pysankey import sankey

df = pd.read_csv('biprozorro_data_chernivtsi_17_19.csv')
df['Очікувана вартість'] = (df['Очікувана вартість'].str.split()).apply(lambda x: float(x[0].replace(',', ''))/100)

sankey(
      left=df['Організатор'], right=df['Постачальники'], rightWeight=df['Очікувана вартість'].astype(float), aspect=10,
      fontsize=3, figureName="GeneralSankey") 

    # Organizers analysis   
organizers_data = []
organizers=df['Організатор'].unique()
for organizer in organizers:
    organizer_data = {}
    organizer_df= df[(df['Організатор'] == organizer)]
    organizer_data['organizer'] = organizer
    organizer_data['count']=organizer_df['Очікувана вартість'].count()
    organizer_data['sum']=organizer_df['Очікувана вартість'].sum()
    organizer_data['max']=organizer_df['Очікувана вартість'].max()
    organizer_data['min']=organizer_df['Очікувана вартість'].min()
    organizer_data['mean']=organizer_df['Очікувана вартість'].mean()
    organizers_data.append(organizer_data) 

    sankey(
     left=organizer_df['Організатор'], right=organizer_df['Постачальники'], aspect=20, 
     fontsize=3, figureName="./sankeys/{}".format(organizer))

organizer_data_df=pd.DataFrame.from_dict(organizers_data).round(2).sort_values(by=['sum'],ascending=False)
organizer_data_df.to_csv('organizers_info.csv')

# Contractors analysis
contractors = df['Постачальники'].unique()
most_frequency_contractors = Counter(df['Постачальники'].tolist())
most_rich_contractors ={}
for contractor in contractors:
    most_rich_contractors[contractor]= df[(df['Постачальники'] == contractor)]['Очікувана вартість'].sum()

rich_df = pd.DataFrame(list(most_rich_contractors.items()))
rich_df.reset_index().sort_values(by=[1], ascending=False).round(2).head(20).to_csv("top_20_richest_contractors.csv")


contractors_data = []
for contractor in contractors:
    contractor_data = {}
    contractor_df= df[(df['Постачальники'] == contractor)]
    contractor_data['name']=contractor
    contractor_data['sum']=contractor_df['Очікувана вартість'].sum()
    contractor_data['organizers_count']=len(set(df[(df['Постачальники'] == contractor)]['Організатор'].tolist()))
    contractor_data['organizers']=set(df[(df['Постачальники'] == contractor)]['Організатор'].tolist())

    contractors_data.append(contractor_data)

pd.DataFrame.from_dict(contractors_data).round(2).to_csv('contractors_data.csv') 


# FOPs (hardcoded) retriewed from Counter
FOPs = {'ФОП Гаврилюк Василь Васильович | 3041913995': 47, 'ФОП Мартинюк Василь Іванович | 1904417691': 23, 
'ФОП "Шкраба Михайло Дмитрович" | 2003010214': 15, 'ФОП Гордєєва А.М. | 3071810344': 15,
'Фізична особа-підприємець Мойсей Олександр Тарасович | 3163025837': 14, 'ФОП Семенюк Василь Богданович | 2556411275': 14, 
'Фізична особа-підприємець Чорногуз Марія Іванівна | 2998519066': 13, 'Лубяний Павло Олександрович | 2264108092': 12,
 "Галиць Андрій В'ячеславович | 2504510879": 12, 'Фізична особа-підприємець Шевчук Антон Юрійович | 3141918878': 11}

FOPs_data = []
for contractor in FOPs:
    FOP_data = {}
    FOP_df= df[(df['Постачальники'] == contractor)]
    FOP_data['name']=contractor
    FOP_data['sum']=FOP_df['Очікувана вартість'].sum()
    FOP_data['organizers_count']=len(set(df[(df['Постачальники'] == contractor)]['Організатор'].tolist()))
    FOP_data['organizers']=set(df[(df['Постачальники'] == contractor)]['Організатор'].tolist())
    FOP_data['lot_list']=df[(df['Постачальники'] == contractor)]['Лот'].tolist()
    FOPs_data.append(FOP_data)

pd.DataFrame.from_dict(FOPs_data).round(2).sort_values(by=['organizers_count'],ascending=False).to_csv('FOPs_data.csv')


# Wordcloud Generator
wordcloud = df['Лот'].sum()
prepositions = ['згідно','під','за','через','із','для','на','до','без']
for preposition in prepositions:
    wordcloud = wordcloud.replace(preposition,'')

file1 = open("cloud.txt","w") 
file1.writelines(wordcloud)
file1.close()

