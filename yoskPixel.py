import tkinter as tk
from tkinter import ttk  # ### YENİ ### -> Daha modern görünümlü widget'lar için eklendi
from tkinter import simpledialog, colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageColor
import random
import colorsys # ### YENİ ### -> Renk dönüşümleri için eklendi

class EffectDialog(simpledialog.Dialog):
    # ### YENİ ### -> Birden fazla efekti yönetmek için oluşturulan yeni diyalog sınıfı
    def body(self, master):
        self.title("Efekt Ayarları")

        # Efekt Seçimi
        tk.Label(master, text="Efekt Türü:", font=("Courier New", 9, "bold")).grid(row=0, column=0, sticky='w', columnspan=2)
        self.effect_var = tk.StringVar(value="Glitch")
        effects = ["Glitch", "Scanline", "Noise"]
        self.effect_menu = ttk.Combobox(master, textvariable=self.effect_var, values=effects, state="readonly")
        self.effect_menu.grid(row=1, column=0, padx=5, pady=(0,10), columnspan=2)
        self.effect_menu.bind("<<ComboboxSelected>>", self.on_effect_change)

        # Ortak Ayarlar
        tk.Label(master, text="Hız (FPS, 1-30):", font=("Courier New", 9, "bold")).grid(row=2, column=0, sticky='w', columnspan=2)
        self.speed_slider = tk.Scale(master, from_=1, to=30, orient=tk.HORIZONTAL, length=250)
        self.speed_slider.set(10)
        self.speed_slider.grid(row=3, column=0, padx=5, columnspan=2)

        # Efekte Özel Ayarlar için Çerçeve
        self.settings_frame = tk.Frame(master)
        self.settings_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.create_glitch_settings() # Başlangıçta Glitch ayarlarını göster

        return self.effect_menu

    def on_effect_change(self, event=None):
        # Ayarlar çerçevesini temizle
        for widget in self.settings_frame.winfo_children():
            widget.destroy()
        
        # Seçilen efekte göre yeni ayarları oluştur
        effect = self.effect_var.get()
        if effect == "Glitch":
            self.create_glitch_settings()
        elif effect == "Scanline":
            self.create_scanline_settings()
        elif effect == "Noise":
            self.create_noise_settings()

    def create_glitch_settings(self):
        tk.Label(self.settings_frame, text="Yoğunluk (1-10):", font=("Courier New", 9, "bold")).grid(row=0, sticky='w')
        self.intensity_slider = tk.Scale(self.settings_frame, from_=1, to=10, orient=tk.HORIZONTAL, length=250)
        self.intensity_slider.set(3)
        self.intensity_slider.grid(row=1, padx=5)

    def create_scanline_settings(self):
        tk.Label(self.settings_frame, text="Çizgi Kalınlığı (1-5):", font=("Courier New", 9, "bold")).grid(row=0, sticky='w')
        self.line_thickness = tk.Scale(self.settings_frame, from_=1, to=5, orient=tk.HORIZONTAL, length=250)
        self.line_thickness.set(1)
        self.line_thickness.grid(row=1, padx=5)
        tk.Label(self.settings_frame, text="Koyuluk (%):", font=("Courier New", 9, "bold")).grid(row=2, sticky='w')
        self.darkness = tk.Scale(self.settings_frame, from_=10, to=90, orient=tk.HORIZONTAL, length=250)
        self.darkness.set(50)
        self.darkness.grid(row=3, padx=5)

    def create_noise_settings(self):
        tk.Label(self.settings_frame, text="Yoğunluk (1-100):", font=("Courier New", 9, "bold")).grid(row=0, sticky='w')
        self.intensity_slider = tk.Scale(self.settings_frame, from_=1, to=100, orient=tk.HORIZONTAL, length=250)
        self.intensity_slider.set(20)
        self.intensity_slider.grid(row=1, padx=5)
        self.is_monochrome = tk.BooleanVar(value=True)
        tk.Checkbutton(self.settings_frame, text="Siyah-Beyaz Parazit", variable=self.is_monochrome, font=("Courier New", 9, "bold")).grid(row=2, sticky='w', pady=5)


    def apply(self):
        self.result = {"effect": self.effect_var.get(), "speed": self.speed_slider.get()}
        effect = self.result["effect"]
        if effect == "Glitch":
            self.result["intensity"] = self.intensity_slider.get()
        elif effect == "Scanline":
            self.result["thickness"] = self.line_thickness.get()
            self.result["darkness"] = self.darkness.get() / 100.0
        elif effect == "Noise":
            self.result["intensity"] = self.intensity_slider.get()
            self.result["monochrome"] = self.is_monochrome.get()

class PixelArtEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("yoskPixel")
        
        self.font_retro = ("Courier New", 9, "bold")
        self.themes = {
            "Windows 98 Classic": {'bg':"#c0c0c0",'fg':"#000000",'button_bg':"#c0c0c0",'button_fg':"#000000",'active_bg':"#000080",'active_fg':"#ffffff",'trough':"#a0a0a0",'grid_color':'#808080'},
            "XP Luna Blue": {'bg':"#ece9d8",'fg':"#000000",'button_bg':"#f0f0f0",'button_fg':"#000000",'active_bg':"#316ac5",'active_fg':"#ffffff",'trough':"#d4d0c8",'grid_color':'#b0b0b0'},
            "Matrix Green": {'bg':"#000000",'fg':"#00ff00",'button_bg':"#101010",'button_fg':"#00ff00",'active_bg':"#008000",'active_fg':"#ffffff",'trough':"#202020",'grid_color':'#008000'},
            "Command Prompt": {'bg':"#000000",'fg':"#f0c808",'button_bg':"#202020",'button_fg':"#f0c808",'active_bg':"#806000",'active_fg':"#000000",'trough':"#303030",'grid_color':'#806000'}
        }
        self.current_theme = tk.StringVar(value="Windows 98 Classic")

        (self.pixel_size, self.grid_width, self.grid_height) = (20, 32, 32)
        self.current_color, self.current_tool = "#000000", "pencil"
        self.mirror_mode = tk.StringVar(value="none")
        self.show_grid = tk.BooleanVar(value=True)
        self.undo_stack, self.animation_frames, self.original_pixel_colors, self.ui_widgets = [], [], [], [] # ### GÜNCELLENDİ ###
        self.is_animating = False # ### GÜNCELLENDİ ###
        self.animation_job_id = None # ### YENİ ### -> after() döngüsünü iptal etmek için

        self.create_menu()
        self.main_frame = tk.Frame(self.root, relief=tk.RIDGE, bd=2); self.main_frame.pack(fill=tk.BOTH, expand=True); self.ui_widgets.append(self.main_frame)
        self.create_toolbar(self.main_frame)
        
        canvas_frame = tk.Frame(self.main_frame, relief=tk.SUNKEN, bd=2); canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0); self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_canvas_grid(); self.bind_events(); self.create_statusbar(); self.apply_theme()

    # --- EFEKT ALGORİTMALARI ---
    def restore_original_canvas(self):
        # ### YENİ ### -> Animasyon kareleri arasında tuvali orijinal haline döndürür
        for y, row in enumerate(self.original_pixel_colors):
            for x, color in enumerate(row):
                self.canvas.itemconfig(self.grid[y][x], fill=color)

    def glitch_animation_loop(self, intensity, speed_ms):
        if not self.is_animating: return
        self.restore_original_canvas()

        # Yatay & Dikey Kaydırma
        for y in range(self.grid_height):
            if random.random() < 0.05 * intensity:
                shift = random.randint(-intensity, intensity)
                row_colors = self.original_pixel_colors[y]
                for x, color in enumerate(row_colors): self.canvas.itemconfig(self.grid[y][(x + shift) % self.grid_width], fill=color)
        for x in range(self.grid_width):
            if random.random() < 0.05 * intensity:
                shift = random.randint(-intensity, intensity)
                col_colors = [self.original_pixel_colors[y][x] for y in range(self.grid_height)]
                for y, color in enumerate(col_colors): self.canvas.itemconfig(self.grid[(y + shift) % self.grid_height][x], fill=color)
        
        # Piksel Değişimi
        for _ in range(intensity * 3):
            dest_x, dest_y = random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1)
            source_x, source_y = random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1)
            source_color = self.original_pixel_colors[source_y][source_x]
            self.canvas.itemconfig(self.grid[dest_y][dest_x], fill=source_color)
        
        self.animation_frames.append(self.get_canvas_as_image().resize((self.grid_width * 10, self.grid_height * 10), Image.NEAREST))
        self.animation_job_id = self.root.after(speed_ms, lambda: self.glitch_animation_loop(intensity, speed_ms))

    def scanline_animation_loop(self, thickness, darkness, speed_ms, frame=0):
        # ### YENİ ###
        if not self.is_animating: return
        self.restore_original_canvas()
        
        for y in range(self.grid_height):
            # Animasyon için çizgilerin pozisyonunu her karede kaydır
            if (y + frame) % (thickness * 2) < thickness:
                for x in range(self.grid_width):
                    original_color = self.original_pixel_colors[y][x]
                    # Rengi karart
                    r, g, b = self.canvas.winfo_rgb(original_color)
                    r, g, b = int(r/256 * (1-darkness)), int(g/256 * (1-darkness)), int(b/256 * (1-darkness))
                    darkened_color = f"#{r:02x}{g:02x}{b:02x}"
                    self.canvas.itemconfig(self.grid[y][x], fill=darkened_color)

        self.animation_frames.append(self.get_canvas_as_image().resize((self.grid_width * 10, self.grid_height * 10), Image.NEAREST))
        self.animation_job_id = self.root.after(speed_ms, lambda: self.scanline_animation_loop(thickness, darkness, speed_ms, frame + 1))

    def noise_animation_loop(self, intensity, is_monochrome, speed_ms):
        # ### YENİ ###
        if not self.is_animating: return
        self.restore_original_canvas()

        num_pixels_to_change = (self.grid_width * self.grid_height * intensity) // 100
        for _ in range(num_pixels_to_change):
            x, y = random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1)
            if is_monochrome:
                val = random.randint(0, 255)
                noise_color = f"#{val:02x}{val:02x}{val:02x}"
            else:
                noise_color = f"#{random.randint(0, 0xFFFFFF):06x}"
            self.canvas.itemconfig(self.grid[y][x], fill=noise_color)

        self.animation_frames.append(self.get_canvas_as_image().resize((self.grid_width * 10, self.grid_height * 10), Image.NEAREST))
        self.animation_job_id = self.root.after(speed_ms, lambda: self.noise_animation_loop(intensity, is_monochrome, speed_ms))

    # --- GERİ KALAN TÜM FONKSİYONLAR ---
    def create_menu(self):
        self.menubar = tk.Menu(self.root, font=self.font_retro, tearoff=0)
        self.root.config(menu=self.menubar)
        file_menu = tk.Menu(self.menubar, tearoff=0, font=self.font_retro)
        file_menu.add_command(label="Yeni Tuval...", command=self.new_canvas_dialog); file_menu.add_command(label="Aç (PNG)...", command=self.open_image); file_menu.add_separator()
        file_menu.add_command(label="PNG Olarak Kaydet...", command=self.save_as_png); file_menu.add_command(label="GIF Olarak Kaydet...", command=self.save_as_gif); file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        self.menubar.add_cascade(label="Dosya", menu=file_menu)
        edit_menu = tk.Menu(self.menubar, tearoff=0, font=self.font_retro)
        edit_menu.add_command(label="Geri Al", command=self.undo_last_action, accelerator="Ctrl+Z"); edit_menu.add_command(label="Tuvali Temizle", command=self.clear_canvas)
        self.menubar.add_cascade(label="Düzenle", menu=edit_menu)
        self.root.bind_all("<Control-z>", lambda event: self.undo_last_action())
        view_menu = tk.Menu(self.menubar, tearoff=0, font=self.font_retro)
        view_menu.add_checkbutton(label="Izgarayı Göster", variable=self.show_grid, command=self.toggle_grid)
        theme_menu = tk.Menu(view_menu, tearoff=0, font=self.font_retro)
        for theme_name in self.themes.keys(): theme_menu.add_radiobutton(label=theme_name, variable=self.current_theme, command=self.apply_theme)
        view_menu.add_cascade(label="Temalar", menu=theme_menu)
        self.menubar.add_cascade(label="Görünüm", menu=view_menu)

    def create_toolbar(self, parent):
        self.toolbar = tk.Frame(parent, relief=tk.RIDGE, bd=2, padx=5, pady=5); self.toolbar.pack(side=tk.LEFT, fill=tk.Y); self.ui_widgets.append(self.toolbar)
        title_label = tk.Label(self.toolbar, text="yoskPixel v1.1", font=(self.font_retro[0], 10, "bold")); title_label.pack(pady=(0, 10)); self.ui_widgets.append(title_label)
        tools_frame = tk.LabelFrame(self.toolbar, text="Araçlar", font=self.font_retro, relief=tk.GROOVE); tools_frame.pack(fill=tk.X, pady=2); self.ui_widgets.append(tools_frame)
        self.tool_buttons = {}
        for tool_name, text in [("pencil", "Kalem"), ("eraser", "Silgi"), ("bucket", "Kova"), ("picker", "Seçici")]:
            btn = tk.Button(tools_frame, text=text, font=self.font_retro, relief=tk.RAISED, bd=2, command=lambda t=tool_name: self.select_tool(t)); btn.pack(fill=tk.X, padx=4, pady=2)
            self.tool_buttons[tool_name] = btn; self.ui_widgets.append(btn)
        color_frame = tk.LabelFrame(self.toolbar, text="Renk", font=self.font_retro, relief=tk.GROOVE); color_frame.pack(fill=tk.X, pady=2); self.ui_widgets.append(color_frame)
        self.color_preview = tk.Label(color_frame, bg=self.current_color, width=4, height=2, relief=tk.SUNKEN, bd=2); self.color_preview.pack(pady=5)
        color_btn = tk.Button(color_frame, text="Palet...", font=self.font_retro, relief=tk.RAISED, bd=2, command=self.choose_color); color_btn.pack(); self.ui_widgets.append(color_btn)
        palette_frame = tk.Frame(color_frame); palette_frame.pack(pady=5); self.ui_widgets.append(palette_frame)
        colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#800080", "#808080"]
        for i, color in enumerate(colors):
            btn = tk.Button(palette_frame, bg=color, width=2, relief=tk.FLAT, command=lambda c=color: self.set_color(c)); btn.grid(row=i//4, column=i%4)
        options_frame = tk.LabelFrame(self.toolbar, text="Seçenekler", font=self.font_retro, relief=tk.GROOVE); options_frame.pack(fill=tk.X, pady=2); self.ui_widgets.append(options_frame)
        lbl_brush = tk.Label(options_frame, text="Fırça Boyutu:", font=self.font_retro); lbl_brush.pack(); self.ui_widgets.append(lbl_brush)
        self.brush_size_slider = tk.Scale(options_frame, from_=1, to=10, orient=tk.HORIZONTAL, font=self.font_retro, length=100); self.brush_size_slider.set(1); self.brush_size_slider.pack(fill=tk.X); self.ui_widgets.append(self.brush_size_slider)
        lbl_mirror = tk.Label(options_frame, text="Simetri:", font=self.font_retro); lbl_mirror.pack(pady=(5,0)); self.ui_widgets.append(lbl_mirror)
        for text, value in [("Yok", "none"), ("Yatay", "horizontal"), ("Dikey", "vertical")]:
            rb = tk.Radiobutton(options_frame, text=text, variable=self.mirror_mode, value=value, font=self.font_retro, anchor='w'); rb.pack(fill='x'); self.ui_widgets.append(rb)
        
        effect_frame = tk.LabelFrame(self.toolbar, text="Animasyon", font=self.font_retro, relief=tk.GROOVE); effect_frame.pack(fill=tk.X, pady=2); self.ui_widgets.append(effect_frame) # ### GÜNCELLENDİ ###
        self.effect_button = tk.Button(effect_frame, text="Efekt Uygula", font=self.font_retro, relief=tk.RAISED, bd=2, command=self.toggle_effect); self.effect_button.pack(fill=tk.X, padx=4, pady=2); self.ui_widgets.append(self.effect_button) # ### GÜNCELLENDİ ###

    def create_statusbar(self):
        self.status_bar = tk.Label(self.root, text=" Hazır", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=self.font_retro); self.status_bar.pack(side=tk.BOTTOM, fill=tk.X); self.ui_widgets.append(self.status_bar)

    def apply_theme(self):
        theme_name = self.current_theme.get(); colors = self.themes[theme_name]
        self.root.config(bg=colors['bg']); self.menubar.config(bg=colors['button_bg'], fg=colors['fg'], activebackground=colors['active_bg'], activeforeground=colors['active_fg'])
        for widget in self.ui_widgets:
            widget_class = widget.winfo_class()
            try:
                if widget_class != "Frame": widget.config(bg=colors['bg'], fg=colors['fg'])
                else: widget.config(bg=colors['bg'])
                if widget_class in ('Button', 'TButton'): widget.config(bg=colors['button_bg'], fg=colors['button_fg'], activebackground=colors['active_bg'], activeforeground=colors['active_fg'])
                elif widget_class == 'Radiobutton': widget.config(activebackground=colors['bg'], selectcolor=colors['active_bg'])
                elif widget_class in ('Scale', 'TScale'): widget.config(troughcolor=colors['trough'], activebackground=colors['active_bg'])
                elif widget_class in ('Labelframe', 'TLabelframe'): widget.config(fg=colors['fg'])
            except tk.TclError: pass
        self.toggle_grid(); self.select_tool(self.current_tool)

    def select_tool(self, tool):
        self.current_tool = tool; self.update_statusbar(None)
        colors = self.themes[self.current_theme.get()]
        for tool_name, button in self.tool_buttons.items():
            is_active = tool_name == tool
            button.config(relief=tk.SUNKEN if is_active else tk.RAISED, bg=colors['active_bg'] if is_active else colors['button_bg'], fg=colors['active_fg'] if is_active else colors['button_fg'])

    def create_canvas_grid(self, clear_undo=True):
        self.canvas.delete("all"); self.canvas.config(width=self.grid_width * self.pixel_size, height=self.grid_height * self.pixel_size)
        self.grid = [[self.canvas.create_rectangle(x*self.pixel_size, y*self.pixel_size, (x+1)*self.pixel_size, (y+1)*self.pixel_size, fill="white", outline="") for x in range(self.grid_width)] for y in range(self.grid_height)]
        self.toggle_grid()
        if clear_undo: self.undo_stack.clear()

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_canvas_press); self.canvas.bind("<B1-Motion>", self.on_canvas_drag); self.canvas.bind("<Motion>", self.update_statusbar)
        self.canvas.bind("<Leave>", lambda e: self.status_bar.config(text=" Hazır"))

    def get_pixel_coords(self, event):
        x, y = int(self.canvas.canvasx(event.x) // self.pixel_size), int(self.canvas.canvasy(event.y) // self.pixel_size)
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height: return x, y
        return None, None

    def on_canvas_press(self, event):
        if self.is_animating: return
        self.push_to_undo(); x, y = self.get_pixel_coords(event)
        if x is None: return
        if self.current_tool == "bucket": self.flood_fill(x, y, self.current_color)
        elif self.current_tool == "picker": self.pick_color(x, y)
        else: self.draw_pixel(x, y)

    def on_canvas_drag(self, event):
        if self.is_animating or self.current_tool not in ["pencil", "eraser"]: return
        x, y = self.get_pixel_coords(event)
        if x is not None: self.draw_pixel(x, y)

    def draw_pixel(self, x, y):
        color = "white" if self.current_tool == "eraser" else self.current_color; offset = self.brush_size_slider.get() // 2
        for i in range(-offset, self.brush_size_slider.get() - offset):
            for j in range(-offset, self.brush_size_slider.get() - offset):
                px, py = x + i, y + j
                if 0 <= px < self.grid_width and 0 <= py < self.grid_height:
                    self.canvas.itemconfig(self.grid[py][px], fill=color); mode = self.mirror_mode.get()
                    if mode == "horizontal": self.canvas.itemconfig(self.grid[py][self.grid_width-1-px], fill=color)
                    elif mode == "vertical": self.canvas.itemconfig(self.grid[self.grid_height-1-py][px], fill=color)

    def flood_fill(self, x, y, new_color):
        target_color = self.canvas.itemcget(self.grid[y][x], "fill"); q = [(x, y)]
        if target_color == new_color: return
        visited = set()
        while q:
            cx, cy = q.pop(0); 
            if (cx, cy) in visited or not (0 <= cx < self.grid_width and 0 <= cy < self.grid_height): continue
            if self.canvas.itemcget(self.grid[cy][cx], "fill") == target_color:
                self.canvas.itemconfig(self.grid[cy][cx], fill=new_color); visited.add((cx, cy))
                q.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])

    def pick_color(self, x, y): self.set_color(self.canvas.itemcget(self.grid[y][x], "fill")); self.select_tool("pencil")
    def set_color(self, color): self.current_color = color; self.color_preview.config(bg=self.current_color)
    def choose_color(self): color_code = colorchooser.askcolor(title="Renk Seç", initialcolor=self.current_color); self.set_color(color_code[1]) if color_code and color_code[1] else None
    def toggle_grid(self): outline = self.themes[self.current_theme.get()]['grid_color'] if self.show_grid.get() else ""; [self.canvas.itemconfig(i, outline=outline) for r in self.grid for i in r]
    def update_statusbar(self, event): coords = f"X: {int(self.canvas.canvasx(event.x)//self.pixel_size)}, Y: {int(self.canvas.canvasy(event.y)//self.pixel_size)} | " if event and self.get_pixel_coords(event)[0] is not None else ""; self.status_bar.config(text=f"{coords}Araç: {self.current_tool.capitalize()}")
    def push_to_undo(self): self.undo_stack.append([[self.canvas.itemcget(p, "fill") for p in r] for r in self.grid]); self.undo_stack = self.undo_stack[-20:]
    def undo_last_action(self): [self.canvas.itemconfig(self.grid[y][x], fill=c) for y, r in enumerate(self.undo_stack.pop()) for x, c in enumerate(r)] if self.undo_stack else None
    def clear_canvas(self): self.push_to_undo(); [self.canvas.itemconfig(i, fill="white") for r in self.grid for i in r]; self.animation_frames = []

    def new_canvas_dialog(self):
        if self.is_animating: self.toggle_effect()
        dims = simpledialog.askstring("Yeni Tuval", "Genişlik x Yükseklik (örn: 64x64):", parent=self.root)
        if dims:
            try: w, h = map(int, dims.lower().split('x')); self.grid_width, self.grid_height = w, h; self.create_canvas_grid() if 1<=w<=256 and 1<=h<=256 else messagebox.showerror("Hata", "Boyutlar 1-256 arasında olmalı.")
            except: messagebox.showerror("Hata", "Geçersiz format.")

    def get_canvas_as_image(self):
        img = Image.new("RGB", (self.grid_width, self.grid_height)); [img.putpixel((x, y), ImageColor.getrgb(self.canvas.itemcget(self.grid[y][x], "fill"))) for y in range(self.grid_height) for x in range(self.grid_width)]; return img

    def save_as_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if file_path: self.get_canvas_as_image().resize((self.grid_width*10, self.grid_height*10), Image.NEAREST).save(file_path); messagebox.showinfo("Başarılı", f"Kaydedildi: {file_path}")

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG", "*.png")]);
        if not file_path: return
        self.push_to_undo()
        img = Image.open(file_path).resize((self.grid_width, self.grid_height), Image.NEAREST).convert('RGB')
        img_data = list(img.getdata())
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                r, g, b = img_data[y * self.grid_width + x]
                self.canvas.itemconfig(self.grid[y][x], fill=f"#{r:02x}{g:02x}{b:02x}")
    
    def toggle_effect(self):
        # ### GÜNCELLENDİ ### -> Birden fazla efekti yöneten ana fonksiyon
        if self.is_animating:
            self.is_animating = False
            if self.animation_job_id:
                self.root.after_cancel(self.animation_job_id) # Animasyon döngüsünü durdur
                self.animation_job_id = None
            
            self.effect_button.config(text="Efekt Uygula", relief=tk.RAISED)
            colors = self.themes[self.current_theme.get()]
            self.effect_button.config(bg=colors['button_bg'], fg=colors['button_fg'])
            
            if self.original_pixel_colors: 
                self.restore_original_canvas()
        else:
            dialog = EffectDialog(self.root)
            if dialog.result:
                settings = dialog.result
                speed_ms = 1000 // settings["speed"]
                self.is_animating = True
                self.effect_button.config(text="Durdur", relief=tk.SUNKEN)
                colors = self.themes[self.current_theme.get()]
                self.effect_button.config(bg=colors['active_bg'], fg=colors['active_fg'])
                
                self.original_pixel_colors = [[self.canvas.itemcget(p, "fill") for p in r] for r in self.grid]
                self.animation_frames = []
                
                # Seçilen efekte göre ilgili animasyon fonksiyonunu çağır
                effect_name = settings["effect"]
                if effect_name == "Glitch":
                    self.glitch_animation_loop(settings["intensity"], speed_ms)
                elif effect_name == "Scanline":
                    self.scanline_animation_loop(settings["thickness"], settings["darkness"], speed_ms)
                elif effect_name == "Noise":
                    self.noise_animation_loop(settings["intensity"], settings["monochrome"], speed_ms)


    def save_as_gif(self):
        # ### GÜNCELLENDİ ###
        if self.is_animating: messagebox.showwarning("Uyarı", "GIF kaydetmek için efekti durdurun."); return
        if not self.animation_frames: messagebox.showinfo("Bilgi", "Kaydedilecek animasyon yok. Önce bir efekt uygulayın."); return
        file_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        if file_path:
            # Hızı, animasyonun oluşturulduğu FPS'ye göre ayarla
            dialog_speed = simpledialog.askinteger("GIF Hızı", "Saniyedeki Kare Sayısı (FPS):", initialvalue=10, minvalue=1, maxvalue=30)
            if not dialog_speed: return
            duration = 1000 // dialog_speed
            self.animation_frames[0].save(file_path, save_all=True, append_images=self.animation_frames[1:], duration=duration, loop=0)
            messagebox.showinfo("Başarılı", f"Animasyon kaydedildi: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtEditor(root)
    root.mainloop()