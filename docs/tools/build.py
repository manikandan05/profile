#!/usr/bin/env python3
"""Generates the static pages for the profile site.

Usage: python3 tools/build.py   (run from the manikandan-profile folder)
Icons are Phosphor (MIT) copied into tools/icons and inlined as an SVG sprite.
"""
import html
import json
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent
ICONS = pathlib.Path(__file__).resolve().parent / "icons"
BASE = "https://manikandan05.github.io"
EMAIL = "mani_kandan05@yahoo.com"
LINKEDIN = "https://www.linkedin.com/in/manikandan-mariappan-758b9676/"
DEVTO = "https://dev.to/manikandan"
GITHUB = "https://github.com/manikandan05"
TIMELINE = "https://manikandan05.github.io/profile"
MAILTO = f"mailto:{EMAIL}?subject=Architecture%20conversation"


def sprite():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">']
    for f in sorted(ICONS.glob("*.svg")):
        s = f.read_text()
        inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
        out.append(f'<symbol id="i-{f.stem}" viewBox="0 0 256 256">{inner}</symbol>')
    out.append("</svg>")
    return "".join(out)


def ic(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def tags(items):
    return '<ul class="tags">' + "".join(f'<li class="tag caption-4">{esc(x)}</li>' for x in items) + "</ul>"


THEME_BOOT = (
    '<script>(function(){var r=document.documentElement;r.classList.add("js");'
    'var c="dark";try{var s=localStorage.getItem("theme");if(s==="light"||s==="dark"||s==="system")c=s}catch(e){}'
    'var t=c==="system"?(matchMedia("(prefers-color-scheme: light)").matches?"light":"dark"):c;'
    'r.setAttribute("data-theme",t);r.setAttribute("data-theme-pref",c)})()</script>'
)


def theme_switch(extra_cls=""):
    opts = [("light", "sun", "Light theme"), ("dark", "moon", "Dark theme"), ("system", "desktop", "System theme")]
    btns = "".join(
        f'<button class="theme-btn" type="button" data-theme-choice="{k}" aria-pressed="false" aria-label="{l}" title="{l}">{ic(i, "icon icon-sm")}</button>'
        for k, i, l in opts
    )
    return f'<div class="theme-switch {extra_cls}" role="group" aria-label="Theme">{btns}</div>'


def head(title, desc, path, extra="", robots="index,follow"):
    url = f"{BASE}/{path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#000000">
<link rel="canonical" href="{url}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/Geist-Variable.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="website">
<meta property="og:site_name" content="Manikandan M">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta property="og:image:alt" content="Manikandan M, software architect for secure and compliant systems">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/assets/og.png">
{THEME_BOOT}
<link rel="stylesheet" href="styles.css">
{extra}
</head>"""


NAV_ITEMS = [("impact", "Impact"), ("work", "Work"), ("credentials", "Credentials"), ("writing", "Writing"), ("faq", "FAQ")]


def nav():
    links = "".join(f'<li><a class="nav-link title-4" href="#{i}">{l}</a></li>' for i, l in NAV_ITEMS)
    menu = "".join(f'<a class="menu-link heading-4" style="--i:{n}" href="#{i}">{l}</a>' for n, (i, l) in enumerate(NAV_ITEMS))
    return f"""<header>
<nav class="nav" aria-label="Primary">
<a class="brand title-4" href="#top" aria-label="Manikandan M, back to top">{ic("shield-check", "brand-mark")}<span>Manikandan M</span></a>
<ul class="nav-links">{links}</ul>
<a class="btn btn-sm button-sm nav-cta" href="#contact">Start a conversation</a>
{theme_switch("nav-theme")}
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu"><span class="bar"></span><span class="bar"></span></button>
</nav>
<div class="menu" id="menu" aria-label="Mobile menu">
{menu}
<a class="btn button-md" style="--i:5" href="#contact">Start a conversation {ic("arrow-right", "icon icon-sm")}</a>
<div class="menu-item" style="--i:6"><p class="caption-3 muted menu-label">Theme</p>{theme_switch("menu-theme")}</div>
</div>
</header>"""


def footer():
    return f"""<footer class="footer">
<div class="container footer-inner">
<div class="footer-meta">
<p class="title-3">Manikandan M</p>
<p class="caption-2 muted">Software architect, data security and compliance. Based in Sivakasi, India.</p>
<small class="caption-2">© 2026 Manikandan M. Views are my own and do not represent IBM.</small>
</div>
<ul class="footer-links body-5">
<li><a href="{LINKEDIN}" rel="noopener">{ic("linkedin-logo", "icon icon-sm")} LinkedIn</a></li>
<li><a href="{GITHUB}" rel="noopener">{ic("github-logo", "icon icon-sm")} GitHub</a></li>
<li><a href="{DEVTO}" rel="noopener">{ic("article", "icon icon-sm")} Dev.to</a></li>
<li><a href="privacy.html">Privacy policy</a></li>
<li><a href="terms.html">Terms</a></li>
</ul>
</div>
</footer>"""


def page_shell(title, desc, path, body, robots="index,follow", extra=""):
    return head(title, desc, path, extra, robots) + f"""
<body>
{sprite()}
{body}
</body>
</html>
"""


# ---------------- Content ----------------

STATS = [
    ("14+", "Years building software", "Full stack engineering since 2013"),
    ("4+", "Years in IBM security engineering", "Aegis platform team since October 2022"),
    ("1,400+", "Products onboarded each day", "Through the Concert data broker, with zero data loss"),
    ("95%", "Unit test coverage", "Raised across the full Aegis codebase"),
    ("25+", "Technical articles", "Published on Dev.to"),
    ("{badges}", "Digital badges", "IBM credentials and awards"),
]

PIPE = [
    ("code", "Static analysis", "SonarQube Enterprise"),
    ("bug", "Dynamic API testing", "OWASP ZAP"),
    ("detective", "Interactive testing", "IAST at runtime"),
    ("package", "Dependency scanning", "Mend OSS and SAST"),
    ("cube", "Container images", "Twistlock on Kubernetes"),
    ("scales", "Open source clearance", "CSAR, APR, CoO, OSSC"),
]

BENEFITS = [
    ("flow-arrow", "Security gates in every pipeline", "Static, dynamic, interactive, dependency and container scans run inside CI/CD, so teams see findings before release."),
    ("clipboard-text", "Audit evidence on demand", "A Twistlock scanner for product Kubernetes clusters produced OS and application level reports that helped teams through SOC\u00a02 audits."),
    ("shield-checkered", "One view of security posture", "Aegis brings vulnerability tracking, compliance scorecards, PSIRT, ITSS and SPbD boards into one place."),
    ("scales", "Legal and open source checks automated", "CSAR automation turned a manual legal step into a delivery check for Abbreviated Pedigree Reviews, Certificates of Originality and OSSC clearances."),
    ("queue", "Architecture that holds at scale", "A queue backed broker onboards 1,400+ products a day into IBM Concert with zero data loss."),
]

STEPS = [
    ("01", "Map the risk", "Start from the data, the services and the controls your auditors ask about. Decide which scans and policies matter first."),
    ("02", "Automate the controls", "Wire scanners, policy checks and reporting into the pipeline as self service tooling that product teams can adopt without a ticket."),
    ("03", "Report in one place", "Normalize results into a single dashboard so engineers, security leads and executives read the same facts."),
]

WORK = [  # newest first
    ("Oct 2026", "OpenDataBridge", "An open source project that unifies pagination, authentication, error recovery and rate limits across Jira, GitHub Enterprise, ServiceNow and custom endpoints.", ["Open source", "APIs", "Hacktoberfest"], "plugs-connected"),
    ("Sep 2026", "GitHub compliance analyzer", "A proof of concept for repository policy and compliance analysis, built with and approved by the IBM CISO organization.", ["Policy checks", "GitHub", "CISO"], "git-branch"),
    ("Apr 2026", "Concert data broker", "A queue backed broker with onboarding screens and transformation stages, handling 1,400+ product records a day with zero data loss.", ["IBM Concert", "Queues", "Data broker"], "queue"),
    ("Dec 2025", "Open source and legal compliance", "End to end automation around CSAR for Abbreviated Pedigree Reviews, Certificates of Originality and OSSC open source clearances.", ["CSAR", "APR", "OSSC"], "scales"),
    ("Apr 2025", "Runtime security testing", "IAST automation that instruments running applications to catch business logic flaws and multi stage injection that static and external dynamic scans miss.", ["IAST", "AppSec", "Runtime"], "detective"),
    ("Jan 2025", "Dependency and SAST ingestion", "A pipeline that pulls Mend OSS and Mend SAST findings into Aegis dashboards and removes manual dependency reviews.", ["Mend", "SCA", "Data pipeline"], "package"),
    ("May 2024", "Enterprise static analysis", "A SonarQube Enterprise automation framework for bugs, code smells and vulnerabilities, with portfolio and executive views.", ["SonarQube", "SAST", "Reporting"], "code"),
    ("Feb 2024", "Self service API security testing", "An OWASP ZAP automation framework. Teams plug in API endpoints and get scripted attacks and scan reports before production.", ["OWASP ZAP", "DAST", "CI/CD"], "bug"),
    ("Oct 2023", "Container and cluster scanning", "A Twistlock (Prisma Cloud) scanner for product Kubernetes clusters, covering OS and application level images and surfacing critical CVEs and misconfigurations.", ["Twistlock", "Kubernetes", "SOC\u00a02"], "cube"),
]

CAREER = [
    ("Oct 2022 to present", "IBM", "Senior Advisory Data Security Engineer", "Built the automation that configures OWASP, Mend, SonarQube and Twistlock scans across container images, source code and APIs, with results in a central dashboard."),
    ("Jan 2021 to Sep 2022", "Photon for Samsung ecommerce", "Senior Technical Team Lead", "Built the B2B customer service console for agents, admins and supervisors, with order and customer search, returns, refunds, cancellations and a timeline of order status. Added pay by phone and payment links."),
    ("Aug 2012 to Dec 2020", "Syncfusion", "Senior Product Manager and Technical Team Lead", "Created ColorPicker and TimePicker widgets, then the File Manager and Tree View products in TypeScript and React. Led a team of 8 developers and 1 tester."),
]

CREDS = [
    ("cert", "Architectural Thinking", "IBM Architect Profession, Foundational. A repeatable and consistent approach to developing IT architectures through a common thought process.", "Architecture"),
    ("cert", "Developer Profession Level 2 Experienced", "IBM professional certification for sustained technical excellence and impact.", "Certification"),
    ("lead", "IBM Volunteers Engagement Award", "40 hours of community giving and social impact.", "Community"),
    ("sec", "Digital Sovereignty 201", "IBM Data and AI. Intermediate cloud sovereignty architecture.", "Sovereignty"),
    ("ai", "2026 IBMer watsonx Challenge", "Foundational AI engineering and agentic workflows.", "watsonx"),
    ("sec", "Digital Sovereignty 101", "IBM Automation. Foundational data protection and geographic boundaries.", "Sovereignty"),
    ("sec", "Practical Introduction to Quantum Safe Cryptography", "IBM Quantum. Post quantum algorithms and cryptographic agility.", "Cryptography"),
    ("ai", "2025 IBMer watsonx Challenge", "Applied generative AI solutions and automation.", "watsonx"),
    ("cert", "Eureka InCITE Product led Innovation Gold", "IBM Data and AI. Top tier innovation recognition.", "Gold award"),
    ("ai", "IBM watsonx.ai Technical Essentials", "Foundation models, prompting, fine tuning and the LLM lifecycle.", "watsonx"),
    ("cert", "Turbonomic Sales Foundation", "Application resource management and multi cloud optimization.", "Cloud operations"),
    ("lead", "Leadership Essentials for the Aspiring Manager", "Team coaching, talent development and delegation.", "Leadership"),
    ("cert", "Dependency Based Build Fundamentals", "IBM Systems. Modern continuous integration architectures.", "DevOps"),
    ("sec", "Security and Privacy by Design Practitioner", "Enterprise and technology security, intermediate. SPbD implementation.", "SPbD"),
    ("cert", "Intermediate Kubernetes Operators", "IBM Data Platform. Custom resource definitions and controller logic.", "Kubernetes"),
    ("sec", "IBM DevSecOps Explorer", "Security and automation for DevOps pipelines from the IBM CISO Office.", "DevSecOps"),
    ("sec", "Security and Privacy by Design Foundations", "IBM CISO Office. Foundational security governance.", "SPbD"),
    ("lead", "IBM Agile Explorer", "IBM Agile Academy. Scrum, Kanban and iterative delivery.", "Agile"),
    ("lead", "Power Skills: Resilience and Growth Mindset", "Learning agility, active adaptation and time management.", "Power skills"),
    ("lead", "IBM Growth Behaviors", "Customer focus, continuous improvement and collaborative impact.", "Culture"),
    ("lead", "Enterprise Design Thinking Practitioner", "User centered problem solving, empathy mapping and co creation.", "Design thinking"),
]
FILTERS = [("all", "All"), ("cert", "Certifications"), ("sec", "Security and privacy"), ("ai", "AI and watsonx"), ("lead", "Leadership and agile")]

ARTICLES = [
    ("Oct 1, 2026", "MCP Is Becoming the New Attack Surface: Securing the Next Generation of AI Agents", "https://dev.to/manikandan/mcp-is-becoming-the-new-attack-surface-securing-the-next-generation-of-ai-agents-1d87"),
    ("Mar 6, 2026", "AI Weaponization: Understanding the Threat and OpenAI's Defense Strategies", "https://dev.to/manikandan/ai-weaponization-understanding-the-threat-and-openais-defense-strategies-4p23"),
    ("Nov 11, 2025", "Quantum Cryptography: The Future of Unbreakable Security", "https://dev.to/manikandan/quantum-cryptography-the-future-of-unbreakable-security-1amb"),
]

SKILLS = [
    ("Security and compliance", ["OWASP Top 10", "SAST", "DAST", "IAST", "Dependency scanning", "Container security", "SOC\u00a02 evidence", "Security and Privacy by Design", "Data security"]),
    ("Architecture and platform", ["Microservices", "REST APIs", "GraphQL", "Design patterns", "Queue based pipelines", "Docker", "Kubernetes", "Helm", "OpenShift", "Terraform", "Jenkins", "CI/CD"]),
    ("Languages and frameworks", ["JavaScript", "TypeScript", "Python", "Node.js", "Express", "Spring Boot", "React", "Next.js", "Redux", "Rust", "Tailwind CSS"]),
    ("Data", ["PostgreSQL", "MongoDB", "MySQL", "Elasticsearch"]),
]

FAQ = [
    ("What does a software architect with a security focus do for my team?",
     "I design systems where scanning, policy checks and evidence collection are part of the delivery pipeline. At IBM that means self service tooling for static, dynamic, interactive, dependency and container testing, with results in one dashboard."),
    ("Which security tools have you automated?",
     "OWASP ZAP for dynamic API testing, SonarQube Enterprise for static analysis, Mend for open source and SAST findings, Twistlock for container and cluster scanning, IAST for runtime testing, and CSAR for open source and legal clearance."),
    ("Have you supported compliance audits?",
     "My Twistlock scanner for product Kubernetes clusters has been used by teams going through SOC\u00a02 audits. I also work on the Aegis boards for PSIRT, ITSS and Security and Privacy by Design. I cannot speak for how your own organization is certified."),
    ("Which technologies do you build with?",
     "React, Next.js, JavaScript, TypeScript, Node.js, Python, Spring Boot and Rust, with PostgreSQL, MongoDB and MySQL. For delivery I use Docker, Kubernetes, Helm, OpenShift, Terraform and Jenkins."),
    ("Can you lead a team as well as design the system?",
     "Yes. At Syncfusion I led 8 developers and 1 tester and delivered to timeline without cutting quality. At IBM I mentor engineers across teams on technical depth and career growth."),
    ("What is the best way to reach you?",
     "Email is the fastest route. Describe the system, the control or audit you are working toward, and the timeline. I will tell you plainly whether it is a fit."),
    ("Where are you based and which languages do you work in?",
     "I am based in Sivakasi, India. I work in English at a professional level and Tamil is my native language."),
    ("Where can I read more of your work?",
     "I have published 25+ technical articles on Dev.to, covering security, AI agents and cloud native engineering. My IBM career timeline is on a separate page linked in the Work section."),
]

TAGLINE = "Security that ships with the code. Compliance that runs on every commit, not once a year."


# ---------------- Pages ----------------

def index():
    stats = "".join(f'<li class="card reveal"><p class="stat-value">{v}</p><div><p class="title-3">{esc(t)}</p><p class="caption-2">{esc(d)}</p></div></li>' for v, t, d in ((v.format(badges=len(CREDS)), t, d) for v, t, d in STATS))
    pipe = "".join(f'<li class="pipeline-row">{ic(i)}<div class="info"><p class="title-4">{esc(t)}</p><p class="caption-2 muted">{esc(s)}</p></div><span class="status caption-3">{ic("check-circle", "icon icon-sm")} Automated</span></li>' for i, t, s in PIPE)
    ben = "".join(f'<li class="card reveal">{ic(i)}<h3 class="heading-6">{esc(t)}</h3><p class="body-6">{esc(d)}</p></li>' for i, t, d in BENEFITS)
    steps = "".join(f'<li class="card reveal"><p class="step-num mono title-4">{n}</p><h3 class="heading-6">{esc(t)}</h3><p class="body-6">{esc(d)}</p></li>' for n, t, d in STEPS)
    work = "".join(f'<li class="card reveal">{ic(i)}<p class="caption-4 muted">{esc(d)}</p><h3 class="heading-6">{esc(t)}</h3><p class="body-6">{esc(b)}</p>{tags(tg)}</li>' for d, t, b, tg, i in WORK)
    career = "".join(f'<li class="card reveal"><p class="caption-4 muted">{esc(d)}</p><h3 class="heading-6">{esc(c)}</h3><p class="title-4">{esc(r)}</p><p class="body-6">{esc(b)}</p></li>' for d, c, r, b in CAREER)
    chips = "".join(f'<button class="chip button-sm" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>' for k, l in FILTERS)
    creds = "".join(f'<li class="cred" data-cat="{c}">{ic("certificate")}<h3 class="title-3">{esc(t)}</h3><p class="body-6">{esc(d)}</p><p class="caption-4 muted">{esc(tag)}</p></li>' for c, t, d, tag in CREDS)
    arts = "".join(f'<li><a class="article-card" href="{u}" rel="noopener"><div class="meta caption-4"><span>{d}</span>{ic("arrow-up-right", "icon icon-sm")}</div><h3 class="title-2">{esc(t)}</h3></a></li>' for d, t, u in ARTICLES)
    skills = "".join(f'<li class="card reveal"><h3 class="heading-6">{esc(t)}</h3>{tags(items)}</li>' for t, items in SKILLS)
    faq = "".join(f'<details><summary class="title-3"><span>{esc(q)}</span>{ic("caret-down")}</summary><p class="body-6">{esc(a)}</p></details>' for q, a in FAQ)
    words = " ".join(f'<span class="word">{esc(w)}</span>' for w in TAGLINE.split())

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Person", "name": "Manikandan M", "jobTitle": "Software architect, data security and compliance",
             "worksFor": {"@type": "Organization", "name": "IBM"}, "email": f"mailto:{EMAIL}",
             "address": {"@type": "PostalAddress", "addressLocality": "Sivakasi", "addressCountry": "IN"},
             "url": f"{BASE}/about_me.html", "sameAs": [LINKEDIN, GITHUB, DEVTO],
             "knowsAbout": ["Software architecture", "Data security", "DevSecOps", "Compliance automation", "OWASP", "Kubernetes"]},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>'

    body = f"""<a class="skip-link button-sm" href="#main">Skip to content</a>
{nav()}
<main id="main">

<section class="hero" id="top" aria-labelledby="hero-title">
<img class="hero-scene" src="assets/hero-scene.svg" width="1600" height="900" fetchpriority="high" alt="Illustration of a boy sitting on a grassy hill at dusk, typing on a laptop where code is running, with fireflies and a village below.">
<div class="hero-shade" aria-hidden="true"></div>
<div class="container">
<div class="hero-copy">
<p class="pill caption-4"><span class="dot" aria-hidden="true"></span> Software architect at IBM, Aegis security platform</p>
<h1 class="heading-1" id="hero-title"><span class="line">Secure software,</span> <span class="line">ready for audit</span></h1>
<p class="lead body-3 balance">I am Manikandan M. For 14+ years I have built full stack systems, and for the last four I have turned data security and compliance checks into pipelines that product teams use on their own.</p>
<div class="hero-actions">
<div class="hero-buttons">
<a class="btn button-md" href="{MAILTO}">{ic("envelope-simple", "icon icon-sm")} Start a conversation</a>
<a class="btn btn-linkedin button-md" href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">{ic("linkedin-logo-fill", "icon icon-sm")} Connect on LinkedIn<span class="sr-only"> (opens in a new tab)</span></a>
</div>
<p class="proof-line caption-2">{ic("check-circle", "icon icon-sm")} Behind the OWASP, Mend, SonarQube and Twistlock automation at IBM</p>
</div>
</div>
</div>
</section>

<section class="proof-panel" aria-label="Scan coverage">
<div class="container">
<figure class="pipeline reveal" aria-label="Illustration of the scan coverage I automate">
<div class="pipeline-head"><p class="title-3">Security pipeline coverage</p><p class="caption-2 muted">What I automated for IBM product teams</p></div>
<ul class="pipeline-rows">{pipe}</ul>
</figure>
</div>
</section>

<section class="section" id="impact" aria-labelledby="impact-title">
<div class="container">
<div class="section-head reveal">
<p class="eyebrow caption-3">{ic("trophy", "icon icon-sm")} Impact</p>
<h2 class="heading-3" id="impact-title">Numbers from the work, not from a brochure</h2>
<p class="body-3">Figures come from my resume and my IBM career timeline.</p>
</div>
<ul class="grid stats">{stats}</ul>
</div>
</section>

<section class="section" aria-labelledby="problem-title">
<div class="container">
<div class="section-head reveal">
<p class="eyebrow caption-3">{ic("lock-key", "icon icon-sm")} The problem</p>
<h2 class="heading-3" id="problem-title">Security reviews arrive late and audits arrive in a rush</h2>
</div>
<div class="grid pair">
<div class="card reveal"><h3 class="heading-6">Where it breaks</h3><p class="body-6">Scans are set up by hand, results sit in separate tools, and evidence is collected the week before an audit. Findings reach engineers after the release is already planned.</p></div>
<div class="card reveal"><h3 class="heading-6">What I build instead</h3><p class="body-6">Self service automation that runs scans on every change, normalizes the results and shows them in one dashboard, so evidence already exists when someone asks for it.</p></div>
</div>
</div>
</section>

<section class="tagline" aria-label="Tagline">
<div class="container">
<p class="tagline-text heading-2" id="tagline" aria-label="{esc(TAGLINE)}">{words}</p>
</div>
</section>

<section class="section" id="benefits" aria-labelledby="benefits-title">
<div class="container">
<div class="section-head reveal">
<p class="eyebrow caption-3">{ic("shield-check", "icon icon-sm")} What you get</p>
<h2 class="heading-3" id="benefits-title">An architect who treats compliance as an engineering problem</h2>
</div>
<ul class="grid benefits">{ben}</ul>
<div class="sub-head reveal"><h2 class="heading-4">How we would work together</h2></div>
<ol class="grid steps">{steps}</ol>
</div>
</section>

<section class="section" id="work" aria-labelledby="work-title">
<div class="container">
<div class="section-head reveal">
<p class="eyebrow caption-3">{ic("rocket-launch", "icon icon-sm")} Selected work</p>
<h2 class="heading-3" id="work-title">Systems I designed and shipped at IBM</h2>
<p class="body-3">Each item is a framework, pipeline or product that other teams use directly. The full IBM story is on my <a class="link-inline" href="{TIMELINE}" rel="noopener">career timeline</a>.</p>
</div>
<ul class="grid work-grid">{work}</ul>
<div class="sub-head reveal"><h2 class="heading-4">Career</h2></div>
<ol class="grid career-grid">{career}</ol>
<p class="edu body-6 reveal">Education: B.Tech in Information Technology, P.S.R Engineering College (8.49 CGPA). Diploma in Computer Engineering, Arasan Ganesan Polytechnic College (9.5 CGPA).</p>
</div>
</section>

<section class="section" id="credentials" aria-labelledby="cred-title">
<div class="container">
<div class="section-head reveal">
<p class="eyebrow caption-3">{ic("medal", "icon icon-sm")} Credentials</p>
<h2 class="heading-3" id="cred-title">{len(CREDS)} digital badges</h2>
<p class="body-3">Security, privacy, sovereignty, cryptography, cloud and AI. Filter or search them.</p>
</div>
<div class="cred-tools">
<div class="chips" role="group" aria-label="Filter credentials">{chips}</div>
<label class="sr-only" for="cred-search">Search credentials</label>
<input class="search" id="cred-search" type="search" placeholder="Search credentials" autocomplete="off">
<p class="caption-2 muted" id="cred-count" role="status" aria-live="polite">Showing {len(CREDS)} of {len(CREDS)}</p>
</div>
<ul class="cred-grid" id="cred-grid">{creds}</ul>
<div class="empty" id="cred-empty" hidden>
{ic("magnifying-glass")}
<h3 class="heading-6">No credentials match</h3>
<p class="body-6">Try a shorter search term, or clear the filters to see all {len(CREDS)} badges.</p>
<button class="btn btn-ghost button-sm" type="button" id="cred-reset">Clear filters</button>
</div>
</div>
</section>

<section class="section" id="writing" aria-labelledby="writing-title">
<div class="container">
<div class="section-head reveal">
<p class="eyebrow caption-3">{ic("article", "icon icon-sm")} Writing</p>
<h2 class="heading-3" id="writing-title">Security notes for working engineers</h2>
<p class="body-3">25+ articles on Dev.to about AI agent security, threats and cryptography.</p>
</div>
<ul class="articles">{arts}</ul>
<a class="more-link body-5" href="{DEVTO}" rel="noopener">Read all articles on Dev.to {ic("arrow-up-right", "icon icon-sm")}</a>
</div>
</section>

<section class="section" id="skills" aria-labelledby="skills-title">
<div class="container">
<div class="section-head reveal">
<p class="eyebrow caption-3">{ic("stack", "icon icon-sm")} Skills</p>
<h2 class="heading-3" id="skills-title">The stack behind the work</h2>
</div>
<ul class="grid skills">{skills}</ul>
</div>
</section>

<section class="section" id="faq" aria-labelledby="faq-title">
<div class="container">
<div class="section-head reveal">
<p class="eyebrow caption-3">{ic("magnifying-glass", "icon icon-sm")} FAQ</p>
<h2 class="heading-3" id="faq-title">Questions before you write</h2>
</div>
<div class="faq reveal">{faq}</div>
</div>
</section>

<section class="section" id="contact" aria-labelledby="contact-title">
<div class="container">
<div class="cta reveal">
<h2 class="heading-3" id="contact-title">Tell me which control or audit you are building toward</h2>
<p class="body-3">One short email is enough. No forms and no sales funnel. It goes straight to my inbox.</p>
<a class="btn button-md" href="{MAILTO}">{ic("envelope-simple", "icon icon-sm")} Start a conversation</a>
</div>
</div>
</section>

</main>
{footer()}
<button class="to-top" id="to-top" type="button" aria-label="Scroll to top" title="Scroll to top">{ic("arrow-up")}</button>
<script src="script.js" defer></script>"""
    return page_shell(
        "Manikandan M | Software architect for secure, compliant systems",
        "Software architect at IBM with 14+ years of experience in data security, compliance automation and full stack engineering. See selected work and get in touch.",
        "about_me.html", body, extra=extra)


def simple(title, desc, path, h1, paras):
    body = f"""<a class="skip-link button-sm" href="#main">Skip to content</a>
<main id="main" class="page">
<a class="btn btn-ghost button-sm" href="about_me.html">{ic("arrow-left", "icon icon-sm")} Back to profile</a>
{h1}
{"".join(paras)}
</main>
{footer()}"""
    return page_shell(title, desc, path, body, robots="noindex,follow" if path == "404.html" else "index,follow")


def build():
    (SITE / "about_me.html").write_text(index())
    (SITE / "404.html").write_text(simple(
        "Page not found | Manikandan M", "This page does not exist.", "404.html",
        '<h1 class="heading-3">Page not found</h1>',
        ['<p class="body-3">That address does not match anything on this site. It may have moved or been typed incorrectly.</p>',
         f'<a class="btn button-md" href="about_me.html">Go to the profile {ic("arrow-right", "icon icon-sm")}</a>']))
    (SITE / "privacy.html").write_text(simple(
        "Privacy policy | Manikandan M", "How this site handles your data.", "privacy.html",
        '<h1 class="heading-3">Privacy policy</h1>',
        ['<p class="body-3">Last updated November 2026.</p>',
         '<p class="body-3">This site is a static profile. It does not use cookies, analytics, advertising trackers or forms, and it does not store anything about your visit. Fonts and icons are served from this site, so no third party receives your request for them.</p>',
         f'<h2 class="heading-5">Email</h2><p class="body-3">If you email me at <a href="mailto:{EMAIL}">{EMAIL}</a>, I use your message only to reply to you and do not share it.</p>',
         '<h2 class="heading-5">Outbound links</h2><p class="body-3">Links to LinkedIn, GitHub and Dev.to open sites with their own privacy policies.</p>',
         '<h2 class="heading-5">Hosting</h2><p class="body-3">The site is hosted on GitHub Pages, which may keep standard server logs under the GitHub privacy statement.</p>']))
    (SITE / "terms.html").write_text(simple(
        "Terms | Manikandan M", "Terms of use for this profile site.", "terms.html",
        '<h1 class="heading-3">Terms</h1>',
        ['<p class="body-3">Last updated November 2026.</p>',
         '<p class="body-3">This site describes my professional background. The views expressed are my own and do not represent IBM or any other employer. Product and company names belong to their owners.</p>',
         '<p class="body-3">Content is provided as is for information. Please do not copy the text, design or code of this site without permission.</p>']))


build()
