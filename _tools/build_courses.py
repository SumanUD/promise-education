"""Generate courses/<slug>.html for every course in courses.json, and rebuild
the course grid on class.html.

Content lives in courses.json only — edit that, re-run this, commit the output.

    python _tools/build_courses.py
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
COURSE_DIR = os.path.join(ROOT, "courses")
WHATSAPP = "https://wa.me/919830153484"

with open(os.path.join(HERE, "courses.json"), encoding="utf-8") as fh:
    COURSES = json.load(fh)


def shell_from_index():
    """Reuse index.html's navbar and footer so every page shares one shell."""
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    nav = src[src.index("<!-- Navbar Start -->"):src.index("<!-- Navbar End -->") + len("<!-- Navbar End -->")]
    tail = src[src.index("<!-- Footer Start -->"):]
    return nav, tail


def to_subdir(markup):
    """Rewrite root-relative asset and page links for pages one level down."""
    markup = re.sub(r'(?<=")(img/|css/|js/|lib/)', r"../\1", markup)
    markup = re.sub(r'(?<=href=")([a-z-]+\.html)', r"../\1", markup)
    return markup


NAV, TAIL = shell_from_index()
NAV = to_subdir(NAV).replace(
    '<a href="../class.html" class="nav-item nav-link">',
    '<a href="../class.html" class="nav-item nav-link active">',
)
NAV = NAV.replace(' class="nav-item nav-link active">Home', ' class="nav-item nav-link">Home')
TAIL = to_subdir(TAIL)

PAGE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{name} — Promise Centre for Education, Kolkata</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <meta content="{desc}" name="description" />
    <link rel="canonical" href="https://promise-education.netlify.app/courses/{slug}.html" />

    <meta property="og:type" content="article" />
    <meta property="og:site_name" content="Promise Centre for Education &amp; International Studies" />
    <meta property="og:title" content="{name} — Promise Centre for Education" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:image" content="https://promise-education.netlify.app/img/{image}" />
    <meta property="og:url" content="https://promise-education.netlify.app/courses/{slug}.html" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{name} — Promise Centre for Education" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="https://promise-education.netlify.app/img/{image}" />

    <link href="../img/LOGO.png" rel="icon" />

    <link rel="preconnect" href="https://fonts.gstatic.com" />
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.0/css/all.min.css" rel="stylesheet" />
    <link href="../lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet" />
    <link href="../lib/lightbox/css/lightbox.min.css" rel="stylesheet" />
    <link href="../css/style.css" rel="stylesheet" />
  </head>

  <body>
    {nav}

    <!-- Page Header Start -->
    <div class="page-header container-fluid text-center">
      <div class="container">
        <h1>{name}</h1>
        <p>{tagline}</p>
        <p class="breadcrumb-line m-0"><a href="../index.html">Home</a> / <a href="../class.html">Courses</a> / {name}</p>
      </div>
    </div>
    <!-- Page Header End -->

    <!-- Course Detail Start -->
    <div class="container-fluid section">
      <div class="container">
        <div class="row">
          <div class="col-lg-5 mb-5 mb-lg-0">
            <div class="poster-mount">
              <figure class="poster-card m-0">
                <img src="../img/{image}" alt="{name} at Promise Centre for Education" />
                <figcaption>{name} <small>{meta_short}</small></figcaption>
              </figure>
            </div>
          </div>
          <div class="col-lg-7 pl-lg-5">
            <p class="section-title"><span>About this programme</span></p>
            <h2 class="mb-4">{tagline}</h2>
            <p>{summary}</p>

            <h3 class="mt-5 mb-3">What your child will learn</h3>
            <ul class="tick-list mb-5">
{learn_items}
            </ul>

            <h3 class="mb-3">Quick facts</h3>
            <table class="table mb-4">
              <tbody>
{fact_rows}
              </tbody>
            </table>
            {note}
            <p class="text-muted"><i class="fas fa-info-circle mr-2"></i>Fees depend on level, batch and mode. Ask us for the current fee for this programme.</p>
          </div>
        </div>
      </div>
    </div>
    <!-- Course Detail End -->

    <!-- Enquiry Start -->
    <div class="container-fluid section bg-light">
      <div class="container">
        <div class="row align-items-start">
          <div class="col-lg-5 mb-5 mb-lg-0">
            <p class="section-title"><span>Enquire</span></p>
            <h2 class="mb-3">Ask about {name}</h2>
            <p>
              Tell us your child's age and what you are hoping this programme will change.
              We will come back with the right level, the next batch date and the fee.
            </p>
            <a href="{whatsapp}" target="_blank" rel="noopener" class="btn btn-secondary py-3 px-5 mt-2">
              <i class="fab fa-whatsapp mr-2"></i>Message us on WhatsApp
            </a>
            <p class="mt-4 mb-0"><strong>Or call</strong><br />
              <a href="tel:+919830153484">+91 98301 53484</a> · <a href="tel:+919330932848">+91 93309 32848</a>
            </p>
          </div>
          <div class="col-lg-7 pl-lg-5">
            <div class="enquiry-panel">
              <h3>Course enquiry</h3>
              <p class="mb-4">We usually reply the same day.</p>
              <form name="course-enquiry" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="../thanks.html">
                <input type="hidden" name="form-name" value="course-enquiry" />
                <p class="d-none"><label>Leave this empty <input name="bot-field" /></label></p>
                <input type="hidden" name="course" value="{name}" />
                <div class="form-row">
                  <div class="form-group col-md-6">
                    <label for="parent">Parent's name</label>
                    <input type="text" class="form-control p-3" id="parent" name="parent" placeholder="Your full name" required />
                  </div>
                  <div class="form-group col-md-6">
                    <label for="phone">Phone or WhatsApp</label>
                    <input type="tel" class="form-control p-3" id="phone" name="phone" placeholder="10-digit mobile number" required />
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group col-md-6">
                    <label for="student">Student's name</label>
                    <input type="text" class="form-control p-3" id="student" name="student" placeholder="Your child's name" />
                  </div>
                  <div class="form-group col-md-6">
                    <label for="age">Age or class</label>
                    <input type="text" class="form-control p-3" id="age" name="age" placeholder="e.g. 9 years / Class IV" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="email">Email <span class="text-muted">(optional)</span></label>
                  <input type="email" class="form-control p-3" id="email" name="email" placeholder="you@example.com" />
                </div>
                <div class="form-group">
                  <label for="message">Anything else we should know?</label>
                  <textarea class="form-control p-3" rows="4" id="message" name="message" placeholder="Preferred timings, what you would like to see improve, questions about the level…"></textarea>
                </div>
                <button class="btn btn-primary py-3 px-5" type="submit">Send enquiry</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Enquiry End -->

    <!-- Other Courses Start -->
    <div class="container-fluid section">
      <div class="container">
        <div class="text-center">
          <p class="section-title"><span>Also at Promise</span></p>
          <h2 class="mb-5">Other programmes</h2>
        </div>
        <div class="row">
{others}
        </div>
        <div class="text-center mt-4">
          <a href="../class.html" class="btn btn-outline-primary py-2 px-4">See all courses</a>
        </div>
      </div>
    </div>
    <!-- Other Courses End -->

    {tail}
"""


def card(course, prefix=""):
    metas = "".join(f"<li>{html.escape(m)}</li>" for m in course["meta"])
    return f"""          <div class="col-lg-3 col-md-6 mb-4">
            <a class="course-card" href="{prefix}courses/{course['slug']}.html">
              <img class="course-thumb" src="{prefix}img/{course['image']}" alt="{html.escape(course['name'])}" />
              <div class="course-body">
                <h4>{html.escape(course['name'])}</h4>
                <p>{html.escape(course['tagline'])}</p>
                <ul class="course-meta">{metas}</ul>
                <span class="course-link">View programme <i class="fas fa-arrow-right ml-1"></i></span>
              </div>
            </a>
          </div>"""


os.makedirs(COURSE_DIR, exist_ok=True)

for course in COURSES:
    others = [c for c in COURSES if c["slug"] != course["slug"]][:4]
    note = course["note"]
    note_html = (
        f'<p class="mb-4"><i class="fas fa-star text-primary mr-2"></i>{html.escape(note)}</p>\n            '
        if note
        else ""
    )
    page = PAGE.format(
        name=html.escape(course["name"]),
        slug=course["slug"],
        image=course["image"],
        tagline=html.escape(course["tagline"]),
        desc=html.escape(course["summary"][:180].rsplit(" ", 1)[0] + "…"),
        summary=html.escape(course["summary"]),
        meta_short=html.escape(" · ".join(course["meta"])),
        learn_items="\n".join(f"              <li>{html.escape(x)}</li>" for x in course["learn"]),
        fact_rows="\n".join(
            f"                <tr><th scope=\"row\" style=\"width: 34%\">{html.escape(k)}</th><td>{html.escape(v)}</td></tr>"
            for k, v in course["facts"]
        ),
        note=note_html,
        others="\n".join(card(c, prefix="../") for c in others),
        whatsapp=WHATSAPP,
        nav=NAV,
        tail=TAIL,
    )
    out = os.path.join(COURSE_DIR, f"{course['slug']}.html")
    open(out, "w", encoding="utf-8").write(page)
    print(f"  courses/{course['slug']}.html")

# --- rebuild the grid on class.html -----------------------------------------
grid = "\n".join(card(c) for c in COURSES)
class_path = os.path.join(ROOT, "class.html")
src = open(class_path, encoding="utf-8").read()
start = "<!-- COURSE GRID START -->"
end = "<!-- COURSE GRID END -->"
if start in src:
    i = src.index(start) + len(start)
    j = src.index(end)
    src = src[:i] + "\n" + grid + "\n        " + src[j:]
    open(class_path, "w", encoding="utf-8").write(src)
    print("  class.html grid rebuilt")
else:
    print("  class.html has no COURSE GRID markers — skipped")
