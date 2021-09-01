/*
Триггерная функция. 
Выполнятеся из-за рекции триггера t_product_price1 на обновление количества игнридиента в таблице ProductHasIngr
Изменяет цену у продукта (поле Price таблицы Product)

Локальные переменные:
ingPrice - переменная для размещения цены ингридента
sum - переменная для посчёта итоговой суммы по одному ингридиенту
*/
create or replace function update_product_price1()
returns trigger as $$
declare
  ingPrice decimal(100,2);
  sum decimal(100,2);
Begin
    
  if TG_OP = 'INSERT' or TG_OP = 'UPDATE' then

	 select price 
	  into ingPrice
	 from ingredient where new.idIngredient = id;
	 
     sum = new.ingAmount * 0.01 * ingPrice;
	
     update Product set
	    Price = Price + sum
	 where new.idProduct = id;
	 RETURN New;
  else
     select price 
	  into ingPrice
	 from ingredient where old.idIngredient = id;
	 
  	 sum = old.ingAmount * 0.01 * ingPrice;
    
	 update Product set
	    Price = Price - sum
	 where old.idProduct = id;
	 return old;
  end if;
End;
$$ LANGUAGE plpgsql;

/*
Триггер, реагирующий на добавление/изменение/удаление ингридиента в/из продукт/а
*/
create trigger t_product_price1
after insert or update or delete on ProductHasIngr for each row
execute procedure update_product_price1();

/*
Триггерная функция. 
Выполнятеся из-за рекции триггера t_product_price2 на обновления/удаление игнридиента в таблице Ingredient
Изменяет цену у продукта (поле Price таблицы Product)

*/
create or replace function update_product_price2()
returns trigger as $$
Begin
    
  if TG_OP = 'UPDATE' then
	 update ProductHasIngr set
	   IngAmount = IngAmount
	 where new.id = idIngredient;
	 
	 return New;
  else
     
	 delete from ProductHasIngr where old.id = idIngredient;
	 
	 return old;
  end if;
End;
$$ LANGUAGE plpgsql;

/*
Триггер, реагирующий на изменение/удаление ингридиента 
*/
create trigger t_product_price2
after update or delete on ingredient for each row
execute procedure update_product_price2();

/*
Триггерная функция. 
Выполнятеся из-за рекции триггера t_order_price на обновление количества продукта в таблице OrdersHaveProduct
Изменяет цену у заказа (поле Price таблицы Orders)

Локальные переменные:
prodPrice - переменная для размещения цены продукта
sum - переменная для посчёта итоговой суммы по одному продукту
*/
create or replace function update_order_price1()
returns trigger as $$
declare
  prodPrice decimal(100,2);
  sum decimal(100,2);
Begin
    
  if TG_OP = 'INSERT' or TG_OP = 'UPDATE' then

	 select price 
	  into prodPrice
	 from product where new.idproduct = id;
	 
     sum = new.productamount * prodPrice;
	
     update Orders set
	    Price = Price + sum
	 where new.idorder = id;
	
	 RETURN New;
  else
     select price 
	  into prodPrice
	 from product where old.idproduct = id;
	 
  	 sum = old.productamount * prodPrice;
    
	 update Orders set
	    Price = Price - sum
	 where old.idorder = id;	
	 return old;
  end if;
End;
$$ LANGUAGE plpgsql;

/*
Триггер, реагирующий на добавление/изменение/удаление продукта в/из заказе/а
*/
create trigger t_order_price1
after insert or update or delete on OrdersHaveProduct for each row
execute procedure update_order_price1();

/*
Триггерная функция. 
Выполнятеся из-за рекции триггера t_product_removal на удаление продукта
Изменяет таблицу ProductHasIngr и OrdersHaveProduct
*/
create or replace function remove_product()
returns trigger as $$
Begin
    
  delete from ProductHasIngr where old.id = idProduct;
  delete from OrdersHaveProduct where old.id = idProduct;
  return old;
  
End;
$$ LANGUAGE plpgsql;

/*
Триггер, реагирующий на удаление продукта
*/
create trigger t_product_removal
after delete on Product for each row
execute procedure remove_product();

/*
Триггерная функция. 
Выполнятеся из-за рекции триггера t_customer_removal на удаление покупателя
Изменяет таблицу Orders
*/
create or replace function remove_customer()
returns trigger as $$
Begin
    
  delete from Orders where old.id = idCustomer;
  return old;
  
End;
$$ LANGUAGE plpgsql;

/*
Триггер, реагирующий на удаление покупателя
*/
create trigger t_customer_removal
after delete on Customer for each row
execute procedure remove_customer();

/*
Триггерная функция. 
Выполнятеся из-за рекции триггера t_order_removal на удаление заказа
Изменяет таблицу OrdersHaveProduct
*/
create or replace function remove_order()
returns trigger as $$
Begin
    
  delete from OrdersHaveProduct where old.id = idOrder;
  return old;
  
End;
$$ LANGUAGE plpgsql;

/*
Триггер, реагирующий на удаление заказа
*/
create trigger t_order_removal
after delete on Orders for each row
execute procedure remove_order();

