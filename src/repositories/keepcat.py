from typing import List, Dict, Optional
from repositories.connector import get_connection

class KeepCatRepository:

    def get_places_with_free_count(self, date: str) -> List[Dict]:
        """Получает список мест и количество свободных мест на указанную дату."""
        query = """
            SELECT 
                p.place_id,
                p.address,
                COALESCE(p.count_free - COUNT(b.place_id), p.count_free) AS free_count
            FROM places p
            LEFT JOIN bookings b ON p.place_id = b.place_id AND b.booking_date = %s
            GROUP BY p.place_id, p.address, p.count_free
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (date,))
                rows = cur.fetchall()
                # Преобразование в список словарей
                result = []
                for row in rows:
                    result.append({
                        "place_id": row[0],
                        "address": row[1],
                        "free_count": row[2]
                    })
                return result
            
    def get_place_info(self, place_id: int) -> Optional[Dict[str, Optional[int]]]:
        """ Получает информацию о месте по его ID. """
        query = """
            SELECT place_id, address, count_free FROM places WHERE place_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (place_id,))
                row = cur.fetchone()
                if row:
                    return {"place_id": row[0], "address": row[1], "count_free": row[2]}
                else:
                    return None  # Если место не найдено

    def book_place(self, user_id: int, cat_id: int, place_id: int, booking_date: str) -> Optional[int]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    conn.autocommit = False  # Начало транзакции
                    cur.execute("""
                        INSERT INTO bookings (user_id, cat_id, place_id, booking_date)
                        VALUES (%s, %s, %s, %s)
                        RETURNING booking_id;
                    """, (user_id, cat_id, place_id, booking_date))
                    booking_id = cur.fetchone()[0]
                    conn.commit()
                    return booking_id
                except Exception as e:
                    conn.rollback()
                    raise e
                
    def create_cat(self, nickname: str, age: int, features: str, breed: str) -> Optional[int]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """
                        INSERT INTO cats (nickname, age, features, breed)
                        VALUES (%s, %s, %s, %s)
                        RETURNING cat_id;
                        """, (nickname, age, features, breed)
                    )
                    cat_id = cur.fetchone()[0]
                    conn.commit()
                    return cat_id
                except Exception as e:
                    conn.rollback()
                    raise e

    def get_cat_id(self, nickname: str, age: int, features: str, breed: str) -> Optional[int]:
        query = """
            SELECT cat_id FROM cats
            WHERE nickname = %s AND age = %s AND features = %s AND breed = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (nickname, age, features, breed))
                row = cur.fetchone()
                return row[0] if row else None

    def get_bookings_by_place(self, place_id: int, date:str) -> List[Dict[str, Optional[int]]]:
        query = """
            SELECT b.booking_id, u.first_name, u.email, c.nickname, b.booking_date
            FROM bookings b
            JOIN users u ON b.user_id = u.user_id
            JOIN cats c ON b.cat_id = c.cat_id
            WHERE b.place_id = %s AND b.booking_date = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (place_id, date,))
                return [{
                    "booking_id": row[0],
                    "user_first_name": row[1],
                    "email": row[2],
                    "cat_nickname": row[3],
                    "booking_date": row[4]
                } for row in cur.fetchall()]        
        
    def add_place(self, address: str, count_free: int) -> int:
        """ Добавляет новое место в базу. """
        
        # Получаем текущий максимальный id из базы данных
        max_id_query = "SELECT COALESCE(MAX(place_id), 0) FROM places;" 
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(max_id_query)
                result = cur.fetchone()[0]
                
        next_id = result + 1  # Формируем следующий уникальный идентификатор

        insert_query = """
            INSERT INTO places (place_id, address, count_free)
            VALUES (%s, %s, %s)
            RETURNING place_id;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(insert_query, (next_id, address, count_free))
                new_id = cur.fetchone()[0]  # Получаем возвращенный идентификатор
                conn.commit()  # Подтверждаем транзакцию
                return new_id
            
    def check_future_bookings(self, place_id: int) -> bool:
        """ Проверяет наличие будущих бронирований для места. """
        query = """
            SELECT EXISTS (
                SELECT 1
                FROM bookings
                WHERE place_id = %s AND booking_date >= CURRENT_DATE
            );
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (place_id,))
                return cur.fetchone()[0] #Вернет True, если есть бронирования, False, если нет
    
    def delete_place(self, place_id: int):
        """ Удаляет место по его ID. """
        query = """
            DELETE FROM places
            WHERE place_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (place_id,))
                conn.commit()
                
    def update_status(self, payment_id: int, status: str) -> None:
        """ Обновляет статус платежа в базе данных. """
        query = """
            UPDATE payments
            SET status = %s
            WHERE payment_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (status, payment_id))

    def get_user_bookings(self, user_id: int) -> List[Dict[str, Optional[int]]]:
        """ Получает все бронирования для указанного пользователя. """
        query = """
            SELECT b.booking_id, p.address, b.booking_date, c.nickname
            FROM bookings b
            JOIN places p ON b.place_id = p.place_id
            JOIN cats c ON b.cat_id = c.cat_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date ASC;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                return [{
                    "booking_id": row[0],
                    "place_address": row[1],
                    "booking_date": row[2],
                    "cat_nickname": row[3]
                } for row in cur.fetchall()]
            
    def get_booking_info(self, booking_id: int) -> Optional[Dict[str, Optional[int]]]:
        """ Получает информацию о конкретном бронировании. """
        query = """
            SELECT b.booking_id, u.first_name, u.last_name, c.nickname, p.address, b.booking_date
            FROM bookings b
            JOIN users u ON b.user_id = u.user_id
            JOIN cats c ON b.cat_id = c.cat_id
            JOIN places p ON b.place_id = p.place_id
            WHERE b.booking_id = %s;

        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (booking_id,))
                row = cur.fetchone()
                if row:
                    return {
                        "booking_id": row[0],
                        "user_first_name": row[1],
                        "user_last_name": row[2],
                        "cat_nickname": row[3],
                        "place_address": row[4],
                        "booking_date": row[5]
                    }
                else:
                    print(f"No booking found for booking id {booking_id}")
                    return None