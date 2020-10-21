### Для запуска микросервиса
```bash
docker-compose build
docker-compose up db
```
Ждём пока БД инициализируется

Запускаем всё вместе
```bash
docker-compose up
```

Для запуска тестов
```bash
docker-compose run web pytest
```