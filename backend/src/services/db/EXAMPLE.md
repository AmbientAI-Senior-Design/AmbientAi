# Creating Database Manager Classes

## Example Usage for a `UserManager` class (Asuming there exists a `User` BaseModel):
```python

class UserManager(DatabaseManager): # This class inherits all the properties from DatabaseManager (i.e. cursor, conn, etc)

    def get_users() -> User:
        query = "SELECT * FROM USERS"
        self.cursor.execute(query, (,))
        results = self.cursor.fetchall()
        return results # connection closes automaticaslly and the cursor does the same
    

```

## Example using `UserManager` outside:

```python

with UserManager("users_DB") as db:
    users = db.get_users()
    for user in users:
        print(user.name)
        
```