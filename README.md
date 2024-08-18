HTML to PDF Conversion Service using Flask and wkhtmltopdf

This project provides a web service for converting HTML content to PDF files using Python's Flask framework and wkhtmltopdf. The service accepts HTML content via a POST request and returns a PDF file as the response.

API Endpoint
Request JSON Payload:
{
    "html": "<html>Your HTML content here</html>",
    "options": {
        "page-size": "A4",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in"
    }
}
