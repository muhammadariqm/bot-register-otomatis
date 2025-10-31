from playwright.sync_api import sync_playwright
import random
import time
from faker import Faker

fake = Faker("id_ID")

def generate_feedback():
    nama = fake.name()
    email = "ibnurdk1325@gmail.com"  # email tetap
    sebagai = random.choice(["PESERTA", "PANITIA", "PEMATERI"])
    message = fake.paragraph(nb_sentences=2)
    return nama, email, sebagai, message

def isi_feedback(page, data):
    nama, email, sebagai, message = data

    # buka halaman feedback
    page.goto("http://127.0.0.1:8000/feedback", wait_until="domcontentloaded")
    page.wait_for_selector('#feedback-form', state='visible')

    # isi input nama & email
    page.fill('input[name="participant_name"]', nama)
    page.fill('input[name="email"]', email)

    # scroll agar dropdown terlihat
    page.evaluate("window.scrollBy(0, 400)")
    page.wait_for_timeout(500)

    # pastikan select terlihat dan aktif
    page.evaluate("""
        () => {
            const select = document.querySelector('select[name="sebagai"]');
            if (select) {
                select.style.display = 'block';
                select.removeAttribute('hidden');
            }
        }
    """)

    # pilih salah satu opsi "sebagai"
    page.select_option('select[name="sebagai"]', label=sebagai)

    # isi pesan
    page.fill('textarea[name="message"]', message)

    # pastikan tombol submit terlihat lalu klik via JavaScript agar pasti berhasil
    page.evaluate("""
        () => {
            const btn = document.querySelector('#feedback-form button[type="submit"]');
            if (btn) {
                btn.scrollIntoView({behavior: 'smooth', block: 'center'});
                btn.click();
            }
        }
    """)

    # tunggu proses submit selesai
    page.wait_for_timeout(4000)

    print(f"✅ Feedback terkirim dari: {nama} ({sebagai})")

def run(total_feedback=5):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        for i in range(total_feedback):
            data = generate_feedback()
            isi_feedback(page, data)
            time.sleep(1)

        browser.close()

if __name__ == "__main__":
    run(total_feedback=50)  # jumlah feedback yang mau dikirim
