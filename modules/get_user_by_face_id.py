import mysql.connector

def get_user_by_face_id(face_id):
    try:
        # Establish the database connection
        conn = mysql.connector.connect(
            user="root",
            password="Anish@123",
            host="localhost",
            database="movies_db" 
        )
        cursor = conn.cursor(dictionary=True)

        # Query to fetch user details by face_id
        query = "SELECT id, name FROM users WHERE face_id = %s;"
        cursor.execute(query, (face_id,))

        # Fetch the result
        user = cursor.fetchone()

        # Return the result or None if no match is found
        return user

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

