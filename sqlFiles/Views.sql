-- Все заказы 
Create or replace view AllOrders as
	select Customer.Name as Company_Name, Orders.Date, Orders.Status, Orders.Price 
    from Orders
    Join customer on Orders.idcustomer = customer.id
	order by date desc, status, price

-- Все продукты
create or replace view AllProducts as
	select name, price, info from Product
	order by name, price;

-- Все ингриденты
create or replace view AllIngredients as
	select name, price, info from Ingredient
	order by name, price;	
	
-- Все покупатели	
create or replace view AllCustomers as
	select name, phone from Customer
	order by name;		

-- Все ингриденты в продукте
create or replace view AllIngsInProduct as
	select Product.Name as Product, Ingredient.name as Ingredient,ProductHasIngr.ingAmount, Ingredient.info from Ingredient
	join ProductHasIngr on Ingredient.id =ProductHasIngr.idIngredient
	join Product on Product.id =ProductHasIngr.idProduct

	order by ProductHasIngr.idProduct
	
-- Все продукты в заказе	
create or replace view AllProductsInOrder as
	select
  		Orders.id as OrderId,
  		Customer.Name as Customer, 
  		Product.Name as Product, 
  		OrdersHaveProduct.ProductAmount, 
  		Product.Price,
  		SUM(OrdersHaveProduct.ProductAmount * Product.Price) over (Partition by Orders.id order by Product.Price) as TotalPrice
	from Product
	join OrdersHaveProduct on OrdersHaveProduct.idProduct = Product.Id
	join Orders on Orders.Id = OrdersHaveProduct.idOrder
	join Customer on Customer.id = Orders.idCustomer






