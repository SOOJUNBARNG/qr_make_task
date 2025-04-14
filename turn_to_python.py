import qrcode
import base64

# Step 1: Read the HTML file
with open("first_html.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Step 2: Encode HTML as base64
encoded_html = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")

# Step 3: Create a data URL
data_url = f"data:text/html;base64,{encoded_html}"

# Step 4: Generate QR code
qr = qrcode.make(data_url)

# Step 5: Save the QR image
qr.save("first_html_qr.png")

print("✅ QR code saved as 'first_html_qr.png'")
