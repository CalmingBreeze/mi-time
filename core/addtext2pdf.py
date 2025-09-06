from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas

class AddTextToPDF:
    def __init__(self, input_pdf_path, output_pdf_path):
        self.input_pdf = PdfReader(input_pdf_path)
        self.output_pdf = PdfWriter()
        self.output_path = output_pdf_path

    def add_text(self, text, coords):
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        can.setFillColorRGB(0.624, 0.494, 0.416) #9f7e6a
        can.setStrokeColorRGB(0.624, 0.494, 0.416) #9f7e6a
        can.drawString(coords[0], coords[1], text)
        can.save()
        packet.seek(0)

        new_pdf = PdfReader(packet)
        existing_page = self.input_pdf.pages[0]
        existing_page.merge_page(new_pdf.pages[0])
        self.output_pdf.add_page(existing_page)

    # Fill the blank pdf file with the infos provided
    def buildGiftcard(self, gift_name, code, expires_at):
        gift_name_coords = (255, 344)
        code_coords = (225, 283)
        expires_at_coords = (310, 252)
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        can.setFillColorRGB(0.624, 0.494, 0.416) #9f7e6a
        can.setStrokeColorRGB(0.624, 0.494, 0.416) #9f7e6a
        can.drawString(gift_name_coords[0], gift_name_coords[1], gift_name)
        can.drawString(code_coords[0], code_coords[1], code)
        can.drawString(expires_at_coords[0], expires_at_coords[1], expires_at)
        can.save()
        packet.seek(0)

        new_pdf = PdfReader(packet)
        existing_page = self.input_pdf.pages[0]
        existing_page.merge_page(new_pdf.pages[0])
        self.output_pdf.add_page(existing_page)

    def save(self):
        with open(self.output_path, "wb") as outputStream:
            self.output_pdf.write(outputStream)