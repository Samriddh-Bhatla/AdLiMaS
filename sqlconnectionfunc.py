import pandas as pd
import pymysql as p
import sqlalchemy as sql


def csv_to_table(path: str, tablename: str, bo: str, index_send: bool = False):
    """

    :param bo: pass 'replace' to replace existing(if) table, 'append' to add below existing(if)
    :param index_send: Send indexes to SQL Table or not
    :param tablename: Name of table to be created
    :param path: absolute path of csv file
    :return: list of failure/success with boolean at '0' and error(if occurs)
    """
    df = pd.read_csv(path)
    tablename = tablename.lower()
    try:
        file_conn = sql.create_engine('mysql+pymysql://root@localhost/library').connect()
        conn = p.connect(host='localhost', user='root', passwd='', db='library')
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT = 0")
        df.to_sql(tablename, file_conn, index=index_send, if_exists=bo)
        c.execute("COMMIT")
        conn.close()
        file_conn.close()
        return [True]
    except p.MySQLError as err:
        return [False, err]


def alter_table_cell(update_val, tablename: str, columnname: str, primary_key_field, pri_key):
    """

    :param update_val: Value to be inserted into cell
    :param primary_key_field: PRI constraint column
    :param tablename: MySQL table in which data cell to be altered
    :param columnname: Name of column of the cell
    :param pri_key: Value of pri_key_field column
    :return: list of failure and error(if occurs)
    """
    try:
        test_var_def = [update_val, tablename, columnname, pri_key]
        test_var_def.extend('1234')
        try:
            file_conn = sql.create_engine('mysql+pymysql://root@localhost/library').connect()
            conn = p.connect(host='localhost', user='root', passwd='', db='library')
            c = conn.cursor()
            c.execute("SET AUTOCOMMIT = 0")
            x = c.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(
                tablename, columnname, update_val, primary_key_field, pri_key))
            if x == 0:
                c.execute("ROLLBACK")
                return [False, 'There was no ROW with Primary Key Field set to {}'.format(pri_key)]
            elif x == 1:
                c.execute("COMMIT")
            else:
                c.execute("ROLLBACK")
                return [False, 'More than 1 row was affected!']
            c.execute("SET AUTOCOMMIT = 1")
            conn.close()
            file_conn.close()
        except p.MySQLError as err:
            return [False, err]
    except NameError as err:
        return [False, err]


def read_table_cell(tablename: str, columnname: str, primary_key_field: str, pri_key):
    """

    :param tablename:
    :param columnname:
    :param primary_key_field:
    :param pri_key:
    :return:
    """
    try:
        test_var_def = [tablename, columnname, pri_key]
        test_var_def.extend('1234')
        try:
            conn = p.connect(host='localhost', user='root', passwd='', db='library')
            c = conn.cursor()
            x = c.execute("SELECT {} FROM {} WHERE {} = {}".format(
                columnname, tablename, primary_key_field, pri_key))
            f = c.fetchall()
            conn.close()
            return [True, f, x]
        except p.MySQLError as err:
            return [False, err]
    except NameError as err:
        return [False, err]


def add_table_row(row: dict, tablename: str):
    """

    :param row: dictionary object with keys matching the fields of MySQL Table
    :param tablename: Table row to be appended into
    :return: list of failure with error(if occurs)
    """
    try:
        local_use_var = [row, tablename]
        local_use_var.extend('1234')
        try:
            file_conn = sql.create_engine('mysql+pymysql://root@localhost/library').connect()
            conn = p.connect(host='localhost', user='root', passwd='', db='library')
            c = conn.cursor()
            c.execute("SET AUTOCOMMIT = 0")
            x = c.execute(
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}' AND "
                "TABLE_SCHEMA='library'".format(tablename))
            t = list(c.fetchall())
            if len(row) == x:
                zeta = 0
                for y, z in zip(row.keys(), t):
                    for locale in z:
                        if y.strip() == locale.strip():
                            zeta += 1
                if zeta == x:
                    local_use_var.clear()
                    query = "INSERT INTO {} VALUES{}".format(tablename, tuple(row.values()))
                    c.execute(query)
                    c.execute("COMMIT")
                    c.execute("SET AUTOCOMMIT = 1")
                else:
                    return [False, 'Columns and Keys do not match']
            else:
                return [False, 'Values passed do not match no. of columns in table']
            conn.close()
            file_conn.close()
        except p.MySQLError as err:
            return [False, err]
    except NameError as err:
        return [False, err]
    return [True]


def delete_table_row(row_field_val: str, tablename: str, delete_field: str):
    """
    
    :param row_field_val: value of field using which selection for deletion to be done
    :param tablename: table from which row to be dropped
    :param delete_field: Column set to have the row_field_value
    :return: list of failure and error(if occurs)
    """
    try:
        local_use_var = [row_field_val, tablename, delete_field]
        local_use_var.extend('1234')
        try:
            file_conn = sql.create_engine('mysql+pymysql://root@localhost/library').connect()
            conn = p.connect(host='localhost', user='root', passwd='', db='library')
            c = conn.cursor()
            c.execute("SET AUTOCOMMIT = 0")
            x = c.execute("DELETE FROM {} WHERE {} = '{}'".format(tablename, delete_field, row_field_val))

            if x == 0:
                return [False,
                        'Nothing was deleted as {} was not set was not found in {} column of {}'.format(row_field_val,
                                                                                                        delete_field,
                                                                                                        tablename)]
            elif x == 1:
                c.execute("COMMIT")
            else:
                c.execute("ROLLBACK")
                return [False, r'More than the one anticipated row was/were deleted. Changes have been undone']
            c.execute("SET AUTOCOMMIT = 1")
            conn.close()
            file_conn.close()
        except p.MySQLError as err:
            return [False, err]
    except NameError as err:
        return [False, err]
    pass


def check_sql_account(username: str, password: str):
    """

    :param username: Username of account to verify(case sensitive)
    :param password: password to check(case sensitive)
    :return: bool: Account existent/non_existent
    """
    try:
        conn = p.connect(host='localhost', user='root', passwd='', db='library')
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT = 0")
        x = c.execute(
            "SELECT * FROM ACCOUNTS WHERE USERNAME=MD5('{}') AND PASSWORD=MD5('{}')".format(username, password))
        if x == 0:
            return False
        elif x == 1:
            return True
        conn.close()
    except ValueError:
        return False
    finally:
        pass
    pass


def add_sql_account(username: str, password: str):
    try:
        conn = p.connect(host='localhost', user='root', passwd='', db='library')
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT = 0")
        x = c.execute(
            "INSERT INTO ACCOUNTS(USERNAME, PASSWORD) VALUES(MD5('{}'), MD5('{}'))".format(username, password))
        if x == 0:
            return False
        elif x == 1:
            c.execute("COMMIT")
            return True
        conn.close()
    except ValueError:
        return False
    finally:
        pass


def check_sql_username(username: str):
    try:
        conn = p.connect(host='localhost', user='root', passwd='', db='library')
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT = 0")
        x = c.execute(
            "SELECT * FROM ACCOUNTS WHERE USERNAME=MD5('{}')".format(username))
        if x == 0:
            return True
        elif x >= 1:
            return False
        conn.close()
    except ValueError:
        return False


def run_query(query: str):
    try:
        conn = p.connect(host='localhost', user='root', passwd='', db='library')
        c = conn.cursor()
        c.execute("SET AUTOCOMMIT = 0")
        x = c.execute(query.strip().upper())
        f = c.fetchall()
        conn.close()
        return [x, f]
    except p.MySQLError:
        pass
