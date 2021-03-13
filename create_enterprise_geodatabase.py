import arcpy
from pathlib import Path
import os


def create_enterprise_database(database_location, db_user):
    db_name = Path(database_location).stem.lower()

    print(f"Creating Enterprise Geodatabase for: {db_name}")
    arcpy.management.CreateEnterpriseGeodatabase("PostgreSQL", "localhost,5433", f"{db_name}", "DATABASE_AUTH","postgres", "pwd", "SDE_SCHEMA", "sde", "pwd", '', r"C:\Program Files\ESRI\License10.8\sysgen\keycodes")
    print("Creating Super User Database Connection")
    super_user_connection_file = arcpy.management.CreateDatabaseConnection(os.path.dirname(database_location), f"{db_name}_postgres", "POSTGRESQL", "localhost,5433", "DATABASE_AUTH", "postgres", "pwd", "SAVE_USERNAME", f"{db_name}", '', "TRANSACTIONAL", "sde.DEFAULT", None)
    print("Creating new user")
    arcpy.management.CreateDatabaseUser(super_user_connection_file, "DATABASE_USER", "user", "pwd", '', '')
    print("Create new user database connection file")
    user_connection_file = arcpy.management.CreateDatabaseConnection(os.path.dirname(database_location), f"{db_name}_{db_user}", "POSTGRESQL", "localhost,5433", "DATABASE_AUTH", f"{db_user}", "pwd", "SAVE_USERNAME", f"{db_name}", '', "TRANSACTIONAL", "sde.DEFAULT", None)
    print("Done\n")
    return user_connection_file


create_enterprise_database(r"C:\Users\fran\access_database.accdb", "db_user_name")







