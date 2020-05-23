# vollmacht
produce pdf in python backend from simple bootstrap vue frontend and download to browser

Frontend in one file with bootstrap-vue (allthough vue isn't really used here... just for test puposes): calls
backend with GET, loading PDF with parameters filled in.

Backend using python with PyMuPDF (import name: fitz) to write parameters in PDF-form, and fastapi to 
collect parameters and return pdf-file.
