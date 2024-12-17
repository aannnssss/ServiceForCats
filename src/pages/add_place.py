import streamlit as st # type: ignore
from services.keep_cat_service import KeepCatService

keep_cat_service = KeepCatService()

def add_place():

    st.title("Добавить новое место")

    address = st.text_input("Адрес места", "")
    count_free = 5

    if st.button("Добавить место"):
        if address:
            try:
                place_id = keep_cat_service.add_place(address, count_free)
                st.success("Место добавлено успешно!")
                # Обновление состояния в сессии
                st.session_state.places.append({
                    "place_id": place_id,
                    "address": address,
                    "count_free": count_free
                })

            except Exception as e:
                st.error(f"Произошла ошибка: {str(e)}")
        else:
            st.warning("Пожалуйста, введите адрес места.")

if __name__ == "__main__":
    add_place()