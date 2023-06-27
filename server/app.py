from flask import Flask, request, jsonify,make_response
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == "GET":
        messages = Message.query.all()
        messages_list = []
        for message in messages:
            messages_dict = {
                "id":message.id,
                "username":message.username,
                "body":message.body
            }
            messages_list.append(messages_dict)

        return jsonify(messages_list)

    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            username=data["username"], 
            body=data["body"]
            )
        db.session.add(message)
        db.session.commit()
        response = make_response(jsonify(message.to_dict()),200)
        return response


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def message_by_id(id):
    message = db.session.get(Message, id)

    if request.method == 'PATCH':
        data = request.get_json()
        for attr, value in data.items():
            setattr(message, attr, value)
        db.session.commit()
        response = make_response(jsonify(message.to_dict()), 200)
        return response

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body = make_response(jsonify(
            {'message': 'Message deleted successfully'}
            ), 200)
        return response_body


if __name__ == '__main__':
    app.run(port=5555)