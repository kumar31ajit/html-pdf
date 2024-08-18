from flask import Flask, request, send_file, url_for
import pdfkit
import os
from bs4 import BeautifulSoup
import base64

app = Flask(__name__, static_folder='static')

# Configure pdfkit to use wkhtmltopdf executable with local file access enabled
config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

@app.route('/convert_html_to_pdf', methods=['POST'])
def convert_html_to_pdf():
    try:
        # Get HTML content and image data from the request
        data = request.get_json()
        if not isinstance(data, dict):
            return "Invalid JSON payload", 400

        html_content = data.get('html')
        pdf_options = data.get('options', {})
        # image_data = data.get('images', {})

        if not html_content:
            return "HTML content is missing", 400

        # if not isinstance(image_data, dict):
        #     return "Invalid images data", 400

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Path to the local CSS files
        css_files = [
            'bootstrap-3.3.5.min.css',
            'font-awesome.min.css',
            'main.css',
            'uni_pdf.css'
        ]

        # Update the link tags in the HTML content
        for link_tag in soup.find_all('link'):
            href = link_tag.get('href')
            if href and any(css_file in href for css_file in css_files):
                css_filename = os.path.basename(href)
                new_href = url_for('static', filename=f'css/{css_filename}', _external=True)
                link_tag['href'] = new_href

        # If the <head> tag does not exist, create it
        if not soup.head:
            head_tag = soup.new_tag('head')
            soup.insert(0, head_tag)

        # Append the modified link tags to the <head> tag
        for link_tag in soup.find_all('link'):
            soup.head.append(link_tag)
      
        # Convert the modified HTML content back to a string
        full_html_content = str(soup)

        # Generate a PDF file from the HTML content
        default_options = {
            'page-size': 'A4',
            'enable-local-file-access': ''
        }

        options = {**default_options, **pdf_options}

        pdf_data = pdfkit.from_string(full_html_content, False, configuration=config, options=options)

        # Save the PDF file
        pdf_filename = 'output.pdf'
        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(pdf_data)

        return send_file(pdf_filename, download_name='output.pdf', as_attachment=True)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
