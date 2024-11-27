import os
import fitz  
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path

# Function to convert PDF to images with progress tracking and HD quality
def pdf_to_images(pdf_path, progress_var, progress_bar, zoom_factor=2.0):
    # Check if the file exists and is a PDF
    if not pdf_path.endswith(".pdf") or not os.path.isfile(pdf_path):
        messagebox.showerror("Error", "Invalid file or path. Please provide a valid PDF file.")
        return

    # Get the base name (without extension) for the folder
    pdf_name = Path(pdf_path).stem
    output_folder = os.path.join(os.getcwd(), pdf_name)

    # Create the folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        total_pages = len(pdf_document)
        
        for page_num in range(total_pages):
            # Get the page
            page = pdf_document.load_page(page_num)
            # Apply zoom factor to get a higher resolution image (HD quality)
            mat = fitz.Matrix(zoom_factor, zoom_factor)  # Zoom factor for higher quality
            pixmap = page.get_pixmap(matrix=mat)  # Render page with applied zoom
            # Save the image
            image_path = os.path.join(output_folder, f"page_{page_num + 1}.jpg")
            pixmap.save(image_path)

            # Update progress bar
            progress_var.set((page_num + 1) / total_pages * 100)
            progress_bar.update_idletasks()

        pdf_document.close()
        messagebox.showinfo("Success", f"PDF conversion completed successfully.\nImages saved to: {output_folder}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to open file dialog and select PDF
def select_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        # Reset progress before starting the conversion
        progress_var.set(0)
        progress_bar["value"] = 0
        # Call pdf_to_images function with progress tracking and HD quality
        pdf_to_images(pdf_path, progress_var, progress_bar)

# Main Tkinter window
root = tk.Tk()
root.title("PDF to Image Converter by: ARSLANR369")
root.geometry("400x250")

# Add a label
label = tk.Label(root, text="Select a PDF file to convert to images:", padx=10, pady=10)
label.pack()

# Add a button to select PDF
select_button = tk.Button(root, text="Select PDF", command=select_pdf, padx=10, pady=5)
select_button.pack()

# Add a Progressbar widget
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, length=300, variable=progress_var, maximum=100)
progress_bar.pack(pady=10)

# Add an exit button
exit_button = tk.Button(root, text="Exit", command=root.quit, padx=10, pady=5)
exit_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
