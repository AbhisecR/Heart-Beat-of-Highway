import hashlib
import time

# ========== BLOCKCHAIN SETUP ==========
class EmotionBlock:
    def __init__(self, emotion, prev_hash):
        self.timestamp = time.time()
        self.emotion = emotion
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        record = str(self.timestamp) + self.emotion + self.prev_hash
        return hashlib.sha256(record.encode()).hexdigest()

# Initialize the blockchain
blockchain = []
genesis_block = EmotionBlock("Genesis", "0")
blockchain.append(genesis_block)

# Function to log emotion into blockchain
def log_emotion_to_blockchain(emotion):
    prev_hash = blockchain[-1].hash
    new_block = EmotionBlock(emotion, prev_hash)
    blockchain.append(new_block)
    print(f"[LOGGED] Emotion: {emotion} | Hash: {new_block.hash[:10]}...")