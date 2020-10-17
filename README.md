### О проекте
Индексация при помощи elasticsearch данных о госзакупках. Данные берутся из проекта [clearspending](https://clearspending.ru/opendata/)

https://clearspending.ru/opendata

### Подготовка к индексации
В корне проекта нужно создать папку `data`, и туда сложить выкаченные с url https://clearspending.ru/opendata данные в  формате `jsonl.zip`.


Названия индексов будут созданны в соответствии с названиями архивов.
Например:
```
contracts_223fz_202010-20201009.jsonl.zip --> contracts_223fz
```

### Примеры поисковых запросов:

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