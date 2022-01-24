from django.core.management.base import BaseCommand
import psycopg2, time

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        is_online = False
        conn = None
        while(not is_online):
            try:
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(
                    host="db",
                    database="bpmnhu",
                    user="bpmnhu",
                    password="bpmnhu"
                )
                cur = conn.cursor()
                print('PostgreSQL database version:')
                cur.execute('SELECT version()')
                db_version = cur.fetchone()
                is_online = True

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
            time.sleep(3)
