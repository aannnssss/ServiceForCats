import streamlit as st # type: ignore
from services.keep_cat_service import KeepCatService

keep_cat_service = KeepCatService()

def view_place():
    st.title("Просмотр места")

    selected_date = st.date_input("Выберите дату")
    formatted_date = selected_date.strftime("%Y-%m-%d")
    places = keep_cat_service.get_places_with_free_count(formatted_date)
    
    place_options = {f"{place['address']}": place['place_id'] for place in places}

    selected_place = st.selectbox("Выберите место", options=list(place_options.keys()))
    if selected_place:
        place_id = place_options[selected_place]
        try:
            place_info = keep_cat_service.get_place_info(place_id)
            if place_info:
                st.write(f"Список бронирований для места {selected_place} на {formatted_date}:")
                bookings = keep_cat_service.view_booking_details(place_id, formatted_date)
                if bookings:
                    for booking in bookings:
                        st.write(f"Пользователь: {booking['user_first_name']} {booking['email']}, "
                                f"Кот: {booking['cat_nickname']}")
                else:
                    st.write("Нет бронирований для этого места на выбранную дату.")
            else:
                st.warning("Место не найдено.")
        except Exception as e:
            st.error(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    view_place()