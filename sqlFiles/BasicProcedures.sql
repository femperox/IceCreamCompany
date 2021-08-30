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
