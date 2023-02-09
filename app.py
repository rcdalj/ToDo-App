import streamlit as st
import streamlit.components.v1 as stc

# EDA Packages
import numpy as np
import pandas as pd

# DB functions
from db_funcs import *

# Plotting packages
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import altair as alt
import plotly.express as px

HTML_BANNER = """ 
    <div style="background-color:coral;padding:10px;border-radius:10px"> 
    <h1 style="color:white;text-align:center;">ToDo App (CRUD) </h1> 
    </div> 
    """

def main():
    stc.html(HTML_BANNER)
    create_table()
    menu=["Home", "Create", "Read", "Update", "Delete", "About"]
    choice=st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        pass
    elif choice=="Create":
        st.subheader("Add Item")
        df=pd.DataFrame()
        c1, c2 = st.columns(2)
        with c1:
            task = st.text_area("Task To Do")
        with c2:
            status = st.selectbox("Status", "ToDo Doing Done".split())
            date = st.date_input("Due Date")
        submitted = st.button("Add Task")
        if submitted:
            try:
                add_task(task, status, date)
                st.success(f"Added {task} to Tasks.")
            except Exception as e:
                print(e)
            df = pd.DataFrame(read_all(),
                                  columns="Task Task_Status Due_Date".split())
        with st.expander("Current Data"):
            st.dataframe(df)
    elif choice == "Read":
        df = pd.DataFrame(read_all(),
                          columns="Task Task_Status Due_Date".split())
        with st.expander("View Items"):
            #st.write("View All")
            st.dataframe(df)
        with st.expander("Task Status"):
            task_status_counts=df["Task_Status"].value_counts()
            # fig=plt.figure()
            # sns.countplot(x=df["Task_Status"])
            # st.pyplot(fig)
            task_df = df["Task_Status"].value_counts().to_frame()
            #st.write(task_df)
            task_df=task_df.reset_index()
            st.dataframe(task_df)
            p1=px.bar(task_df, x="index", y="Task_Status")
            st.plotly_chart(p1)
    elif choice == "Update":
        st.subheader("Edit Items")
        df = pd.DataFrame(read_all(),
                          columns="Task Task_Status Due_Date".split())
        edited_data=""
        with st.expander("Current Data"):
            st.dataframe(df)
        with st.expander("Task"):
            #st.write(read_unique_tasks())
            tasks_list=[i[0] for i in read_unique_tasks()]
            #st.write(tasks_list)
            selected_task=st.selectbox("Task to Edit", tasks_list)
            full_task=get_task_by_name(selected_task)[0]
            if full_task:
                c1, c2 = st.columns(2)
                with c1:
                    new_task = st.text_area("Task To Do", full_task[0])
                with c2:
                    new_status = st.selectbox(full_task[1], "ToDo Doing Done".split())
                    new_date = st.date_input(full_task[2])
                submitted = st.button("Update Task")
                if submitted:
                    edited_data=update_task_data(new_task, new_status, new_date, full_task[0], full_task[1], full_task[2])
                    #st.write(edited_data)
        with st.expander("View Updated Data"):
            df = pd.DataFrame(read_all(),
                              columns="Task Task_Status Due_Date".split())
            st.dataframe(df)
    elif choice=="Delete":
        st.subheader("Delete Item")
        df = pd.DataFrame(read_all(),
                          columns="Task Task_Status Due_Date".split())
        with st.expander("Current Data"):
            #st.write("Current Data")
            st.dataframe(df)
        with st.expander("Task to Delete"):
            tasks_list=[i[0] for i in read_unique_tasks()]
            #st.write(tasks_list)
            selected_task=st.selectbox("Task to Edit", tasks_list)
            submitted = st.button("Delete")
            if submitted:
                full_task = get_task_by_name(selected_task)[0]
                delete_task(full_task[0], full_task[1], full_task[2])
                st.warning(f"Deleted {full_task[0]} task")
                st.experimental_rerun()
                df = pd.DataFrame(read_all(),
                          columns="Task Task_Status Due_Date".split())
        with st.expander("Updated Data"):
            st.dataframe(df)
    else:
        with st.subheader("About"):
            st.write("About")



if __name__ == "__main__":
    main()

