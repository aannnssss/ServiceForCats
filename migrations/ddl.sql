
-- Таблица для хранения информации о месте
CREATE TABLE places (
    place_id SERIAL PRIMARY KEY,
    address VARCHAR(100) NOT NULL,
    count_free INT NOT NULL CHECK (count_free BETWEEN 0 AND 5)
);

COMMENT ON TABLE places IS 'Информация о местах';
COMMENT ON COLUMN places.place_id IS 'Уникальный идентификатор места';
COMMENT ON COLUMN places.address IS 'Адрес места';
COMMENT ON COLUMN places.count_free IS 'Количество свободных мест';


-- Таблица для хранения информации о пользователях
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'admin'))
);

COMMENT ON TABLE users IS 'Информация о пользователях';
COMMENT ON COLUMN users.user_id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN users.first_name IS 'Имя пользователя';
COMMENT ON COLUMN users.last_name IS 'Фамилия пользователя';
COMMENT ON COLUMN users.email IS 'Email пользователя';
COMMENT ON COLUMN users.password_hash IS 'Хеш пароля пользователя';
COMMENT ON COLUMN users.role IS 'Роль пользователя (например, "admin", "user")';

-- Таблица для хранения информации о котах
CREATE TABLE cats (
    cat_id SERIAL PRIMARY KEY,
    nickname VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    features VARCHAR(100) NOT NULL,
    breed VARCHAR(50) NOT NULL
);

COMMENT ON TABLE cats IS 'Информация о котах';
COMMENT ON COLUMN cats.cat_id IS 'Уникальный идентификатор кота';
COMMENT ON COLUMN cats.nickname IS 'Кличка кота';
COMMENT ON COLUMN cats.age IS 'Возраст кота';
COMMENT ON COLUMN cats.features IS 'Особенности кота';
COMMENT ON COLUMN cats.breed IS 'Порода кота';

-- Таблица для хранения информации о бронированиях
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY, 
    user_id INT NOT NULL,
    cat_id INT NOT NULL, 
    place_id INT NOT NULL,
    booking_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (cat_id) REFERENCES cats(cat_id),
    FOREIGN KEY (place_id) REFERENCES places(place_id)
);

COMMENT ON TABLE bookings IS 'Информация о бронированиях';
COMMENT ON COLUMN bookings.booking_id IS 'Уникальный идентификатор бронирования';
COMMENT ON COLUMN bookings.user_id IS 'Идентификатор пользователя, который сделал бронирование';
COMMENT ON COLUMN bookings.cat_id IS 'Идентификатор кота, для которого было сделано бронирование';
COMMENT ON COLUMN bookings.place_id IS 'Идентификатор места, в котором было забронировано';
COMMENT ON COLUMN bookings.booking_date IS 'Дата бронирования';

-- Таблица для хранения информации о платежах
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    booking_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    status VARCHAR(50) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    card_expiry VARCHAR(7) NOT NULL,
    card_cvc VARCHAR(4) NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);

COMMENT ON TABLE payments IS 'Информация о платежах';
COMMENT ON COLUMN payments.payment_id IS 'Уникальный идентификатор платежа';
COMMENT ON COLUMN payments.booking_id IS 'Идентификатор бронирования, к которому привязан платеж';
COMMENT ON COLUMN payments.payment_date IS 'Дата платежа';
COMMENT ON COLUMN payments.amount IS 'Сумма платежа';
COMMENT ON COLUMN payments.status IS 'Статус платежа';
COMMENT ON COLUMN payments.card_number IS 'Номер карты';
COMMENT ON COLUMN payments.card_expiry IS 'Срок действия карты';
COMMENT ON COLUMN payments.card_cvc IS 'CVC';

-- Функция триггера, уменьшающая count_free для места
CREATE OR REPLACE FUNCTION decrease_place_count_free()
RETURNS TRIGGER AS $$
BEGIN
    -- Уменьшаем count_free на 1 для места из новой записи в bookings
    UPDATE places
    SET count_free = count_free - 1
    WHERE place_id = NEW.place_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер, выполняющийся после добавления записи в bookings
CREATE TRIGGER bookings_after_insert
AFTER INSERT ON bookings
FOR EACH ROW
EXECUTE FUNCTION decrease_place_count_free();
