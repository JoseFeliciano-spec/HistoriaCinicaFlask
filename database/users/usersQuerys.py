from database.connectDb import connectDb;
import psycopg2;

class UsersDB:
    def registerUserInDb(data):
        try:
            db = connectDb();
            cursor = db.cursor();
            """ Query para insertar, entre comillado a los campos. """
            query = """INSERT INTO "public"."users" ("Iden", "Name", "Phone", "Email", "Type", "Pass") VALUES (%s, %s, %s, %s, %s, %s)""";
            val = (data["id"], data["name"], data["phone"], data["email"], data["type"], data["pass"]);
            cursor.execute(query, val);
            db.commit(); 
            return True;
        except (Exception, psycopg2.Error) as error:
            print("ha ocurrido un error");
            return False;
    
    def loginUserInDb(data):
        try:
            db = connectDb();
            cursor = db.cursor();

            sql = """SELECT * FROM public.users where "Iden" = {} and "Pass" = '{}' and "Verification" = TRUE""".format(data[0], data[1]);

            cursor.execute(sql);

            row = cursor.fetchone()
            
            if row is None:
                return False;
            else:
                return True;
        except (Exception, psycopg2.Error) as error:
            return False;