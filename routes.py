from flask import request, jsonify
from . import nexus_chat_bp
import requests


global_params = {
    "model": "qwen2.5-coder:7b-instruct-q4_K_M",
    "role": "user",
    "stream": False
}

chat_params = {
    "num_gpu": 99,
    "num_ctx": 4096
}


@nexus_chat_bp.route('/message', methods=['POST'])
def handle_message():
    # Parse incoming JSON data
    data = request.get_json()
    try:
        message = data["message"]
    except:
        # Fallback
        return jsonify({"error": "Message input is invalid format. Must be valid JSON and pass a 'message' field", "dict": data}), 500


    llm_request = {
        "model": global_params["model"],
        "messages": [
            { "role": global_params["role"], 
            "content": message
            }
        ],
        "stream": global_params["stream"],
        "options": {}
    }

    for key, value in chat_params.items():
        llm_request["options"][key] = value

    print(llm_request)


    r = requests.post('http://192.168.1.122:11434/api/chat', json=llm_request)
    
    try:
        response_data = r.json()
    except requests.exceptions.JSONDecodeError:
        # Fallback
        return jsonify({"error": "External API did not return valid JSON", "text": r.text}), 500

    return jsonify(response_data), r.status_code


