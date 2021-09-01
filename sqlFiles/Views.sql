select * from orders
select * from customer

call orderinsert(5, NOW(), 'shipped')

drop view if exists TopShopsForProduct;

Create or replace view TopShopsForProduct as
	select Name from Product;

select * from topshopsforproduct