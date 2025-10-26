"""
MetaFinder - Universal Metadata Extraction Tool
Extract metadata from ANY file type and save to .txt
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from pathlib import Path

# Import our modules
from utils.file_detection import detect_type, get_file_category
from utils.normalize import normalize_metadata
from utils.text_writer import save_metadata, generate_output_filename

from extractors import (
    image_extractor,
    audio_extractor,
    video_extractor,
    document_extractor,
    archive_extractor,
    generic_extractor
)


class MetaFinderApp:
    """Main application class for MetaFinder GUI."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MetaFinder - Universal Metadata Extractor")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Variables
        self.selected_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        # Create UI
        self.create_widgets()
        
        # Apply theme
        self.apply_theme()
    
    def create_widgets(self):
        """Create all UI widgets."""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔍 MetaFinder",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Extract metadata from ANY file type",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Main content frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # File selection section
        file_section = tk.LabelFrame(
            main_frame,
            text="1. Select Input File",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        file_section.pack(fill='x', pady=(0, 15))
        
        file_frame = tk.Frame(file_section)
        file_frame.pack(fill='x')
        
        self.file_entry = tk.Entry(
            file_frame,
            textvariable=self.selected_file,
            font=("Arial", 10),
            state='readonly'
        )
        self.file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            file_frame,
            text="📂 Browse",
            command=self.browse_file,
            font=("Arial", 10, "bold"),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            padx=20,
            pady=5
        )
        browse_btn.pack(side='left')
        
        # File info display
        self.info_label = tk.Label(
            file_section,
            text="",
            font=("Arial", 9),
            fg='#7f8c8d',
            anchor='w'
        )
        self.info_label.pack(fill='x', pady=(10, 0))
        
        # Output section
        output_section = tk.LabelFrame(
            main_frame,
            text="2. Output Location",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        output_section.pack(fill='x', pady=(0, 15))
        
        output_frame = tk.Frame(output_section)
        output_frame.pack(fill='x')
        
        self.output_entry = tk.Entry(
            output_frame,
            textvariable=self.output_file,
            font=("Arial", 10)
        )
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        output_browse_btn = tk.Button(
            output_frame,
            text="📁 Choose",
            command=self.browse_output,
            font=("Arial", 10, "bold"),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            padx=20,
            pady=5
        )
        output_browse_btn.pack(side='left')
        
        # Action buttons
        action_frame = tk.Frame(main_frame)
        action_frame.pack(fill='x', pady=(0, 15))
        
        self.extract_btn = tk.Button(
            action_frame,
            text="🚀 Extract Metadata",
            command=self.extract_metadata,
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            padx=30,
            pady=10,
            state='disabled'
        )
        self.extract_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(
            action_frame,
            text="🗑️ Clear",
            command=self.clear_all,
            font=("Arial", 10),
            bg='#e74c3c',
            fg='white',
            cursor='hand2',
            padx=20,
            pady=10
        )
        clear_btn.pack(side='left')
        
        # Progress section
        self.progress_frame = tk.Frame(main_frame)
        self.progress_frame.pack(fill='x', pady=(0, 15))
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Arial", 10),
            fg='#2c3e50'
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=400
        )
        
        # Preview section
        preview_section = tk.LabelFrame(
            main_frame,
            text="3. Metadata Preview",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        preview_section.pack(fill='both', expand=True)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_section,
            font=("Courier New", 9),
            wrap='word',
            state='disabled'
        )
        self.preview_text.pack(fill='both', expand=True)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to extract metadata",
            font=("Arial", 9),
            bg='#34495e',
            fg='white',
            anchor='w',
            padx=10
        )
        self.status_label.pack(fill='both')
    
    def apply_theme(self):
        """Apply consistent theme to widgets."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TProgressbar",
            troughcolor='#ecf0f1',
            background='#3498db',
            thickness=20
        )
    
    def browse_file(self):
        """Open file dialog to select input file."""
        file_path = filedialog.askopenfilename(
            title="Select a file to extract metadata",
            filetypes=[("All Files", "*.*")]
        )
        
        if file_path:
            self.selected_file.set(file_path)
            
            # Auto-generate output path
            output_path = generate_output_filename(file_path)
            self.output_file.set(output_path)
            
            # Display file info
            file_size = os.path.getsize(file_path)
            size_mb = file_size / (1024 * 1024)
            ext = os.path.splitext(file_path)[1]
            
            self.info_label.config(
                text=f"📄 {os.path.basename(file_path)} | "
                     f"Size: {size_mb:.2f} MB | "
                     f"Type: {ext if ext else 'No extension'}"
            )
            
            # Enable extract button
            self.extract_btn.config(state='normal')
            self.update_status("File selected. Ready to extract metadata.", "#27ae60")
    
    def browse_output(self):
        """Open file dialog to select output location."""
        file_path = filedialog.asksaveasfilename(
            title="Save metadata as",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.output_file.set(file_path)
    
    def extract_metadata(self):
        """Main extraction process."""
        input_path = self.selected_file.get()
        output_path = self.output_file.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please specify an output location")
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input file does not exist")
            return
        
        # Start progress
        self.show_progress("Analyzing file...")
        self.extract_btn.config(state='disabled')
        
        try:
            # Detect file type
            self.update_progress("Detecting file type...")
            mime_type = detect_type(input_path)
            category = get_file_category(mime_type)
            
            # Select appropriate extractor
            self.update_progress(f"Extracting metadata ({category})...")
            metadata = self.get_metadata(input_path, category)
            
            # Normalize to text
            self.update_progress("Formatting metadata...")
            text_content = normalize_metadata(metadata, input_path, mime_type)
            
            # Save to file
            self.update_progress("Saving to file...")
            success = save_metadata(text_content, output_path)
            
            if success:
                # Show preview
                self.preview_text.config(state='normal')
                self.preview_text.delete(1.0, tk.END)
                
                # Limit preview to first 5000 characters
                preview = text_content[:5000]
                if len(text_content) > 5000:
                    preview += "\n\n... (Preview truncated. Full content saved to file)"
                
                self.preview_text.insert(1.0, preview)
                self.preview_text.config(state='disabled')
                
                # Success message
                self.hide_progress()
                self.update_status(f"✅ Metadata extracted successfully! Saved to {output_path}", "#27ae60")
                
                # Ask to open file
                if messagebox.askyesno(
                    "Success",
                    f"Metadata extracted successfully!\n\n"
                    f"Output: {output_path}\n\n"
                    f"Do you want to open the file?"
                ):
                    self.open_file(output_path)
            else:
                raise Exception("Failed to write output file")
        
        except Exception as e:
            self.hide_progress()
            self.update_status(f"❌ Error: {str(e)}", "#e74c3c")
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
        
        finally:
            self.extract_btn.config(state='normal')
    
    def get_metadata(self, file_path, category):
        """Get metadata using appropriate extractor."""
        if category == 'image':
            return image_extractor.extract(file_path)
        elif category == 'audio':
            return audio_extractor.extract(file_path)
        elif category == 'video':
            return video_extractor.extract(file_path)
        elif category == 'document':
            return document_extractor.extract(file_path)
        elif category == 'archive':
            return archive_extractor.extract(file_path)
        else:
            return generic_extractor.extract(file_path)
    
    def show_progress(self, message):
        """Show progress bar with message."""
        self.progress_label.config(text=message)
        self.progress_bar.pack(pady=(5, 0))
        self.progress_bar.start(10)
        self.root.update()
    
    def update_progress(self, message):
        """Update progress message."""
        self.progress_label.config(text=message)
        self.root.update()
    
    def hide_progress(self):
        """Hide progress bar."""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")
    
    def update_status(self, message, color="#2c3e50"):
        """Update status bar message."""
        self.status_label.config(text=message, fg=color if color != "#2c3e50" else "white")
    
    def clear_all(self):
        """Clear all inputs and outputs."""
        self.selected_file.set("")
        self.output_file.set("")
        self.info_label.config(text="")
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.config(state='disabled')
        self.extract_btn.config(state='disabled')
        self.update_status("Cleared. Ready to extract metadata.", "#2c3e50")
    
    def open_file(self, file_path):
        """Open file with default application."""
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":  # macOS
                os.system(f"open '{file_path}'")
            else:  # Linux
                os.system(f"xdg-open '{file_path}'")
        except Exception as e:
            print(f"Could not open file: {e}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = MetaFinderApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
