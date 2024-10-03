## 2. Saga Ísfólksins

#### Möppustrúktur
```
data/
├─ isfolkid.db
create_isfolkid.sql
isfolkid.sql
README.md
```

#### Allar skipanalínur sem þarf að keyra til að keyra lausnina ykkar
Skrifa í terminal...
```
sqlite3 data/isfolkid.db
.read isfolkid.sql
```
og 

```
sqlite3 data/create_isfolkid.db
.read create_isfolkid.sql
```