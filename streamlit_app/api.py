import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

def login_user(username, password):
    url = f"{BASE_URL}/user/login"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response

def register_user(name, username, email, password):
    url = f"{BASE_URL}/user/register"
    payload = {
        "name": name,
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response

def get_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def fetch_tasks(token):
    url = f"{BASE_URL}/tasks/all_tasks"
    response = requests.get(url, headers=get_auth_headers(token))
    return response

def create_task(token, title, description, is_completed):
    url = f"{BASE_URL}/tasks/create"
    payload = {
        "title": title,
        "description": description,
        "is_Completed": is_completed
    }
    response = requests.post(url, json=payload, headers=get_auth_headers(token))
    return response

def update_task(token, task_id, title, description, is_completed):
    url = f"{BASE_URL}/tasks/update/{task_id}"
    payload = {
        "title": title,
        "description": description,
        "is_Completed": is_completed
    }
    response = requests.put(url, json=payload, headers=get_auth_headers(token))
    return response

def delete_task(token, task_id):
    url = f"{BASE_URL}/tasks/delete/{task_id}"
    response = requests.delete(url, headers=get_auth_headers(token))
    return response
