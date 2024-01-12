## Установка и запуск проекта

docker-compose up --build -d

docker-compose exec fast-api sh -c "cd /code/ProductService && alembic upgrade head"

docker-compose exec fast-api sh -c "cd /code/InventoryService && alembic upgrade head"

- Для остановки процессов используйте команду:

docker-compose stop

- Если необходимо полностью очистить память или вы внесли какие-то изменения, то:

docker-compose down
