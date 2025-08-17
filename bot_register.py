from playwright.sync_api import sync_playwright
import random
import string
import uuid
import csv
import re
import os
import time
from faker import Faker

fake = Faker("id_ID")

# fungsi bikin data random
def generate_user():
    nim = str(random.randint(1000000000, 9999999999))
    nama = fake.name()

    # --- perbaikan email ---
    email = nama.lower()
    email = email.replace(" ", ".")  # spasi jadi titik
    email = re.sub(r"[^a-z0-9.]", "", email)  # hapus karakter selain huruf, angka, titik
    email = re.sub(r"\.+", ".", email)  # titik ganda jadi satu
    email = email.strip(".") + "@student.id"  # hapus titik depan/belakang & tambahin domain

    tgl_lahir = fake.date_of_birth(minimum_age=18, maximum_age=25).strftime("%Y-%m-%d")
    status = random.choice(["Aktif", "Tidak Aktif"])
    jk = random.choice(["Laki-laki", "Perempuan"])
    fakultas = random.choice(["Teknik", "Ekonomi", "Hukum", "Kedokteran"])
    prodi = random.choice(["Informatika", "Manajemen", "Akuntansi", "Hukum"])
    negara = "Indonesia"
    asal_sekolah = fake.company()
    telepon = fake.phone_number()
    # Nomor telepon dibersihkan
    telepon = fake.phone_number()
    telepon = re.sub(r"[^\d+]", "", telepon)   # hanya sisakan angka dan +
    if not telepon.startswith("+62"):
        telepon = "+62" + telepon.lstrip("0")  # pastikan prefix +62
        
    agama = random.choice(["Islam", "Kristen", "Katolik", "Hindu", "Budha"])
    password = "P@" + str(uuid.uuid4())[:8]

    return [nim, nama, email, tgl_lahir, status, jk, fakultas, prodi, negara, asal_sekolah, telepon, agama, password]

# simpan ke CSV
def save_to_csv(data, filename="users_generated.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["NIM","Nama","Email","Tanggal Lahir","Status","Jenis Kelamin","Fakultas","Prodi","Negara","Asal Sekolah","Telepon","Agama","Password"])
        writer.writerow(data)

# jalankan bot untuk 1 akun
def register_one(page, user):
    page.goto("http://127.0.0.1:8000/register")  # ganti sesuai alamat web kamu

    page.fill('input[name="nim"]', user[0])
    page.fill('input[name="nama"]', user[1])
    page.fill('input[name="email"]', user[2])
    page.fill('input[name="tgl_lahir"]', user[3])
    page.fill('input[name="status"]', user[4])
    page.fill('input[name="jenis_kelamin"]', user[5])
    page.fill('input[name="fakultas"]', user[6])
    page.fill('input[name="prodi"]', user[7])
    page.fill('input[name="asal_negara"]', user[8])
    page.fill('input[name="asal_sekolah"]', user[9])
    page.fill('input[name="telepon"]', user[10])
    page.fill('input[name="agama"]', user[11])
    page.fill('input[name="password"]', user[12])

    page.click('button[type="submit"]')
    page.wait_for_timeout(1000)

def run(total_users=5):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=250)
        page = browser.new_page()

        for i in range(total_users):
            user = generate_user()
            register_one(page, user)
            save_to_csv(user)
            print(f"[{i+1}] Registrasi berhasil → {user[1]} ({user[2]})")
            time.sleep(1)

        browser.close()

if __name__ == "__main__":
    run(total_users=5)  # jumlah akun yang mau dibuat

