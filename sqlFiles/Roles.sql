-- роль: главный менеджер
-- 		 1. Просмотр всех таблиц
--		 2. Изменение всех таблиц
Create Role GenManager
		with login encrypted password 'admin';

Grant Select, 
	  Insert, 
	  Update,
	  Delete
On Ingredient,
   Product,
   ProductHasIngr,
   Orders,
   OrdersHaveProduct,
   Customer
To GenManager;

Grant Select
On AllCustomers,
   AllIngredients,
   AllIngsInProduct,
   AllOrders,
   AllProducts,
   AllProductsInOrder,
   DemandedProductMonthly,
   ShopAvrgOrderMonthly,
   Top5IngsMonthly,
   TopCustomerForPrd,
   CanceledOrders
To GenManager;

Grant Usage, 
      select
On all sequences in schema public
To GenManager;

-- роль: комплектовщик заказа
--		 1. Просмотр таблицы заказов
--		 2. Добавление заказа
Create Role OrderPicker
		with login encrypted password 'orders';

Grant Select,
	  Insert,
	  Update,
	  Delete
On Orders,
   OrdersHaveProduct
To OrderPicker;

Grant Select
On AllOrders,
   AllProductsInOrder,
   AllProducts,
   CanceledOrders,
   Customer,
   Product
To OrderPicker;

Grant Usage, 
      Select
On orders_id_seq
To OrderPicker;

Grant Select
On customer_id_seq,
   product_id_seq,
To OrderPicker;

