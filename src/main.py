import streamlit as st # type: ignore
import time
from pages.add_place import add_place
from pages.delete_place import delete_place
from pages.booking import booking
from pages.payment import render_payments_page, render_payment_page
from pages.view_all_places import view_all_places
from pages.view_place import view_place
from pages.login import render_login_page
from pages.register import render_register_page
from pages.data_base_page import admin_page

def show_message(mes: str):
    message = st.success(mes)
    time.sleep(1)
    message.empty()


def main():

    st.markdown(
        """
        <style>
        body {
            background-color: rgba(211,110,112);
            font-family: sans-serif;
        }

        .stApp {
            width: 80%;
            margin: 0 auto;
            font-family: sans-serif;
        }

        .big-button {
            font-size: 24px;
            padding: 20px;
            width: 100%;
            text-align: center;
            margin: 10px 0;
            background-color: rgba(0, 255, 255, 0.8); /* Добавлено для лучшей видимости текста на фоне */
            border-radius: 10px; /* Добавлен скругленный угол */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Добро пожаловать в сервис по передержке котов")

    # Инициализация состояния сессии
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "page" not in st.session_state:
        st.session_state.page = None
    if "selected_keep_cat" not in st.session_state:
        st.session_state.selected_keep_cat = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "places" not in st.session_state:
        st.session_state.places = []
    if "booking_id" not in st.session_state:
        st.session_state.booking_id = None

    if st.session_state.user_role is None:
        col1 = st.columns(1)[0]
        
        with col1:
            if st.button("Войти", key="login_button", help="Перейти на страницу входа", use_container_width=True):
                st.session_state.page = "login"
        
        with col1:
            if st.button("Зарегистрироваться", key="register_button", help="Перейти на страницу регистрации", use_container_width=True):
                st.session_state.page = "register"
        
        if st.session_state.page == "login":
            render_login_page()
        elif st.session_state.page == "register":
            render_register_page()
    else:
        # Логика для авторизованных пользователей
        col2 = st.columns(1)[0]

        if st.session_state.user_role == "admin":
            with col2:
                st.success("Добро пожаловать, Администратор!")
                if st.button("Добавить место", key="add_place_button", use_container_width=True):
                    st.session_state.page = "add_place"
                if st.button("Удалить место", key="delete_place_button", use_container_width=True):
                    st.session_state.page = "delete_place"
                if st.button("Все места", key="view_all_places_button", use_container_width=True):
                    st.session_state.page = "view_all_places"
                if st.button("Просмотр места", key="view_place_button", use_container_width=True):
                    st.session_state.page = "view_place"
                if st.button("Администрирование", key="admin_button", use_container_width=True):
                    st.session_state.page = "admin"
        
        elif st.session_state.user_role == "user":
            with col2:
                st.success("Добро пожаловать, пользователь!")
                if st.button("Все места", key="view_all_places_button", use_container_width=True):
                    st.session_state.page = "view_all_places"
                if st.button("Забронировать место", key="booking_button", use_container_width=True):
                    st.session_state.page = "booking"
                if st.button("Просмотреть бронирования", key="view_booking_payments_button", use_container_width=True):
                    st.session_state.page = "payments"

        with col2:
            if st.button("Выйти", key="logout_button", use_container_width=True):
                st.session_state.page = "exit"

        if st.session_state.page == "add_place":
            add_place()
        elif st.session_state.page == "delete_place":
            delete_place()
        elif st.session_state.page == "view_all_places":
            view_all_places()
        elif st.session_state.page == "view_place":
            view_place()
        elif st.session_state.page == "admin":
            admin_page()
        elif st.session_state.page == "booking":
            booking()
        elif st.session_state.page == "payments":
            render_payments_page()
        elif st.session_state.page == "payment":
            render_payment_page()
        elif st.session_state.page == "exit":
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()