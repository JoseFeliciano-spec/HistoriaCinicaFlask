from database.connectDb import connectDb;
import psycopg2;
import json;

class MedicDB:
    def loginMedicInDb(data):
        try:
            #Data es un arreglo.
            db = connectDb();
            cursor = db.cursor();
            query = """SELECT * FROM public.medico where "Id" = {} and "Pass" = '{}'""".format(data[0], data[1]);

            cursor.execute(query);

            row = cursor.fetchone();

            if row is None:
                return False, 0;
            else:
                map = {
                    "id" : str(row[1]),
                    "Spec": row[3]
                }
                return True, map;
        except (Exception) as ex:
            print("Ocurrió un problema: " + str(ex));
            return False;
    
    def changePasswordM(data):
        try:
            db = connectDb();
            cursor = db.cursor();
            query = """ 
                UPDATE public.medico SET "Pass" = '{}', "Used" = {}  where "Id" = {}
            """.format(data[0], True, data[1]);
            cursor.execute(query);
            db.commit();
            return True;
        except Exception as err:
            print("Error: " + str(err));
            return False;

    def firtTime(id):
        try:
            db = connectDb();
            cursor = db.cursor();

            query = """ 
                SELECT ("Used") FROM public.medico where "Id" = {}
            """.format(id)

            cursor.execute(query);

            row = cursor.fetchone();

            if row is None:
                return False;
            else:
                if not bool(row[0]):
                    return True;
                else:
                    return False;
        except:
            return False;
            