import os
from flask import Flask, request, render_template
from source_deploy.pdf_processor import PDFProcessor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'data', 'resumes')  # Use absolute path

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

pdf_processor = PDFProcessor()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            try:
                file.save(file_path)
                text = pdf_processor.extract_text_from_pdf(file_path)
                names, emails = pdf_processor.extract_names_and_emails(text)
                
                # Add a message if no names or emails were found
                if not names:
                    names = ['Không tìm thấy tên.']
                if not emails:
                    emails = ['Không tìm thấy email.']
                
                return render_template('result.html', names=names, emails=emails, file_name=file.filename)
            except Exception as e:
                return f"An error occurred: {e}"
        else:
            return "Please upload a valid PDF file."
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)  # Set debug to False in production
