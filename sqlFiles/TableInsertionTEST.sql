-- Покупатели
insert into customer(Name, Phone) values
('Магнит','+8(800)200-90-02'),
('Пятёрочка', '88005555505'),
('Перекрёсток', '+7(495)662-88-88'),
('Fix Price', '+7(495)902-50-00'),
('ОКЕЙ', '78612739750');

-- Ингридиенты
insert into ingredient(Name, Price, Info) values
('ТРИРАПИДО 50', 400 , 'Универсальная основа для производства сливочного мороженого с пастеризацией или без, сорбетов, мороженого с фруктовым, ореховым, йогуртовым и другими вкусами, а также мягкого мороженого и молочных коктейлей.'),
('Cливки', 335, ''),
('Cливочное масло', 350, ''),
('Патока',  200, ''),
('Какао-порошок', 155.55, ''),
('Ваниль', 400,'');
call productInsert('Пломбир', 'Классическое мороженое')

-- Продукты
insert into product(Name, Info) values
('Шербет', 'Мягкое мороженое на основе фруктов, ягод, соков'),
('Фруктовый лёд', 'Относительно твёрдое мороженое на палочке на основе сока, обычно без молока'),
('Джелато','Мягкое мороженое с добавлением ягод, орехов, шоколада и свежих фруктов');

-- Ингридиенты в продуктах
--  Щербет 
call PHIInsertUpdate(1, 1);
call PHIInsertUpdate(1, 4, 2);
--  Фруктовый лёд
call PHIInsertUpdate(2, 1);
--  Джелато
call PHIInsertUpdate(3, 2);
call PHIInsertUpdate(3, 3, 2);
call PHIInsertUpdate(3, 4);
-- Пломбир
call PHIInsertUpdate(4, 2);
call PHIInsertUpdate(4, 5);
call PHIInsertUpdate(4, 6);

-- Заказы 
--  Магнит
call orderinsert(1, '2021-08-04', 'shipped');
call orderinsert(1);
--  Пятёрочка
call orderinsert(2, '2021-08-15', 'shipped');
call orderinsert(2, cast(NOW() as date),'in stock');
call orderinsert(2, cast(NOW() as date),'shipped');
--  Перекрёсток
call orderinsert(3, '2021-08-15');
call orderinsert(3, cast(NOW() as date),'in stock');
call orderinsert(3, cast(NOW() as date),'shipped');
call orderinsert(3, '2021-08-20', 'shipped');
--  Fix Price
call orderinsert(4, '2021-08-15', 'shipped');
call orderinsert(4, cast(NOW() as date),'in stock');
call orderinsert(4, cast(NOW() as date));
-- Окей

call orderinsert(5, '2021-07-15');


-- Продукты в заказах
call OHPInsertUpdate(1, 1, 2);
call OHPInsertUpdate(1, 2);

call OHPInsertUpdate(2, 1, 10);
call OHPInsertUpdate(2, 2, 3);
call OHPInsertUpdate(2, 4);

call OHPInsertUpdate(3, 3, 10);

call OHPInsertUpdate(5, 1);
call OHPInsertUpdate(5, 2);
call OHPInsertUpdate(5, 3);
call OHPInsertUpdate(5, 4);
call OHPInsertUpdate(5, 1, 15);
call OHPInsertUpdate(5, 4, 20);

call OHPInsertUpdate(6, 1, 15);
call OHPInsertUpdate(6, 4, 20);

call OHPInsertUpdate(7, 2, 4);
call OHPInsertUpdate(7, 3, 10);
call OHPInsertUpdate(7, 1);

call OHPInsertUpdate(8, 1, 5);
call OHPInsertUpdate(8, 2, 10);
call OHPInsertUpdate(8, 3);

call OHPInsertUpdate(9, 4, 5);
call OHPInsertUpdate(9, 2, 10);
call OHPInsertUpdate(9, 3, 15);

call OHPInsertUpdate(10, 1, 5);

call OHPInsertUpdate(11, 3);

call OHPInsertUpdate(12, 4);

call OHPInsertUpdate(13, 4, 2);
call OHPInsertUpdate(13, 1, 4);

call OHPInsertUpdate(14, 2);
call OHPInsertUpdate(14, 1);

