/*
Возвращает из Date номер месяца
Date - дата
*/
create or replace function getMonth(Date Date)
returns integer as $$
   select extract(month from date);
$$ LANGUAGE sql
