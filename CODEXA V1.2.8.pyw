#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA - QR Codes em Série (Tron Neon Inverted / Custom Light Selected / In-App Terminal)
Desenvolvido com CustomTkinter para interface moderna
Autor: Breno_Santos
Versão: 1.2.8
"""

import customtkinter as ctk
import qrcode
from PIL import Image, ImageDraw
import os
import pandas as pd
from tkinter import filedialog, messagebox
import threading
from datetime import datetime
import json
from pathlib import Path
import re

# Definição do tema TRON_NEON_THEME (Inverted Hover/Selected)
# pip install customtkinter qrcode[pil] Pillow pandas openpyxl
TRON_NEON_THEME = {
  "CTk": {
    "fg_color": ["#EAEAEA", "#1E1E1E"] # Light: Light Gray, Dark: Darkest Gray
  },
  "CTkToplevel": {
    "fg_color": ["#EAEAEA", "#1E1E1E"] # Terminal também usará isso
  },
  "CTkFrame": { # Sidebar and Main Content Area Frame
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ["#DCDCDC", "#2C2C2C"], # Light: Medium Light Gray, Dark: Darker Gray
    "top_fg_color": ["#C8C8C8", "#252525"],
    "border_color": ["#B0B0B0", "#007080"] # Light: Gray Border, Dark: Darker Cyan Border
  },
  "CTkButton": {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ["#00D1D1", "#00D1D1"],         # Base color (Bright Cyan for Tron)
    "selected_fg_color": ["#00c6c7", "#00A0A0"],# Light Mode (Sidebar Selected): Custom Cyan, Dark Mode (Sidebar Selected): Darker Cyan
    "hover_color": ["#00A0A0", "#00A0A0"],      # Hover color (Darker Cyan for Tron)
    "text_color": ["#001010", "#001010"],       # Dark text for high contrast on cyan (consistent)
    "text_color_disabled": ["#007080", "#007080"],
    "fg_color_disabled": ["#A0E0E8", "#00404A"],
    "grayscale_fg_color_light": "#C8C8C8",      # For non-Tron content buttons in light mode
    "grayscale_hover_color_light": "#BDBDBD",
    "grayscale_text_color_light": "#333333"
  },
  "CTkLabel": {
    "corner_radius": 0,
    "fg_color": "transparent",
    "text_color": ["#424242", "#00D1D1"] # Light: Dark Gray, Dark: Bright Cyan
  },
  "CTkEntry": {
    "corner_radius": 6,
    "border_width": 1,
    "fg_color": ["#FFFFFF", "#3A3A3A"], # Dark: Input BG slightly lighter than frame
    "border_color": ["#B0B0B0", "#00D1D1"], # Light: Gray, Dark: Bright Cyan
    "text_color": ["#333333", "#E0E0E0"],
    "placeholder_text_color": ["#9E9E9E", "#00A0A0"]
  },
  "CTkCheckBox": { # General CheckBox style
    "corner_radius": 6,
    "border_width": 2,
    "fg_color": ["#757575", "#00D1D1"],   # Checkmark/selected radio color
    "border_color": ["#BDBDBD", "#00A0A0"], # Box/circle border
    "hover_color": ["#8A8A8A", "#00A0A0"], # Hover for interactive part (darker for Tron)
    "checkmark_color": ["#FFFFFF", "#001010"],
    "text_color": ["#424242", "#00D1D1"], # Text next to checkbox
    "text_color_disabled": ["#BDBDBD", "#007080"]
  },
  "CTkSwitch": {
    "corner_radius": 1000,
    "border_width": 2,
    "button_length": 0,
    "fg_color": ["#D0D0D0", "#505050"],     # Track when off
    "progress_color": ["#00c6c7", "#00D1D1"], # Light mode switch ON uses the new selected cyan
    "button_color": ["#BDBDBD", "#A0D8E0"],   # Switch button/knob
    "button_hover_color": ["#ADADAD", "#00A0A0"], # Darker Cyan for hover
    "text_color": ["#424242", "#00D1D1"],     # Text "Modo Escuro" (Bright Cyan for Dark)
    "text_color_disabled": ["#BDBDBD", "#007080"]
  },
  "CTkRadioButton": {
    "corner_radius": 1000,
    "border_width_checked": 6,
    "border_width_unchecked": 2,
    "fg_color": ["#757575", "#00D1D1"],
    "border_color": ["#BDBDBD", "#00A0A0"],
    "hover_color": ["#8A8A8A", "#00A0A0"],
    "text_color": ["#424242", "#00D1D1"],
    "text_color_disabled": ["#BDBDBD", "#007080"]
  },
  "CTkProgressBar": {
    "corner_radius": 1000,
    "border_width": 0,
    "fg_color": ["#D0D0D0", "#505050"],
    "progress_color": ["#757575", "#00D1D1"], # Bright Cyan for Dark
    "border_color": ["#B0B0B0", "#007080"]
  },
  "CTkSlider": {
    "corner_radius": 1000,
    "button_corner_radius": 1000,
    "border_width": 3,
    "button_length": 0,
    "fg_color": ["#D0D0D0", "#505050"],
    "progress_color": ["#757575", "#00D1D1"], # Bright Cyan for Dark
    "button_color": ["#757575", "#00D1D1"],   # Bright Cyan for Dark
    "button_hover_color": ["#8A8A8A", "#00A0A0"] # Darker Cyan for hover
  },
  "CTkOptionMenu": { # For content area OptionMenus
    "corner_radius": 6,
    "fg_color": ["#C8C8C8", "#00D1D1"],   # Light: Gray, Dark: Bright Cyan
    "button_color": ["#BDBDBD", "#00A0A0"], # Light: Darker Gray, Dark: Darker Cyan (arrow)
    "button_hover_color": ["#ADADAD", "#007080"],# Light: Even Darker Gray, Dark: Darkest Cyan (arrow hover)
    "text_color": ["#333333", "#001010"],   # Light: Dark Gray Text, Dark: Darkest text on cyan
    "text_color_disabled": ["#9E9E9E", "#007080"]
  },
  "CTkComboBox": { # For content area ComboBoxes
    "corner_radius": 6,
    "border_width": 1,
    "fg_color": ["#FFFFFF", "#3A3A3A"],
    "border_color": ["#B0B0B0", "#00D1D1"],
    "button_color": ["#C8C8C8", "#00D1D1"],
    "button_hover_color": ["#BDBDBD", "#00A0A0"],
    "text_color": ["#333333", "#E0E0E0"],
    "text_color_disabled": ["#9E9E9E", "#007080"]
  },
  "CTkScrollbar": {
    "corner_radius": 1000,
    "border_spacing": 4,
    "fg_color": "transparent",
    "button_color": ["#BDBDBD", "#505050"],
    "button_hover_color": ["#ADADAD", "#00A0A0"]
  },
  "CTkSegmentedButton": {
    "corner_radius": 6,
    "border_width": 1,
    "fg_color": ["#DCDCDC", "#3A3A3A"],
    "selected_color": ["#00c6c7", "#00D1D1"], # Light mode selected uses new cyan
    "selected_hover_color": ["#00A0A0", "#00A0A0"], # Darker cyan for hover on selected
    "unselected_color": ["#DCDCDC", "#3A3A3A"],
    "unselected_hover_color": ["#C8C8C8", "#4F4F4F"],
    "text_color": ["#001010", "#001010"], # Dark text on selected segment
    "text_color_disabled": ["#BDBDBD", "#007080"]
  },
  "CTkTextbox": { # General Textbox, Terminal Textbox will be styled specifically if needed
    "corner_radius": 6,
    "border_width": 1,
    "fg_color": ["#FFFFFF", "#2C2C2C"], # Dark mode: same as frame for seamless look
    "border_color": ["#B0B0B0", "#00D1D1"],
    "text_color": ["#333333", "#E0E0E0"],
    "scrollbar_button_color": ["#BDBDBD", "#505050"],
    "scrollbar_button_hover_color": ["#ADADAD", "#00A0A0"]
  },
  "DropdownMenu": {
    "fg_color": ["#E0E0E0", "#3A3A3A"],
    "hover_color": ["#00c6c7", "#00A0A0"], # Light mode hover uses new cyan
    "text_color": ["#333333", "#E0E0E0"]
  }
}

ctk.set_appearance_mode("dark")

class QRAutoGen:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CODEXA – Automação em QR Codes")
        self.root.geometry("900x650")
        self.root.configure(fg_color=TRON_NEON_THEME["CTk"]["fg_color"])

        self.version = "1.2.8 - Edição Definitiva"
        self.current_mode = "único"
        self.logo_path = None
        self.csv_path = None
        self.base_output_dir_unico = Path.home()
        self.base_output_dir_macro = Path.home()
        self.subfolder_unico_name = "QR_Codes_Unicos"
        self.subfolder_macro_name = "QR_Codes_Lotes"
        self.image_size_var = ctk.StringVar(value="1083")
        self.fixed_qr_box_size = 20
        self.fixed_logo_ratio = 0.28
        self.image_format = "PNG"
        self.appearance_mode_var = ctk.StringVar(value=ctk.get_appearance_mode().lower())

        self.terminal_window = None
        self.terminal_log_area = None
        self.terminal_input = None
        self.terminal_visible = False

        self.setup_ui()
        self._apply_widget_colors()
        self.changelog = self.load_changelog()
        self.log_message("Aplicação iniciada.", startup=True)

        self.root.bind("<Control-KeyPress-t>", self.toggle_terminal_visibility)
        self.root.bind("<Control-KeyPress-T>", self.toggle_terminal_visibility)


    def log_message(self, message, level="INFO", startup=False):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] [{level}] {message}"
        
        print(formatted_message) 

        if self.terminal_log_area and self.terminal_log_area.winfo_exists():
            self.terminal_log_area.configure(state="normal")
            if not startup and self.terminal_log_area.index("end-1c") != "1.0":
                 self.terminal_log_area.insert("end", "\n")
            self.terminal_log_area.insert("end", formatted_message)
            self.terminal_log_area.configure(state="disabled") 
            self.terminal_log_area.see("end") 
        elif not startup: 
            print(f"[{timestamp}] [DEBUG] Terminal UI (widget) não disponível para: {message}")


    def setup_terminal_ui(self):
        if self.terminal_window and self.terminal_window.winfo_exists():
            self.terminal_window.deiconify()
            self.terminal_window.lift()
            self.terminal_window.focus_set()
            if self.terminal_input: self.terminal_input.focus_set()
            return

        self.terminal_window = ctk.CTkToplevel(self.root)
        self.terminal_window.title("Console de Log - CODEXA")
        self.terminal_window.geometry("800x400")
        self.terminal_window.attributes("-topmost", False) 
        
        self.terminal_window.configure(fg_color=TRON_NEON_THEME["CTkToplevel"]["fg_color"])
        
        term_main_frame = ctk.CTkFrame(self.terminal_window, fg_color="transparent")
        term_main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        term_main_frame.grid_rowconfigure(0, weight=1)
        term_main_frame.grid_columnconfigure(0, weight=1)

        self.terminal_log_area = ctk.CTkTextbox(
            term_main_frame,
            wrap="word",
            state="disabled", 
            font=("Consolas", 11) if os.name == 'nt' else ("Monospace", 11), 
            fg_color=["#FFFFFF", "#1A1A1A"], 
            text_color=["#1A1A1A", "#00D1D1"], 
            border_color=["#B0B0B0", "#00A0A0"],
            border_width=1
        )
        self.terminal_log_area.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(0,5))

        input_frame = ctk.CTkFrame(term_main_frame, fg_color="transparent")
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,0))
        input_frame.grid_columnconfigure(0, weight=1)

        self.terminal_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite 'clear' para limpar...",
            font=("Consolas", 11) if os.name == 'nt' else ("Monospace", 11),
            fg_color=TRON_NEON_THEME["CTkEntry"]["fg_color"],
            text_color=TRON_NEON_THEME["CTkEntry"]["text_color"],
            border_color=TRON_NEON_THEME["CTkEntry"]["border_color"],
            placeholder_text_color=TRON_NEON_THEME["CTkEntry"]["placeholder_text_color"]
        )
        self.terminal_input.grid(row=0, column=0, sticky="ew", padx=(0,5))
        self.terminal_input.bind("<Return>", self.process_terminal_command)

        copy_button = ctk.CTkButton(
            input_frame, text="Copiar Logs", command=self.copy_terminal_logs, width=120,
            fg_color=TRON_NEON_THEME["CTkButton"]["fg_color"],
            hover_color=TRON_NEON_THEME["CTkButton"]["hover_color"],
            text_color=TRON_NEON_THEME["CTkButton"]["text_color"]
        )
        copy_button.grid(row=0, column=1, padx=(5,0))
        
        self.terminal_window.protocol("WM_DELETE_WINDOW", self.hide_terminal)
        self.log_message("Terminal UI inicializado.")
        if self.terminal_input: self.terminal_input.focus_set()


    def toggle_terminal_visibility(self, event=None):
        if not self.terminal_visible or not self.terminal_window or not self.terminal_window.winfo_exists():
            self.setup_terminal_ui() 
            self.terminal_window.deiconify()
            self.terminal_window.lift()
            self.terminal_visible = True
            if self.terminal_input: self.terminal_input.focus_set()
        else:
            self.hide_terminal()
        return "break" 

    def hide_terminal(self):
        if self.terminal_window and self.terminal_window.winfo_exists():
            self.terminal_window.withdraw()
        self.terminal_visible = False
        self.log_message("Terminal fechado/ocultado.")


    def process_terminal_command(self, event=None):
        if not self.terminal_input or not self.terminal_log_area: return
        command = self.terminal_input.get().strip().lower()
        self.log_message(f"Comando recebido: '{command}'", level="CMD")
        self.terminal_input.delete(0, "end")

        if command == "clear":
            self.clear_terminal_logs()
        elif command == "exit":
            self.hide_terminal()
        else:
            self.log_message(f"Comando desconhecido: '{command}'", level="WARN")
        return "break"

    def clear_terminal_logs(self):
        if self.terminal_log_area and self.terminal_log_area.winfo_exists():
            self.terminal_log_area.configure(state="normal")
            self.terminal_log_area.delete("1.0", "end")
            self.terminal_log_area.configure(state="disabled")
            self.log_message("Logs do terminal limpos.", level="CMD")

    def copy_terminal_logs(self):
        if self.terminal_log_area and self.terminal_log_area.winfo_exists():
            logs = self.terminal_log_area.get("1.0", "end-1c") 
            self.root.clipboard_clear()
            self.root.clipboard_append(logs)
            self.log_message("Logs copiados para a área de transferência.", level="CMD")
            messagebox.showinfo("Logs Copiados", "O conteúdo do terminal foi copiado!", parent=self.terminal_window if self.terminal_window and self.terminal_window.winfo_exists() else self.root)

    def _apply_widget_colors(self):
        current_theme = TRON_NEON_THEME
        self.root.configure(fg_color=current_theme["CTk"]["fg_color"])
        self.sidebar_frame.configure(fg_color=current_theme["CTkFrame"]["fg_color"])
        self.menu_title.configure(text_color=current_theme["CTkLabel"]["text_color"])

        sidebar_button_attrs = {
            "fg_color": current_theme["CTkButton"]["fg_color"], 
            "hover_color": current_theme["CTkButton"]["hover_color"],
            "text_color": current_theme["CTkButton"]["text_color"],
            "corner_radius": current_theme["CTkButton"]["corner_radius"]
        }
        self.btn_modo_unico.configure(**sidebar_button_attrs)
        self.btn_modo_macro.configure(**sidebar_button_attrs)
        self.btn_updates.configure(**sidebar_button_attrs)
        self.btn_sobre.configure(**sidebar_button_attrs)
        
        self.appearance_mode_switch.configure(
            fg_color=current_theme["CTkSwitch"]["fg_color"],
            progress_color=current_theme["CTkSwitch"]["progress_color"],
            button_color=current_theme["CTkSwitch"]["button_color"],
            button_hover_color=current_theme["CTkSwitch"]["button_hover_color"],
            text_color=current_theme["CTkSwitch"]["text_color"]
        )
        self.version_label.configure(text_color=current_theme["CTkLabel"]["text_color"])
        self.main_container.configure(fg_color=current_theme["CTkFrame"]["fg_color"])

        self._reconfigure_modo_unico_frame_colors()
        self._reconfigure_modo_macro_frame_colors()
        self.switch_mode(self.current_mode) 


    def _reconfigure_options_widgets_colors(self, options_frame, mode_suffix):
        current_theme = TRON_NEON_THEME
        current_mode_str = ctk.get_appearance_mode().lower()
        options_frame.configure(fg_color=current_theme["CTkFrame"]["fg_color"])
        
        if current_mode_str == "light":
            btn_fg = current_theme["CTkButton"]["grayscale_fg_color_light"]
            btn_hover = current_theme["CTkButton"]["grayscale_hover_color_light"]
            btn_text = current_theme["CTkButton"]["grayscale_text_color_light"]
            opt_menu_fg = "#C8C8C8" 
            opt_menu_btn = "#BDBDBD"
            opt_menu_btn_hover = "#ADADAD"
            opt_menu_text = "#333333"
        else: 
            btn_fg = current_theme["CTkButton"]["fg_color"] 
            btn_hover = current_theme["CTkButton"]["hover_color"]
            btn_text = current_theme["CTkButton"]["text_color"]
            opt_menu_fg = current_theme["CTkOptionMenu"]["fg_color"]
            opt_menu_btn = current_theme["CTkOptionMenu"]["button_color"]
            opt_menu_btn_hover = current_theme["CTkOptionMenu"]["button_hover_color"]
            opt_menu_text = current_theme["CTkOptionMenu"]["text_color"]

        for widget in options_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=current_theme["CTkLabel"]["text_color"])
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=btn_fg, hover_color=btn_hover, text_color=btn_text, corner_radius=current_theme["CTkButton"]["corner_radius"])
            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.configure(
                    fg_color=opt_menu_fg, button_color=opt_menu_btn,
                    button_hover_color=opt_menu_btn_hover, text_color=opt_menu_text,
                    corner_radius=current_theme["CTkOptionMenu"]["corner_radius"]
                )
            elif isinstance(widget, ctk.CTkEntry):
                widget.configure(
                    fg_color=current_theme["CTkEntry"]["fg_color"],
                    border_color=current_theme["CTkEntry"]["border_color"],
                    text_color=current_theme["CTkEntry"]["text_color"]
                )
        getattr(self, f"logo_label{mode_suffix}").configure(text_color=current_theme["CTkLabel"]["text_color"])
        getattr(self, f"dir_label{mode_suffix}").configure(text_color=current_theme["CTkLabel"]["text_color"])

    def _reconfigure_modo_unico_frame_colors(self):
        current_theme = TRON_NEON_THEME
        current_mode_str = ctk.get_appearance_mode().lower()
        self.frame_unico.configure(fg_color=current_theme["CTkFrame"]["fg_color"])
        
        for child in self.frame_unico.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                child.configure(text_color=current_theme["CTkLabel"]["text_color"])
            elif isinstance(child, ctk.CTkFrame) and child != self.options_frame_unico : 
                child.configure(fg_color=current_theme["CTkFrame"]["fg_color"])


        entry_attrs = {
            "fg_color": current_theme["CTkEntry"]["fg_color"],
            "border_color": current_theme["CTkEntry"]["border_color"],
            "text_color": current_theme["CTkEntry"]["text_color"],
            "placeholder_text_color": current_theme["CTkEntry"]["placeholder_text_color"]
        }
        self.url_entry.configure(**entry_attrs)
        self.name_entry.configure(**entry_attrs)
        
        if current_mode_str == "light":
            action_btn_fg = current_theme["CTkButton"]["grayscale_fg_color_light"]
            action_btn_hover = current_theme["CTkButton"]["grayscale_hover_color_light"]
            action_btn_text = current_theme["CTkButton"]["grayscale_text_color_light"]
        else: 
            action_btn_fg = current_theme["CTkButton"]["fg_color"] 
            action_btn_hover = current_theme["CTkButton"]["hover_color"]
            action_btn_text = current_theme["CTkButton"]["text_color"]

        self.btn_generate_unico.configure(fg_color=action_btn_fg, hover_color=action_btn_hover, text_color=action_btn_text)
        self.btn_reset_unico.configure(fg_color=action_btn_fg, hover_color=action_btn_hover, text_color=action_btn_text)
        
        if hasattr(self, 'options_frame_unico'): 
            self._reconfigure_options_widgets_colors(self.options_frame_unico, "_unico")


    def _reconfigure_modo_macro_frame_colors(self):
        current_theme = TRON_NEON_THEME
        current_mode_str = ctk.get_appearance_mode().lower()
        self.frame_macro.configure(fg_color=current_theme["CTkFrame"]["fg_color"])

        for child in self.frame_macro.winfo_children():
            if isinstance(child, ctk.CTkLabel) and child not in [self.csv_label, self.progress_label]:
                child.configure(text_color=current_theme["CTkLabel"]["text_color"])
            elif isinstance(child, ctk.CTkFrame) and child != self.options_frame_macro and child != self.btn_select_csv.master : 
                 child.configure(fg_color=current_theme["CTkFrame"]["fg_color"])

        
        file_frame_macro = self.btn_select_csv.master
        file_frame_macro.configure(fg_color="transparent") 
        
        if current_mode_str == "light":
            content_btn_fg = current_theme["CTkButton"]["grayscale_fg_color_light"]
            content_btn_hover = current_theme["CTkButton"]["grayscale_hover_color_light"]
            content_btn_text = current_theme["CTkButton"]["grayscale_text_color_light"]
        else: 
            content_btn_fg = current_theme["CTkButton"]["fg_color"] 
            content_btn_hover = current_theme["CTkButton"]["hover_color"]
            content_btn_text = current_theme["CTkButton"]["text_color"]

        self.btn_select_csv.configure(fg_color=content_btn_fg, hover_color=content_btn_hover, text_color=content_btn_text)
        self.csv_label.configure(text_color=current_theme["CTkLabel"]["text_color"])
        
        self.prefix_entry.configure(
            fg_color=current_theme["CTkEntry"]["fg_color"],
            border_color=current_theme["CTkEntry"]["border_color"],
            text_color=current_theme["CTkEntry"]["text_color"],
            placeholder_text_color=current_theme["CTkEntry"]["placeholder_text_color"]
        )
        
        self.progress_bar.configure(
            fg_color=current_theme["CTkProgressBar"]["fg_color"],
            progress_color=current_theme["CTkProgressBar"]["progress_color"]
        )
        self.progress_label.configure(text_color=current_theme["CTkLabel"]["text_color"])
        
        self.btn_generate_macro.configure(fg_color=content_btn_fg, hover_color=content_btn_hover, text_color=content_btn_text)
        self.btn_reset_macro.configure(fg_color=content_btn_fg, hover_color=content_btn_hover, text_color=content_btn_text)

        if hasattr(self, 'options_frame_macro'): 
            self._reconfigure_options_widgets_colors(self.options_frame_macro, "_macro")

    def setup_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) 

        self.menu_title = ctk.CTkLabel(self.sidebar_frame, text="Opções", font=ctk.CTkFont(size=20, weight="bold"))
        self.menu_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

        self.btn_modo_unico = ctk.CTkButton(self.sidebar_frame, text="Modo Único", command=lambda: self.switch_mode("único"), font=ctk.CTkFont(size=14))
        self.btn_modo_unico.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        self.btn_modo_macro = ctk.CTkButton(self.sidebar_frame, text="Modo Macro", command=lambda: self.switch_mode("macro"), font=ctk.CTkFont(size=14))
        self.btn_modo_macro.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        self.btn_updates = ctk.CTkButton(self.sidebar_frame, text="Atualizações", command=self.show_changelog, font=ctk.CTkFont(size=14))
        self.btn_updates.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="n") 

        self.btn_sobre = ctk.CTkButton(self.sidebar_frame, text="Sobre", command=self.show_sobre_window, font=ctk.CTkFont(size=14))
        self.btn_sobre.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="n") 

        def toggle_appearance_mode():
            new_mode = self.appearance_mode_var.get()
            ctk.set_appearance_mode(new_mode)
            self.log_message(f"Modo de aparência alterado para: {new_mode}")
            self._apply_widget_colors() 
            if new_mode == "dark":
                self.appearance_mode_switch.configure(text="Modo Dark")
            else:
                self.appearance_mode_switch.configure(text="Modo Light")

        self.appearance_mode_switch = ctk.CTkSwitch(self.sidebar_frame,
                                                    text="Modo Dark" if self.appearance_mode_var.get() == "dark" else "Modo Light",
                                                    command=toggle_appearance_mode,
                                                    variable=self.appearance_mode_var,
                                                    onvalue="dark", offvalue="light",
                                                    font=ctk.CTkFont(size=12))
        self.appearance_mode_switch.grid(row=5, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="s") 

        self.version_label = ctk.CTkLabel(self.sidebar_frame, text=f"Versão {self.version}", font=ctk.CTkFont(size=12))
        self.version_label.grid(row=6, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="s") 

        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.create_modo_unico_frame()
        self.create_modo_macro_frame()

    def _create_options_widgets(self, parent_frame, mode_suffix):
        options_frame = ctk.CTkFrame(parent_frame, fg_color="transparent") 
        options_frame.grid_columnconfigure(1, weight=0) 
        options_frame.grid_columnconfigure(2, weight=1) 
        row_idx = 0
        left_padding_for_labels = (15, 10) 
        
        logo_desc_label = ctk.CTkLabel(options_frame, text="Logo:", font=ctk.CTkFont(size=12))
        logo_desc_label.grid(row=row_idx, column=0, padx=left_padding_for_labels, pady=10, sticky="w")
        btn_logo = ctk.CTkButton(options_frame, text="Selecionar Logo", command=self.select_logo, width=150)
        btn_logo.grid(row=row_idx, column=1, padx=0, pady=10, sticky="w")
        logo_status_label = ctk.CTkLabel(options_frame, text="Nenhuma logo selecionada", font=ctk.CTkFont(size=12))
        logo_status_label.grid(row=row_idx, column=2, padx=10, pady=10, sticky="w")
        setattr(self, f"logo_label{mode_suffix}", logo_status_label)
        row_idx += 1

        format_desc_label = ctk.CTkLabel(options_frame, text="Formato de saída:", font=ctk.CTkFont(size=12))
        format_desc_label.grid(row=row_idx, column=0, padx=left_padding_for_labels, pady=10, sticky="w")
        format_var = ctk.StringVar(value="PNG")
        format_dropdown = ctk.CTkOptionMenu(options_frame, values=["PNG", "JPEG", "JPG"], variable=format_var,
                                            command=self.update_format_selection, width=150)
        format_dropdown.grid(row=row_idx, column=1, padx=0, pady=10, sticky="w")
        setattr(self, f"format_var{mode_suffix}", format_var)
        row_idx += 1

        dir_desc_label = ctk.CTkLabel(options_frame, text="Diretório de Saída:", font=ctk.CTkFont(size=12))
        dir_desc_label.grid(row=row_idx, column=0, padx=left_padding_for_labels, pady=10, sticky="w")
        btn_dir = ctk.CTkButton(options_frame, text="Selecionar Diretório",
                                command=lambda m=mode_suffix.strip('_'): self.select_output_dir(m), width=150)
        btn_dir.grid(row=row_idx, column=1, padx=0, pady=10, sticky="w")
        initial_dir_text = str(getattr(self, f"base_output_dir{mode_suffix}") / getattr(self, f"subfolder{mode_suffix}_name"))
        dir_status_label = ctk.CTkLabel(options_frame, text=initial_dir_text, font=ctk.CTkFont(size=12), wraplength=300) 
        dir_status_label.grid(row=row_idx, column=2, padx=10, pady=10, sticky="w")
        setattr(self, f"dir_label{mode_suffix}", dir_status_label)
        row_idx += 1

        img_size_desc_label = ctk.CTkLabel(options_frame, text="Tamanho Imagem (px):", font=ctk.CTkFont(size=12))
        img_size_desc_label.grid(row=row_idx, column=0, padx=left_padding_for_labels, pady=10, sticky="w")
        img_size_entry = ctk.CTkEntry(options_frame, textvariable=self.image_size_var, width=150)
        img_size_entry.grid(row=row_idx, column=1, padx=0, pady=10, sticky="w")
        row_idx += 1
        return options_frame

    def create_modo_unico_frame(self):
        self.frame_unico = ctk.CTkFrame(self.main_container, fg_color="transparent") 
        self.frame_unico.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self.frame_unico, text="Criação de QR's Individuais", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        url_label = ctk.CTkLabel(self.frame_unico, text="URL/Link:", font=ctk.CTkFont(size=14))
        url_label.grid(row=1, column=0, sticky="w", padx=(50, 0), pady=(10, 5))
        self.url_entry = ctk.CTkEntry(self.frame_unico, placeholder_text="https://exemplo.com", width=500, height=40, font=ctk.CTkFont(size=13))
        self.url_entry.grid(row=2, column=0, columnspan=2, padx=50, pady=(0, 10), sticky="ew") 
        name_label = ctk.CTkLabel(self.frame_unico, text="Nome do arquivo:", font=ctk.CTkFont(size=14))
        name_label.grid(row=3, column=0, sticky="w", padx=(50, 0), pady=(10, 5))
        self.name_entry = ctk.CTkEntry(self.frame_unico, placeholder_text="Exemplo_qrcode", width=500, height=40, font=ctk.CTkFont(size=13))
        self.name_entry.grid(row=4, column=0, columnspan=2, padx=50, pady=(0, 10), sticky="ew") 
        
        self.options_frame_unico = self._create_options_widgets(self.frame_unico, "_unico")
        self.options_frame_unico.grid(row=5, column=0, columnspan=2, padx=50, pady=10, sticky="new")
        
        action_frame = ctk.CTkFrame(self.frame_unico, fg_color="transparent")
        action_frame.grid(row=6, column=0, columnspan=2, pady=(20, 20)) 
        self.btn_generate_unico = ctk.CTkButton(action_frame, text="Gerar QR", command=self.generate_single_qr, font=ctk.CTkFont(size=16, weight="bold"), width=150, height=40)
        self.btn_generate_unico.grid(row=0, column=0, padx=10)
        self.btn_reset_unico = ctk.CTkButton(action_frame, text="Redefinir", command=lambda: self.reset_form("único"), font=ctk.CTkFont(size=16), width=150, height=40)
        self.btn_reset_unico.grid(row=0, column=1, padx=10)

    def create_modo_macro_frame(self):
        self.frame_macro = ctk.CTkFrame(self.main_container, fg_color="transparent") 
        self.frame_macro.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self.frame_macro, text="QR Codes em Lotes Infinitos", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        file_frame = ctk.CTkFrame(self.frame_macro, fg_color="transparent") 
        file_frame.grid(row=1, column=0, columnspan=2, padx=50, pady=10, sticky="ew")
        file_frame.grid_columnconfigure(1, weight=1) 
        self.btn_select_csv = ctk.CTkButton(file_frame, text="Importar CSV/Excel", command=self.select_csv_file, width=150)
        self.btn_select_csv.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w") 
        self.csv_label = ctk.CTkLabel(file_frame, text="Nenhum arquivo selecionado", font=ctk.CTkFont(size=12), wraplength=300) 
        self.csv_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        prefix_label = ctk.CTkLabel(self.frame_macro, text="Prefixo para os arquivos:", font=ctk.CTkFont(size=14))
        prefix_label.grid(row=2, column=0, sticky="w", padx=(50, 0), pady=(10, 5))
        self.prefix_entry = ctk.CTkEntry(self.frame_macro, placeholder_text="Exemplo_qrcode - ", width=500, height=40, font=ctk.CTkFont(size=13))
        self.prefix_entry.grid(row=3, column=0, columnspan=2, padx=50, pady=(0, 10), sticky="ew") 
        
        self.options_frame_macro = self._create_options_widgets(self.frame_macro, "_macro")
        self.options_frame_macro.grid(row=4, column=0, columnspan=2, padx=50, pady=10, sticky="new")
        
        self.progress_bar = ctk.CTkProgressBar(self.frame_macro, width=600) 
        self.progress_bar.grid(row=5, column=0, columnspan=2, padx=50, pady=(10, 0), sticky="ew") 
        self.progress_bar.set(0)
        self.progress_label = ctk.CTkLabel(self.frame_macro, text="", font=ctk.CTkFont(size=12))
        self.progress_label.grid(row=6, column=0, columnspan=2, pady=(0, 10)) 
        
        action_frame_macro = ctk.CTkFrame(self.frame_macro, fg_color="transparent")
        action_frame_macro.grid(row=7, column=0, columnspan=2, pady=(10, 20)) 
        self.btn_generate_macro = ctk.CTkButton(action_frame_macro, text="Iniciar", command=self.generate_batch_qr, font=ctk.CTkFont(size=16, weight="bold"), width=150, height=40)
        self.btn_generate_macro.grid(row=0, column=0, padx=10)
        self.btn_reset_macro = ctk.CTkButton(action_frame_macro, text="Redefinir", command=lambda: self.reset_form("macro"), font=ctk.CTkFont(size=16), width=150, height=40)
        self.btn_reset_macro.grid(row=0, column=1, padx=10)

    def switch_mode(self, mode):
        current_theme = TRON_NEON_THEME
        current_mode_str = ctk.get_appearance_mode().lower()
        self.current_mode = mode
        self.log_message(f"Mudando para modo: {mode}")
        self.frame_unico.grid_forget()
        self.frame_macro.grid_forget()
        
        unselected_fg = current_theme["CTkButton"]["fg_color"] 
        
        if current_mode_str == "light":
            selected_fg_unico = current_theme["CTkButton"]["selected_fg_color"][0] if isinstance(current_theme["CTkButton"]["selected_fg_color"], list) else current_theme["CTkButton"]["selected_fg_color"]
            selected_fg_macro = selected_fg_unico 
        else: 
            selected_fg_unico = current_theme["CTkButton"]["selected_fg_color"][1] if isinstance(current_theme["CTkButton"]["selected_fg_color"], list) else current_theme["CTkButton"]["selected_fg_color"]
            selected_fg_macro = selected_fg_unico 

        button_text_color = current_theme["CTkButton"]["text_color"]


        if mode == "único":
            self.frame_unico.grid(row=0, column=0, sticky="nsew")
            self.btn_modo_unico.configure(fg_color=selected_fg_unico, text_color=button_text_color)
            self.btn_modo_macro.configure(fg_color=unselected_fg, text_color=button_text_color)
        else: 
            self.frame_macro.grid(row=0, column=0, sticky="nsew")
            self.btn_modo_macro.configure(fg_color=selected_fg_macro, text_color=button_text_color)
            self.btn_modo_unico.configure(fg_color=unselected_fg, text_color=button_text_color)
        self.log_message(f"Modo '{mode}' ativado.")

    def select_logo(self):
        self.log_message("Botão 'Selecionar Logo' clicado.")
        filename = filedialog.askopenfilename(title="Selecionar Logo", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos os arquivos", "*.*")])
        if filename:
            self.logo_path = filename
            logo_name = os.path.basename(filename)
            self.logo_label_unico.configure(text=f"{logo_name}")
            self.logo_label_macro.configure(text=f"{logo_name}")
            self.log_message(f"Logo selecionado: {filename}")
        else:
            self.log_message("Seleção de logo cancelada.")

    def select_csv_file(self):
        self.log_message("Botão 'Importar CSV/Excel' clicado.")
        filename = filedialog.askopenfilename(title="Selecionar arquivo CSV/Excel", filetypes=[("CSV/Excel", "*.csv *.xlsx *.xls"), ("Todos os arquivos", "*.*")])
        if filename:
            self.csv_path = filename
            self.csv_label.configure(text=f"{os.path.basename(filename)}")
            self.log_message(f"Arquivo CSV/Excel selecionado: {filename}")
        else:
            self.log_message("Seleção de arquivo CSV/Excel cancelada.")
            
    def update_format_selection(self, choice):
        self.image_format = choice 
        self.log_message(f"Formato de imagem padrão alterado para: {choice}")


    def select_output_dir(self, mode_str): 
        self.log_message(f"Selecionando diretório de saída para modo: {mode_str}")
        directory = filedialog.askdirectory(title="Selecionar diretório de saída base")
        if directory:
            base_dir_path = Path(directory)
            if mode_str == "unico":
                self.base_output_dir_unico = base_dir_path
                full_path_to_show = self.base_output_dir_unico / self.subfolder_unico_name
                self.dir_label_unico.configure(text=str(full_path_to_show))
            else: 
                self.base_output_dir_macro = base_dir_path
                full_path_to_show = self.base_output_dir_macro / self.subfolder_macro_name
                self.dir_label_macro.configure(text=str(full_path_to_show))
            self.log_message(f"Diretório de saída base ({mode_str}) alterado para: {directory}. Caminho exibido: {full_path_to_show}")
        else:
            self.log_message("Seleção de diretório de saída cancelada.")

    def _get_current_qr_configs(self):
        try:
            image_size = int(self.image_size_var.get())
            if image_size < 100 or image_size > 5000: 
                self.log_message(f"Tamanho da imagem inválido ({image_size}px), usando padrão 1083px.", level="WARN")
                raise ValueError("Tamanho da imagem fora dos limites (100-5000px)")
        except ValueError as e:
            messagebox.showwarning("Configuração Inválida", f"Tamanho da Imagem: {e}. Usando padrão 1083px.")
            image_size = 1083 
            self.image_size_var.set(str(image_size)) 
        
        qr_box_size = self.fixed_qr_box_size 
        logo_ratio = self.fixed_logo_ratio 
        self.log_message(f"Configurações QR: Tamanho Imagem={image_size}, Box Size={qr_box_size}, Logo Ratio={logo_ratio}", level="DEBUG")
        return image_size, qr_box_size, logo_ratio

    def create_qr_with_logo(self, data, logo_path=None, pre_processed_logo_img=None):
        image_size, qr_box_size, logo_ratio = self._get_current_qr_configs()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=qr_box_size, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        img = img.resize((image_size, image_size), Image.Resampling.LANCZOS)
        
        logo_to_paste = None
        actual_logo_width_for_paste = 0
        actual_logo_height_for_paste = 0

        if pre_processed_logo_img:
            logo_to_paste = pre_processed_logo_img['image']
            actual_logo_width_for_paste = pre_processed_logo_img['width']
            actual_logo_height_for_paste = pre_processed_logo_img['height']
        elif logo_path and os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                logo_target_width = int(image_size * logo_ratio)
                logo.thumbnail((logo_target_width, logo_target_width), Image.Resampling.LANCZOS)
                
                if logo.mode == 'RGBA': logo_to_paste = logo
                elif logo.mode == 'RGB': logo_to_paste = logo
                else: logo_to_paste = logo.convert('RGBA') 
                
                actual_logo_width_for_paste = logo_to_paste.width
                actual_logo_height_for_paste = logo_to_paste.height
            except Exception as e:
                self.log_message(f"Erro ao adicionar logo: {e}", level="WARN")
                self.root.after(0, lambda: messagebox.showwarning("Erro de Logo", f"Não foi possível adicionar a logo: {e}\nQR Code gerado sem logo."))
                logo_to_paste = None
        
        if logo_to_paste:
            pos_x = (image_size - actual_logo_width_for_paste) // 2
            pos_y = (image_size - actual_logo_height_for_paste) // 2
            if logo_to_paste.mode == 'RGBA':
                img.paste(logo_to_paste, (pos_x, pos_y), mask=logo_to_paste)
            else: 
                img.paste(logo_to_paste, (pos_x, pos_y))
        return img
    
    def sanitize_filename(self, name):
        name = re.sub(r'[<>:"/\\|?*]', '_', name) 
        name = re.sub(r'\s+', '_', name) 
        return name


    def generate_single_qr(self):
        self.log_message("Botão 'Gerar QR' (Modo Único) clicado.")
        url = self.url_entry.get().strip()
        name_input = self.name_entry.get().strip()
        
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL.")
            self.log_message("Erro: URL não inserida para QR único.", level="ERROR")
            return
            
        self.log_message(f"Gerando QR único para URL: {url}, Nome base: {name_input}")
        if not name_input:
            final_name = "qrcode_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            final_name = self.sanitize_filename(name_input)
            if final_name != name_input: 
                self.log_message(f"Nome do arquivo ajustado de '{name_input}' para '{final_name}'.")

        output_dir_final = self.base_output_dir_unico / self.subfolder_unico_name
        output_dir_final.mkdir(parents=True, exist_ok=True)

        try:
            qr_img = self.create_qr_with_logo(url, logo_path=self.logo_path)
            format_selected = self.format_var_unico.get() 
            extension = format_selected.lower()
            output_path = output_dir_final / f"{final_name}.{extension}"
            
            if format_selected in ["JPEG", "JPG"]:
                if qr_img.mode == 'RGBA': 
                    rgb_img = Image.new('RGB', qr_img.size, 'white')
                    mask = qr_img.split()[3] if len(qr_img.split()) == 4 else None 
                    rgb_img.paste(qr_img, (0,0), mask=mask) 
                    qr_img = rgb_img
                qr_img.save(str(output_path), format='JPEG', quality=95, optimize=True)
            else: 
                qr_img.save(str(output_path), format='PNG', optimize=True)
            
            messagebox.showinfo("Sucesso!!!", f"QR Code Gerado!\nSalvo em: {output_path}")
            self.log_message(f"QR Único gerado com sucesso: {output_path}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar QR Code: {str(e)}")
            self.log_message(f"Falha ao gerar QR Único: {str(e)}", level="ERROR")
            
    def generate_batch_qr(self):
        self.log_message("Botão 'Iniciar' (Modo Macro) clicado.")
        if not self.csv_path:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo CSV/Excel.")
            self.log_message("Erro: Arquivo CSV/Excel não selecionado para lote.", level="ERROR")
            return
        self.log_message(f"Iniciando geração em lote do arquivo: {self.csv_path}")
        output_dir_final = self.base_output_dir_macro / self.subfolder_macro_name
        output_dir_final.mkdir(parents=True, exist_ok=True)
            
        thread = threading.Thread(target=self._process_batch_qr, args=(output_dir_final,))
        thread.daemon = True 
        thread.start()
        
    def _process_batch_qr(self, final_output_directory):
        self.log_message(f"Thread de processamento em lote iniciada. Diretório de saída: {final_output_directory}")
        current_theme = TRON_NEON_THEME
        current_mode_str = ctk.get_appearance_mode().lower()
        
        processed_logo_data = None
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo_img_obj = Image.open(self.logo_path)
                image_size, _, logo_ratio = self._get_current_qr_configs() 
                logo_target_width = int(image_size * logo_ratio)
                logo_img_obj.thumbnail((logo_target_width, logo_target_width), Image.Resampling.LANCZOS)
                
                final_logo_to_cache = None
                if logo_img_obj.mode == 'RGBA': final_logo_to_cache = logo_img_obj
                elif logo_img_obj.mode == 'RGB': final_logo_to_cache = logo_img_obj
                else: final_logo_to_cache = logo_img_obj.convert('RGBA')
                
                processed_logo_data = {'image': final_logo_to_cache, 'width': final_logo_to_cache.width, 'height': final_logo_to_cache.height}
                self.log_message("Logo pré-processado para o lote.")
            except Exception as e_logo_cache:
                self.log_message(f"Erro ao pré-processar logo para o lote: {e_logo_cache}", level="WARN")
                self.root.after(0, lambda: messagebox.showwarning("Erro de Cache de Logo", f"Não foi possível pré-processar a logo: {e_logo_cache}\nOs QR Codes serão gerados sem logo."))
                processed_logo_data = None 
        try:
            if current_mode_str == "light":
                disabled_fg = current_theme["CTkButton"]["grayscale_fg_color_light"] 
                disabled_text = "#A0A0A0" 
            else: 
                disabled_fg = current_theme["CTkButton"]["fg_color_disabled"]
                disabled_text = current_theme["CTkButton"]["text_color_disabled"]

            self.root.after(0, lambda: self.btn_generate_macro.configure(state="disabled", fg_color=disabled_fg, text_color=disabled_text))
            self.root.after(0, lambda: self.btn_reset_macro.configure(state="disabled", fg_color=disabled_fg, text_color=disabled_text))

            file_extension = Path(self.csv_path).suffix.lower()
            self.log_message(f"Lendo arquivo: {self.csv_path} (extensão: {file_extension})")
            if file_extension == '.csv': df = pd.read_csv(self.csv_path, sep=';', encoding='utf-8-sig', header=0, dtype=str, keep_default_na=False)
            elif file_extension in ['.xlsx', '.xls']: df = pd.read_excel(self.csv_path, header=0, dtype=str, keep_default_na=False)
            else:
                self.log_message(f"Formato de arquivo não suportado: {file_extension}", level="ERROR")
                self.root.after(0, lambda: messagebox.showerror("Erro de Arquivo", "Formato de arquivo não suportado. Use CSV ou Excel."))
                return 
            
            if df.empty:
                self.log_message("Arquivo CSV/Excel está vazio.", level="WARN")
                self.root.after(0, lambda: messagebox.showerror("Erro de Arquivo", "O arquivo CSV/Excel está vazio."))
                return 
            
            self.log_message(f"Arquivo lido. Total de linhas: {len(df)}. Colunas: {list(df.columns)}")
            df_columns_lower = [str(col).lower() for col in df.columns]
            url_col_idx, name_col_idx = -1, -1
            
            url_keywords = ["url", "link", "endereço", "site"]
            name_keywords = ["nome", "título", "title", "qr code title", "qr title", "identificador", "id", "filename", "nome do arquivo"]

            for keyword in url_keywords:
                if keyword in df_columns_lower: url_col_idx = df_columns_lower.index(keyword); break
            for keyword in name_keywords:
                if keyword in df_columns_lower: name_col_idx = df_columns_lower.index(keyword); break
            
            self.log_message(f"Índice da coluna URL: {url_col_idx}, Nome: {name_col_idx}")

            if url_col_idx == -1: 
                if df.shape[1] >= 1: url_col_idx = 0 
                else:
                    self.log_message("Arquivo não possui colunas suficientes para URL.", level="ERROR")
                    self.root.after(0, lambda: messagebox.showerror("Erro de Arquivo", "O arquivo precisa ter pelo menos uma coluna para as URLs."))
                    return
            if name_col_idx == -1: 
                if df.shape[1] >= 2 and url_col_idx != 1: name_col_idx = 1 
                elif df.shape[1] >= 2 and url_col_idx == 1 and df.shape[1] > 2: name_col_idx = 2 
                elif df.shape[1] >= 1 and url_col_idx != 0: name_col_idx = 0 

            prefix_str = self.prefix_entry.get()
            format_selected = self.format_var_macro.get() 
            extension = format_selected.lower()
            total_rows = len(df)
            processed_count = 0
            error_count = 0
            self.log_message(f"Iniciando loop de processamento de {total_rows} linhas. Prefixo: '{prefix_str}', Formato: {extension.upper()}")

            for index, row in df.iterrows():
                progress_value = (index + 1) / total_rows
                progress_percent = int(progress_value * 100)
                if (index + 1) % (total_rows // 20 if total_rows > 40 else 1) == 0 or index == 0 or index == total_rows -1 :
                    self.log_message(f"Processando linha {index + 1}/{total_rows} ({progress_percent}%)", level="DEBUG")
                
                self.root.after(0, lambda p=progress_value: self.progress_bar.set(p))
                self.root.after(0, lambda txt=f"Processando {index + 1} de {total_rows} ({progress_percent}%)...": self.progress_label.configure(text=txt))
                
                try:
                    url = str(row.iloc[url_col_idx]).strip()
                    if not url: 
                        self.log_message(f"Linha {index+2}: URL vazia, pulando.", level="WARN")
                        error_count += 1
                        continue
                    
                    if name_col_idx != -1 and len(row) > name_col_idx and str(row.iloc[name_col_idx]).strip():
                        base_name_part = str(row.iloc[name_col_idx]).strip() 
                    else: base_name_part = f"qr_item_{index+1}" 
                    
                    sanitized_base_name = self.sanitize_filename(base_name_part)
                    final_name = prefix_str + sanitized_base_name
                    
                    qr_img = self.create_qr_with_logo(url, pre_processed_logo_img=processed_logo_data)
                    output_path = final_output_directory / f"{final_name}.{extension}"
                    
                    if format_selected in ["JPEG", "JPG"]:
                        if qr_img.mode == 'RGBA': 
                            rgb_img = Image.new('RGB', qr_img.size, 'white')
                            mask = qr_img.split()[3] if len(qr_img.split()) == 4 else None
                            rgb_img.paste(qr_img, (0,0), mask=mask) 
                            qr_img = rgb_img
                        qr_img.save(str(output_path), format='JPEG', quality=95, optimize=True)
                    else: 
                        qr_img.save(str(output_path), format='PNG', optimize=True)
                    processed_count += 1
                except Exception as e_row:
                    error_count += 1
                    current_url_for_log = url if 'url' in locals() and url else 'N/A'
                    self.log_message(f"Erro ao processar linha {index+1} (URL: {current_url_for_log}): {e_row}", level="ERROR")
                    error_text = f"Erro linha {index+2}: {str(e_row)[:50]}..." 
                    self.root.after(0, lambda txt=error_text: self.progress_label.configure(text=txt))
            
            self.root.after(0, lambda: self.progress_bar.set(1)) 
            final_message = f"Sucesso!!! {processed_count} QR Codes Gerados (100%)."
            if error_count > 0: final_message += f"\n{error_count} Falharam ou foram pulados. Verifique o log."
            self.log_message(f"Processamento em lote finalizado. Gerados: {processed_count}, Falhas: {error_count}. Salvo em: {final_output_directory}")
            self.root.after(0, lambda msg=final_message: self.progress_label.configure(text=msg))
            self.root.after(0, lambda msg=final_message: messagebox.showinfo("Processamento Concluído", f"{msg}\nSalvos em: {final_output_directory}"))
        
        except Exception as e: 
            self.log_message(f"Erro crítico no processamento em lote: {str(e)}", level="CRITICAL")
            self.root.after(0, lambda: messagebox.showerror("Erro Crítico no Lote", f"Erro: {str(e)}"))
            
        finally: 
            if current_mode_str == "light":
                enabled_fg = current_theme["CTkButton"]["grayscale_fg_color_light"]
                enabled_text = current_theme["CTkButton"]["grayscale_text_color_light"]
            else: 
                enabled_fg = current_theme["CTkButton"]["fg_color"] 
                enabled_text = current_theme["CTkButton"]["text_color"]

            self.root.after(0, lambda: self.btn_generate_macro.configure(state="normal", fg_color=enabled_fg, text_color=enabled_text))
            self.root.after(0, lambda: self.btn_reset_macro.configure(state="normal", fg_color=enabled_fg, text_color=enabled_text))
            self.root.after(7000, lambda: self.progress_bar.set(0)) 
            self.root.after(7000, lambda: self.progress_label.configure(text=""))
            self.log_message("Botões do modo macro reativados e UI de progresso resetada.")

    def reset_form(self, mode):
        self.log_message(f"Redefinindo formulário para modo: {mode}")
        self.image_size_var.set("1083") 
        self.logo_path = None 
        
        if mode == "único":
            self.url_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.logo_label_unico.configure(text="Nenhum logo selecionado")
            self.format_var_unico.set("PNG") 
            self.base_output_dir_unico = Path.home() 
            self.dir_label_unico.configure(text=str(self.base_output_dir_unico / self.subfolder_unico_name))
        else: 
            self.csv_path = None 
            self.csv_label.configure(text="Nenhum arquivo selecionado")
            self.prefix_entry.delete(0, 'end')
            self.logo_label_macro.configure(text="Nenhum logo selecionado")
            self.format_var_macro.set("PNG") 
            self.base_output_dir_macro = Path.home() 
            self.dir_label_macro.configure(text=str(self.base_output_dir_macro / self.subfolder_macro_name))
            if hasattr(self, 'progress_bar'): self.progress_bar.set(0)
            if hasattr(self, 'progress_label'): self.progress_label.configure(text="")
        self.log_message(f"Formulário do modo '{mode}' redefinido.")

    def load_changelog(self):
        return {
            "1.2.8 - Definitive Edition": ["Adicionado Terminal de Log Interno (Ctrl+T).", "Otimização: Cache de Logotipo.", "Interface: Progresso em % no Modo Macro.", "Fix: Barra de progresso inicia vazia."],
            "1.2.0": ["QR Codes em Subpastas.", "Melhor detecção de colunas CSV/Excel."],
            "1.1.0": ["Validação de Inputs.", "Tamanho de imagem configurável.", "Melhorias Modo Lote."],
            "1.0.0": ["Versão inicial do Codexa"]
        }

    def show_changelog(self):
        self.log_message("Exibindo changelog.")
        current_theme = TRON_NEON_THEME
        changelog_window = ctk.CTkToplevel(self.root)
        changelog_window.title("Atualizações - Changelog")
        changelog_window.geometry("650x500")
        changelog_window.attributes("-topmost", True)
        changelog_window.grab_set() 
        changelog_window.configure(fg_color=current_theme["CTkToplevel"]["fg_color"])

        title_label = ctk.CTkLabel(changelog_window, text="Histórico de Atualizações",
                                   font=ctk.CTkFont(size=20, weight="bold"),
                                   text_color=current_theme["CTkLabel"]["text_color"])
        title_label.pack(pady=20)
        
        textbox = ctk.CTkTextbox(changelog_window, width=650, height=400, wrap="word",
                                 fg_color=current_theme["CTkTextbox"]["fg_color"],
                                 border_color=current_theme["CTkTextbox"]["border_color"],
                                 text_color=current_theme["CTkTextbox"]["text_color"],
                                 scrollbar_button_color=current_theme["CTkTextbox"]["scrollbar_button_color"],
                                 scrollbar_button_hover_color=current_theme["CTkTextbox"]["scrollbar_button_hover_color"],
                                 corner_radius=current_theme["CTkTextbox"]["corner_radius"],
                                 border_width=current_theme["CTkTextbox"]["border_width"])
        textbox.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        
        # Usar cor para ênfase, já que 'font' não é permitido para tags no CTkTextbox
        emphasis_color = "#00D1D1" # Cor ciano de destaque do tema
        textbox.tag_config("version_style", foreground=emphasis_color) 
        
        for version, changes in sorted(self.changelog.items(), reverse=True): 
            start_index = textbox.index("end-1c")
            if textbox.index("end-1c") == "1.0" and not textbox.get("1.0", "end-1c"):
                start_index = "1.0"

            version_text_to_insert = f"Versão {version}"
            textbox.insert("end", version_text_to_insert + "\n")

            end_index = f"{start_index}+{len(version_text_to_insert)}c"
            textbox.tag_add("version_style", start_index, end_index)
            
            textbox.insert("end", "-" * 30 + "\n")
            for change_item_text in changes:
                textbox.insert("end", f"• {change_item_text}\n")
            textbox.insert("end", "\n")
        
        textbox.configure(state="disabled")

    def show_sobre_window(self):
        self.log_message("Exibindo janela 'Sobre'.")
        current_theme = TRON_NEON_THEME
        current_mode_str = ctk.get_appearance_mode().lower() 
        
        sobre_window = ctk.CTkToplevel(self.root)
        sobre_window.title("Sobre CODEXA")
        sobre_window.geometry("500x490") 
        sobre_window.attributes("-topmost", True)
        sobre_window.grab_set() 
        sobre_window.configure(fg_color=current_theme["CTkToplevel"]["fg_color"])

        content_frame = ctk.CTkFrame(sobre_window, fg_color="transparent")
        content_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        label_attrs_title = {"font": ctk.CTkFont(size=20, weight="bold"), "text_color": current_theme["CTkLabel"]["text_color"]}
        label_attrs_version = {"font": ctk.CTkFont(size=12), "text_color": current_theme["CTkLabel"]["text_color"]}
        label_attrs_body = {"wraplength": 440, "justify": "left", "font": ctk.CTkFont(size=13), "text_color": current_theme["CTkLabel"]["text_color"]}
        label_attrs_features_title = {"font": ctk.CTkFont(size=14, weight="bold"), "text_color": current_theme["CTkLabel"]["text_color"]}
        label_attrs_dev = {"font": ctk.CTkFont(size=12, slant="italic"), "text_color": current_theme["CTkLabel"]["text_color"]}
        
        if current_mode_str == "light":
            close_btn_fg = current_theme["CTkButton"]["grayscale_fg_color_light"] 
            close_btn_hover = current_theme["CTkButton"]["grayscale_hover_color_light"] 
            close_btn_text = current_theme["CTkButton"]["grayscale_text_color_light"] 
        else: 
            close_btn_fg = current_theme["CTkButton"]["fg_color"] 
            close_btn_hover = current_theme["CTkButton"]["hover_color"]
            close_btn_text = current_theme["CTkButton"]["text_color"]
        
        button_attrs_close = {
            "width": 100, "fg_color": close_btn_fg, "hover_color": close_btn_hover,
            "text_color": close_btn_text, "corner_radius": current_theme["CTkButton"]["corner_radius"]
        }

        title_label = ctk.CTkLabel(content_frame, text="Codexa - Automação em QR Codes", **label_attrs_title)
        title_label.pack(pady=(0, 10))
        version_label_sobre = ctk.CTkLabel(content_frame, text=f"Versão {self.version}", **label_attrs_version)
        version_label_sobre.pack(pady=(0, 20))
        descricao_text = ("O CODEXA automatiza a criação de QR Codes em larga escala, "
                          "a partir de links, otimizando processos como Rastreamento, Logística, e "
                          "Identificação de Produtos.")
        descricao_label = ctk.CTkLabel(content_frame, text=descricao_text, **label_attrs_body)
        descricao_label.pack(pady=(0, 15))
        caracteristicas_title = ctk.CTkLabel(content_frame, text="Características principais:", **label_attrs_features_title)
        caracteristicas_title.pack(pady=(10, 5), anchor="w")
        caracteristicas_text = ("• Geração em lotes infinitos\n"
                                "• Detecção inteligente de colunas em CSV/Excel\n"
                                "• Cache de Logotipo para geração rápida em massa\n"
                                "• Nomes de arquivos padronizados automaticamente\n"
                                "• Exportação em múltiplos formatos (PNG, JPG, JPEG)\n"
                                "• Organização automática em subpastas\n"
                                "• 100% offline, sem dependência de internet\n"
                                "• Compatível com qualquer máquina Windows, Mac e Linux")
        caracteristicas_label = ctk.CTkLabel(content_frame, text=caracteristicas_text, **label_attrs_body)
        caracteristicas_label.pack(pady=(0, 20), anchor="w")
        dev_label = ctk.CTkLabel(content_frame, text="©2025 - Breno_Santos", **label_attrs_dev)
        dev_label.pack(pady=(10, 20))
        btn_fechar = ctk.CTkButton(content_frame, text="Fechar", command=sobre_window.destroy, **button_attrs_close)
        btn_fechar.pack(pady=(10, 0))

    def run(self):
        self.log_message("Iniciando loop principal da GUI.")
        self.root.mainloop()
        self.log_message("Aplicação encerrada.")

def main():
    app = QRAutoGen()
    app.run()

if __name__ == "__main__":
    main()