-- Добавление информации о местах
INSERT INTO 
    places(address, count_free) 
VALUES 
    ('Алтуфьевское шоссе, 28к1', 5),
    ('улица Короленко, 3с12', 5),
    ('Авиамоторная улица, 4к4', 5),
    ('Подъёмная улица, 12А', 5),
    ('Волгоградский проспект, 32к45', 5),
    ('Варшавское шоссе, 9с1', 5),
    ('Варшавское шоссе, 118к1', 5),
    ('улица Довженко, 8', 5),
    ('улица Мнёвники, 1с5', 5),
    ('улица Адмирала Макарова, 11', 5);

-- Добавление пользователей (админов)
INSERT INTO 
    users(first_name, last_name, email, password_hash, role)
VALUES
    ('Иван', 'Иванов', 'admin@example.com', '$2b$12$WWivymLjMT2MYLQxwY7UsOuU21u52rbPckBK1XB5guOQUC/FlQ0Uu', 'admin'),
    ('Олег', 'Шепс', 'superadmin@example.com', '$2b$12$1eQRCLcl0QfQ2jUunoHVx.hLwV.zaPiB8NtaP8k9b6nEBWmjsuMbO', 'admin');