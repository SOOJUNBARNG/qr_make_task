import qrcode

# URL you want to link to
url = "https://hatogaya-jotform.web.app/"

# Generate QR code
qr = qrcode.make(url)

# Save the QR code image
qr.save("qr_link.png")

print("✅ QR code saved as 'qr_link.png'")
