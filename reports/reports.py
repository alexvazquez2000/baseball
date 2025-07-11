from flask import Blueprint, make_response
#for PDF
#from flask import make_response
from fpdf import FPDF

reports_bp = Blueprint('pdf_reports', __name__)
# -- Experimental section
@reports_bp.route('/generate-pdf')
def generate_pdf():
	# https://py-pdf.github.io/fpdf2/Tutorial.html#tuto-1-minimal-example
    #Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    # Add content to the PDF
    pdf.cell(200, 10, txt="Hello from Flask and FPDF!", ln=1, align="C")
    pdf.cell(200, 10, txt="This is a dynamically generated PDF.", ln=1, align="C")

    # PDF is ready
    # for usage on flask https://py-pdf.github.io/fpdf2/UsageInWebAPI.html

    # Output the PDF as bytes
    pdf_output = pdf.output(dest='S').encode('latin-1')
    # Create a Flask response and Output the PDF as bytes
    response = make_response(pdf_output)
    # Set appropriate headers for PDF
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=generated_document.pdf" 
    return response
