from flask import Flask, jsonify, abort, make_response
from flask_redis import FlaskRedis
import settings

app = Flask(__name__)
app.config['REDIS_URL'] = settings.REDIS_URL
redis_client = FlaskRedis(app, decode_responses=True)

@app.route('/api/games', methods=['GET'])
def get_games():
    games = redis_client.scan_iter(match='game*')
    response = {}
    for game in games:
        response[game] = redis_client.hgetall(game)

    if len(response) == 0:
        abort(404)
    return jsonify(response)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No game found'}), 404)

if __name__ == '__main__':
    app.run(debug=False)
