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
    
    # Print to console
    print(f"[LOGGED] Emotion: {emotion} | Hash: {new_block.hash[:10]}...")

    # Append to file
    with open("emotion_blockchain_log.txt", "a") as f:
        f.write(f"Timestamp: {new_block.timestamp}\n")
        f.write(f"Emotion: {new_block.emotion}\n")
        f.write(f"Previous Hash: {new_block.prev_hash}\n")
        f.write(f"Hash: {new_block.hash}\n")
        f.write("-" * 40 + "\n")
