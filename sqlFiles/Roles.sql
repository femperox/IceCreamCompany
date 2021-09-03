-- роль: главный менеджер
-- 		 1. Просмотр всех таблиц
--		 2. Изменение всех таблиц
Create Role GenManager
		with login encrypted password 'admin'

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

-- роль: комплектовщик заказа
--		 1. Просмотр таблицы заказов
--		 2. Добавление заказа
Create Role OrderPicker
		with login encrypted password 'orders'

Grant Select,
	  Insert,
	  Update
On Orders
To OrderPicker;

