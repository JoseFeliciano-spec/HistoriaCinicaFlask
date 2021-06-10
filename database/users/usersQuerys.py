from database.connectDb import connectDb;
import psycopg2;
import json;

class UsersDB:
    def registerUserInDb(data):
        try:
            db = connectDb();
            cursor = db.cursor();
            """ Query para insertar, entre comillado a los campos. """
            query = """INSERT INTO "public"."users" ("Iden", "Phone", "Email", "Type", "Pass") VALUES (%s, %s, %s, %s, %s)""";
            val = (data["id"], data["phone"], data["email"], data["type"], data["pass"]);
            cursor.execute(query, val);
            db.commit(); 
            return True;
        except (Exception, psycopg2.Error) as error:
            print("ha ocurrido un error");
            return False;
    
    def loginUserInDb(data):
        """ Solamente se logueará cuando el usuario esté verificado. """
        try:
            db = connectDb();
            cursor = db.cursor();

            sql = """SELECT * FROM public.users where "Iden" = {} and "Pass" = '{}' and "Verification" = TRUE""".format(data[0], data[1]);

            cursor.execute(sql);

            row = cursor.fetchone()
            """ print(list(row)); """
            if row is None:
                return False, 0;
            else:
                map = {
                    "id": str(row[0]),
                    "phone": str(row[1]),
                    "type": row[3]
                };
                """ print(map); """
                return True, map;
        except (Exception, psycopg2.Error) as error:
            return False, 0;
    
    def regBasicInfoHospital(data, session):
        try:
            db = connectDb();
            cursor = db.cursor();
            query = """ 
                INSERT INTO "public"."hospital" ("Id", "Name", "Address", "MedicService") VALUES (%s, %s, %s, %s)
            """;
            val = (session["id"], data["name"], data["address"], data["serviceMedical"]);
            cursor.execute(query, val);
            db.commit();
            return True;
        except (Exception, psycopg2.Error) as error:
            print("ha ocurrido un error");
            return False;

    def regBasicInfoUser(data, session):
        try:
            db = connectDb();
            cursor = db.cursor();
            sql = """ 
                INSERT INTO "public"."paciente" ("Id", "Name", "Address","DateBirth") VALUES(%s,%s,%s,now())
            """;
            var = (session["id"], data["name"], data["address"]);    
            cursor.execute(sql, var);
            db.commit();
            return True;
        except:
            print("ha ocurrido un error");
            return False;
