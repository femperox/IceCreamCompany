Create or Replace Procedure IngInsert(IngName varchar(45), IngPrice decimal(100,2), IngInfo varchar(45))
LANGUAGE sql
as $$
 insert into ingredient(Name, Price, Info)
 	values (IngName, IngPrice, IngInfo);
$$;


Create or Replace Procedure IngUpdate(IngId int, IngName varchar(45), IngPrice decimal(100,2), IngInfo varchar(45))
LANGUAGE sql
as $$
 update ingredient set 
    Name = IngName, 
    Price = IngPrice, 
    Info = IngInfo
 where IngId = id
$$;

Create or Replace Procedure IngDelete(IngId int)
LANGUAGE sql
as $$
 delete from ingredient where IngId = id;
$$;

Create or Replace Procedure ProductInsert(PrdName varchar(45), PrdInfo varchar(45))
LANGUAGE sql
as $$
 insert into Product(Name, Info)
 	values (PrdName, PrdInfo);
$$;


Create or Replace Procedure ProductUpdate(PrdId int, PrdName varchar(45), PrdInfo varchar(45))
LANGUAGE sql
as $$
 update Product set 
    Name = PrdName, 
    Info = PrdInfo
 where PrdId = id
$$;

Create or Replace Procedure ProductDelete(PrdId int)
LANGUAGE sql
as $$
 delete from Product where PrdId = id;
$$;

Create or Replace Procedure CustomerInsert(CusName varchar(45), CusPhone varchar(20))
LANGUAGE sql
as $$
 insert into Customer(Name, Phone)
 	values (CusName, CusPhone);
$$;


Create or Replace Procedure CustomerUpdate(CusId int, CusName varchar(45), CusPhone varchar(20))
LANGUAGE sql
as $$
 update Customer set 
    Name = CusName, 
    Phone = CusPhone
 where CusId = id
$$;

Create or Replace Procedure CustomerDelete(CusId int)
LANGUAGE sql
as $$
 delete from Customer where CusId = id;
$$;

Create or Replace Procedure PHIInsertUpdate(IngId int, ProdId int) as $$
begin
		
	if exists(select idProduct, idIngredient from producthasingr where (ProdId = producthasingr.idproduct and IngId = producthasingr.idingredient)) then 
		update producthasingr 
		  set ingamount = ingamount + 1
		where (prodid = idProduct and IngId = idIngredient);
	else 
	   insert into producthasingr values (ProdId, IngId, 1);
	end if;
end;
$$ Language plpgsql; 

Create or Replace Procedure PHIDelete(IngId int, ProdId int)
LANGUAGE sql
as $$
 delete from producthasingr where (prodid = idProduct and IngId = idIngredient);
$$;

Create or Replace Procedure OHPInsertUpdate(OrdId int, ProdId int) as $$
begin
		
	if exists(select idProduct, idOrder from ordershaveproduct where (ProdId = ordershaveproduct.idproduct and OrdId = ordershaveproduct.idorder)) then 
		update ordershaveproduct 
		  set productamount = productamount + 1
		where (ProdId = idProduct and OrdId = idOrder);
	else 
	   insert into ordershaveproduct values (OrdId,ProdId, 1);
	end if;
end;
$$ Language plpgsql; 

Create or Replace Procedure OHPDelete(ProdId int, OrdId int)
LANGUAGE sql
as $$
 delete from ordershaveproduct where (ProdId = ordershaveproduct.idproduct and OrdId = ordershaveproduct.idorder);
$$;

call PHIInsertUpdate(1,1);
call PHIInsertUpdate(1,2);

call OHPInsertUpdate(5, 1)

