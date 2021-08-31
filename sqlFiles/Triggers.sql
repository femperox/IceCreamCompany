create or replace function update_product_price()
returns trigger as $$
declare
  ingPrice decimal(100,2);
  sum decimal(100,2);
Begin
    
  if TG_OP = 'INSERT' or TG_OP = 'UPDATE' then

	 select price 
	  into ingPrice
	 from ingredient where new.idingredient = id;
	 
     sum = new.ingamount * 0.01 * ingPrice;
	
     update Product set
	    Price = Price + sum
	 where new.idproduct = id;
	 RETURN New;
  else
     select price 
	  into ingPrice
	 from ingredient where old.idingredient = id;
	 
  	 sum = old.ingamount * 0.01 * ingPrice;
    
	 update Product set
	    Price = Price - sum
	 where old.idproduct = id;
	 return old;
  end if;
End;
$$ LANGUAGE plpgsql;

create trigger t_product_price
after insert or update or delete on ProductHasIngr for each row
execute procedure update_product_price();

create or replace function update_order_price()
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

create trigger t_order_price
after insert or update or delete on OrdersHaveProduct for each row
execute procedure update_order_price();

create or replace function remove_product()
returns trigger as $$
Begin
    
  delete from ProductHasIngr where old.id = idProduct;
  return old;
  
End;
$$ LANGUAGE plpgsql;

create trigger t_product_removal
after delete on Product for each row
execute procedure remove_product();

create or replace function remove_customer()
returns trigger as $$
Begin
    
  delete from Orders where old.id = idCustomer;
  return old;
  
End;
$$ LANGUAGE plpgsql;

create trigger t_customer_removal
after delete on Customer for each row
execute procedure remove_customer();

create or replace function remove_order()
returns trigger as $$
Begin
    
  delete from ordershaveproduct where old.id = idOrder;
  return old;
  
End;
$$ LANGUAGE plpgsql;

create trigger t_order_removal
after delete on Orders for each row
execute procedure remove_order();

