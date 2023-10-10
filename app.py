from flask import Flask, request, jsonify, render_template, session
from data_processing import identify_application

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    uploaded_file.save(uploaded_file.filename)
    file_path = uploaded_file.filename  # Store the file path in session
    return process_file(file_path)
@app.route('/process_file', methods=['POST'])
def process_file(file_path):
    if file_path:
        file_name = file_path.split('/')[-1]
        process_function = identify_application(file_path)
        process_function(file_path)  # Pass the file path to the processing function
        return jsonify({"message": "File processed successfully."})
    else:
        return jsonify({"error": "No file uploaded."})

if __name__ == '__main__':
    app.run(port=8000, debug=True)
