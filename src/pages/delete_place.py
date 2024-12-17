import streamlit as st # type: ignore
from services.keep_cat_service import KeepCatService
import datetime

keep_cat_service = KeepCatService()

def delete_place():
    st.title("Удаление места")
    today = datetime.date.today()

    places = keep_cat_service.get_places_with_free_count(today)
    place_options = {f"{place['address']}": place['place_id'] for place in places}

    # Выбор места
    selected_address = st.selectbox("Выберите место", options=list(place_options.keys()))

    if selected_address:
        place_id_to_delete = place_options[selected_address]

        if st.button("Удалить место"):
            try:
                # Проверка наличия будущих бронирований
                has_future_bookings = keep_cat_service.check_future_bookings(place_id_to_delete)

                if has_future_bookings:
                    st.error(f"Невозможно удалить место '{selected_address}', так как есть будущие бронирования.")
                else:
                    # Удаление места
                    keep_cat_service.delete_place(place_id_to_delete)
                    st.success(f"Место '{selected_address}' успешно удалено.")
            except Exception as e:
                st.error(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    delete_place()
