from repositories.keepcat import KeepCatRepository
from datetime import datetime, timedelta

class KeepCatService:
    def __init__(self):
        self.repo = KeepCatRepository()

    def get_places_with_free_count(self, date: str):
        """Получает список мест с количеством свободных мест на указанную дату."""
        return self.repo.get_places_with_free_count(date) 
    
    def get_place_info(self, place_id: int):
        """ Получает информацию о месте по его ID """
        place = self.repo.get_place_info(place_id)
        if place:
            return {"place_id": place["place_id"], "address": place["address"], "count_free": place["count_free"]}
        else:
            return None  # Если место не найдено

    def create_booking(self, user_id: int, nickname: str, age: int, features: str, breed: str, place_id: int, booking_date: str):
        """
        Creates a booking and returns booking data
        """
        print(f"create_booking: user_id={user_id}, nickname={nickname}, age={age}, features={features}, breed={breed}, place_id={place_id}, booking_date={booking_date}")
        
        cat_id = self._get_or_create_cat_id(nickname, age, features, breed)
        if cat_id is None:
            print(f"create_booking: _get_or_create_cat_id returned None")
            return None
        return {
            "user_id": user_id,
            "cat_id": cat_id,
            "place_id": place_id,
            "booking_date": booking_date
        }
    
    def confirm_booking(self, booking_data):
        """
        Confirms a booking by adding it to the database
        """
        if not booking_data:
            print(f"confirm_booking: no booking data")
            return None
        print(f"confirm_booking: booking_data={booking_data}")

        booking_id = self.repo.book_place(**booking_data)  # Pass the dict directly
        print(f"confirm_booking: booking_id={booking_id}")
        return booking_id

    def _get_or_create_cat_id(self, nickname: str, age: int, features: str, breed: str):
        print(f"_get_or_create_cat_id: nickname={nickname}, age={age}, features={features}, breed={breed}")
        cat_id = self.repo.get_cat_id(nickname, age, features, breed)
        if cat_id:
            print(f"_get_or_create_cat_id: Cat found with id {cat_id}")
            return cat_id
        else:
            print(f"_get_or_create_cat_id: Cat not found, creating new cat")
            return self.repo.create_cat(nickname, age, features, breed)
        
    def view_booking_details(self, place_id: int, date: str):
        """ Просмотр всех бронирований для определенного места """
        return self.repo.get_bookings_by_place(place_id, date)

    def add_place(self, address: str, count_free: int) -> int:
        """ Добавление нового места """
        return self.repo.add_place(address, count_free)

    def check_future_bookings(self, place_id: int) -> bool:
        """ Проверяет наличие будущих бронирований для места. """
        return self.repo.check_future_bookings(place_id)

    def delete_place(self, place_id: int):
        """ Удаляет место по его ID. """
        self.repo.delete_place(place_id)

    def update_payment_status(self, payment_id: int, status: str):
        """ Обновление статуса платежа """
        return self.repo.update_status(payment_id, status)

    def get_user_bookings(self, user_id: int):
        """ Получение всех бронирований для пользователя """
        return self.repo.get_user_bookings(user_id)

    def get_booking_info(self, booking_id: int):
         return self.repo.get_booking_info(booking_id)