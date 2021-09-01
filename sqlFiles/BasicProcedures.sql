/*
Добавить ингридиент
IngName - имя ингридиента
IngPrice - стоимость ингридиента
IngInfo - информация об ингридиенте
*/
Create or Replace Procedure IngInsert(IngName varchar(45), IngPrice decimal(100,2), IngInfo varchar(45) default '')
LANGUAGE sql
as $$
 insert into Ingredient(Name, Price, Info)
 	values (IngName, IngPrice, IngInfo);
$$;

/*
Обновить ингридиент
IngId - айди игридиента
IngName - имя ингридиента
IngPrice - стоимость ингридиента
IngInfo - информация обингридиента
*/
Create or Replace Procedure IngUpdate(IngId int, IngName varchar(45), IngPrice decimal(100,2), IngInfo varchar(45) default '')
LANGUAGE sql
as $$
 update Ingredient set 
    Name = IngName, 
    Price = IngPrice, 
    Info = IngInfo
 where IngId = id
$$;

/*
Удалить ингридиент
IngId - айди игридиента
*/
Create or Replace Procedure IngDelete(IngId int)
LANGUAGE sql
as $$
 delete from Ingredient where IngId = id;
$$;

/*
Добавить продукт
PrdName - имя продукта
PrdInfo - информация о продукте
*/
Create or Replace Procedure ProductInsert(PrdName varchar(45), PrdInfo varchar(45) default '')
LANGUAGE sql
as $$
 insert into Product(Name, Info)
 	values (PrdName, PrdInfo);
$$;

/*
Обновить продукт
PrdId - айди продукта
PrdName - имя продукта
PrdInfo - информация о продукте
*/
Create or Replace Procedure ProductUpdate(PrdId int, PrdName varchar(45), PrdInfo varchar(45) default '')
LANGUAGE sql
as $$
 update Product set 
    Name = PrdName, 
    Info = PrdInfo
 where PrdId = id
$$;

/*
Удалить продукт
PrdId - айди продукта
*/
Create or Replace Procedure ProductDelete(PrdId int)
LANGUAGE sql
as $$
 delete from Product where PrdId = id;
$$;

/*
Добавить покупателя
CusName - имя покупателя
CusPhone - телефон покупателя
*/
Create or Replace Procedure CustomerInsert(CusName varchar(45), CusPhone varchar(20))
LANGUAGE sql
as $$
 insert into Customer(Name, Phone)
 	values (CusName, CusPhone);
$$;

/*
Обновить покупателя
CusId - айди покупателя
CusName - имя покупателя
CusPhone - телефон покупателя
*/
Create or Replace Procedure CustomerUpdate(CusId int, CusName varchar(45), CusPhone varchar(20))
LANGUAGE sql
as $$
 update Customer set 
    Name = CusName, 
    Phone = CusPhone
 where CusId = id
$$;

/*
Удалить покупателя
CusId - айди покупателя
*/
Create or Replace Procedure CustomerDelete(CusId int)
LANGUAGE sql
as $$
 delete from Customer where CusId = id;
$$;

/*
Добавить/Обновить ингридиент в продукт/e
IngId - айди ингридиента
ProdId - айди продукта
amount - количество ингридиента
*/
Create or Replace Procedure PHIInsertUpdate(ProdId int, IngId int, amount int default 1) as $$
begin
		
	if exists(select idProduct, idIngredient from ProductHasIngr where (ProdId = ProductHasIngr.idProduct and IngId = ProductHasIngr.idIngredient)) then 
		update ProductHasIngr
		  set ingAmount = ingAmount + amount
		where (prodid = idProduct and IngId = idIngredient);
	else 
	   insert into ProductHasIngr values (ProdId, IngId, amount);
	end if;
end;
$$ Language plpgsql; 

/*
Удалить ингридиент из продукта
IngId - айди ингридиента
ProdId - айди продукта
*/
Create or Replace Procedure PHIDelete(ProdId int, IngId int)
LANGUAGE sql
as $$
 delete from ProductHasIngr where (prodid = idProduct and IngId = idIngredient);
$$;

/*
Добавить/Обновить продукт в заказ/е
IngId - айди ингридиента
ProdId - айди продукта
amount - количество продукта
*/
Create or Replace Procedure OHPInsertUpdate(OrdId int, ProdId int, amount int default 1) as $$
begin
		
	if exists(select idProduct, idOrder from OrdersHaveProduct where (ProdId = OrdersHaveProduct.idproduct and OrdId = OrdersHaveProduct.idorder)) then 
		update OrdersHaveProduct
		  set productAmount = productAmount + amount
		where (ProdId = idProduct and OrdId = idOrder);
	else 
	   insert into OrdersHaveProduct values (OrdId,ProdId, amount);
	end if;
end;
$$ Language plpgsql; 

/*
Удалить продукт из заказа
IngId - айди ингридиента
ProdId - айди продукта
*/
Create or Replace Procedure OHPDelete(ProdId int, OrdId int)
LANGUAGE sql
as $$
 delete from OrdersHaveProduct where (ProdId = idProduct and OrdId =idOrder);
$$;

/*
Добавить заказ
CusId -  айди покупателя
OrdDate - дата поступления заказа
OrdStatus - статус заказа
*/
Create or Replace Procedure OrderInsert(CusId int, OrdDate date default now(), OrdStatus orderStatus default 'not in stock') as $$
begin
		insert into Orders(idCustomer, date, status) values(CusId, OrdDate, OrdStatus);
end;
$$ Language plpgsql; 

/*
Добавить заказ
OrdId - айди заказа
CusId -  айди покупателя
OrdDate - дата поступления заказа
OrdStatus - статус заказа
*/
Create or Replace Procedure OrderUpdate(OrdId int, CusId int, OrdDate date default now(), OrdStatus orderStatus default 'not in stock') as $$
begin
		update orders set 
		  idCustomer = CusId,
		  date = OrdDate,
		  status = orderStatus
		where OrdId = id;

end;
$$ Language plpgsql; 

/*
Удалить заказ
OrdId - айди заказа
*/
Create or Replace Procedure OrdersDelete(OrdId int)
LANGUAGE sql
as $$
 delete from Orders where OrdId = id;
$$;

