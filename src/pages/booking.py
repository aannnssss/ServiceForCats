import streamlit as st # type: ignore
from services.keep_cat_service import KeepCatService
from datetime import datetime

keep_cat_service = KeepCatService()

def booking():
    st.title("Бронирование места для вашего кота")
    user_id = st.session_state.user_id
    booking_date = st.date_input("Выберите дату бронирования")
    formatted_date = booking_date.strftime("%Y-%m-%d")

    places = keep_cat_service.get_places_with_free_count(formatted_date)
    available_places = [place for place in places if place['free_count'] > 0]

    if not available_places:
            st.warning("На выбранную дату нет свободных мест. Пожалуйста, выберите другую дату или другое место")
            return

    place_options = {f"{place['address']} (Свободно: {place['free_count']})": place['place_id'] for place in available_places}
    
    selected_place = st.selectbox("Выберите место", options=list(place_options.keys()))

    if selected_place:
        place_id = place_options[selected_place]
        nickname = st.text_input("Введите кличку кота")
        age_str = st.text_input("Введите полное число лет")
        breed = st.text_input("Введите породу кота")
        features = st.text_input("Расскажите об особенностях кота")

        if st.button("Забронировать"):
            if nickname and age_str and breed and features and place_id:
                try:
                    age = int(age_str)
                    booking_data = keep_cat_service.create_booking(
                        user_id=user_id,
                        nickname=nickname,
                        age=age,
                        features=features,
                        breed=breed,
                        place_id=place_id,
                        booking_date=booking_date
                    )
                    if booking_data:
                        st.session_state["booking_data"] = booking_data # save the booking data
                        st.success("Бронирование создано, переходим к оплате.")
                        st.session_state.page = "payment"
                        st.rerun()
                    else:
                         st.error("Ошибка при создании бронирования.")
                except ValueError:
                    st.error("Пожалуйста, введите корректный возраст (целое число).")
                except Exception as e:
                    st.error(f"Ошибка: {str(e)}")
            else:
                 st.warning("Пожалуйста, заполните все поля.")
    else:
         st.warning("Пожалуйста, выберите место.")

if __name__ == "__main__":
    if "booking_data" not in st.session_state:
        st.session_state["booking_data"] = None
    if st.session_state.page == "booking":
        booking()