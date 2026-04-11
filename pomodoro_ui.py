import tkinter as tk
import math
import time
import datetime
import os
root = tk.Tk()
root.title("Focus Bloom")
root.geometry("520x860")
root.resizable(False, False)
# STATE 
work_time = 1500
break_time = 300
total_cycles = 1
current_cycle = 1
mode = "Work"
running = False
start_time = 0
dark_mode = True
last_segment = -1
streak = 0
last_completed_date = None
#  STREAK FILE 
def load_streak():
    global streak, last_completed_date
    if os.path.exists("streak.txt"):
        with open("streak.txt", "r") as f:
            data = f.read().split(",")
            if len(data) == 2:
                streak = int(data[0])
                last_completed_date = data[1]
def save_streak():
    with open("streak.txt", "w") as f:
    
        f.write(f"{streak},{last_completed_date}")
def update_streak():
    global streak, last_completed_date
    today = str(datetime.date.today())
    if last_completed_date == today:
        return
    if last_completed_date:
        last_date = datetime.datetime.strptime(last_completed_date, "%Y-%m-%d").date()
        if (datetime.date.today() - last_date).days == 1:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1
    last_completed_date = today
    save_streak()
    streak_label.config(text=f"🔥 Streak: {streak}")
#  COLORS
def get_colors():
    if dark_mode:
        return {
            "bg": "#1f1f1f",
            "fg": "#ffffff",
            "accent": "#7a9e7e",
            "muted": "#444444",
            "btn": "#7a9e7e",
            "btn_hover": "#92b494"
        }
    else:
        return {
            "bg": "#f5efe6",
            "fg": "#2b2b2b",
            "accent": "#d6a75f",
            "muted": "#cccccc",
            "btn": "#d6a75f",
            "btn_hover": "#e0b97a"
        }
# SOUND
def play_tick():
    try:
        import winsound
        winsound.Beep(800, 40)
    except:
        pass
# UI
main = tk.Frame(root)
main.pack(fill="both", expand=True)
title = tk.Label(main, font=("Segoe UI", 14))
title.pack(pady=10)
mode_label = tk.Label(main, font=("Segoe UI", 12, "bold"))
mode_label.pack()
streak_label = tk.Label(main, font=("Segoe UI", 11))
streak_label.pack()
canvas = tk.Canvas(main, width=340, height=340, highlightthickness=0)
canvas.pack(pady=20)
time_label = tk.Label(main, font=("Segoe UI", 34, "bold"))
time_label.pack()
status_label = tk.Label(main)
status_label.pack(pady=5)
#DRAW
def draw_circle(progress):
    global last_segment
    colors = get_colors()
    canvas.delete("all")
    canvas.config(bg=colors["bg"])
    cx, cy = 170, 170
    radius = 130
    segments = 30
    filled = int(progress * segments)
    if filled != last_segment:
        if last_segment != -1:
            play_tick()
        last_segment = filled
    for i in range(segments):
        angle = (360 / segments) * i
        rad = math.radians(angle)
        x1 = cx + math.cos(rad) * (radius - 10)
        y1 = cy + math.sin(rad) * (radius - 10)
        x2 = cx + math.cos(rad) * radius
        y2 = cy + math.sin(rad) * radius
        color = colors["accent"] if i < filled else colors["muted"]
        canvas.create_line(x1, y1, x2, y2, fill=color, width=4)
    if dark_mode:
        canvas.create_text(cx, cy, text="🌙", font=("Segoe UI Emoji", 44), fill="white")
    else:
        canvas.create_text(cx, cy, text="☀", font=("Segoe UI Emoji", 44), fill="#d6a75f")
# TIMER
def update_loop():
    if running:
        elapsed = time.time() - start_time
        total = work_time if mode == "Work" else break_time
        progress = min(elapsed / total, 1)
        remaining = max(total - int(elapsed), 0)
        mins = remaining // 60
        secs = remaining % 60
        time_label.config(text=f"{mins:02d}:{secs:02d}")
        draw_circle(progress)
        if remaining <= 0:
            handle_phase_change()
    root.after(50, update_loop)
#FLOW
def handle_phase_change():
    global mode, current_cycle, running, start_time, last_segment
    last_segment = -1
    if mode == "Work":
        mode = "Break"
        start_time = time.time()
        update_labels()
    else:
        if current_cycle < total_cycles:
            current_cycle += 1
            mode = "Work"
            start_time = time.time()
            update_labels()
        else:
            running = False
            update_streak()  # 🔥 update streak here
            mode_label.config(text="Completed")
            status_label.config(text="All cycles finished")
            time_label.config(text="00:00")
def update_labels():
    colors = get_colors()
    title.config(text=f"Focus period ({current_cycle} of {total_cycles})")
    mode_label.config(text=f"{mode} Time", fg=colors["accent"])
    if mode == "Work":
        status_label.config(text="Up next: Break")
    else:
        status_label.config(text="Up next: Work")
# CONTROLS
def start():
    global running, start_time
    if not running:
        running = True
        start_time = time.time()
def reset():
    global running, current_cycle, mode, last_segment
    running = False
    current_cycle = 1
    mode = "Work"
    last_segment = -1
    update_labels()
    time_label.config(text=f"{work_time//60:02d}:00")
def set_cycles(event=None):
    global total_cycles, current_cycle
    try:
        val = int(cycle_input.get())
        if val > 0:
            total_cycles = val
            current_cycle = 1
            update_labels()
    except:
        pass
def set_time(w, b):
    global work_time, break_time, running, last_segment
    running = False
    work_time = w
    break_time = b
    last_segment = -1
    time_label.config(text=f"{w//60:02d}:00")
def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()
    draw_circle(0)
#BUTTON STYLE 
def styled_btn(parent, text, cmd):
    btn = tk.Button(parent, text=text, command=cmd,
                    relief="flat", padx=14, pady=8)
    def on_enter(e):
        colors = get_colors()
        btn.config(bg=colors["btn_hover"], relief="raised")
    def on_leave(e):
        colors = get_colors()
        btn.config(bg=colors["btn"], relief="flat")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn
# BUTTONS
btn_frame = tk.Frame(main)
btn_frame.pack(pady=10)
styled_btn(btn_frame, "Start", start).pack(side="left", padx=6)
styled_btn(btn_frame, "Reset", reset).pack(side="left", padx=6)
preset_frame = tk.Frame(main)
preset_frame.pack()
styled_btn(preset_frame, "25 / 5", lambda: set_time(1500,300)).pack(side="left", padx=5)
styled_btn(preset_frame, "50 / 10", lambda: set_time(3000,600)).pack(side="left", padx=5)
styled_btn(preset_frame, "100 / 20", lambda: set_time(6000,1200)).pack(side="left", padx=5)
cycle_frame = tk.Frame(main)
cycle_frame.pack(pady=10)
tk.Label(cycle_frame, text="Cycles:").pack(side="left")
cycle_input = tk.Entry(cycle_frame, width=5)
cycle_input.pack(side="left", padx=5)
cycle_input.insert(0, "1")
cycle_input.bind("<Return>", set_cycles)
styled_btn(cycle_frame, "Apply", set_cycles).pack(side="left")
toggle_btn = tk.Button(main, command=toggle_mode)
toggle_btn.pack(pady=20)
# THEME
def apply_theme():
    colors = get_colors()
    root.config(bg=colors["bg"])
    main.config(bg=colors["bg"])
    title.config(bg=colors["bg"], fg=colors["fg"])
    mode_label.config(bg=colors["bg"], fg=colors["accent"])
    time_label.config(bg=colors["bg"], fg=colors["fg"])
    status_label.config(bg=colors["bg"], fg=colors["fg"])
    streak_label.config(bg=colors["bg"], fg=colors["accent"])
    canvas.config(bg=colors["bg"])

    toggle_btn.config(
        text="Light Mode" if dark_mode else "Dark Mode",
        bg=colors["btn"],
        fg="white",
        activebackground=colors["btn_hover"]
    )

    for widget in main.winfo_children():
        if isinstance(widget, tk.Frame):
            for b in widget.winfo_children():
                if isinstance(b, tk.Button):
                    b.config(
                        bg=colors["btn"],
                        fg="white",
                        activebackground=colors["btn_hover"]
                    )
# INIT 
load_streak()
streak_label.config(text=f"🔥 Streak: {streak}")
apply_theme()
update_labels()
draw_circle(0)
update_loop()
root.mainloop()
