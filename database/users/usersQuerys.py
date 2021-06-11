from database.connectDb import connectDb;
import psycopg2;
import json;

#Clase que contiene todas las "Querys" de tipo usuario
class UsersDB:
    #Registrar usuarios de diferentes tipos.
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
    
    #Login para los usuarios de diferentes tipos
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
    
    # Registrar información adicional del hospital (Sólo válido para el hopsital)
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

    #Registrar información básica del usuario (Paciente)
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
    
    # Registrar al médico (sólo válido para los usuarios tipo hospital)
    def registerMedic(data, session):
        try:
            db = connectDb();
            cursor = db.cursor();

            sql = """ 
                INSERT INTO "public"."medico" ("Email", "Id",   "Name", "Pass", "Specialty", "IdHospital") VALUES (%s,%s,%s,%s,%s,%s)
            """;

            val = (data["email"], data["id"], data["name"], data["pass"], data["spec"], session["id"]);

            cursor.execute(sql, val);

            db.commit();

            return True;
        except:
            print("Ocurrió un error");
            return False;
    
    #Traer todas las observaciones del paciente
    def printObservationUser(id):
        try:
            db = connectDb();

            cursor = db.cursor();

            query = """ 
                SELECT * FROM "public"."observaciones" where "IdPaciente" = {} 
            """.format(id);

            cursor.execute(query);

            rows = cursor.fetchall();

            arr = [];
            for row in rows:
                map = {
                    "idPaciente": str(row[1]),
                    "idMedico": str(row[2]),
                    "observation": str(row[3]),
                    "healthCondition": row[4]
                }
                arr.append(map);
            return True, arr;
        except Exception as ex:
            return False, None;
            print("Error : {}".format(ex));
    
    #Traer todas las observaciones del paciente
    """ def printObservationMedico(id):
        try:
            db = connectDb();

            cursor = db.cursor();

            query =  
                SELECT * FROM "public"."observaciones" where "IdMedico" = {} 
            .format(id);

            cursor.execute(query);

            rows = cursor.fetchall();

            arr = [];
            for row in rows:
                map = {
                    "idPaciente": str(row[1]),
                    "idMedico": str(row[2]),
                    "observation": str(row[3]),
                    "healthCondition": row[4]
                }
                arr.append(map);
            return True, arr;
        except Exception as ex:
            return False, None;
            print("Error : {}".format(ex)); """
    
    