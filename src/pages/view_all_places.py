import streamlit as st # type: ignore
from services.keep_cat_service import KeepCatService

# Инициализация сервиса
keep_cat_service = KeepCatService()

def view_all_places():
    st.title("Список всех мест")

    selected_date = st.date_input("Выберите дату")
    formatted_date = selected_date.strftime("%Y-%m-%d")
    places = keep_cat_service.get_places_with_free_count(formatted_date)

    # Отображение списка мест
    if places:
        for place in places:
            st.write(f"Адрес: {place["address"]}")
            st.write(f"Количество свободных мест: {place["free_count"]}")
            st.write("---")
    else:
        st.warning("Нет доступных мест.")

if __name__ == "__main__":
    view_all_places()