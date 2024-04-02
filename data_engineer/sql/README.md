# Тест SQL

На основе таблиц базы данных, напишите SQL код, который возвращает необходимые результаты
Пример: 

Общее количество товаров
```sql
select count (*) from items
```

## Структура данных

Используемый синтаксис: Oracle SQL или другой

| Сustomer       | Description           |
| -------------- | --------------------- |
| customer\_id   | customer unique id    |
| customer\_name | customer name         |
| country\_code  | country code ISO 3166 |

| Items             | Description       |
| ----------------- | ----------------- |
| item\_id          | item unique id    |
| item\_name        | item name         |
| item\_description | item description  |
| item\_price       | item price in USD |

| Orders       | Description                 |
| ------------ | --------------------------- |
| date\_time   | date and time of the orders |
| item\_id     | item unique id              |
| customer\_id | user unique id              |
| quantity     | number of items in order    |

| Countries     | Description           |
| ------------- | --------------------- |
| country\_code | country code          |
| country\_name | country name          |
| country\_zone | AMER, APJ, LATAM etc. |


| Сonnection\_log         | Description                           |
| ----------------------- | ------------------------------------- |
| customer\_id            | customer unique id                    |
| first\_connection\_time | date and time of the first connection |
| last\_connection\_time  | date and time of the last connection  |

## Задания

### 1) Количество покупателей из Италии и Франции

| **Country_name** | **CustomerCountDistinct** |
| ------------------------- | ----------------------------- |
| France                    | #                             |
| Italy                     | #                             |

```sql
select country_name, count(customer_id) as CustomerCountDistinct
from customer t1
left join countries t2
on t1.country_code = t2.country_code
where country_name in ('France', 'Italy')
group by country_name;
```

### 2) ТОП 10 покупателей по расходам

| **Customer_name** | **Revenue** |
| ---------------------- | ----------- |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |

```sql
with pokupki as(
select customer_name, t1.customer_id, item_id, quantity
from customer t1
inner join orders t2
on t1.customer_id = t2.customer_id
),

pokupki_with_prices as(
select * from pokupki t3
inner join items t4
on t3.item_id = t4.item_id
),

customer_costs as (
select customer_name, item_price * quantity as purch_sum
from pokupki_with_prices
)

select customer_name, sum(purch_sum) as Revenue
from customer_costs
group by customer_name
order by 2 desc
limit 10;
```

### 3) Общая выручка USD по странам, если нет дохода, вернуть NULL

| **Country_name** | **RevenuePerCountry** |
| ------------------------- | --------------------- |
| Italy                     | #                     |
| France                    | NULL                  |
| Mexico                    | #                     |
| Germany                   | #                     |
| Tanzania                  | #                     |

```sql
with pokupki as(
select customer_name, t1.customer_id, item_id, quantity, country_code
from customer t1
inner join orders t2
on t1.customer_id = t2.customer_id
),

pokupki_with_prices as(
select * from pokupki t3
inner join items t4
on t3.item_id = t4.item_id
),

customer_costs as (
select customer_name, item_price * quantity as purch_sum, country_name
from pokupki_with_prices t5
right join countries t6
on t5.country_code = t6.country_code
)

select country_name, sum(purch_sum) as RevenuePerCountry
from customer_costs
group by country_name;
```

### 4) Самый дорогой товар, купленный одним покупателем

| **Customer\_id** | **Customer\_name** | **MostExpensiveItemName** |
| ---------------- | ------------------ | ------------------------- |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |

```sql
with pokupki as(
select customer_name, t1.customer_id as customer_id, item_id           
from customer t1
left join orders t2
on t1.customer_id = t2.customer_id
),

pokupki_with_prices as(
select * from pokupki t3
inner join items t4
on t3.item_id = t4.item_id
) 

select customer_id, customer_name, item_name as MostExpansiveItemName
from(
select *, rank() over (partition by customer_id order by item_price desc)
from pokupki_with_prices
) t5
where rank = 1;
```

### 5) Ежемесячный доход

| **Month (MM format)** | **Total Revenue** |
| --------------------- | ----------------- |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
select extract(month from date_time) as Month, sum(quantity * item_price) as TotalRevenue
from items t1
inner join orders t2
on t1.item_id =  t2.item_id 
group by Month;
```

### 6) Найти дубликаты

Во время передачи данных произошел сбой, в таблице orders появилось несколько 
дубликатов (несколько результатов возвращаются для date_time + customer_id + item_id). 
Вы должны их найти и вернуть количество дубликатов.

```sql
select count(*)                        
from(
select date_time, customer_id, item_id
from orders
group by date_time, customer_id, item_id    
having count(*)  > 1
) t;
```

### 7) Найти "важных" покупателей

Создать запрос, который найдет всех "важных" покупателей,
т.е. тех, кто совершил наибольшее количество покупок после своего первого заказа.

| **Customer\_id** | **Total Orders Count** |
| --------------------- |-------------------------------|
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |

```sql
with t1 as (
select customer_id, min(date_time) as first      
from orders
group by customer_id
),

t2 as (
select t.customer_id, count(*) as TotalOrdersCount
from orders t
inner join t1             
on t.customer_id = t1.customer_id
where date_time > first
group by t.customer_id
)

select customer_id, TotalOrderscount
from t2
order by 2 desc;
```

### 8) Найти покупателей с "ростом" за последний месяц

Написать запрос, который найдет всех клиентов,
у которых суммарная выручка за последний месяц
превышает среднюю выручку за все месяцы.

| **Customer\_id** | **Total Revenue** |
| --------------------- |-------------------|
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
with t1 as (
select extract(month from date_time) as Month, avg(quantity * item_price) as AvgRevenue
from items t1
inner join orders t2
on t1.item_id =  t2.item_id
group by Month
),
yearavg as (
select avg(avgrevenue) as yearavg
from t1),

pokupki as(
select customer_name, t1.customer_id, item_id, quantity, date_time
from customer t1
inner join orders t2
on t1.customer_id = t2.customer_id
),

pokupki_with_prices as(
select * from pokupki t3
inner join items t4
on t3.item_id = t4.item_id
),

customer_costs as (
select extract(month from date_time) as month, customer_id, item_price * quantity as purch_sum
from pokupki_with_prices
)

select customer_id, sum(purch_sum) as TotalRevenue
from (
select customer_id, purch_sum, rank() over (partition by customer_id order by month desc) as rank
from customer_costs
) tt
where rank = 1        
group by customer_id
having sum(purch_sum) >  (select  yearavg  from yearavg)
order by 2 desc;
```
