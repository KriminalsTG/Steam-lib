from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)

# Configuration
FOLDER_PATH = r"E:\Steam Games\manifest"

@app.route('/')
def index():
    """Display the main page"""
    return render_template('index.html', folder_path=FOLDER_PATH.replace('\\', '/'))

@app.route('/download/<filename>')
def download_file(filename):
    """Download a specific file"""
    try:
        return send_from_directory(
            FOLDER_PATH, 
            filename, 
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return f"Error downloading file: {str(e)}", 404

@app.route('/open/<filename>')
def open_file(filename):
    """Open file in browser"""
    try:
        return send_from_directory(FOLDER_PATH, filename, as_attachment=False)
    except Exception as e:
        return f"Error opening file: {str(e)}", 404

@app.route('/api/files')
def get_files():
    """API endpoint to get file list as JSON"""
    try:
        files = []
        if os.path.exists(FOLDER_PATH):
            for filename in sorted(os.listdir(FOLDER_PATH)):
                if filename.lower().endswith('.zip'):
                    file_path = os.path.join(FOLDER_PATH, filename)
                    file_size = os.path.getsize(file_path)
                    if file_size < 1024:
                        size_str = f"{file_size} B"
                    elif file_size < 1024 * 1024:
                        size_str = f"{file_size / 1024:.1f} KB"
                    else:
                        size_str = f"{file_size / (1024 * 1024):.1f} MB"
                    
                    files.append({
                        'name': filename,
                        'size': size_str
                    })
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Steam Manifest File Browser")
    print("=" * 60)
    print(f"Folder: {FOLDER_PATH}")
    print("-" * 60)
    print("Starting server...")
    print("Local: http://127.0.0.1:5000")
    print("Ngrok: Check your ngrok URL")
    print("-" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)