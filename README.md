### О проекте
Индексация при помощи elasticsearch данных о госзакупках. Данные берутся из проекта [clearspending](https://clearspending.ru/opendata/)

https://clearspending.ru/opendata

### Как запустить

#### Установка зависимостей
Требования: `docker`, `docker-compose`, `python3`, свободное место на жестком диске для индекса `elasticsearch`.
Так же установите библиотеки `python3` из `requirements.txt`
```bash
pip3 install -r requirements.txt
```


#### Скачивание данных
В корне проекта нужно создать папку `data`, и туда сложить выкаченные с url https://clearspending.ru/opendata данные в  формате `jsonl.zip`.


Названия индексов будут созданны в соответствии с названиями архивов.
Например:
```
contracts_223fz_202010-20201009.jsonl.zip --> contracts_223fz
```

#### Инициализация elasticsearch
В файле `docker-compose.yml` нужно выставить актуальные пути для директории где будет храниться индекс:
По умолчанию это `/Volumes/my_passport/.jdata_elastic`.

После этого запускаем `elasticsearch` ноду:
```bash
docker-compose -f docker-compose.yml up
```

#### Создание индекса
```bash
python3 crate_indexes.py
```
#### Profit
Теперь можно делать запросы к вашим `elasticsearch` индексам.


### Примеры поисковых запросов

```bash
curl -XGET 'localhost:9200/contracts_223fz/_search' \
--header 'Content-Type: application/json' \
-d '{
    "query": {
        "term": {
            "id.keyword": {
                "value": "43ed37af-2bd9-4544-b2a4-5276d7ffab85"
            } 
        }
    }
}'
```
