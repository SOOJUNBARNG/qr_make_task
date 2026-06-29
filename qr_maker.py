import qrcode
import os

def make_qr(url: str, filename: str = None) -> str:
    if not filename:
        safe = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")
        filename = f"qr_{safe[:40]}.png"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    return filename


if __name__ == "__main__":
    print("=== QR Code Maker ===")
    while True:
        url = input("\nEnter URL (or 'q' to quit): ").strip()
        if url.lower() == "q":
            break
        if not url.startswith("http"):
            url = "https://" + url

        name = input("Save as (leave blank for auto): ").strip() or None
        saved = make_qr(url, name)
        print(f"✅ Saved: {os.path.abspath(saved)}")
