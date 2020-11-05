from mysql import connector
import creds


def connect():
    connection = connector.connect(
        host=creds.HOST,
        user=creds.USER,
        password=creds.PASSWORD,
        database=creds.DATABASE
    )
    return connection


def init():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS milestones_accounts (name text, password text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS milestones (id text, date text, milestone text, name text)")
    connection.commit()
    connection.close()


def get_account_names():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM milestones_accounts")
    result = format_result(cursor.fetchall())
    connection.close()
    return result


def get_account_password(name: str):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT password FROM milestones_accounts WHERE name='{name}'")
    result = format_result(cursor.fetchone())
    connection.close()
    return result


def create_account(name: str, password: str):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO milestones_accounts VALUES ('{name}', '{password}')")
    connection.commit()
    connection.close()


def add_milestone(name: str, date: str, milestone: str):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT milestone FROM milestones WHERE name='{name}'")
    prev_milestones = format_result(cursor.fetchall())
    identifier = 1

    if prev_milestones is not None:
        identifier = str(len(prev_milestones) + 1)

    cursor.execute(f"INSERT INTO milestones VALUES ('{identifier}', '{date}', '{milestone}', '{name}')")
    connection.commit()
    connection.close()


def remove_milestone(name: str, identifier: str):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM milestones WHERE name='{name}' AND id='{identifier}'")
    connection.commit()
    connection.close()


def list_milestones(name: str):
    result = []
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM milestones WHERE name='{name}'")
    ids = format_result(cursor.fetchall())
    cursor.execute(f"SELECT milestone FROM milestones WHERE name='{name}'")
    milestones = format_result(cursor.fetchall())
    cursor.execute(f"SELECT date FROM milestones WHERE name='{name}'")
    dates = format_result(cursor.fetchall())
    length = 0

    if ids is not None:
        length = len(ids)

    for x in range(0, length):
        result.append(f'#{ids[x]}: {milestones[x]} on {dates[x]}')

    connection.close()
    return result


def format_result(result):
    formatted = []
    if len(result) > 0:
        if len(result) > 1:
            for x in range(0, len(result)):
                formatted.append(result[x][0])
        else:
            return result[0]
    else:
        return None
    if len(formatted) == 1:
        return formatted[0]
    else:
        return formatted