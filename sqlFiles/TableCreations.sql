Create table Ingredient
( Id serial primary key,
  Name varchar(45) default 'unknown',
  Price money
);

Create table Product
( Id serial primary key,
  Name varchar(45) default 'unknown',
  Info text,
  Price money
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
  Name varchar(45) default 'unknown',
  Phone varchar(20),
 
 Constraint CustomerPhone check( Phone like '+[0-9]_(___)___-__-__' or Phone like '[0-9]___________' );
)


Create type OrderStatus as enum('ready', 'complete', 'shipped', 'returned to warehouse', 'shipment cancellation');

Create table Orders
( Id serial primary key,
  IdCustomer integer,
  Name varchar(45) default 'unknown',
  Date date,
  Status OrderStatus,
  Price money,
  
  Foreign key (IdCustomer) references Customer(Id) on delete cascade
);