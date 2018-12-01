import sqlite3
from sqlite3 import Error
import datetime
import datatyper
import logg

# version 1.1


sql_create_car_add_table = """ CREATE TABLE IF NOT EXISTS car_adds (
                                        id nvarchar(16) PRIMARY KEY,
                                        regnr char(6) NOT NULL,
                                        price INT NOT NULL,
                                        brand TEXT NOT NULL,
                                        model TEXT NOT NULL,
                                        model_year TEXT NOT NULL,
                                        make_year TEXT NOT NULL,
                                        gear TEXT NOT NULL,
                                        fuel TEXT NOT NULL,
                                        milage text NOT NULL,
                                        type TEXT NOT NULL,
                                        hp TEXT,
                                        geo TEXT,
                                        add_date DATETIME
                                    ); """



sql_create_car_add_price_table = """ CREATE TABLE IF NOT EXISTS car_add_prices (
                                        car_add_id nvarchar(16) NOT NULL,
                                        price INT NOT NULL,
                                        add_date DATETIME NOT NULL,
                                        PRIMARY KEY (car_add_id, add_date),
                                        FOREIGN KEY (car_add_id) REFERENCES car_adds(id)
                                    ); """



sql_create_car_add_ref_table = """ CREATE TABLE IF NOT EXISTS car_add_refs (
                                        id nvarchar(16) PRIMARY KEY,
                                        link text NOT NULL,
                                        price int NOT NULL
                                    ); """


sql_truncate_car_adds_ref_table = """ DELETE FROM car_add_refs; """


sql_insert_car_add = ''' INSERT INTO car_adds(id, regnr, price, brand, model, model_year, make_year, gear, fuel, milage, type, hp, geo, add_date)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''


sql_update_car_add = ''' UPDATE car_adds SET price = ?, add_date = ?
        WHERE id = ? '''


sql_insert_prices = ''' INSERT OR REPLACE INTO car_add_prices(car_add_id, price, add_date)
        VALUES(?,?,?) '''


sql_insert_add_refs = ''' INSERT OR REPLACE INTO car_add_refs(id, link, price) VALUES(?,?,?) '''



def create_connection():
    try:
        db_file = "car_add_database.db"
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def run_sql(conn, script):
    try:
        c = conn.cursor()
        c.execute(script)
    except Error as e:
        logg.save("Error running SQL script: " + str(e))


## insert array of adds
def insert_car_adds(car_adds):
    inserted_items = 0

    adds = []
    prices = []

    for car_add in car_adds:
        adds.append((car_add.id, car_add.regnr, car_add.price, car_add.brand, car_add.model, car_add.model_year, car_add.make_year, car_add.gear, car_add.fuel, car_add.milage, car_add.type, car_add.hp, car_add.geo, car_add.add_date))
        prices.append((car_add.id, car_add.price, car_add.add_date))

    try:
        conn = create_connection()
        if conn is not None:
            try:
                curr = conn.cursor()
                curr.executemany(sql_insert_car_add, adds)
                inserted_items += curr.rowcount
                curr.executemany(sql_insert_prices, prices)
            except Exception as exc:
                logg.save("Error inserting car adds! Exception: " + str(exc))
        
            conn.commit()
        else:
            print("Error in insert_car_adds! cannot create the database connection.")
    
    except Exception as exc:
        print("Error in insert_car_adds! Exception: " + str(exc))
    finally:
        if conn is not None:
            conn.close
        return inserted_items


## update array of adds
def update_car_adds(car_adds):
    updated_items = 0

    adds = []
    prices = []

    for car_add in car_adds:
        adds.append((car_add.price, car_add.id, car_add.add_date))
        prices.append((car_add.id, car_add.price, car_add.add_date))

    try:
        conn = create_connection()
        if conn is not None:
            try:
                curr = conn.cursor()
                curr.executemany(sql_update_car_add, adds)
                updated_items += curr.rowcount
                curr.executemany(sql_insert_prices, prices)
            except Exception as exc:
                logg.save("Error inside loop of update_car_add! Item id: " + car_add.id + ". Exception: " + str(exc))
        
            conn.commit()
        else:
            print("Error in update_car_adds! cannot create the database connection.")
    
    except Exception as exc:
        print("Error in update_car_adds! Exception: " + str(exc))
    finally:
        if conn is not None:
            conn.close
        return updated_items


# Insert an array of car add refs
def insert_car_add_refs(car_add_refs):
    inserted_items = 0

    adds_refs = []

    for car_ref in car_add_refs:
        adds_refs.append((car_ref.id, car_ref.link, car_ref.price))

    try:
        conn = create_connection()
        if conn is not None:
            try:
                curr = conn.cursor()
                curr.executemany(sql_insert_add_refs, adds_refs)
                inserted_items += curr.rowcount
            except Exception as exc:
                logg.save("Error inserting add refs. Exception: " + str(exc))
        
            conn.commit()
        else:
            print("Error in insert_car_add_refs! cannot create the database connection.")
    except Exception as exc:
        logg.save("Error in insert_car_add_refs! Exception: " + str(exc))
    finally:
        if conn is not None:
            conn.close
        return inserted_items


# Initalize the database
def init():
    try:
        conn = create_connection()
        if conn is not None:
            run_sql(conn, sql_create_car_add_ref_table)
            run_sql(conn, sql_truncate_car_adds_ref_table)
            run_sql(conn, sql_create_car_add_table)
            run_sql(conn, sql_create_car_add_price_table)
            conn.commit()
            conn.close()
        else:
            print("Error in init! cannot create the database connection.")
    
    except Exception as exc:
        logg.save("Error in init! Exception: " + str(exc))
    finally:
        if conn is not None:
            conn.close


# Clean up the staging table
def finish_up():
    try:
        conn = create_connection()
        if conn is not None:
            run_sql(conn, sql_truncate_car_adds_ref_table)
            conn.commit()
            conn.close()
        else:
            print("Error in finish_up! cannot create the database connection.")
    
    except Exception as exc:
        logg.save("Error in finish_up! Exception: " + str(exc))
    finally:
        if conn is not None:
            conn.close

# Query add refs
def get_all_new_adds():

    add_refs = []

    sql_select_all_new_car_add_refs = """
                                    SELECT ref.id, ref.link, ref.price
                                    FROM car_add_refs AS ref
                                    LEFT JOIN car_adds as ad ON ref.id = ad.id
                                    WHERE ad.id IS NULL;
                                    """

    try:
        conn = create_connection()
        if conn is not None:
            cur = conn.cursor()
            cur.execute(sql_select_all_new_car_add_refs)
            rows = cur.fetchall()

            for row in rows:
                add = datatyper.Annons_ref(id = row[0], link = row[1], price = row[2])
                add_refs.append(add)

            conn.close()
        else:
            print("Error in get_all_new_adds! cannot create the database connection.")

        return add_refs
    
    except Exception as exc:
        logg.save("Error in get_all_new_adds! Exception: " + str(exc))
    finally:
        if conn is not None:
            conn.close



# Query updated add refs
def get_all_updated_adds():

    add_refs = []

    sql_select_all_new_car_add_refs = """
                                    SELECT ref.id, ref.link, ref.price
                                    FROM car_add_refs AS ref
                                    LEFT JOIN car_adds as ad ON ref.id = ad.id
                                    WHERE ad.price != ref.price;
                                    """

    try:
        conn = create_connection()
        if conn is not None:
            cur = conn.cursor()
            cur.execute(sql_select_all_new_car_add_refs)
            rows = cur.fetchall()

            for row in rows:
                add = datatyper.Annons_ref(id = row[0], link = row[1], price = row[2])
                add_refs.append(add)

            conn.close()
        else:
            print("Error in get_all_updated_adds! cannot create the database connection.")

        return add_refs
    
    except Exception as exc:
        logg.save("Error in get_all_updated_adds! Exception: " + str(exc))
    finally:
        if conn is not None:
            conn.close
