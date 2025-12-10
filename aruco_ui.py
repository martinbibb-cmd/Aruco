#!/usr/bin/env python3
"""
ArUco Marker Generator - Simple UI
A standalone GUI application to create and print ArUco markers.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import sys

# Import the core functions from generate_aruco
from generate_aruco import generate_aruco_marker, generate_print_layout


class ArucoMarkerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ArUco Marker Generator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Current marker image
        self.current_marker = None
        self.current_image = None
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ArUco Marker Generator", 
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # ===== Settings Frame =====
        settings_frame = ttk.LabelFrame(main_frame, text="Marker Settings", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Marker ID
        ttk.Label(settings_frame, text="Marker ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.marker_id_var = tk.IntVar(value=0)
        self.marker_id_spin = ttk.Spinbox(settings_frame, from_=0, to=999, 
                                          textvariable=self.marker_id_var, width=10)
        self.marker_id_spin.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Dictionary selection
        ttk.Label(settings_frame, text="Dictionary:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dict_var = tk.StringVar(value='DICT_4X4_50')
        dict_options = ['DICT_4X4_50', 'DICT_4X4_100', 'DICT_4X4_250', 'DICT_4X4_1000',
                       'DICT_5X5_50', 'DICT_5X5_100', 'DICT_5X5_250', 'DICT_5X5_1000',
                       'DICT_6X6_50', 'DICT_6X6_100', 'DICT_6X6_250', 'DICT_6X6_1000',
                       'DICT_7X7_50', 'DICT_7X7_100', 'DICT_7X7_250', 'DICT_7X7_1000']
        dict_combo = ttk.Combobox(settings_frame, textvariable=self.dict_var, 
                                 values=dict_options, state='readonly', width=20)
        dict_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Marker size
        ttk.Label(settings_frame, text="Marker Size (px):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.size_var = tk.IntVar(value=200)
        size_spin = ttk.Spinbox(settings_frame, from_=50, to=1000, increment=50,
                               textvariable=self.size_var, width=10)
        size_spin.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # ===== Print Layout Frame =====
        layout_frame = ttk.LabelFrame(main_frame, text="Print Layout Options", padding="10")
        layout_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        layout_frame.columnconfigure(1, weight=1)
        
        # Layout type
        ttk.Label(layout_frame, text="Layout Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.layout_var = tk.StringVar(value='single')
        layout_options = ['single', 'creditcard', 'a5', 'a4']
        layout_combo = ttk.Combobox(layout_frame, textvariable=self.layout_var,
                                    values=layout_options, state='readonly', width=20)
        layout_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        layout_combo.bind('<<ComboboxSelected>>', self.on_layout_change)
        
        # Number of markers (for print layouts)
        ttk.Label(layout_frame, text="Count:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.count_var = tk.IntVar(value=1)
        self.count_spin = ttk.Spinbox(layout_frame, from_=1, to=9,
                                     textvariable=self.count_var, width=10, state='disabled')
        self.count_spin.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # DPI setting
        ttk.Label(layout_frame, text="DPI:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dpi_var = tk.IntVar(value=300)
        dpi_spin = ttk.Spinbox(layout_frame, from_=150, to=600, increment=50,
                              textvariable=self.dpi_var, width=10)
        dpi_spin.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # ===== Action Buttons =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        generate_btn = ttk.Button(button_frame, text="Generate Marker", 
                                 command=self.generate_marker)
        generate_btn.grid(row=0, column=0, padx=5)
        
        save_btn = ttk.Button(button_frame, text="Save As...", 
                            command=self.save_marker)
        save_btn.grid(row=0, column=1, padx=5)
        
        print_btn = ttk.Button(button_frame, text="Print", 
                             command=self.print_marker)
        print_btn.grid(row=0, column=2, padx=5)
        
        # ===== Preview Frame =====
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(4, weight=1)
        
        # Canvas for displaying the marker
        self.canvas = tk.Canvas(preview_frame, bg='white', width=500, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready. Click 'Generate Marker' to create an ArUco marker.")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
    def on_layout_change(self, event=None):
        """Enable/disable count spinner based on layout type"""
        layout = self.layout_var.get()
        if layout == 'single':
            self.count_spin.config(state='disabled')
            self.count_var.set(1)
        elif layout == 'creditcard':
            self.count_spin.config(state='disabled')
            self.count_var.set(1)
        elif layout == 'a5':
            self.count_spin.config(state='normal')
            self.count_var.set(4)
        elif layout == 'a4':
            self.count_spin.config(state='normal')
            self.count_var.set(9)
    
    def generate_marker(self):
        """Generate the ArUco marker based on current settings"""
        try:
            marker_id = self.marker_id_var.get()
            dictionary = self.dict_var.get()
            size = self.size_var.get()
            layout_type = self.layout_var.get()
            
            if layout_type == 'single':
                # Generate single marker
                marker_img = generate_aruco_marker(marker_id, dictionary, size, None)
                # Convert from grayscale to RGB for PIL
                if len(marker_img.shape) == 2:
                    marker_img_rgb = cv2.cvtColor(marker_img, cv2.COLOR_GRAY2RGB)
                else:
                    marker_img_rgb = marker_img
                self.current_marker = Image.fromarray(marker_img_rgb)
                self.status_var.set(f"Generated marker ID {marker_id} ({dictionary})")
                
            else:
                # Generate print layout
                count = self.count_var.get()
                marker_ids = list(range(marker_id, marker_id + count))
                dpi = self.dpi_var.get()
                
                # Create temporary file for the layout
                temp_path = '/tmp/temp_aruco_layout.png'
                self.current_marker = generate_print_layout(
                    marker_ids=marker_ids,
                    dictionary_name=dictionary,
                    format_type=layout_type,
                    output_path=temp_path,
                    dpi=dpi,
                    margin_mm=10
                )
                self.status_var.set(f"Generated {layout_type.upper()} layout with {count} marker(s)")
            
            # Display the marker
            self.display_marker()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate marker: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
    
    def display_marker(self):
        """Display the generated marker on the canvas"""
        if self.current_marker is None:
            return
        
        # Get canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # If canvas not properly sized yet, use default
        if canvas_width <= 1:
            canvas_width = 500
        if canvas_height <= 1:
            canvas_height = 500
        
        # Calculate scaling to fit in canvas while maintaining aspect ratio
        marker_width, marker_height = self.current_marker.size
        scale_w = (canvas_width - 20) / marker_width
        scale_h = (canvas_height - 20) / marker_height
        scale = min(scale_w, scale_h, 1.0)  # Don't scale up, only down
        
        new_width = int(marker_width * scale)
        new_height = int(marker_height * scale)
        
        # Resize the marker for display
        display_marker = self.current_marker.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to PhotoImage
        self.current_image = ImageTk.PhotoImage(display_marker)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.current_image)
    
    def save_marker(self):
        """Save the generated marker to a file"""
        if self.current_marker is None:
            messagebox.showwarning("Warning", "Please generate a marker first.")
            return
        
        layout_type = self.layout_var.get()
        marker_id = self.marker_id_var.get()
        
        # Suggest a filename
        if layout_type == 'single':
            default_name = f'aruco_marker_{marker_id}.png'
        else:
            default_name = f'aruco_print_{layout_type}.png'
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=default_name
        )
        
        if file_path:
            try:
                self.current_marker.save(file_path)
                self.status_var.set(f"Saved to {file_path}")
                messagebox.showinfo("Success", f"Marker saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save marker: {str(e)}")
    
    def print_marker(self):
        """Print the generated marker"""
        if self.current_marker is None:
            messagebox.showwarning("Warning", "Please generate a marker first.")
            return
        
        try:
            # Save to temporary file
            temp_path = '/tmp/aruco_print_temp.png'
            self.current_marker.save(temp_path)
            
            # Try to open with default image viewer which usually has print option
            if sys.platform == 'win32':
                os.startfile(temp_path)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{temp_path}"')
            else:  # Linux
                os.system(f'xdg-open "{temp_path}"')
            
            self.status_var.set("Opened marker in default viewer. Use the viewer's print function.")
            messagebox.showinfo("Print", 
                              "The marker has been opened in your default image viewer.\n"
                              "Please use the viewer's print function to print the marker.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open print dialog: {str(e)}")


def main():
    """Main entry point for the UI application"""
    root = tk.Tk()
    app = ArucoMarkerUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
