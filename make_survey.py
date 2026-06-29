questions = [
    {
        "text": "How did you hear about us?",
        "type": "radio",
        "options": ["Social media", "Friend / referral", "Search engine", "Other"],
    },
    {
        "text": "How satisfied are you with our service?",
        "type": "radio",
        "options": ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied"],
    },
    {
        "text": "Which features do you use? (select all that apply)",
        "type": "checkbox",
        "options": ["QR generator", "Survey tool", "Analytics", "Sharing"],
    },
    {
        "text": "Any feedback or suggestions?",
        "type": "textarea",
        "options": [],
    },
]


def build_question_html(i, q):
    n = i + 1
    options_html = ""

    if q["type"] in ("radio", "checkbox"):
        items = "".join(
            f'<label><input type="{q["type"]}" name="q{n}" value="{o}"> {o}</label>\n'
            for o in q["options"]
        )
        options_html = f'<div class="options">\n{items}</div>'
    elif q["type"] == "textarea":
        options_html = (
            '<div class="options">'
            f'<textarea name="q{n}" placeholder="Write anything here..."></textarea>'
            "</div>"
        )

    return f"""
  <div class="question {'active' if i == 0 else ''}" id="q{n}">
    <p>{n}. {q["text"]}</p>
    {options_html}
  </div>"""


def build_html(questions, title="Quick Survey", output="survey.html"):
    total = len(questions)
    labels_js = ", ".join(f'"{q["text"]}"' for q in questions)
    checkbox_qs = {i + 1 for i, q in enumerate(questions) if q["type"] == "checkbox"}
    textarea_qs = {i + 1 for i, q in enumerate(questions) if q["type"] == "textarea"}

    get_answer_cases = ""
    for n in range(1, total + 1):
        if n in checkbox_qs:
            get_answer_cases += f"""
    if (qNum === {n}) {{
      const checked = [...document.querySelectorAll(`input[name="q{n}"]:checked`)];
      return checked.map(el => el.value).join(", ") || null;
    }}"""
        elif n in textarea_qs:
            get_answer_cases += f"""
    if (qNum === {n}) {{
      const val = document.querySelector(`textarea[name="q{n}"]`).value.trim();
      return val || null;
    }}"""

    questions_html = "".join(build_question_html(i, q) for i, q in enumerate(questions))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: sans-serif; background: #f5f5f5; display: flex; justify-content: center; padding: 40px 16px; }}
    .card {{ background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 32px; max-width: 560px; width: 100%; }}
    h1 {{ font-size: 1.4rem; margin-bottom: 24px; color: #222; }}
    .progress {{ background: #eee; border-radius: 99px; height: 6px; margin-bottom: 28px; }}
    .progress-bar {{ background: #4f46e5; height: 6px; border-radius: 99px; transition: width 0.3s; }}
    .question {{ display: none; }}
    .question.active {{ display: block; }}
    .question p {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 16px; color: #333; }}
    .options {{ display: flex; flex-direction: column; gap: 10px; }}
    .options label {{ display: flex; align-items: center; gap: 10px; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 8px; cursor: pointer; transition: border-color 0.15s, background 0.15s; }}
    .options label:hover {{ border-color: #4f46e5; background: #f0f0ff; }}
    .options input[type="radio"], .options input[type="checkbox"] {{ accent-color: #4f46e5; width: 18px; height: 18px; }}
    .options input[type="text"], .options textarea {{ width: 100%; padding: 10px 14px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 1rem; outline: none; transition: border-color 0.15s; }}
    .options input[type="text"]:focus, .options textarea:focus {{ border-color: #4f46e5; }}
    .options textarea {{ resize: vertical; min-height: 80px; }}
    .nav {{ display: flex; justify-content: space-between; margin-top: 28px; }}
    button {{ padding: 10px 24px; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: background 0.15s; }}
    .btn-back {{ background: #e5e7eb; color: #333; }}
    .btn-back:hover {{ background: #d1d5db; }}
    .btn-next {{ background: #4f46e5; color: white; }}
    .btn-next:hover {{ background: #4338ca; }}
    .result {{ display: none; text-align: center; }}
    .result h2 {{ font-size: 1.5rem; margin-bottom: 12px; color: #4f46e5; }}
    .result p {{ color: #555; margin-bottom: 20px; }}
    .result ul {{ text-align: left; list-style: none; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }}
    .result ul li {{ padding: 10px 16px; border-bottom: 1px solid #e5e7eb; font-size: 0.9rem; }}
    .result ul li:last-child {{ border-bottom: none; }}
    .result ul li span {{ font-weight: 600; color: #333; }}
  </style>
</head>
<body>
<div class="card">
  <h1>{title}</h1>
  <div class="progress"><div class="progress-bar" id="bar"></div></div>
  {questions_html}
  <div class="result" id="result">
    <h2>Thank you! 🎉</h2>
    <p>Your answers have been recorded.</p>
    <ul id="summary"></ul>
  </div>
  <div class="nav">
    <button class="btn-back" id="backBtn" onclick="navigate(-1)" style="visibility:hidden">Back</button>
    <button class="btn-next" id="nextBtn" onclick="navigate(1)">Next</button>
  </div>
</div>
<script>
  const total = {total};
  let current = 1;

  function updateUI() {{
    document.getElementById("bar").style.width = ((current - 1) / total * 100) + "%";
    document.getElementById("backBtn").style.visibility = current > 1 ? "visible" : "hidden";
    document.getElementById("nextBtn").textContent = current === total ? "Submit" : "Next";
  }}

  function getAnswer(qNum) {{
    {get_answer_cases}
    const sel = document.querySelector(`input[name="q${{qNum}}"]:checked`);
    return sel ? sel.value : null;
  }}

  function navigate(dir) {{
    if (dir === 1) {{
      const ans = getAnswer(current);
      const isTextarea = {str(sorted(textarea_qs))}.includes(current);
      if (!isTextarea && !ans) {{ alert("Please answer before continuing."); return; }}
      if (current === total) {{ showResult(); return; }}
    }}
    document.getElementById(`q${{current}}`).classList.remove("active");
    current += dir;
    document.getElementById(`q${{current}}`).classList.add("active");
    updateUI();
  }}

  function showResult() {{
    const labels = [{labels_js}];
    const ul = document.getElementById("summary");
    ul.innerHTML = "";
    for (let i = 1; i <= total; i++) {{
      const ans = getAnswer(i) || "(skipped)";
      const li = document.createElement("li");
      li.innerHTML = `<span>${{labels[i-1]}}:</span> ${{ans}}`;
      ul.appendChild(li);
    }}
    for (let i = 1; i <= total; i++) document.getElementById(`q${{i}}`).style.display = "none";
    document.getElementById("result").style.display = "block";
    document.querySelector(".nav").style.display = "none";
    document.getElementById("bar").style.width = "100%";
  }}

  updateUI();
</script>
</body>
</html>"""

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Generated: {output}  ({total} questions)")


if __name__ == "__main__":
    build_html(questions, title="Quick Survey", output="survey.html")
