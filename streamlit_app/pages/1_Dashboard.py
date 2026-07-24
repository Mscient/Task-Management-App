import streamlit as st
import api
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide")

def render():
    st.title("Task Dashboard")
    
    if st.session_state.get("token") is None:
        st.warning("Please login first to view your dashboard.")
        st.stop()
        
    token = st.session_state["token"]
    
    st.header("Create New Task")
    with st.form("create_task"):
        new_title = st.text_input("Title")
        new_desc = st.text_area("Description")
        new_completed = st.checkbox("Is Completed?")
        
        submit_create = st.form_submit_button("Create Task")
        if submit_create:
            if new_title and new_desc:
                res = api.create_task(token, new_title, new_desc, new_completed)
                if res.status_code == 201:
                    st.success("Task created successfully!")
                else:
                    st.error("Failed to create task")
            else:
                st.warning("Title and description are required")

    st.divider()
    
    st.header("Your Tasks")
    if st.button("Refresh Tasks"):
        st.rerun()
        
    res = api.fetch_tasks(token)
    if res.status_code == 200:
        tasks = res.json()
        if not tasks:
            st.info("No tasks found. Create one above!")
        else:
            for task in tasks:
                with st.expander(f"{'✅' if task['is_Completed'] else '⏳'} {task['title']} (ID: {task['id']})"):
                    st.write(f"**Description:** {task['description']}")
                    st.write(f"**Completed:** {task['is_Completed']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Delete Task", key=f"del_{task['id']}"):
                            del_res = api.delete_task(token, task['id'])
                            if del_res.status_code == 204:
                                st.success("Task deleted!")
                                st.rerun()
                            else:
                                st.error("Failed to delete task")
                    
                    with col2:
                        with st.popover("Edit Task"):
                            edit_title = st.text_input("New Title", value=task['title'], key=f"title_{task['id']}")
                            edit_desc = st.text_area("New Description", value=task['description'], key=f"desc_{task['id']}")
                            edit_completed = st.checkbox("Is Completed?", value=task['is_Completed'], key=f"comp_{task['id']}")
                            if st.button("Save Changes", key=f"save_{task['id']}"):
                                update_res = api.update_task(token, task['id'], edit_title, edit_desc, edit_completed)
                                if update_res.status_code == 201:
                                    st.success("Task updated!")
                                    st.rerun()
                                else:
                                    st.error("Failed to update task")
    elif res.status_code == 401:
        st.error("Session expired or unauthorized. Please login again.")
        st.session_state["token"] = None
    else:
        st.error("Failed to fetch tasks.")

if __name__ == "__main__":
    render()
