from datetime import datetime, timedelta
import jwt

class JwtAuth:
    def __init__(self):
        pass

    def generate_token(self, user_data,private_key):
        now = datetime.utcnow()
        expiration_time = now + timedelta(hours=72)
        expiration_timestamp = int(expiration_time.timestamp())

        payload = {
            "user_name": user_data['user_name'],
            "email": user_data['email'],
            "user_id": user_data['user_id'],
            "iat": datetime.now(),
            "exp": expiration_timestamp
        }

        token = jwt.encode(payload, private_key, algorithm='RS256')
        return token
    
    def validate_token(self, token,public_key):
        try:
            token_decode = jwt.decode(token, public_key, algorithms=['RS256'])
            current_timestamp = int(datetime.utcnow().timestamp())

            if token_decode['exp'] < current_timestamp:
                raise jwt.ExpiredSignatureError

            return {
                'response': 200,
                'message': 'token is valid.',
                'token': token
            }
        
        except jwt.ExpiredSignatureError:
            return {
                'response': 401,
                'message': 'This token has expired!'
            }
        
        except jwt.InvalidTokenError:
            return {
                'response': 401,
                'message': 'This token is Invalid!'
            }