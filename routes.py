from flask import request, jsonify
from . import nexus_chat_bp
import requests
from db_instance import db
from models import chat_history
from datetime import datetime
import json

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
    except KeyError as e:
        # Fallback for missing 'message'
        return jsonify({
            "error": "Missing required field: 'message'",
            "dict": data,
            "error_reason": f"KeyError: {str(e)}"
        }), 400
    
    chat_id = data.get("chat_id")
    chat_history = retrieve_chat_history(chat_id)
    message_history = {"messages":[]}
    for chat in chat_history:
        chunk =  { "role": global_params["role"], 
            "content": chat.message_content
            }
        message_history["messages"].append(chunk)
    
    print(json.dumps(message_history, indent=2))

    #for chat in chat_history:
     #   print(chat.message_content, chat.message_date)
    save_chat(chat_id, message)

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


    r = requests.post('http://192.168.1.122:11434/api/chat', json=llm_request)
    
    try:
        response_data = r.json()
    except requests.exceptions.JSONDecodeError:
        # Fallback
        return jsonify({"error": "External API did not return valid JSON", "text": r.text}), 500

    return jsonify(response_data), r.status_code


def save_chat(chat_id, message):

    if chat_id is None:
        existing = chat_history.query.order_by(chat_history.chat_id.desc()).first()
        if existing is None:
            current_chat = 0
        else:
            current_chat = existing.chat_id + 1
    else:
        current_chat = chat_id
    
    current_date = datetime.utcnow()
    message_db = {"chat_id": current_chat,
                  "message_content": message,
                  "message_date": current_date}
    db.session.add(chat_history(**message_db))
    db.session.commit()
        
    return None

def retrieve_chat_history(chat):
    if chat is None:
        return None
    else:
        history = chat_history.query.filter_by(chat_id=chat).order_by(chat_history.chat_id.desc()).all()
        return(history)