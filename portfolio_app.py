import streamlit as st
import os
import time
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
from pathlib import Path

st.set_page_config(
    page_title="Devansh Shah",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def apply_theme():
    is_dark = st.session_state.dark_mode
    bg = "#0f1117" if is_dark else "#f0f2f6"
    bg2 = "#1a1d29" if is_dark else "#ffffff"
    card_bg = "#181b26" if is_dark else "#ffffff"
    text = "#e4e6f0" if is_dark else "#1f2937"
    text_muted = "#9ca3af" if is_dark else "#6b7280"
    border = "#2a2e42" if is_dark else "#e5e7eb"
    accent = "#6c8cff" if is_dark else "#4A90E2"
    info_bg = "#1a2744" if is_dark else "#d1e7ff"
    info_text = "#a0c4ff" if is_dark else "#0c4a6e"

    st.markdown(f"""
    <style>
    html {{
        scroll-behavior: smooth;
    }}
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    .stApp, .main, .block-container {{ background-color: {bg} !important; }}
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}
    h1, h2, h3, h4, h5, h6, p, li, span:not(.st-badge), .stMarkdown, .stText {{
        color: {text} !important;
    }}
    .hero-text-container, .hero-text-container * {{
        text-align: center !important;
    }}
    .nav-wrapper {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        flex-wrap: nowrap;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        padding: 4px 0 8px 0;
        width: 100%;
        margin: 0 auto;
    }}
    .nav-wrapper::-webkit-scrollbar {{
        display: none;
    }}
    .nav-item {{
        color: {text} !important;
        text-decoration: none !important;
        font-weight: 500;
        font-size: 14px;
        padding: 6px 14px;
        border-radius: 20px;
        background-color: {bg2};
        border: 1px solid {border};
        transition: all 0.2s ease-in-out;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        white-space: nowrap;
        flex-shrink: 0;
    }}
    .nav-item:hover {{
        background-color: {accent} !important;
        color: #ffffff !important;
        border-color: {accent} !important;
        transform: translateY(-1px);
    }}
    .nav-item:active {{
        transform: scale(0.97);
    }}
    .section-anchor {{
        scroll-margin-top: 80px;
    }}
    .experience-card, .education-card {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .experience-card:hover, .education-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
    }}
    .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        flex-wrap: wrap;
        margin-bottom: 6px;
    }}
    .card-title {{
        font-size: 18px;
        font-weight: 600;
        color: {text} !important;
    }}
    .card-subtitle {{
        font-size: 15px;
        font-weight: 500;
        color: {accent} !important;
    }}
    .card-date {{
        font-size: 13px;
        color: {text_muted} !important;
    }}
    button[data-testid], button[data-testid] * {{
        color: {accent} !important;
    }}
    [data-testid="stLinkButton"], [data-testid="stLinkButton"] * {{
        color: #ffffff !important;
    }}
    button[data-testid]:hover, button[data-testid]:hover * {{
        background-color: {accent} !important;
        color: {"#0f1117" if is_dark else "#ffffff"} !important;
    }}
    [data-testid="stLinkButton"]:hover, [data-testid="stLinkButton"]:hover * {{
        background-color: #4A90E2 !important;
        color: white !important;
    }}
    hr {{ border-color: {border} !important; }}
    .stAlert, .stInfo {{ background-color: {bg2} !important; color: {text} !important; }}
    .stInfo {{ background-color: {info_bg} !important; color: {info_text} !important; }}
    input, textarea, .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: {bg2} !important;
        color: {text} !important;
        border-color: {border} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: #e4e6f0 !important;
    }}
    section[data-testid="stSidebar"] a {{
        color: #6c8cff !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: #ffffff !important;
    }}
    @media (max-width: 768px) {{
        .block-container {{
            padding-top: 1.5rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }}
        .nav-wrapper {{
            justify-content: flex-start !important;
            gap: 8px !important;
        }}
        .nav-item {{
            font-size: 12.5px;
            padding: 5px 10px;
        }}
        .hero-text-container p:first-child {{
            font-size: 1.85rem !important;
        }}
        div[data-testid="stImage"] {{
            display: flex;
            justify-content: center;
        }}
        div[data-testid="stImage"] > img {{
            margin: 0 auto;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

CSS = """
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stButton>button, button[data-testid] {
    border: 2px solid #4A90E2;
    border-radius: 20px;
    padding: 10px 24px;
    background-color: transparent !important;
    transition: all 0.3s ease-in-out;
    text-decoration: none;
}
.stButton>button:hover, button[data-testid]:hover, button[data-testid]:hover * {
    background-color: #4A90E2 !important;
    color: white !important;
}

.contact-form {
    max-width: 600px;
    margin: 0 auto;
}
.blog-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 0;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    overflow: hidden;
}
.blog-card img {
    width: 100%;
    border-radius: 12px 12px 0 0;
}
.blog-card .content {
    padding: 15px;
}
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

def load_image(path_or_url, fallback_size=(300, 300), fallback_color=(52, 152, 219)):
    try:
        if isinstance(path_or_url, str) and (path_or_url.startswith("http://") or path_or_url.startswith("https://")):
            response = requests.get(path_or_url, timeout=5)
            if response.status_code == 200:
                try:
                    return Image.open(BytesIO(response.content))
                except UnidentifiedImageError:
                    pass
        elif isinstance(path_or_url, (str, Path)) and os.path.exists(path_or_url):
            return Image.open(path_or_url)
    except Exception:
        pass
    return Image.new("RGB", fallback_size, fallback_color)

profile_pic = load_image("img/profile.jpeg")
project_image_1 = load_image("img/BulkHead.jpg")
project_image_2 = load_image("img/RhoScale.jpg")
project_image_3 = load_image("img/RelayAgent.jpg")
project_image_4 = load_image("img/Orderly.jpg")

RESUME_URL = "https://www.dropbox.com/scl/fi/j7i6kpgzeffz6vj0gyjo9/Devansh-Shah-Resume.pdf?rlkey=5ivofne11jbc6tk357h2fvezw&dl=0"

def load_blog_posts():
    posts = []
    blog_dir = Path("blog")
    if not blog_dir.exists():
        return posts
    for post_dir in sorted(blog_dir.iterdir()):
        if not post_dir.is_dir():
            continue
        md_file = post_dir / "post.md"
        if not md_file.exists():
            continue
        with open(md_file) as f:
            lines = f.readlines()
        content = "".join(lines)
        images = []
        for f in sorted(post_dir.iterdir()):
            if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp") and f.name != "post.md":
                images.append(load_image(str(f)))
        title_line = lines[0].strip().replace("## ", "").replace("# ", "")
        remaining = "".join(lines[1:]).strip()
        mod_time = os.path.getmtime(md_file)
        mod_date = time.strftime("%b %d, %Y", time.localtime(mod_time))
        posts.append({"content": remaining or content, "images": images, "title": title_line, "slug": post_dir.name, "date": mod_date})
    return list(reversed(posts))

with st.sidebar:
    st.title("📝 Blogs (Easter Egg)")
    blog_posts = load_blog_posts()
    if not blog_posts:
        st.write("No posts yet. Check back soon!")
    for post in blog_posts:
        st.markdown(f"**{post['title']}**  \n*{post['date']}*")
        for img in post["images"]:
            st.image(img, width="stretch")
        st.markdown(post["content"])
        st.divider()

# Top Navigation Bar (Centered)
st.markdown("""
<div class="nav-wrapper">
    <a href="#about" target="_self" class="nav-item">👤 About</a>
    <a href="#skills" target="_self" class="nav-item">⚡ Skills</a>
    <a href="#experience" target="_self" class="nav-item">💼 Experience</a>
    <a href="#projects" target="_self" class="nav-item">🚀 Projects</a>
    <a href="#education" target="_self" class="nav-item">🎓 Education</a>
    <a href="#contact" target="_self" class="nav-item">📬 Contact</a>
</div>
""", unsafe_allow_html=True)

st.divider()

# Hero Header
with st.container():
    col1, col2 = st.columns([1, 2.5], vertical_alignment="center")
    with col1:
        st.image(profile_pic, width=200)
    with col2:
        st.markdown(
            """
            <div class="hero-text-container" style="text-align: center !important; width: 100%;">
                <p style="font-size: 2.3rem; font-weight: 700; margin: 0 auto 0.2rem auto; text-align: center !important; line-height: 1.2;">Devansh Shah</p>
                <p style="font-size: 1.05rem; margin: 0 auto 0.2rem auto; text-align: center !important;">📧 <a href="mailto:devansh.shah.tech@gmail.com" style="text-decoration: none; color: inherit;">devansh.shah.tech@gmail.com</a></p>
                <p style="font-size: 1.15rem; font-weight: 500; margin: 0 auto 1rem auto; text-align: center !important;">AI Infrastructure & Platform Engineer</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        bcol1, bcol2 = st.columns(2)
        with bcol1:
            st.link_button(
                "🔗 LinkedIn",
                "https://linkedin.com/in/devanshshah-tech/",
                width="stretch",
            )
        with bcol2:
            st.link_button(
                "📄 RÉSUMÉ",
                RESUME_URL,
                width="stretch",
            )

# About Section
st.markdown('<div id="about" class="section-anchor"></div>', unsafe_allow_html=True)
with st.container():
    st.divider()
    st.subheader("Hi, I am Devansh 👋")
    st.write(
        "AI Engineer with a strong foundation in MLOps, cloud-native infrastructure automation, and LLM evaluation frameworks. Proven track record deploying scalable systems, including an LLM evaluation pipeline (vLLM, LiteLLM, Opik) that cut model selection time by 50%, and a Kubernetes CI/CD layer that resolved a critical pepr-system mesh crash causing cluster-wide pod admission failure. Adept at bridging advanced machine learning models with robust software engineering to deliver production-ready, data-driven enterprise solutions."
    )
    st.info("🚧 This portfolio is evolving, check back soon for more!")

    st.header("What I Do")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏗️ AI Infrastructure & Platform Engineering")
        st.write(
            """
            - Packaging and deploying AI systems into disconnected, security-restricted Kubernetes clusters (Zarf, UDS, Istio)
            - Building GitOps-managed delivery pipelines (ArgoCD, Terraform) for AI platforms across connected and airgapped environments
            - Designing service-mesh security and reliability patterns (mTLS, circuit breakers) into distributed systems from the start
            """
        )
    with col2:
        st.subheader("🤖 Applied AI & Retrieval Systems")
        st.write(
            """
            - Building retrieval-augmented generation pipelines with local, self-hosted LLM inference
            - Applying queueing theory (Little's Law, G/G/1 modeling) to autoscaling decisions for LLM inference workloads
            - Writing production-oriented Go and Python backend services with CI/CD and reproducible tooling (mise, Docker)
            """
        )

# Skills Section
st.markdown('<div id="skills" class="section-anchor"></div>', unsafe_allow_html=True)
with st.container():
    st.divider()
    st.header("My Skills")
    st.write(
        """
        - **AI & LLM:** LangChain, MCP, vLLM, LiteLLM, Opik, ChromaDB, Streamlit, PyTorch, TensorFlow, Scikit-Learn, XGBoost, Pandas
        - **Cloud & DevOps:** AWS, Google Cloud, Terraform, Docker, Kubernetes, Helm, Tilt, Istio, ArgoCD, GitOps, CI/CD, Zarf, UDS, k3d, mise
        - **Languages:** Python, Go, SQL, JavaScript, Bash, HTML, CSS
        - **Backend & Big Data:** FastAPI, REST, gRPC, GraphQL, Protobuf, Flask, Django, Apache Spark, Apache Iceberg, Databricks, lakeFS, MinIO
        - **Databases, Search & BI:** PostgreSQL, MongoDB, Redis, ElasticSearch, MySQL, OpenSearch, Apache AGE, Tableau, Power BI
        - **Certifications:** AWS Certified - AI Practitioner, NVIDIA - Getting Started with Deep Learning
        """
    )

# Experience Section
st.markdown('<div id="experience" class="section-anchor"></div>', unsafe_allow_html=True)
with st.container():
    st.divider()
    st.header("Experience")

    st.markdown("""
    <div class="experience-card">
        <div class="card-header">
            <span class="card-title">Distributed Systems & Software Engineering</span>
            <span class="card-date">July 2025 – Present</span>
        </div>
        <div class="card-subtitle">Backend & Infrastructure Development</div>
        <p style="margin-top: 10px; margin-bottom: 0;">
            • Engineered highly responsive microservices architecture utilizing <b>Go</b>, <b>gRPC</b>, and <b>Protobuf</b> for high-throughput inter-service communication.<br>
            • Integrated <b>GraphQL API Gateways</b> and distributed storage with <b>PostgreSQL</b> and <b>Elasticsearch</b> for seamless querying and high availability.<br>
            • Orchestrated containerized environments using <b>Docker</b>, <b>Kubernetes</b>, and <b>GitOps/CI/CD</b> workflows.
        </p>
    </div>
    <div class="experience-card">
        <div class="card-header">
            <span class="card-title">AI & Machine Learning Engineer</span>
            <span class="card-date">2024 – 2025</span>
        </div>
        <div class="card-subtitle">Intelligent Systems & Applied ML</div>
        <p style="margin-top: 10px; margin-bottom: 0;">
            • Developed end-to-end recommendation pipelines and predictive models leveraging <b>PyTorch</b>, <b>TensorFlow</b>, and <b>Scikit-Learn</b>.<br>
            • Built interactive data-driven applications with <b>Streamlit</b> and <b>FastAPI</b>, enabling real-time inferences and analytics.<br>
            • Integrated Agentic AI workflows using <b>LangChain</b>, <b>MCP</b>, <b>vLLM</b>, and vector databases like <b>ChromaDB</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Projects Section
st.markdown('<div id="projects" class="section-anchor"></div>', unsafe_allow_html=True)
with st.container():
    st.divider()
    st.header("My Projects")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(project_image_1, width="stretch")
    with text_column:
        st.subheader("Airgap-Deployable RAG Platform")
        st.write(
            """
            *June - Aug 2026*
            - Designed and engineered an offline-first RAG microservice platform (FastAPI, Go gRPC, pgvector, lakeFS-versioned corpus) powered by CPU-quantized local LLM inference, eliminating external API dependencies for fully airgapped operation.
            - Engineered zero-trust service mesh security with Istio enforcing strict mTLS, traffic policies, and egress isolation across all internal hops, managed via declarative ArgoCD GitOps and Terraform infrastructure as code.
            - Packaged the platform into dual-arch Zarf/UDS airgap bundles (≤2GiB) for one-command offline deployment, while operating a $0-cost live public demo via k3s and Cloudflare Tunnel to validate dual delivery modes.

            **Tech Stack:** Go, Python (FastAPI), gRPC, Protobuf, GraphQL, PostgreSQL (pgvector), Istio, Kubernetes, Helm, ArgoCD, Terraform, Zarf/UDS, Ollama, lakeFS, Docker
            """
        )
        st.link_button("View on GitHub", "https://github.com/devanshshah-tech/BulkHead")

    st.divider()

    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(project_image_2, width="stretch")
    with text_column:
        st.subheader("Queue-Aware Kubernetes Autoscaler for LLM Inference")
        st.write(
            """
            *Mar - June 2026*

            - Designed and implemented a Kubernetes autoscaler in Go (MAPE-K control loop, client-go) that replaces CPU-based HPA with a
            queue-depth signal grounded in G/G/1 queueing theory, using Little’s Law (L= λW) to estimate real-time latency degradation from live
            Prometheus metrics without instrumenting individual requests.
            - Empirically calibrated a proportional scaling threshold via Knee Point analysis (second-derivative slope detection) and validated the
            controller reacting 10x faster than standard HPA (4s vs. 40s across 4 scaling events), using a trace-driven replay methodology purpose
            built to eliminate workload confounds by evaluating both algorithms against identical real inference traffic.
            - Stress-tested the system under Poisson-distributed traffic across 6 arrival-rate regimes (λ= 1–26 req/s), quantifying a stability boundary
            where error rate escalated from 0% to 92% past the Knee Point, empirically justifying the entire autoscaling design and threshold
            calibration methodology.

            **Tech Stack:** Go, gRPC, Protobuf, GraphQL, Kafka, Docker, PostgreSQL, Elasticsearch
            """
        )
        st.link_button(
            "View on GitHub", "https://github.com/devanshshah-tech/RhoScale"
        )

    st.divider()

    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(project_image_3, width="stretch")
    with text_column:
        st.subheader("Enterprise AI Agent Platform")
        st.write(
            """
            *Jan - Mar 2026*

            - Designed a hierarchical multi-agent system (supervisor agent routing to search, summarization, and code-execution sub-agents) using a
            ReAct architecture, with each agent as its own microservice and conversation-ID propagation across service boundaries for observability.
            - Built and evaluated a RAG pipeline with sentence-window and parent-document chunking strategies against a ChromaDB knowledge base,
            measuring faithfulness/hallucination rate across strategies to select the retrieval configuration with the best precision-context tradeoff.
            - Deployed each agent independently on Google Cloud Run with Terraform-managed infrastructure and secrets, Docker containerization,
            and GitHub Actions CI/CD, with structured trace logging correlating each conversation across the distributed agent graph.

            **Tech Stack:** Go, gRPC, Protobuf, GraphQL, Kafka, Docker, PostgreSQL, Elasticsearch
            """
        )
        st.link_button(
            "View on GitHub", "https://github.com/devanshshah-tech/RelayAgent"
        )

    st.divider()

    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(project_image_4, width="stretch")
    with text_column:
        st.subheader("Microservices E-Commerce Platform")
        st.write(
            """
            *Oct - Dec 2025*

            - Built a microservices architecture in Go (Account, Catalog, Order services) with gRPC/Protobuf for inter-service communication and a GraphQL API gateway composing calls across services into unified client queries, backed by PostgreSQL and Elasticsearch.
            - Implemented the saga pattern for order-creation consistency across services, using the outbox pattern (atomic local write of state change plus event, relayed to the message broker) to reliably drive each saga step; added circuit breakers and bounded retries on inter-service calls to prevent cascading failure when a dependency degrades.
            - Load-tested the platform with ghz, measuring p95 latency; validated failure handling by killing the Catalog service mid-load-test and confirming the Order service degraded gracefully rather than cascading, recovering within seconds once the dependency returned.
            - Containerized the stack with Docker Compose for reproducible local development, with test coverage across services and a stable, pinned Go toolchain across all components.

            **Tech Stack:** Go, gRPC, Protobuf, GraphQL, Kafka, Docker, PostgreSQL, Elasticsearch
            """
        )
        st.link_button(
            "View on GitHub", "https://github.com/devanshshah-tech/Orderly"
        )

# Education Section
st.markdown('<div id="education" class="section-anchor"></div>', unsafe_allow_html=True)
with st.container():
    st.divider()
    st.header("Education")

    st.markdown("""
    <div class="education-card">
        <div class="card-header">
            <span class="card-title">🎓 North Carolina State University</span>
            <span class="card-date">Aug 2024 - May 2026</span>
        </div>
        <div class="card-subtitle">Master of Computer Science (MCS), Data Science Track</div>
        <p style="margin-top: 8px; margin-bottom: 0;">
            Coursework: Artificial Intelligence, Data Science, Cloud Computing, Neural Networks, Data Analysis, Algorithms
        </p>
    </div>
    <div class="education-card">
        <div class="card-header">
            <span class="card-title">🎓 Dharmsinh Desai University</span>
            <span class="card-date">Oct 2020 - May 2024</span>
        </div>
        <div class="card-subtitle">Bachelor of Technology in Information Technology</div>
        <p style="margin-top: 8px; margin-bottom: 0;">
            Coursework: Software Engineering, System Design Practices, Database Management Systems, Theory of Computation
        </p>
    </div>
    """, unsafe_allow_html=True)

# Contact Section
st.markdown('<div id="contact" class="section-anchor"></div>', unsafe_allow_html=True)
with st.container():
    st.divider()
    st.header("Get In Touch!")
    st.write(
        "I'd love to hear from you! Whether you have a question, want to collaborate, "
        "or just want to say hi, feel free to drop a message below."
    )

    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send Message", width="stretch")

        if submitted:
            if name and email and message:
                try:
                    r = requests.post(
                        "https://formspree.io/f/mkodnard",
                        headers={"Accept": "application/json"},
                        data={"name": name, "email": email, "message": message},
                        timeout=10,
                    )
                    if r.ok:
                        st.success("Thanks! I'll get back to you soon. ✅")
                    else:
                        st.error("Something went wrong. Please try again or email me directly.")
                except requests.exceptions.RequestException:
                    st.error("Network error. Please try again later.")
            else:
                st.warning("Please fill in all fields.")

# Footer
with st.container():
    st.divider()
    foot_col1, foot_col2 = st.columns([1, 1], vertical_alignment="center")
    with foot_col1:
        st.toggle("☀️ Light" if not st.session_state.dark_mode else "🌙 Dark", key="dark_mode")
    with foot_col2:
        st.markdown(
            "<p style='text-align:right;font-size:14px;color:#9ca3af;margin:0;padding:4px 0;'>"
            "Built with Streamlit • © 2026 Devansh Shah</p>",
            unsafe_allow_html=True,
        )
