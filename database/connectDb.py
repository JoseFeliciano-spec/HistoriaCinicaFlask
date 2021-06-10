from psycopg2 import connect;

def connectDb():
   db =  connect(
       host= "postgresql-josespec.alwaysdata.net",
       database="josespec_hospital",
       user="josespec",
       password = "29035683JA"
   )
   return db;
