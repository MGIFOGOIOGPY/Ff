from flask import Flask, request, jsonify
import aiohttp
import asyncio

app = Flask(__name__)

# الدالة للتحقق من التوكن
async def like(id, token):
    like_url = 'https://clientbp.ggblueshark.com/LikeProfile'
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB46',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }

    data = bytes.fromhex(id)

    async with aiohttp.ClientSession() as session:
        async with session.post(like_url, headers=headers, data=data) as response:
            if response.status == 200:
                return {"status": "success", "message": "Token valid"}
            else:
                return {"status": "failure", "message": "Token invalid"}

# إنشاء route للتحقق من التوكن
@app.route('/check_token', methods=['GET'])
def check_token():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token is required"}), 400

    # تحويل التوكن المرسل إلى JWT أو استخدامه كما هو
    jwt_token = token

    # استدعاء الدالة للتحقق
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(like('1234567890abcdef', jwt_token))  # استخدم الـ id المناسب

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)