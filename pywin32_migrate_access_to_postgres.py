# =============================================================================
# Created By  : Francis Polignano
# Created Date: March 2021
# =============================================================================

import arcpy
from pathlib import Path
import os
import win32com.client
import pyodbc
import logging
import sys
import time
arcpy.env.overwriteOutput = True


def create_database(database_location, db_user, password, port):
    db_name = Path(database_location).stem.lower()

    logging.info(f"Creating Enterprise Geodatabase for: {db_name}")

    arcpy.management.CreateEnterpriseGeodatabase("PostgreSQL", f"localhost,{port}", f"{db_name}", "DATABASE_AUTH",
                                                 "postgres", f"{password}", "SDE_SCHEMA", "sde", f"{password}", '',
                                                 r"C:\Program Files\ESRI\License10.8\sysgen\keycodes")
    logging.info("Creating Super User Database Connection")

    super_user_connection_file = arcpy.management.CreateDatabaseConnection(os.path.dirname(database_location),
                                                                           f"{db_name}_postgres", "POSTGRESQL",
                                                                           f"localhost,{port}", "DATABASE_AUTH",
                                                                           "postgres", f"{password}", "SAVE_USERNAME",
                                                                           f"{db_name}", '', "TRANSACTIONAL",
                                                                           "sde.DEFAULT", None)
    logging.info("Creating new  user")
    arcpy.management.CreateDatabaseUser(super_user_connection_file, "DATABASE_USER", f"{db_user}", f"{password}", '', '')
    logging.info("Create  database connection file")
    user_connection_file = arcpy.management.CreateDatabaseConnection(os.path.dirname(database_location),
                                                                     f"{db_name}_{db_user}", "POSTGRESQL",
                                                                     f"localhost,{port}", "DATABASE_AUTH", f"{db_user}",
                                                                     f"{password}", "SAVE_USERNAME", f"{db_name}", '',
                                                                 "TRANSACTIONAL", "sde.DEFAULT", None)
    logging.info(f"Completed Creating Enterprise Geodatabase for {db_name}\n")
    return user_connection_file


def migrate_database_from_access_to_postgres(access_database_location, pg_user, pg_pwd, pg_port, sde_connection):
    conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; 'rf'DBQ={access_database_location};')
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    a = win32com.client.Dispatch("Access.Application")
    a.OpenCurrentDatabase(access_database_location)

    table_list = []

    for table_info in cursor.tables(tableType='TABLE'):
        table_list.append(table_info.table_name)

    for table in table_list:
        logging.info(f"Exporting: {table}")

        acExport = 1
        acTable = 0
        db_name = Path(access_database_location).stem.lower()
        a.DoCmd.TransferDatabase(acExport, "ODBC Database", "ODBC;DRIVER={PostgreSQL Unicode};"f"DATABASE={db_name};"f"UID={pg_user};"f"PWD={pg_pwd};""SERVER=localhost;"f"PORT={pg_port};", acTable, f"{table}", f"{table.lower()}_export_from_access")
        logging.info(f"Finished Export of Table: {table}")
        logging.info("Creating empty table in EGDB based off of this")

        #in postgres "user" is a keyword, so rename any tables called "user"
        if table.lower() != 'user':
            new_table = arcpy.management.CreateTable(sde_connection, f'{table.lower()}', r"{}\{}_export_from_access".format(sde_connection, table.lower()))
            logging.info("Finished creating empty table in EGDB")
        else:
            logging.info(f"Renaming table from: {table.lower()} to: 'users'")
            new_table = arcpy.management.CreateTable(sde_connection, 'users', r"{}\{}_export_from_access".format(sde_connection, table.lower()))
            logging.info("Finished creating empty table in EGDB")

        try:
            logging.info("Loading data into: {}".format(table.lower()))
            arcpy.management.Append(r"{}\{}_export_from_access".format(sde_connection, table.lower()), new_table, "NO_TEST")
            logging.info(f"Completed loading data into table for {table}")
            logging.info(f"Deleting Access export table: {table}")
            arcpy.management.Delete(r"{}\{}_export_from_access".format(sde_connection, table.lower()))
            logging.info(f"Completed Deleting Access export table: {table}\n")
        except Exception as e:
            logging.error(f"Problem loading: {table.lower()} try alternative method... ")
            logging.error(f"Error Message: {e}")
    a.Quit()

# directory containing all access databases 
database_root_directory = r"C:\Users\fran\all_dbs"
# noinspection PyArgumentList
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.FileHandler(os.path.join(database_root_directory, "export_log.log")),
                        logging.StreamHandler(sys.stdout)
                    ]
                    )
start_time = time.time()

for database in os.scandir(database_root_directory):
    if database.path.endswith("accdb"):
        logging.info(f"Processing: {database.path}")
        sde_connection = create_database(database.path, "user", "pwd", "5433")
        migrate_database_from_access_to_postgres(database.path, "user", "pwd", "5433", sde_connection)

logging.info("Done")
logging.info('Program took {} seconds to complete...\n'.format(time.time() - start_time))


