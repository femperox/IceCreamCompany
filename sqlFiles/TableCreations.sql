/*
Таблица ингридиентов
Id - айди ингридиента
Name - имя ингридиента. по дефолту "unknown"
Price - стоймость ингридента. по дефолту 0
Info - информация об игридиенте. по дефолту '-'
*/
Create table Ingredient
( Id serial primary key,
  Name varchar(45) UNIQUE default 'unknown',
  Price numeric(100, 2) default 0,
  Info text default '-'
);

/*
Таблица продуктов
Id - айди продукта
Name - имя продукта. Должно быть уникальным. по дефолту "unknown"
Price - стоймость продукта. по дефолту 0
Info - информация об игридиенте. по дефолту '-'
*/
Create table Product
( Id serial primary key,
  Name varchar(45) UNIQUE default 'unknown',
  Price numeric(100, 2) default 0,
  Info text  default '-'
);

/*
Таблица ингридиентов в продукте
IdProduct - айди продукта. Внешний ключ
IdIngredient - айди ингридиента. Внешний ключ
IngAmount - количество ингридиентов. по дефолту 1
*/
Create table ProductHasIngr
( IdProduct integer,
  IdIngredient integer,
  IngAmount integer default 1,
  
  Foreign key (idProduct) references Product(Id) on delete cascade,
  Foreign key (IdIngredient) references Ingredient(Id) on delete cascade
);


/*
Таблица Покупателей
Id - айди покупателя
Name - имя покупателя. Должно быть уникальным. по дефолту "unknown"
Phone - телефон покупателя

CustomerPhone - ограничение типа телефонов, т.е. определяется соотвествее двум маскам
*/
Create table Customer
( Id serial primary key,
  Name varchar(45) UNIQUE default 'unknown',
  Phone varchar(20),
 
 Constraint CustomerPhone check( Phone Similar to '[0-9]{11}' or Phone Similar to '\+[0-9]\([0-9]{3}\)[0-9]{3}-[0-9]{2}-[0-9]{2}')
);

/*
Тип статусов заказа
not in stock - нет в наличии (комплектуется)
in stock - в наличии (укомплектованно)
shipped - отправлено покупателю
returned to warehouse - отправлено на склад для докомплектации
shipment cancellation - отмена отправки покупателю
*/
Create type OrderStatus as enum('not in stock', 'in stock', 'shipped', 'returned to warehouse', 'shipment cancellation');

/*
Таблица заказов
Id - айди заказа
IdCustomer - айди покупателя. Внешний ключ
Date - дата поступления заказа. По дефолту нынешняя дата
Status - статус заказа. 
Price - итоговая стоймость заказа
*/
Create table Orders
( Id serial primary key,
  IdCustomer integer,
  Date date default NOW(),
  Status OrderStatus default 'not in stock',
  Price numeric(100, 2) default 0,
  
  Foreign key (IdCustomer) references Customer(Id) on delete cascade
);

/*
Таблица продуктов в заказе
IdOrder - айди заказа. Внешний ключ
IdProduct - айди продукта. Внешний ключ
ProductAmount - количество продукта. По дефолту 1
*/
Create table OrdersHaveProduct
( IdOrder integer,
  IdProduct integer,
  ProductAmount integer default 1,
 
  Foreign key (idProduct) references Product(Id) on delete cascade,
  Foreign key (IdOrder) references Orders(Id) on delete cascade
 
);


