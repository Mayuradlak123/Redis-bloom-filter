from flask import Blueprint, request, jsonify
from api.services.bloom_filter import BloomFilter
from api.services.database import db_service
import redis
import json
import os

auth_bp = Blueprint('auth', __name__)

# Initialize Redis and Bloom Filter
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

try:
    redis_client.ping()
    print(f"✅ Successfully connected to Redis on {REDIS_HOST}:{REDIS_PORT}")
except redis.ConnectionError:
    print(f"❌ Failed to connect to Redis on {REDIS_HOST}:{REDIS_PORT}. Please ensure Redis is running.")

BF_KEY = os.getenv('BLOOM_FILTER_KEY', 'username_bloom_filter')
BF_SIZE = int(os.getenv('BLOOM_FILTER_SIZE', 10000000))
BF_HASH_COUNT = int(os.getenv('BLOOM_FILTER_HASH_COUNT', 7))

bf = BloomFilter(redis_client, BF_KEY, size=BF_SIZE, hash_count=BF_HASH_COUNT)

@auth_bp.route('/check-username', methods=['GET'])
def check_username():
    username = request.args.get('username', '').strip()
    if not username:
        return jsonify({'available': True, 'message': 'Username is required'}), 400
    
    # Bloom Filter check (Fast Path)
    might_exist = bf.exists(username)
    
    if not might_exist:
        # Definitely not in the system
        return jsonify({'available': True, 'username': username})
    
    # Slow Path: Verify against PostgreSQL
    is_taken = db_service.user_exists(username)
    
    return jsonify({
        'available': not is_taken,
        'username': username,
        'source': 'PostgreSQL' if is_taken else 'Bloom Filter (False Positive Resolved)'
    })

def seed_bloom_filter(data_path):
    """Seed the bloom filter and postgres with existing usernames from JSON."""
    if not os.path.exists(data_path):
        print(f"Data file not found: {data_path}")
        return

    # Initialize DB table
    db_service.initialize_db()

    with open(data_path, 'r') as f:
        users = json.load(f)
        for user in users:
            username = user.get('username')
            email = user.get('email')
            if username:
                bf.add(username)
                db_service.add_user(username, email)
    print(f"✅ Seeding complete: {len(users)} users added to Bloom Filter and PostgreSQL.")

# Seed on import/initialization
USERS_DATA_PATH = os.getenv('USERS_DATA_PATH', 'data/users.json')
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', USERS_DATA_PATH))
seed_bloom_filter(DATA_PATH)
