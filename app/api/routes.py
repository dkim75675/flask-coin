from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from Models import db, User, Coin, coin_schema, coins_schema 

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/coin', methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    wallet_id = request.json['wallet_id']
    coin_name = request.json['coin_name']
    amount = request.json['amount']
    equity = request.json['equity']
    user_token = current_user_token.token

    coin = Coin(wallet_id, coin_name, amount, equity, user_token=user_token )

    db.session.add(coin)
    db.session.commit()

    response = coin_schema.dump(coin)
    return jsonify(response)

@api.route('/coin', methods = ['GET'])
@token_required
def get_coin(current_user_token):
    a_user = current_user_token.token
    coins =  Coin.query.filter_by(user_token = a_user).all()
    response = coins_schema.dump(coins)
    return jsonify(response)

@api.route('/coin/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    coin = Coin.query.get(id)
    response = coin_schema.dump(coin)
    return jsonify(response)
    

@api.route('/coin/<id>', methods = ['POST', 'PUT'])
@token_required
def update_coin(current_user_token, id):
    coin = Coin.query.get(id)
    coin.wallet_id = request.json['wallet_id']
    coin.coin_name = request.json['coin_name']
    coin.amount = request.json['amount']
    coin.equity= request.json['equity']
    coin.user_token = current_user_token.token

    db.session.commit()
    response = coin_schema.dump(coin)
    return jsonify(response)

@api.route('/coin/<id>', methods = ['DELETE'])
@token_required
def delete_coin(current_user_token, id):
    coin = Coin.query.get(id)
    
    db.session.delete(coin)
    db.session.commit()
    response = coin_schema.dump(coin)
    return jsonify(response)