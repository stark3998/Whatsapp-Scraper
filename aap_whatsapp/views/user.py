# -*- coding: utf-8 -*-
__author__ = ''

from aap_whatsapp import app
from aap_whatsapp.model.message import User, MessageReceived
from aap_whatsapp.schemas.message import UserSchema
from flask import request, jsonify, render_template
import psycopg2


@app.route('/api/v1/create_user', methods=['POST'])
def create_user():
    try:
        ob = User(**request.json)
        ob.save()
        result = UserSchema().dump(ob)
        return jsonify(result.data)
    except Exception as error:
        return jsonify({"error":str(error)})


@app.route('/api/v1/update_user/<user_id>', methods=['PATCH'])
def update_user(user_id):
    ob = User.query.get(user_id)
    if ob:
        for key in request.json:
            setattr(ob, key, request.json[key])
        ob.update()
        result = UserSchema().dump(ob)
        return jsonify(result.data)
    return jsonify({'error': "No User found with id ({})".format(user_id)}), 500


@app.route('/api/v1/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    print(request.json)
    for u in MessageReceived.query.filter_by(user_id=user_id).all():
        u.delete()
    ob = User.query.get(user_id)
    if ob:
        ob.delete()
        return jsonify({'id': ob.id})
    return jsonify({'error': "No User found with id ({})".format(user_id)}), 500


@app.route('/api/v1/users', methods=['GET'])
def users():
    if request.method == 'GET':
        args = request.args.to_dict()
        args.pop('page', None)
        args.pop('per_page', None)
        total = User.query.filter_by(**args).count()
        per_page = int(request.args.get('per_page', 20))
        page = int(request.args.get('page', 1))
        data = User.query.filter_by(**args).order_by(User.created_at.desc()).offset((page - 1) * per_page).limit(
            per_page).all()
        data = UserSchema(many=True).dump(data).data
        response = jsonify({"result": data, "total": total})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route("/user")
def render_user():
    return render_template("user.html")
