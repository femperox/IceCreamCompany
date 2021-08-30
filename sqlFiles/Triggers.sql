create trigger t_product_price
after insert or update or delete on ProductHasIngr for each row
execute procedure update_product_price();

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
	    Price = Price + sum;
	
	 RETURN New;
  else
     select price 
	  into ingPrice
	 from ingredient where old.idingredient = id;
	 
  	 sum = old.ingamount * 0.01 * ingPrice;
    
	 update Product set
	    Price = Price - sum;
	 	
	 return old;
  end if;
End;
$$ LANGUAGE plpgsql;