# Importing libraries
import ast
import numpy as np
import pandas as pd

# To read the data
df=pd.read_csv("Ulta_Women_Fragrance_Data")

# To add 'Composition','Fragrance Family','Scent Type','Key Notes' and 'Features' column to 'Ulta_Women_Fragrance_Data'
df['Composition']=""
df['Fragrance Family']=""
df['Key Notes']=""
df['Scent Type']=""
df['Features']=""

#converting 'Details' TO A dictionary
df['Details']=df['Details'].apply(lambda x:x.strip('][').split(', ')) #to strip and split the 'Details' data
for i in range(len(df)):
    dic={}                                                            #Creating a empty dictionary to store the key-value data
    while dic=={}:
        keys=[]                                                       #creating empty list to store keys
        values=[]                                                     #creating empty list to store keys
        for p in range(len(df['Details'].iloc[i])): 
            section=df['Details'].iloc[i][p]
            section=section.strip("''")                               #strping the 'Details' data
            split_section = section.split('\\n')                      #splitting the 'Details' data
        #     print(split_section)
            
            for j in range(len(split_section)):
                if split_section[j]=='Composition':                   #to get 'Composition' from 'Details' data
                    keys.append(split_section[j])                     #append the key to the key list
                    values.append(split_section[j+1])                 #append the value to the value list

                if split_section[j]=='Fragrance Family':              #to get 'Fragrance Family' from 'Details' data
                    keys.append(split_section[j])                     #append the key to the key list
                    values.append(split_section[j+1])                 #append the value to the value list

                if split_section[j]=='Key Notes':                     #to get 'Key Notes' from 'Details' data
                    keys.append(split_section[j])                     #append the key to the key list
                    values.append(split_section[j+1])                 #append the value to the value list

                if split_section[j]=='Features':                      #to get 'Features' from 'Details' data
                    keys.append(split_section[j])                     #append the key to the key list
                    values.append(split_section[j+1])                 #append the value to the value list

                if split_section[j]=='Scent Type':                    #to get 'Scent Type' from 'Details' data
                    keys.append(split_section[j])                     #append the key to the key list
                    values.append(split_section[j+1])                 #append the value to the value list
                    
                if (p==len(df['Details'].iloc[i])-1) and (j==len(split_section)-1) and (keys==[]):
                    dic=np.nan                                        #if the data note found ,to print NaN value
     
            try:                                                      #try to get the data
                for l in range(len(keys)):
                    dic[keys[l]]=values[l]                            #to store the keys and values in empty dictionary
            except:
                pass                                                  #if the data note found ,to let it pass
            
    df['Details'][i]=dic                                              #to add the dictionary to 'Details' column
    
    
# extracting 'Fragrance Family','Scent Type','Key Notes' and 'Composition' 'Featues' data from 'Details' Dictionary
for i in range(len(df)):                                              #to store the keys and values in empty dictionary
    try: 
        df['Details'][i]=ast.literal_eval(df['Details'][i])           #safely evaluate strings containing data from unknown sources
    except:                                                           #if the data note found ,to let it pass
        pass
    
df=df[df['Details'].apply(lambda x: isinstance(x, dict))]             #converting object to dictionary

for i in range(len(df)):
    df['Fragrance Family'].iloc[i]=df['Details'].iloc[i].get('Fragrance_Family') #To add 'Fragrance Family' data to 'Fragrance Family' column

for i in range(len(df)):
    df['Scent_Type'].iloc[i]=df['Details'].iloc[i].get('Scent_Type')             #To add 'Scent_Type' data to 'Scent_Type' column

for i in range(len(df)):
    df['Key_Notes'].iloc[i]=df['Details'].iloc[i].get('Key_Notes')               #To add 'Key_Notes' data to 'Key_Notes' column   
    
for i in range(len(df)):
    df['Features'].iloc[i]=df['Details'].iloc[i].get('Features')                 #To add 'Features' data to 'Features' column

for i in range(len(df)):
    df['Composition'].iloc[i]=df['Details'].iloc[i].get('Composition')           #To add 'Composition' data to 'Composition' column
    
# to print data
print(df) 

# Convering data to a csv file
df.to_csv("Ulta_Women_Fragrance_Data")

