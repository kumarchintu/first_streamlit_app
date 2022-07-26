import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega3 and Blueberry Oatmeal')
streamlit.text('Kale, Spinch & Rocket Smoothie')
streamlit.text('Hard-boiled free-range egg')
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
#Let's put a pick list here so they can pick the fruit they want to include
#streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])

#display  the table on the page
#streamlit.dataframe(my_fruit_list)

fruits_selected=streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)



#Create a repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get Information.")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    #streamlit.text(fruityvice_response.json())
    #take the json version of the response and normalize it
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #output it to the screen as table
    #streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()
#don't run anything past here while we troubleshoot
streamlit.stop()

my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur=my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
#my_data_row=my_cur.fetchone()
my_data_rows=my_cur.fetchall()
#streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row)
streamlit.header("The fruit load list contains: ")
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

#Allow the end user to add a fruit to the list
add_my_fruit=streamlit.text_input("What fruit would you like to add?")
streamlit.write("Thanks for adding ",add_my_fruit)
#streamlit.text("Thank for adding "+add_my_fruit)
#my_data_rows.append(add_my_fruit)
#streamlit.dataframe(my_data_rows)

#This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")


