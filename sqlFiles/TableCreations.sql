
Create table Ingredient
( Id serial primary key,
  Name varchar(45) UNIQUE default 'unknown',
  Price numeric(100, 2),
  Info text default '-'
);

Create table Product
( Id serial primary key,
  Name varchar(45) UNIQUE default 'unknown',
  Price numeric(100, 2) default 0,
  Info text  default '-'
);

Create table ProductHasIngr
( IdProduct integer,
  IdIngredient integer,
  IngAmount integer default 1,
  
  Foreign key (idProduct) references Product(Id) on delete cascade,
  Foreign key (IdIngredient) references Ingredient(Id) on delete cascade
);


Create table Customer
( Id serial primary key,
  Name varchar(45) UNIQUE default 'unknown',
  Phone varchar(20),
 
 Constraint CustomerPhone check( Phone Similar to '[0-9]{11}' or Phone Similar to '\+[0-9]\([0-9]{3}\)[0-9]{3}-[0-9]{2}-[0-9]{2}')
);

Create type OrderStatus as enum('ready', 'complete', 'shipped', 'returned to warehouse', 'shipment cancellation');

Create table Orders
( Id serial primary key,
  IdCustomer integer,
  Name varchar(45) default 'unknown',
  Date date,
  Status OrderStatus,
  Price numeric(100, 2) default 0,
  
  Foreign key (IdCustomer) references Customer(Id) on delete cascade
);

Create table OrdersHaveProduct
( IdOrder integer,
  IdProduct integer,
  ProductAmount integer,
 
  Foreign key (idProduct) references Product(Id) on delete cascade,
  Foreign key (IdOrder) references Orders(Id) on delete cascade
 
);