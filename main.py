import tkinter as tk
from tkinter import messagebox
import keyboard
import threading
import time
import ctypes
import os

PASSWORD = "1234"

def check_password():
    if password_entry.get() == PASSWORD:
        # إلغاء كل الحماية وإغلاق البرنامج
        root.attributes("-topmost", False)
        keyboard.unhook_all()
        try:
            ctypes.windll.user32.ShowCursor(True)  # إظهار الماوس مرة أخرى
        except:
            pass
        root.destroy()
        os._exit(0)
    else:
        messagebox.showerror("خطأ", "كلمة السر خاطئة!\nأعد المحاولة.")
        password_entry.delete(0, tk.END)
        password_entry.focus()

def block_keys():
    """تعطيل الاختصارات الخطرة"""
    keys_to_block = ['win', 'alt+tab', 'alt+f4', 'ctrl+shift+esc', 'ctrl+esc', 'escape', 'f11', 'tab']
    for key in keys_to_block:
        try:
            keyboard.block_key(key)
        except:
            pass

def keep_focus():
    """الحفاظ على النافذة في المقدمة ومنع أي شيء آخر"""
    while True:
        try:
            root.attributes("-topmost", True)
            root.lift()
            root.focus_force()
            time.sleep(0.3)
        except:
            break

def hide_cursor():
    """إخفاء الماوس"""
    try:
        ctypes.windll.user32.ShowCursor(False)
    except:
        pass

# ====================== إنشاء النافذة ======================
root = tk.Tk()
root.title("شاشة محمية - كلمة السر مطلوبة")

root.attributes('-fullscreen', True)
root.attributes("-topmost", True)
root.resizable(False, False)
root.configure(bg='red')
root.protocol("WM_DELETE_WINDOW", lambda: None)  # تعطيل زر الإغلاق

# إخفاء الماوس
hide_cursor()

# نص التحذير
tk.Label(root, 
         text="⚠️ الجهاز محمي بالكامل ⚠️\n\n"
              "لا يمكن فتح أي برنامج آخر\n"
              "ولا يمكن إغلاق هذه الشاشة\n"
              "إلا بإدخال كلمة السر الصحيحة",
         font=("Arial", 26, "bold"),
         bg='red', fg='white', justify='center').pack(pady=100)

# خانة كلمة السر
frame = tk.Frame(root, bg='red')
frame.pack(pady=40)

tk.Label(frame, text="كلمة السر:", font=("Arial", 20), bg='red', fg='white').pack(side=tk.LEFT, padx=20)

password_entry = tk.Entry(frame, show="●", font=("Arial", 24), width=12, justify='center')
password_entry.pack(side=tk.LEFT, padx=10)
password_entry.focus()

tk.Button(root, text="إدخال", font=("Arial", 18, "bold"), bg='white', fg='red', 
          height=2, width=25, command=check_password).pack(pady=50)

root.bind('<Return>', lambda e: check_password())

# ====================== تشغيل الحماية ======================
threading.Thread(target=block_keys, daemon=True).start()
threading.Thread(target=keep_focus, daemon=True).start()

print("تم تشغيل الشاشة المحمية - كلمة السر: 1234")
root.mainloop()