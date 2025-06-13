from pydantic import BaseModel
from typing import List, Optional

class InvoiceItem(BaseModel):
    description: str
    quantity: Optional[str] = None
    price: Optional[str] = None
    total: Optional[str] = None

class InvoiceData(BaseModel):
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    invoice_id: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_total: Optional[str] = None
    items: List[InvoiceItem] = [] 