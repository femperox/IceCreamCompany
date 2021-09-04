-- Все заказы 
Create or replace view AllOrders as
	select Orders.Id, Customer.Name as Company_Name, Orders.Date, Orders.Status, Orders.Price 
    from Orders
    Join customer on Orders.idcustomer = customer.id
	order by date desc, status, price;

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

	order by ProductHasIngr.idProduct;
	
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
	join Customer on Customer.id = Orders.idCustomer;

-- Для каждого магазина узнать среднюю сумму заказов в каждом месяце.
create or replace view ShopAvrgOrderMonthly as

	select distinct
	  Customer.Name as Customer,
	  getMonth(Orders.Date) as Month,
	  AVG(Orders.Price) over(
		  					   partition by Customer.Name, getMonth(Orders.Date)
		  					   order by getMonth(Orders.Date)  
	  						)
	from Orders
	join Customer on Orders.idCustomer = Customer.id
	order by Customer, Month;


-- Для каждого месяца определить продукт, который добавлялся в заказ наибольшее количество раз.
create or replace view DemandedProductMonthly as
 	 with TopProducts as
  	 (select 
		   getMonth(allOrders.date) as month,
		   product, 
		   productamount,
		   max(productamount) over( partition by getMonth(allOrders.date)
								   ) as topProduct
	  from  allproductsinorder
	  join allOrders on allOrders.id = allproductsinorder.orderid 
	  order by month, topProduct, productamount desc
     )
    select month, product, topProduct from TopProducts
    where productamount = topproduct;
	
-- Определить топ 5 ингредиентов, встречающихся в заказах за последний месяц
create or replace view Top5IngsMonthly as
	with TopIngred as
  		(select distinct
			getMonth(allOrders.date) as month,
			allingsinproduct.ingredient,
			count(allingsinproduct.ingredient) over (partition by getMonth(allOrders.date),ingredient ) as ingCount
	
		 from allingsinproduct
		 join allproductsinorder on allingsinproduct.Product = allproductsinorder.Product
		 join allOrders on allOrders.id = allproductsinorder.orderid 
		 order by month, ingCount desc
		),
  	ListOfTops as
  		( select distinct 
	  	  month, 
	  	  STRING_AGG(ingredient, ', ') over (
	  										  partition by month
	  										  order by ingCount desc
	  										  ROWS BETWEEN UNBOUNDED PRECEDING AND 4 FOLLOWING 
  								    		) as Top5
		  from TopIngred
   		  limit (select count(distinct month) from TopIngred)
  		)
	select * from ListOfTops
	order by month;
 

		  
		  
		  
		  
		  