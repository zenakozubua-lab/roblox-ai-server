from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route('/ai', methods=['POST'])
def ai():
    data = request.json
    prompt = data.get('prompt', '')
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Ты помощник для Roblox Studio. 
                Отвечай ТОЛЬКО в формате JSON вот так:
                {{
                    "lua": "-- код если нужен скрипт, иначе пусто",
                    "parts": [
                        {{
                            "name": "название парта",
                            "size": {{"x": 10, "y": 1, "z": 10}},
                            "position": {{"x": 0, "y": 0, "z": 0}},
                            "color": {{"r": 255, "g": 255, "b": 255}},
                            "anchored": true
                        }}
                    ],
                    "message": "что ты сделал"
                }}
                Запрос: {prompt}"""
            }
        ]
    )
    
    return jsonify({"result": message.content[0].text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
