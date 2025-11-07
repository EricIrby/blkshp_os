# Invoice OCR Processing

## Overview

Invoice OCR Processing extracts data from invoice images using OCR (Optical Character Recognition) technology. Supports multiple OCR libraries including Tesseract, EasyOCR, and InvoiceNet (AI-powered).

## Purpose

- Extract text from invoice images
- Parse structured invoice data
- Automate invoice data entry
- Support multiple OCR technologies
- Enable invoice processing automation

## OCR Options

### Option 1: Tesseract OCR (Recommended)
- **Library**: `pytesseract` + `opencv-python`
- **License**: Apache 2.0
- **Features**: Free, offline, highly customizable
- **Integration**: Python method in Frappe

```python
import pytesseract
from PIL import Image
import cv2

def process_invoice_image(image_path):
    """Extract text from invoice image"""
    # Preprocess image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply OCR
    text = pytesseract.image_to_string(gray, config='--psm 6')
    
    # Parse structured data
    invoice_data = parse_invoice_text(text)
    
    return invoice_data
```

### Option 2: EasyOCR
- **Library**: `easyocr`
- **License**: Apache 2.0
- **Features**: Multi-language, better accuracy than Tesseract
- **Integration**: Python method

```python
import easyocr

def process_invoice_easyocr(image_path):
    """Extract text using EasyOCR"""
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    
    # Process results
    invoice_data = parse_ocr_results(results)
    return invoice_data
```

### Option 3: InvoiceNet (AI-Powered)
- **Library**: `deep` (InvoiceNet)
- **License**: MIT
- **Features**: Machine learning-based invoice parsing
- **Integration**: Train model on invoice dataset

```python
from deep import InvoiceNet

def process_invoice_ai(image_path):
    """Process invoice using InvoiceNet AI"""
    model = InvoiceNet()
    invoice_data = model.predict(image_path)
    return invoice_data
```

## Implementation Steps

### Step 1: Install OCR Libraries
1. Install Tesseract OCR
2. Install Python libraries (pytesseract, opencv-python)
3. Install EasyOCR (optional)
4. Install InvoiceNet (optional)

### Step 2: Implement OCR Processing
1. Create invoice processing function
2. Preprocess invoice images
3. Extract text using OCR
4. Parse structured data

### Step 3: Integrate with Invoice Processing
1. Process invoice images on upload
2. Extract invoice data
3. Populate invoice fields
4. Validate extracted data

## Dependencies

- **OCR Libraries**: Tesseract, EasyOCR, InvoiceNet
- **Image Processing**: OpenCV, PIL
- **Vendor Invoice DocType**: Invoice records

## Usage Examples

### Process Invoice Image
```
1. Upload invoice image
2. Process image with OCR
3. Extract invoice number, date, total
4. Extract line items
5. Populate invoice record
```

## Testing Checklist

- [ ] Process invoice images with Tesseract
- [ ] Process invoice images with EasyOCR
- [ ] Process invoice images with InvoiceNet
- [ ] Extract invoice header data
- [ ] Extract invoice line items
- [ ] Validate extracted data
- [ ] Handle OCR errors

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 6.1

