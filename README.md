# shop_visits_fastapi
### запуск
```
git clone git@github.com:Not-user-1984/shop_visits_fastapi.git
cd docker_shop_visit
docker-compose up -d --build
```
### Документация 
Документация 
Ручки разделены для каждой сушности есть crud, orders,
через swagger и тестить.

```
http://localhost:8000/docs
```


### Админка
Без паролей, есть поиск и сортировки.

```
http://localhost:8000/admin/
```
<br>
<br>


При сборке уже сгенерировалась тестовые данные,
есть уже готовые Заказы, Магазины и Пользователи.
Но Посещения не проставлены,
можно брать номера из готовых и ставить Посещение,
либо создать Заказчика самому и проставить Визит.
<br>
<br>



```
http://localhost:8000/customer/
```

Post запрос создает нового заказчика,
есть валидация номера, принимается все в str,
убираются лишние символы и пробелы,
номере должен быть не короче 9 цифр.

<br>
<br>

```
http://localhost:8000/customers/create_orders/
```
Нужно передать свой номер телефона
так же id магазина
можно сделать только один заказ на одну точку.

<br>
<br>

```
http://localhost:8000/workers/
```
Cоздать работника, добавляется точка к которой он привязан.

<br>
<br>

```
http://localhost:8000/workers/orders/
```
Можно посмотреть все заказы которые есть на точке


<br>
<br>


```
http://localhost:8000/workers/orders/
```
Выбрать заказ на выполнение.
Работник блокируется пока Заказчик не отметит Посещение,
тем самым не сможет взять заказ еще.

<br>
<br>


```
http://localhost:8000/customers/visit/{order_id}
```
Заказчик отмечает визит, Работник разблокирует и может брать заказы на свой точки.


<br>
<br>


```
http://localhost:8000//order/{id_orders}"
```
PUT запрос на изменения статуса заказа.
<br>
<br>
