from database.connectDb import connectDb;

class UsersDB:
    def registerUserInDb(data):
        db = connectDb();
        cursor = db.cursor();

        """ Query para insertar, entre comillado a los campos. """
        query = """INSERT INTO users ("Iden", "Name", "Phone", "Email", "Type", "Pass") VALUES (%s, %s, %s, %s, %s, %s)""";

        val = (data["id"], data["name"], data["phone"], data["email"], data["type"], data["pass"]);
        print(query);
        cursor.execute(query, val); 
        print(cursor.rowcount)
        print("Record inserted successfully into mobile table");
        