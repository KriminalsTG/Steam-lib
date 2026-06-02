from flask import Flask, render_template, redirect, jsonify, abort
import os
from vercel_blob import list_blobs, BlobError

app = Flask(__name__, template_folder='../templates')

# Fallback environment variable for local testing or display
FOLDER_PATH = os.environ.get("BLOB_READ_WRITE_TOKEN", "Vercel Blob Storage")

@app.route('/')
def index():
    """Display the main page"""
    return render_template('index.html', folder_path="Vercel Cloud Blob Storage")

@app.route('/download/<path:filename>')
def download_file(filename):
    """Redirect to the blob URL for downloading"""
    try:
        blobs_data = list_blobs()
        for blob in blobs_data.get('blobs', []):
            if blob['pathname'] == filename:
                # Appending download parameters to force attachment download if supported
                return redirect(f"{blob['url']}?download=1")
        return "File not found", 404
    except Exception as e:
        return f"Error locating download: {str(e)}", 500

@app.route('/open/<path:filename>')
def open_file(filename):
    """Redirect to the blob URL to view in browser"""
    try:
        blobs_data = list_blobs()
        for blob in blobs_data.get('blobs', []):
            if blob['pathname'] == filename:
                return redirect(blob['url'])
        return "File not found", 404
    except Exception as e:
        return f"Error opening file: {str(e)}", 500

@app.route('/api/files')
def get_files():
    """API endpoint to list blobs as JSON"""
    try:
        files = []
        # Fetching items stored inside your Vercel Blob store
        blobs_data = list_blobs()
        
        for blob in blobs_data.get('blobs', []):
            filename = blob['pathname']
            
            # Filter for .zip files just like original local script
            if filename.lower().endswith('.zip'):
                file_size = blob['size'] # size is given in bytes
                
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
                
        # Sort files alphabetically by name
        files.sort(key=lambda x: x['name'])
        return jsonify(files)
    except BlobError as be:
        return jsonify({'error': 'Blob configuration missing or invalid.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# This block is ignored by Vercel serverless but good for local fallback checks
if __name__ == '__main__':
    app.run(debug=True)