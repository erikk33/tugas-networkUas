import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import email
from email.header import decode_header
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time  # Pastikan modul time diimpor
#erik
# Informasi login email pengirim yang sudah diberikan
email_pengirim = 'erikxzc@gmail.com'  # Ganti dengan email Anda
sandi_aplikasi = 'hczloeikihwvnlvo'  # Ganti dengan sandi aplikasi Anda
imap_server = 'imap.gmail.com'  # Server IMAP untuk Gmail
imap_port = 993  # Port IMAP untuk Gmail

# Fungsi untuk mengirim email
def kirim_email(email_pengirim, sandi_aplikasi, email_penerima, subject, body_email):
    try:
        # Membuat objek MIMEMultipart
        msg = MIMEMultipart()
        msg['From'] = email_pengirim
        msg['To'] = email_penerima
        msg['Subject'] = subject

        # Menambahkan body email ke pesan
        msg.attach(MIMEText(body_email, 'plain'))

        # Menghubungi server SMTP Gmail dan mengirim email
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Server SMTP untuk Gmail
        server.starttls()
        server.login(email_pengirim, sandi_aplikasi)
        text = msg.as_string()
        server.sendmail(email_pengirim, email_penerima, text)
        server.quit()

        messagebox.showinfo("Sukses", "Email berhasil dikirim!")
    except Exception as e:
        messagebox.showerror("Gagal", f'Gagal mengirim email. Error: {e}')
#dimas
# Fungsi untuk mengambil email
def terima_email(email_pengirim, sandi_aplikasi):
    try:
        # Menghubungi server IMAP Gmail
        mail = imaplib.IMAP4_SSL(host=imap_server, port=imap_port)
        mail.login(email_pengirim, sandi_aplikasi)
        
        # Memilih inbox
        mail.select("inbox")
        
        # Mencari semua email di inbox
        status, messages = mail.search(None, "ALL")
        
        # Mendapatkan daftar ID email
        email_ids = messages[0].split()
        print(f"Number of emails: {len(email_ids)}")

        # Mengambil email terbaru
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")
                
                email_body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                            try:
                                email_body = part.get_payload(decode=True).decode()
                            except Exception as e:
                                print("Error decoding body:", e)
                else:
                    email_body = msg.get_payload(decode=True).decode()
                
                # Menampilkan email dalam GUI
                email_list.insert(0, f"From: {from_}\nSubject: {subject}\n\nBody:\n{email_body}")

        # Menutup koneksi dan logout
        mail.close()
        mail.logout()
    except Exception as e:
        messagebox.showerror("Gagal", f'Gagal menerima email. Error: {e}')

#yayan
# Fungsi untuk memperbarui email terbaru
def update_email():
    while True:
        terima_email(email_pengirim, sandi_aplikasi)
        time.sleep(3)  # Periksa email baru setiap 3 detik

# Fungsi untuk menampilkan isi email
def show_email(event):
    selected_email = email_list.get(email_list.curselection())
    messagebox.showinfo("Isi Email", selected_email)

# Fungsi untuk menangani menu
def klik_menu(choice):
    if choice == "1":
        kirim_email_menu()
    elif choice == "2":
        start_realtime_email_check()
    elif choice == "3":
        root.quit()

#ilham
# Fungsi untuk memulai pengecekan email real-time
def start_realtime_email_check():
    threading.Thread(target=update_email, daemon=True).start()

# Fungsi untuk menampilkan menu Kirim Email
def kirim_email_menu():
    window = tk.Toplevel(root)
    window.title("Kirim Email")

    tk.Label(window, text="Email Pengirim:").grid(row=0, column=0, sticky=tk.W)
    label_email_pengirim = tk.Label(window, text=email_pengirim, width=50, anchor='w')
    label_email_pengirim.grid(row=0, column=1)

    tk.Label(window, text="Email Penerima:").grid(row=1, column=0, sticky=tk.W)
    entry_email_penerima = tk.Entry(window, width=50)
    entry_email_penerima.grid(row=1, column=1)

    tk.Label(window, text="Subject:").grid(row=2, column=0, sticky=tk.W)
    entry_subject = tk.Entry(window, width=50)
    entry_subject.grid(row=2, column=1)

    tk.Label(window, text="Body Email:").grid(row=3, column=0, sticky=tk.W)
    text_body_email = scrolledtext.ScrolledText(window, height=15, width=50)
    text_body_email.grid(row=3, column=1)

    def klik_kirim():
        email_penerima = entry_email_penerima.get()
        subject = entry_subject.get()
        body_email = text_body_email.get("1.0", tk.END)
        kirim_email(email_pengirim, sandi_aplikasi, email_penerima, subject, body_email)
        window.destroy()

    tk.Button(window, text="Kirim", command=klik_kirim).grid(row=4, column=1, sticky=tk.E)
#kemal
# Membuat GUI utama dengan tkinter
root = tk.Tk()
root.title("Email Client")

tk.Label(root, text="Pilih Menu:").pack()

tk.Button(root, text="1. Kirim Email", command=lambda: klik_menu("1")).pack(fill='x')
tk.Button(root, text="2. Terima Email", command=lambda: klik_menu("2")).pack(fill='x')
tk.Button(root, text="3. Keluar Program", command=lambda: klik_menu("3")).pack(fill='x')

# Listbox untuk menampilkan email
email_list = tk.Listbox(root, height=15, width=100)
email_list.pack(fill='both', expand=True)
email_list.bind('<<ListboxSelect>>', show_email)

root.mainloop()