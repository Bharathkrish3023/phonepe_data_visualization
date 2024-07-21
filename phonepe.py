import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import pymysql
import json
import requests
from PIL import Image


#Dataframe Creation

#sql connection
mydb=pymysql.connect(
        host="localhost",
        user="root",  
        password="root",  
        port=3306,
        database = 'phonepe_data')
mycursor=mydb.cursor()

#aggre_insurance_df
mycursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= mycursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States", "Years", "Quarter", 
                                             "Transaction_type", 
                                             "Transaction_count",
                                             "Transaction_amount"))

#aggre_transaction_df
mycursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= mycursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States", "Years", "Quarter", 
                                             "Transaction_type", 
                                             "Transaction_count",
                                             "Transaction_amount"))

#aggre_user_df
mycursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= mycursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States", "Years", "Quarter", 
                                             "Brands", 
                                             "Transaction_count",
                                             "Percentage"))

#map_insurance_df
mycursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= mycursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States", "Years", "Quarter", 
                                             "District", 
                                             "Transaction_count",
                                             "Transaction_amount"))

#map_transaction_df
mycursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= mycursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States", "Years", "Quarter", 
                                             "District", 
                                             "Transaction_count",
                                             "Transaction_amount"))

#map_user_df
mycursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= mycursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States", "Years", "Quarter", 
                                             "District", 
                                             "RegisteredUsers",
                                             "AppOpens"))

#top_insurance_df
mycursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= mycursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States", "Years", "Quarter", 
                                             "Pincodes", 
                                             "Transaction_count",
                                             "Transaction_amount"))

#top_transaction_df
mycursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= mycursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States", "Years", "Quarter", 
                                             "Pincodes", 
                                             "Transaction_count",
                                             "Transaction_amount"))

#top_user_df
mycursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= mycursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States", "Years", "Quarter", 
                                             "Pincodes", 
                                             "RegisteredUsers"))


# Transaction_Year_Based
def Transaction_amount_count_Y(df, year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(tacyg, x="States", y= "Transaction_amount", title=f"{year} TRANASACTION AMOUNT", 
                           color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y= "Transaction_count", title=f"{year} TRANASACTION COUNT", 
                          color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_amount", color_continuous_scale= "rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANASACTION AMOUNT", fitbounds= "locations",
                                height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_count", color_continuous_scale= "rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} TRANASACTION COUNT", fitbounds= "locations",
                                height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy


# Transaction_Quarter_Based
def Transaction_amount_count_Y_Q(df, quarter):
    #tacyg = transaction amount & count year groupby()
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(tacyg, x="States", y= "Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANASACTION AMOUNT", 
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y= "Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANASACTION COUNT", 
                        color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_amount", color_continuous_scale= "rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANASACTION AMOUNT", fitbounds= "locations",
                                height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_count", color_continuous_scale= "rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANASACTION COUNT", fitbounds= "locations",
                                height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

# Transaction_Type
def Aggre_Tran_Transaction_type(df, state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= tacyg, names="Transaction_type", values="Transaction_amount",
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)
    
    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg, names="Transaction_type", values="Transaction_count",
                        width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)


# Aggregated_user_analysis_using year
def Aggre_user_plot_1(df, year):
    #aguyg = aggregated user year groupby()
    aguy = df[df["Years"]== year]
    aguy.reset_index(drop=True, inplace= True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyg, x="Brands", y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence= px.colors.sequential.Bluered_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggre_user_analysis_using quarter
def Aggre_user_plot_2(df, quarter):
    # aguyqg = aggregated user year quarter groupby()
    aguyq = df[df["Quarter"]== quarter]
    aguyq.reset_index(drop=True, inplace= True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_2 = px.bar(aguyqg, x="Brands", y="Transaction_count",title=f"{quarter} QUARTER  (BRANDS AND TRANSACTION COUNT)",
                    width=900, color_discrete_sequence= px.colors.sequential.Bluered_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_2)

    return aguyq

# Aggre_user_analysis_3
def Aggre_user_plot_3(df,state):
    #auyqs = aggregated user year quarter states
    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop=True, inplace= True)

    fig_line_1= px.line(auyqs, x="Brands", y="Transaction_count",hover_data="Percentage",
                        title=f"{state.upper()} (BRANDS & TRANSACTION COUNT & PERCENTAGE)",width=1000, markers=True)
    st.plotly_chart(fig_line_1)


#Map_insurance_District
def map_insur_District(df, state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x= "Transaction_amount", y="District", orientation= "h",height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT" ,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2 = px.bar(tacyg, x= "Transaction_count", y="District", orientation= "h", height=600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT" ,color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


# Map_user_year_plot
def map_user_plot_1(df, year):
    muy = df[df["Years"]== year]
    muy.reset_index(drop=True, inplace= True)

    muyg = muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1= px.line(muyg, x="States", y=["RegisteredUsers", "AppOpens"],
                            title=f"{year} REGISTEREDUSERS & APPOPENS", width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_1)

    return muy


# Map_user_quarter_plot
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"]== quarter]
    muyq.reset_index(drop=True, inplace= True)

    muyqg = muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_2= px.line(muyqg, x="States", y=["RegisteredUsers", "AppOpens"],
                            title=f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTEREDUSERS & APPOPENS", width=1000, height=800, markers=True,
                            color_discrete_sequence=px.colors.sequential.Bluered)
    st.plotly_chart(fig_line_2)

    return muyq


# Map_user_quarter_district_plot
def map_user_plot_3(df, state):
    muyqs = df[df["States"]== state]
    muyqs.reset_index(drop=True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x="RegisteredUsers", y="District", orientation="h",
                                    title=f"{states.upper()} DISTRICT WISE REGISTEREDUSERS", height= 800, color_discrete_sequence=px.colors.sequential.Emrld_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x="AppOpens", y="District", orientation="h",
                                    title=f"{states.upper()} DISTRICT WISE APPOPENS", height= 800, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)


# Top_insurance_plot_1
def top_insurance_plot_1(df, state ):
    tiy = df[df["States"]== state]
    tiy.reset_index(drop=True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_top_insur_bar_1 = px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data= "Pincodes" ,
                                    title="TRANSACTION AMOUNT", height= 800, color_discrete_sequence=px.colors.sequential.Bluered)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2 = px.bar(tiy, x="Quarter", y="Transaction_count", hover_data= "Pincodes" ,
                                    title="TRANSACTION COUNT", height= 800, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_top_insur_bar_2)

#Top_user_year_wise
def top_user_plot_1(df,year):
    tuy = df[df["Years"]== year]
    tuy.reset_index(drop=True, inplace= True)

    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1= px.bar(tuyg, x="States", y="RegisteredUsers", color="Quarter",hover_name= "States", width= 1000, height= 800,
                        color_discrete_sequence=px.colors.sequential.Bluered_r, title=f"{year} REGISTEREDUSERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


#Top_user_state_wise
def top_user_plot_2(df, state):
    tuys =df[df["States"]== state]
    tuys.reset_index(drop=True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                            width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)


#transaction_amount_for_questions1,2,3,4,5,6,7
def top_chart_transaction_amount(table_name):
    mydb=pymysql.connect(
            host="localhost",
            user="root",  
            password="root",  
            port=3306,
            database = 'phonepe_data')
    mycursor=mydb.cursor()


    # Plot_1 (top 10 details)
    query1 = f'''SELECT states, sum(transaction_amount) as Transaction_amount  
                FROM {table_name}
                group by states
                order by transaction_amount desc
                limit 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns=("states","transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="states", y= "transaction_amount", title="TOP 10 (TRANASACTION AMOUNT)", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_amount_1)


    # Plot_2 (last 10 details)
    query2 = f'''SELECT states, sum(transaction_amount) as Transaction_amount  
                FROM {table_name}
                group by states
                order by transaction_amount 
                limit 10;'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns=("states","transaction_amount"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y= "transaction_amount", title="LAST 10 (TRANASACTION AMOUNT)", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_amount_2)


    # Plot_3 (avg of transaction amount)
    query3 = f'''SELECT states, avg(transaction_amount) as Transaction_amount  
                FROM {table_name}
                group by states
                order by transaction_amount;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns=("states","transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_3= px.bar(df_3, y="states", x= "transaction_amount", title="AVG (TRANASACTION AMOUNT)", hover_name="states", orientation="h",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_3)


#transaction_count_for_questions1,2,3,4,5,6,7
def top_chart_transaction_count(table_name):
    mydb=pymysql.connect(
            host="localhost",
            user="root",  
            password="root",  
            port=3306,
            database = 'phonepe_data')
    mycursor=mydb.cursor()


    # Plot_1 (top 10 details)
    query1 = f'''SELECT states, sum(transaction_count) as Transaction_count  
                FROM {table_name}
                group by states
                order by transaction_count desc
                limit 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns=("states","transaction_count"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="states", y= "transaction_count", title="TOP 10 (TRANASACTION COUNT)", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_amount_1)


    # Plot_2 (last 10 details)
    query2 = f'''SELECT states, sum(transaction_count) as Transaction_count  
                FROM {table_name}
                group by states
                order by transaction_count 
                limit 10;'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns=("states","transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y= "transaction_count", title="LAST 10 (TRANASACTION COUNT)", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_amount_2)


    # Plot_3 (avg of transaction amount)
    query3 = f'''SELECT states, avg(transaction_count) as Transaction_count  
                FROM {table_name}
                group by states
                order by transaction_count;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns=("states","transaction_count"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_3= px.bar(df_3, y="states", x= "transaction_count", title=" AVG (TRANASACTION COUNT)", hover_name="states", orientation="h",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_3)


#REGISTERED USERS_for_questions 8
def top_chart_registeredusers(table_name, state):
    mydb=pymysql.connect(
            host="localhost",
            user="root",  
            password="root",  
            port=3306,
            database = 'phonepe_data')
    mycursor=mydb.cursor()


    # Plot_1 (top 10 details)
    query1 = f'''SELECT district, sum(registeredusers) as registeredusers 
                FROM {table_name}
                where states= '{state}'
                group by district
                order by registeredusers desc
                limit 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns=("district","registeredusers"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="district", y= "registeredusers", title="TOP 10 (REGISTERED USERS)", hover_name="district",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_amount_1)


    # Plot_2 (last 10 details)
    query2 = f'''SELECT district, sum(registeredusers) as registeredusers 
                FROM {table_name}
                where states= '{state}'
                group by district
                order by registeredusers 
                limit 10;'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns=("district","registeredusers"))

    with col2:
        fig_amount_2= px.bar(df_2, x="district", y= "registeredusers", title="LAST 10 (REGISTERED USERS)", hover_name="district",
                            color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_amount_2)


    # Plot_3 (avg of registeredusers)
    query3 = f'''SELECT district, avg(registeredusers) as registeredusers 
                FROM {table_name}
                where states= '{state}'
                group by district
                order by registeredusers;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns=("district","registeredusers"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_3= px.bar(df_3, y="district", x= "registeredusers", title="AVG (REGISTERED USERS)", hover_name="district", orientation="h",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_3)


#APPOPENS_for_questions 9
def top_chart_appopens(table_name, state):
    mydb=pymysql.connect(
            host="localhost",
            user="root",  
            password="root",  
            port=3306,
            database = 'phonepe_data')
    mycursor=mydb.cursor()


    # Plot_1 (top 10 details)
    query1 = f'''SELECT district, sum(appopens) as appopens 
                FROM {table_name}
                where states= '{state}'
                group by district
                order by appopens desc
                limit 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns=("district","appopens"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="district", y= "appopens", title="TOP 10 (APPOPENS)", hover_name="district",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_amount_1)


    # Plot_2 (last 10 details)
    query2 = f'''SELECT district, sum(appopens) as appopens 
                FROM {table_name}
                where states= '{state}'
                group by district
                order by appopens 
                limit 10;'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns=("district","appopens"))

    with col2:
        fig_amount_2= px.bar(df_2, x="district", y= "appopens", title="LAST 10 (APPOPENS)", hover_name="district",
                            color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_amount_2)


    # Plot_3 (avg of transaction amount)
    query3 = f'''SELECT district, avg(appopens) as appopens 
                FROM {table_name}
                where states= '{state}'
                group by district
                order by appopens;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns=("district","appopens"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_3= px.bar(df_3, y="district", x= "appopens", title="AVG (APPOPENS)", hover_name="district", orientation="h",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_3)


#Registered_users_of_top_user_question 10
def top_chart_registeredusers_top_user(table_name):
    mydb=pymysql.connect(
            host="localhost",
            user="root",  
            password="root",  
            port=3306,
            database = 'phonepe_data')
    mycursor=mydb.cursor()


    # Plot_1 (top 10 details)
    query1 = f'''SELECT states, sum(registeredusers) as registeredusers
                FROM {table_name}
                group by states
                order by registeredusers desc 
                limit 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns=("states","registeredusers"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1= px.bar(df_1, x="states", y= "registeredusers", title="TOP 10 (REGISTERED USERS)", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_amount_1)


    # Plot_2 (last 10 details)
    query2 = f'''SELECT states, sum(registeredusers) as registeredusers
                FROM {table_name}
                group by states
                order by registeredusers 
                limit 10;'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns=("states","registeredusers"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y= "registeredusers", title="LAST 10 (REGISTERED USERS)", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Bluered, height=650, width=600)
        st.plotly_chart(fig_amount_2)


    # Plot_3 (avg of transaction amount)
    query3 = f'''SELECT states, avg(registeredusers) as registeredusers
                FROM {table_name}
                group by states
                order by registeredusers;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns=("states","registeredusers"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount_3= px.bar(df_3, y="states", x= "registeredusers", title="AVG (REGISTERED USERS)", hover_name="states", orientation="h",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_3)






#Streamlit interface
st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS",])

if select == "HOME":
    
    col1,col2= st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\BharathKrishna.S\Downloads\images.png"),width= 700)

    col3,col4= st.columns(2)

    with col3:
        st.image(Image.open(r"C:\Users\BharathKrishna.S\Downloads\images.jfif"),width=600)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\BharathKrishna.S\Downloads\maxresdefault.jpg"),width= 700)

elif select== "DATA EXPLORATION":

    tab1, tab2, tab3  = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method = st.radio("select the method",["Aggregated Insurance","Aggregated Transaction","Aggregated User"])
        
        if method == "Aggregated Insurance":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR AI", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(), Aggre_insurance["Years"].min())
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("SELECT THE QUARTER FOR AI", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)
                

        elif method == "Aggregated Transaction":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR AT", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(), Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES FOR AT", Aggre_tran_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("SELECT THE QUARTER FOR AT", Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES TYPE FOR AT", Aggre_tran_tac_Y_Q["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)


        elif method == "Aggregated User":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR AU", Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("SELECT THE QUARTER FOR AU", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES FOR AU", Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
            


    with tab2:

        method_2 = st.radio("select the method",["Map Insurance","Map Transaction","Map User"])
        
        if method_2 == "Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR MI", Map_insurance["Years"].min(), Map_insurance["Years"].max(), Map_insurance["Years"].min())
            map_insur_tac_Y= Transaction_amount_count_Y(Map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES FOR MI", map_insur_tac_Y["States"].unique())
            map_insur_District(map_insur_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("SELECT THE QUARTER FOR MI", map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES TYPES FOR MI", map_insur_tac_Y_Q["States"].unique())
            map_insur_District(map_insur_tac_Y_Q, states)

        elif method_2 == "Map Transaction":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR MT", Map_transaction["Years"].min(), Map_transaction["Years"].max(), Map_transaction["Years"].min())
            map_tran_tac_Y= Transaction_amount_count_Y(Map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES FOR MT", map_tran_tac_Y["States"].unique())
            map_insur_District(map_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("SELECT THE QUARTERS FOR MT", map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES TYPES FOR MT", map_tran_tac_Y_Q["States"].unique())
            map_insur_District(map_tran_tac_Y_Q, states)

        elif method_2 == "Map User":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR MU", Map_user["Years"].min(), Map_user["Years"].max(), Map_user["Years"].min())
            map_user_Y= map_user_plot_1(Map_user, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("SELECT THE QUARTER FOR MU", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES TYPES FOR MU", map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, states)


    with tab3:

        method_3 = st.radio("select the method",["Top Insurance","Top Transaction","Top User"])
        
        if method_3 == "Top Insurance":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR TI", Top_insurance["Years"].min(), Top_insurance["Years"].max(), Top_insurance["Years"].min())
            top_insur_tac_Y= Transaction_amount_count_Y(Top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES TYPES FOR TI", top_insur_tac_Y["States"].unique())
            top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("SELECT THE QUARTER FOR TI", top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)
            

        elif method_3 == "Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR TT", Top_transaction["Years"].min(), Top_transaction["Years"].max(), Top_transaction["Years"].min())
            top_tran_tac_Y= Transaction_amount_count_Y(Top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES TYPES FOR TT", top_tran_tac_Y["States"].unique())
            top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("SELECT THE QUARTER FOR TT", top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)

        elif method_3 == "Top User":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("SELECT THE YEAR FOR TU", Top_user["Years"].min(), Top_user["Years"].max(), Top_user["Years"].min())
            top_user_Y= top_user_plot_1(Top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATES TYPES FOR TU", top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y, states)


elif select== "TOP CHARTS":
    
    question = st.selectbox("SELECT THE QUESTION", ["1.Transaction Amount and Count of Aggregated Insurance",
                                                   "2.Transaction Amount and Count of Map Insurance",
                                                    "3.Transaction Amount and Count of Top Insurance",
                                                    "4.Transaction Amount and Count of Aggregated Transaction",
                                                    "5.Transaction Amount and Count of Map Transaction",
                                                    "6.Transaction Amount and Count of Top Transaction",
                                                    "7.Transaction Count of Aggregated User",
                                                    "8.Registered users of Map User",
                                                    "9.Appopens of Map User",
                                                    "10.Registered users of Top User"])
    
    if question == "1.Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT OF AGGREGATED INSURANCE")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT OF AGGREGATED INSURANCE")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2.Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT OF MAP INSURANCE")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT OF MAP INSURANCE")
        top_chart_transaction_count("map_insurance")

    elif question == "3.Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT OF TOP INSURANCE")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT OF TOP INSURANCE")
        top_chart_transaction_count("top_insurance")

    elif question == "4.Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT OF AGGREGATED TRANSACTION")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT OF AGGREGATED TRANSACTION")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5.Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT OF MAP TRANSACTION")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT OF MAP TRANSACTION")
        top_chart_transaction_count("map_transaction")

    elif question == "6.Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT OF TOP TRANSACTION")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT OF TOP TRANSACTION")
        top_chart_transaction_count("top_transaction")

    elif question == "7.Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT OF AGGREGATED USER")
        top_chart_transaction_count("aggregated_user")

    elif question == "8.Registered users of Map User":

        states = st.selectbox ("SELECT THE STATE", Map_user["States"].unique())
        st.subheader("REGISTERED USERS OF MAP USER")
        top_chart_registeredusers("map_user", states)

    elif question == "9.Appopens of Map User":

        states = st.selectbox ("SELECT THE STATE", Map_user["States"].unique())
        st.subheader("APPOPENS OF MAP USER")
        top_chart_appopens("map_user", states)

    elif question == "10.Registered users of Top User":

        st.subheader("REGISTERED USERS OF TOP USER")
        top_chart_registeredusers_top_user("top_user")


    
