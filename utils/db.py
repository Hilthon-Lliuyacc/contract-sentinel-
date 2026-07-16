import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def guardar_conversacion(session_id, pregunta, respuesta, fuentes=""):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO conversaciones 
               (session_id, pregunta, respuesta, documentos_fuente) 
               VALUES (%s, %s, %s, %s)""",
            (session_id, pregunta, respuesta, fuentes)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Conversación guardada en MySQL.")
    except Exception as e:
        print(f"Error MySQL: {e}")

def obtener_historial(session_id, limite=5):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT pregunta, respuesta 
               FROM conversaciones 
               WHERE session_id = %s 
               ORDER BY created_at DESC LIMIT %s""",
            (session_id, limite)
        )
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado[::-1]
    except Exception as e:
        print(f"Error MySQL: {e}")
        return []