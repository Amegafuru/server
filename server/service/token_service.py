import jwt
import os
from models.token_model import TokenModel

class TokenService:
    def generate_tokens(self, payload):
        access_token = jwt.encode(payload, os.getenv('JWT_ACCESS_SECRET'), algorithm='HS256', expires_in='15s')
        refresh_token = jwt.encode(payload, os.getenv('JWT_REFRESH_SECRE'), algorithm='HS256', expires_in='30s')
        return {
            'accessToken': access_token,
            'refreshToken': refresh_token
        }

    def validate_access_token(self, token):
        try:
            decoded_token = jwt.decode(token, os.getenv('JWT_ACCESS_SECRET'), algorithms=['HS256'])
            return decoded_token
        except jwt.ExpiredSignatureError:
            return None

    def validate_refresh_token(self, token):
        try:
            decoded_token = jwt.decode(token, os.getenv('JWT_REFRESH_SECRET'), algorithms=['HS256'])
            return decoded_token
        except jwt.ExpiredSignatureError:
            return None

    async def save_token(self, user_id, refresh_token):
        token_data = await TokenModel.find_one({'user': user_id})
        if token_data:
            token_data['refreshToken'] = refresh_token
            return await token_data.save()
        token = await TokenModel.create({'user': user_id, 'refreshToken': refresh_token})
        return token

    async def remove_token(self, refresh_token):
        return await TokenModel.delete_one({'refreshToken': refresh_token})

    async def find_token(self, refresh_token):
        return await TokenModel.find_one({'refreshToken': refresh_token})
