#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
filepath = os.path.join ('Resources', 'purchase_data.csv')
purchase_df = pd.read_csv(filepath)
purchase_df.head()


# In[2]:


total_players = len(purchase_df['SN'].unique())

total_players_result = pd.DataFrame([{'Total Players': total_players}])
total_players_result


# In[3]:


numbers_of_unique_items = len(purchase_df['Item ID'].unique())
average_price = purchase_df['Price'].mean()
average_price = round(average_price,2)                    #Keep 2 decimals
average_price = "${:.2f}".format(average_price)          #Add the Dollar sign
number_of_purchases = len(purchase_df.index)
total_revenue = purchase_df['Price'].sum()
total_revenue = "${:.2f}".format(total_revenue)              #Add the Dollar sign

purchasing_analysis_total = pd.DataFrame({'Number of Unique Items': [numbers_of_unique_items],
                                          'Average Price': [average_price],
                                          'Number of Purchases': [number_of_purchases], 
                                          'Total Revenue': [total_revenue]})
purchasing_analysis_total


# In[4]:


unique_purchase_df = purchase_df.drop_duplicates(subset=['SN'])        #Drop the rows with the same SN to get the unique players
number_of_male = len(unique_purchase_df.loc[purchase_df['Gender'] == "Male",:])
number_of_female = len(unique_purchase_df.loc[unique_purchase_df['Gender'] == 'Female', :])
number_of_other = len(unique_purchase_df.loc[unique_purchase_df['Gender'] == 'Other / Non-Disclosed', :])
percentage_of_male = (number_of_male/total_players)
percentage_of_male = "{:.2%}".format(percentage_of_male)     #Adding the dollar sign
percentage_of_female = (number_of_female/total_players)
percentage_of_female = "{:.2%}".format(percentage_of_female)
percentage_of_other = (number_of_other/total_players)
percentage_of_other = "{:.2%}".format(percentage_of_other)

gender_demographics = pd.DataFrame({'Gender':['Male','Female','Other / Non-Disclosed'], 
                                    'Total Count':[number_of_male, number_of_female,number_of_other],
                                    'Percentage of Players': [percentage_of_male,percentage_of_female,percentage_of_other]})
gender_demographics.set_index('Gender')


# In[5]:


grouped_purchase_df = purchase_df.groupby(['Gender'])

purchase_count = grouped_purchase_df['Purchase ID'].count()                 #Purchase count per gender
average_price = list(grouped_purchase_df['Price'].mean())                   #Avg purchase price per gender
total_purchase_value = purchase_count * average_price                       #Total purchase value
total_purchase_value_list = list(purchase_count * average_price)
avg_total_purchase_per_person = list(total_purchase_value/(number_of_female,number_of_male,number_of_other))  
grouped_purchase_df = pd.DataFrame(grouped_purchase_df.size().reset_index(name = "Purchase Count"))
grouped_purchase_df ['Average Purchase Price'] = average_price
grouped_purchase_df ['Average Purchase Price'] = grouped_purchase_df ['Average Purchase Price'].map("${:.2f}".format)
grouped_purchase_df ['Total Purchase Value'] = total_purchase_value_list
grouped_purchase_df ['Total Purchase Value'] = grouped_purchase_df ['Total Purchase Value'].map("${:.2f}".format)
grouped_purchase_df ['Avg Total Purchase per Person'] = avg_total_purchase_per_person
grouped_purchase_df ['Avg Total Purchase per Person'] = grouped_purchase_df ['Avg Total Purchase per Person'].map("${:.2f}".format)
grouped_purchase_df.set_index('Gender')


# In[6]:


unique_sn_df = purchase_df.drop_duplicates(subset = 'SN', keep = 'last').copy()
bins = [0,9.9,14,19,24,29,34,39,100]
group_names = ["<10", "10-14", '15-19','20-24','25-29','30-34','35-39','40+']
age = list(unique_sn_df ['Age'])
pd.cut(unique_sn_df['Age'],bins,labels=group_names)
unique_sn_df['Age Range'] = pd.cut(unique_sn_df['Age'],bins,labels=group_names)
age_df = unique_sn_df.groupby('Age Range')
total_count = list(age_df['Age Range'].count())
age_range_percentage = [age/len(unique_sn_df.index)*100 for age in total_count]
age_range_df = pd.DataFrame ({'':group_names,'Total Count':total_count, 'Percentage of Players':age_range_percentage})
age_range_df['Percentage of Players'] = age_range_df['Percentage of Players'].map("{:.2f}%".format)
age_range_df.reset_index()
age_range_df.set_index('')


# In[7]:


purchase_df['Age Ranges'] = pd.cut(purchase_df['Age'],bins,labels=group_names).copy()
grouped_purchase_df = purchase_df.groupby('Age Ranges')
purchase_count = grouped_purchase_df['SN'].count()
average_purchase_price = grouped_purchase_df['Price'].mean()
totol_purchase_value = purchase_count * average_purchase_price
average_total_purchase_per_person = grouped_purchase_df['Price'].sum()/age_df['Age Range'].count()
purchasing_analysis_age_df = pd.DataFrame ({'Purchase Count':purchase_count, 
                                           'Average Purchase Price':average_purchase_price,
                                           'Total Purchase Value':totol_purchase_value,
                                           'Avg Total Purchase per Person':average_total_purchase_per_person})
purchasing_analysis_age_df['Average Purchase Price'] = purchasing_analysis_age_df['Average Purchase Price'].map("${:.2f}".format)
purchasing_analysis_age_df['Total Purchase Value']= purchasing_analysis_age_df['Total Purchase Value'].map("${:.2f}".format)
purchasing_analysis_age_df['Avg Total Purchase per Person']= purchasing_analysis_age_df['Avg Total Purchase per Person'].map("${:.2f}".format)
purchasing_analysis_age_df


# In[8]:


top_spender_df1 = purchase_df.groupby('SN').sum()
total_purchase_value = top_spender_df1["Price"]
top_spender_df2 = purchase_df.groupby('SN').count()
purchase_count = top_spender_df2['Price']
average_purchase_price = total_purchase_value/purchase_count
top_spender_df = pd.DataFrame({'Purchase Count':purchase_count, 
                               'Average Purchase Price': average_purchase_price,
                               'Total Purchase Value': total_purchase_value})
top_spender_df = top_spender_df.sort_values('Total Purchase Value', ascending = False)
top_spender_df['Average Purchase Price'] = top_spender_df['Average Purchase Price'].map("${:.2f}".format)
top_spender_df['Total Purchase Value'] = top_spender_df['Total Purchase Value'].map("${:.2f}".format)
top_spender_df.head()


# In[9]:


popular_item_df = purchase_df[['Item ID', 'Item Name','Price']]
popular_item_df = popular_item_df.groupby(['Item ID','Item Name'])
purchase_count = popular_item_df['Item ID'].count()
total_purchase_value = popular_item_df ['Price'].sum()
item_price = total_purchase_value/purchase_count
popular_df = pd.DataFrame ({'Purchase Count':purchase_count, 'Item Price' : item_price,
                            'Total Purchase Value': total_purchase_value})
popular_df= popular_df.sort_values('Purchase Count',ascending = False)
popular_df['Item Price'] = popular_df['Item Price'].map("${:.2f}".format)
popular_df['Total Purchase Value'] = popular_df['Total Purchase Value'].map("${:.2f}".format)
popular_df.head()


# In[10]:


popular_item_df = purchase_df[['Item ID', 'Item Name','Price']]
popular_item_df = popular_item_df.groupby(['Item ID','Item Name'])
purchase_count = popular_item_df['Item ID'].count()
total_purchase_value = popular_item_df ['Price'].sum()
item_price = total_purchase_value/purchase_count
popular_df = pd.DataFrame ({'Purchase Count':purchase_count, 'Item Price' : item_price,
                            'Total Purchase Value': total_purchase_value})
popular_df= popular_df.sort_values('Total Purchase Value',ascending = False)
popular_df['Item Price'] = popular_df['Item Price'].map("${:.2f}".format)
popular_df['Total Purchase Value'] = popular_df['Total Purchase Value'].map("${:.2f}".format)
popular_df.head()


# In[ ]:




