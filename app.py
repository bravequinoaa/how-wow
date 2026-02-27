from flask import Flask, send_file, jsonify, request
import os
from datetime import datetime

from log import Log

app = Flask(__name__)
#log = Log()

# Configuration
FILE_PATH = '/data/download/wow.zip'  # Change this to your file path
FILE_NAME = 'wow.zip'  # Change to your desired download filename

# Simple statistics tracking
stats = {
    'total_downloads': 0,
    'last_download': None
}

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'endpoints': {
            'how-wow': '/how-wow',
            'stats': '/stats',
            'info': '/info'
        }
    })

@app.route('/how-wow')
def download():
    if not os.path.exists(FILE_PATH):
        return jsonify({'error': 'File not found'}), 404
    
    # Update stats
    stats['total_downloads'] += 1
    stats['last_download'] = datetime.now().isoformat()
    
    # Get client IP for logging
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"Download #{stats['total_downloads']} - IP: {client_ip} - {datetime.now()}")
    log.info(f"Download #{stats['total_downloads']} - IP: {client_ip} - {datetime.now()}")
    
    return send_file(
        FILE_PATH,
        as_attachment=True,
        download_name=FILE_NAME
    )

@app.route('/stats')
def get_stats():
    file_size = os.path.getsize(FILE_PATH) if os.path.exists(FILE_PATH) else 0
    
    return jsonify({
        'total_downloads': stats['total_downloads'],
        'last_download': stats['last_download'],
        'file_size_bytes': file_size,
        'file_size_gb': round(file_size / (1024**3), 2)
    })

@app.route('/info')
def file_info():
    if not os.path.exists(FILE_PATH):
        return jsonify({'error': 'File not found'}), 404
    
    file_stats = os.stat(FILE_PATH)
    
    return jsonify({
        'filename': FILE_NAME,
        'size_bytes': file_stats.st_size,
        'size_gb': round(file_stats.st_size / (1024**3), 2),
        'modified': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
    })

if __name__ == '__main__':
    # Check if file exists on startup
    if not os.path.exists(FILE_PATH):
        print(f"WARNING: File not found at {FILE_PATH}")
    else:
        file_size_gb = os.path.getsize(FILE_PATH) / (1024**3)
        print(f"File found: {FILE_NAME} ({file_size_gb:.2f} GB)")
    
    # Run on all interfaces, port 8080
    app.run(host='0.0.0.0', port=6969, debug=False)