import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)

    def chapter_title(self, file_path):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'File: %s' % file_path, 0, 1, 'C')

    def chapter_body(self, file_path):
        with open(file_path, 'r', errors='ignore') as f:
            txt = f.read()
        self.set_font('Arial', '', 12)
        # Replace non-Latin-1 characters with a placeholder
        txt = txt.encode('latin1', 'replace').decode('latin1')
        self.multi_cell(0, 10, txt)
        self.ln()

def create_pdf(root_dir, output_path, excluded_files=None, excluded_dirs=None):
    if excluded_files is None:
        excluded_files = []
    if excluded_dirs is None:
        excluded_dirs = []

    pdf = PDF()
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames if os.path.join(dirpath, d) not in excluded_dirs]
        
        for filename in filenames:
            if filename in excluded_files:
                continue  # Skip the files in the excluded list
            file_path = os.path.join(dirpath, filename)
            pdf.add_page()
            pdf.chapter_title(file_path)
            pdf.chapter_body(file_path)
    pdf.output(output_path, 'F')

# Usage:
excluded_files = []  # List of files to exclude
excluded_dirs = ['.git','.DS_Store']  # List of directories to exclude
create_pdf('<PUT FOLDER PATH HERE>', 'output.pdf', excluded_files, excluded_dirs)
