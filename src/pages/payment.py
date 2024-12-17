import streamlit as st # type: ignore
from services.keep_cat_service import KeepCatService
from services.payment_service import PaymentService
from datetime import datetime
import re

keep_cat_service = KeepCatService()


def render_payment_page():
    st.title("Оплата (2000 руб)")
    if "user_id" not in st.session_state:
        st.error("Ошибка: пользователь не авторизован.")
        return

    if "booking_data" not in st.session_state or st.session_state["booking_data"] is None:
        st.error("Ошибка: данные бронирования не найдены.")
        return

    booking_data = st.session_state["booking_data"]
    
    card_number = st.text_input("Введите номер карты")
    card_expiry = st.text_input("Введите срок действия карты (MM/YY)")
    card_cvc = st.text_input("Введите CVC")

    if card_number and not re.match(r"^\d{16}$", card_number):
        st.error("Номер карты должен содержать 16 цифр.")
        return

    if card_expiry and not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", card_expiry):
        st.error("Срок действия карты должен быть в формате MM/YY.")
        return

    if card_cvc and not re.match(r"^\d{3}$", card_cvc):
        st.error("CVC код должен содержать 3 цифры.")
        return
    
    if st.button("Оплатить"):
        if not card_number or not card_expiry or not card_cvc:
            st.error("Пожалуйста, заполните все поля.")
            return

        payment_service = PaymentService()
        try:
            booking_id = keep_cat_service.confirm_booking(booking_data) #add the booking info to the database
            if booking_id:
                payment_id = payment_service.create_payment(
                    booking_id=booking_id,
                    amount=2000,
                    card_number=card_number,
                    card_expiry=card_expiry,
                    card_cvc=card_cvc
                )
                st.success("Оплата прошла успешно!")
                payment_service.update_payment_status(payment_id, 'Оплачено')
                st.session_state.page = "home"
            else:
                st.error("Ошибка при создании бронирования.")


        except Exception as e:
            st.error(f"Ошибка при оплате: {str(e)}")

def render_payments_page():
    st.title("Мои успешные бронирования")

    if "user_id" not in st.session_state:
        st.error("Ошибка: пользователь не авторизован.")
        return

    user_id = st.session_state.user_id

    try:
        bookings = keep_cat_service.get_user_bookings(user_id)
    except Exception as e:
        st.error(f"Ошибка при получении данных о бронированиях: {e}")
        return

    if not bookings:
        st.write("Вы еще ничего не бронировали :(")
        return

    booking_data = []
    for booking in bookings:
        booking_date_str = booking['booking_date']
        if isinstance(booking_date_str, datetime):
            booking_date_str = booking_date_str.strftime('%d %b %Y')
        booking_data.append({
            "Дата бронирования": booking_date_str,
            "Место": booking['place_address'],
            "Кличка": booking['cat_nickname']
        })

    st.dataframe(booking_data)