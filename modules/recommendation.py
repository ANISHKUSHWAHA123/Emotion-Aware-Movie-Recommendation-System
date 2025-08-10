import mysql.connector

def get_recommendations(user_id, current_emotion):
    try:
        conn = mysql.connector.connect(
            user="root",
            password="Anish@123",
            host="localhost",
            database="movies_db"
        )
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT movies.title, movies.genre, movies.video_url
        FROM movies
        JOIN user_preferences ON movies.id = user_preferences.movie_id
        WHERE user_preferences.user_id = %s AND movies.genre IN (
            SELECT genre FROM genre_emotion_mapping WHERE emotion = %s
        )
        ORDER BY user_preferences.ranking DESC LIMIT 10;
        """
        cursor.execute(query, (user_id, current_emotion))
        recommendations = cursor.fetchall()
        return recommendations
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    except Exception as e:
        print(f"General error: {e}")
        return []
    finally:
        if conn.is_connected():
            conn.close()


# user_id = 1
# current_emotion = "happy"
# recommendations = get_recommendations(user_id, current_emotion)
# print(recommendations)
# ----------------------for new user trending movie recommendsaion-------------------
def tred_recommendation(current_emotion):
    try:
        conn = mysql.connector.connect(
            user="root",
            password="Anish@123",
            host="localhost",
            database="movies_db"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Correct query syntax
        query = """
        SELECT 
            trending.title, 
            trending.genre, 
            trending.video_url, 
            trending.views_count, 
            trending.likes_count, 
            trending.avg_ratings 
        FROM trending
        WHERE trending.emotion_cluster = %s
        ORDER BY trending.views_count DESC 
        LIMIT 10;
        """
        
        # Pass parameter as a tuple
        cursor.execute(query, (current_emotion,))
        
        # Fetch recommendations
        recommendations = cursor.fetchall()
        return recommendations if recommendations else []
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    except Exception as e:
        print(f"General error: {e}")
        return []
    finally:
        # Ensure the connection is closed
        if conn.is_connected():
            conn.close()