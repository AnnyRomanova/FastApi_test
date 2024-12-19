import psycopg2


try:
    connection = psycopg2.connect(
        host="localhost",
        user="Anny",
        password="123456",
        database="FAT_db4",
        port=5431
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute("""SELECT
         authors.id AS author_id,
         authors.author_name AS author_name,
         posts.id AS post_id,
         posts.title,
         posts.body
         FROM authors
         JOIN posts
         ON authors.id = posts.author_id""")
        print(cursor.fetchall())

    # with connection.cursor() as cursor:
    #     cursor.execute("""INSERT INTO posts (title, body, author_id) VALUES
    #     ('title_1', 'body_1', 1),
    #     ('title_2', 'body_2', 2),
    #     ('title_3', 'body_3', 1),
    #     ('title_4', 'body_4', 3)""")

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals() and connection:
        connection.close()

