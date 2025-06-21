import socket

def broadcast_emotion_alert(emotion):
    message = f'ALERT: Driver emotion detected - {emotion}'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(message.encode(), ('<broadcast>', 54545))  # Port can be any unused one
    sock.close()
