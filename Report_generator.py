
import datetime

from fillpdf import fillpdfs
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


def add_image_to_existing_pdf(input_pdf, image_path, output_pdf):
  # Read the existing PDF
  reader = PdfReader(input_pdf)
  writer = PdfWriter()

  # Create a temporary PDF with the image on the second page
  packet = BytesIO()
  page_width, page_height = letter  # Assuming letter-sized PDF
  img_width, img_height = 4 * 72, 4 * 72  # Image size (3x3 inches, 1 inch = 72 points)
  x = (page_width - img_width) / 2
  y = (page_height - img_height) / 2

  # Use ReportLab to create the overlay
  c = canvas.Canvas(packet, pagesize=letter)
  c.drawImage(image_path, x, y, width=img_width, height=img_height)
  c.save()
  packet.seek(0)

  # Merge the overlay into the second page
  overlay_reader = PdfReader(packet)
  for i, page in enumerate(reader.pages):
      if i == 1:  # Add the image only to the second page
          page.merge_page(overlay_reader.pages[0])
      writer.add_page(page)

  # Write the output PDF
  with open(output_pdf, "wb") as output:
      writer.write(output)



def report_gen(name, age, gender, symptoms, ai_report, date, logs):

  form_fields=list(fillpdfs.get_form_fields("Report_template/template_1.pdf").keys())

  data_dict={
      form_fields[0]:name,
      form_fields[1]:age,
      form_fields[2]:gender,
      form_fields[3]:symptoms,
      form_fields[4]:ai_report,
      form_fields[5]:str(datetime.datetime.now().date()),
      form_fields[6]:f"Xray results are {logs}",
  }



  # fillpdfs.write_fillable_pdf("Report_template/template_1.pdf",f"{name}.pdf",data_dict)
  fillpdfs.write_fillable_pdf("Report_template/template_1.pdf",f"Records/{name}.pdf",data_dict)
  add_image_to_existing_pdf(f"Records/{name}.pdf", "outputs/output.jpg", f"Records/{name}_full.pdf")





