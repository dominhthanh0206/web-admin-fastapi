import pytesseract
from pdf2image import convert_from_bytes
import re
from typing import Dict, Any
from blog.schemas.invoice import InvoiceData, InvoiceItem

class InvoiceOCRService:
    @staticmethod
    def extract_invoice_data(pdf_bytes: bytes) -> InvoiceData:
        # Convert PDF to images
        images = convert_from_bytes(pdf_bytes)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img, lang='eng') + "\n"
        # Simple regex-based extraction (customize as needed)
        vendor_name = re.search(r"Vendor Name[:\s]*(.*)", text)
        vendor_address = re.search(r"Vendor Address[:\s]*(.*)", text)
        customer_name = re.search(r"Customer Name[:\s]*(.*)", text)
        customer_address = re.search(r"Customer Address[:\s]*(.*)", text)
        invoice_id = re.search(r"Invoice ID[:\s]*(.*)", text)
        invoice_date = re.search(r"Invoice Date[:\s]*(.*)", text)
        invoice_total = re.search(r"Invoice Total[:\s$]*(.*)", text)
        # Dummy item extraction (customize for your format)
        items = []
        item_lines = re.findall(r"(\w+\s+\d+\s+\$\d+)", text)
        for line in item_lines:
            parts = line.split()
            if len(parts) >= 3:
                items.append(InvoiceItem(description=parts[0], quantity=parts[1], price=parts[2]))
        return InvoiceData(
            vendor_name=vendor_name.group(1).strip() if vendor_name else None,
            vendor_address=vendor_address.group(1).strip() if vendor_address else None,
            customer_name=customer_name.group(1).strip() if customer_name else None,
            customer_address=customer_address.group(1).strip() if customer_address else None,
            invoice_id=invoice_id.group(1).strip() if invoice_id else None,
            invoice_date=invoice_date.group(1).strip() if invoice_date else None,
            invoice_total=invoice_total.group(1).strip() if invoice_total else None,
            items=items
        ) 