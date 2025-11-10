import json
import traceback
from app.db.factory import DatabaseFactory

db = DatabaseFactory.create()

def _build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,x-api-key,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps(body)
    }

def handler(event, context):
    try:
        athlete_number = int(event['pathParameters']['id'])
        athlete = db.get_athlete(athlete_number)
        if athlete:
            return _build_response(200, athlete.model_dump())
        else:
            return _build_response(404, {"error": "Pokémon no encontrado"})
    except ValueError:
        return _build_response(400, {"error": "El ID debe ser un número entero."})
    except Exception:
        traceback.print_exc()
        return _build_response(500, {"error": "Error interno del servidor"})
