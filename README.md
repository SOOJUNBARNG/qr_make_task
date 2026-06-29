# qr_make_task

A simple toolkit for generating QR codes and building Q&A survey pages.

---

## Files

| File | Description |
|------|-------------|
| `qr_maker.py` | CLI tool — input a URL, get a QR code PNG |
| `make_survey.py` | Generates `survey.html` from a question list |
| `survey.html` | The output survey page (open in browser) |
| `index.html` | Original QR + medical intake form (Japanese) |

---

## Requirements

```bash
pip install qrcode[pil]
```

---

## 1. Generate a QR Code

```bash
python3 qr_maker.py
```

- Enter any URL when prompted
- Optionally give the output file a custom name
- A `.png` QR code is saved in the current directory
- Type `q` to quit

**Example:**
```
Enter URL (or 'q' to quit): https://example.com
Save as (leave blank for auto): my_qr
✅ Saved: /your/path/my_qr.png
```

---

## 2. Build a Survey Page

Edit the `questions` list in `make_survey.py`:

```python
questions = [
    {
        "text": "Your question here?",
        "type": "radio",          # radio | checkbox | textarea
        "options": ["Option A", "Option B"],
    },
    ...
]
```

Then run:

```bash
python3 make_survey.py
```

This regenerates `survey.html`. Open it in any browser — no server needed.

**Question types:**

| type | use for |
|------|---------|
| `radio` | single choice |
| `checkbox` | multiple choice |
| `textarea` | free text (optional, never blocks Next) |

---

## 3. Open the Survey

Just double-click `survey.html` or open it in a browser:

```bash
open survey.html       # macOS
start survey.html      # Windows
xdg-open survey.html   # Linux
```
