import streamlit as st
import time
from src.answering import AnswerEngine
from src.document_loader import load_documents
from src.knowledge_base import KnowledgeBase

st.set_page_config(
    page_title="DocMind AI",
    page_icon="📘",
    layout="wide",
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
 --bg:#0b0d14;
 --panel:#10131d;
 --blue:#3f5cff;
 --muted:#b7c4de;
 --border:rgba(98,108,255,.82);
}

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"]{

background:
radial-gradient(circle at 15% 20%, rgba(63,92,255,.18), transparent 22%),
radial-gradient(circle at 85% 30%, rgba(0,255,255,.12), transparent 25%),
radial-gradient(circle at 50% 80%, rgba(139,92,246,.16), transparent 30%),
linear-gradient(to bottom,#090b12,#0b0d14)!important;

background-attachment:fixed;
font-family:"Inter",sans-serif;
}

/* HIDE STREAMLIT ELEMENTS */

[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer{
display:none!important;
}

.block-container{
max-width:980px;
padding-top:1rem;
padding-bottom:7rem;
}

/* GLOW EFFECTS */

[data-testid="stAppViewContainer"]::before{

content:"";
position:fixed;

width:320px;
height:320px;

top:-100px;
left:-100px;

background:#3f5cff;

filter:blur(140px);

opacity:.16;

border-radius:50%;

animation:move1 10s infinite alternate;

z-index:-1;
}

[data-testid="stAppViewContainer"]::after{

content:"";
position:fixed;

width:380px;
height:380px;

bottom:-150px;
right:-100px;

background:#8b5cf6;

filter:blur(150px);

opacity:.15;

border-radius:50%;

animation:move2 12s infinite alternate;

z-index:-1;
}

@keyframes move1{
from{transform:translate(0,0);}
to{transform:translate(80px,50px);}
}

@keyframes move2{
from{transform:translate(0,0);}
to{transform:translate(-80px,-70px);}
}

/* TITLE */

.app-title{
text-align:center;
color:white;
font-size:clamp(2.2rem,5vw,3.3rem);
font-weight:800;
margin:0;
}

.subtitle{
text-align:center;
color:var(--muted);
margin:1rem 0 3rem;
font-size:1rem;
}

/* UPLOADER */

div[data-testid="stFileUploader"]{

max-width:620px;
margin:auto;
}

div[data-testid="stFileUploader"] > label{
display:none!important;
}

section[data-testid="stFileUploaderDropzone"]{

min-height:420px;

border:2px dashed var(--border)!important;
border-radius:12px!important;

background:#111111!important;

display:flex!important;
align-items:center!important;
justify-content:center!important;
flex-direction:column!important;

padding:48px!important;

box-shadow:
0 0 30px rgba(63,92,255,.15),
0 0 60px rgba(63,92,255,.08)!important;
}

section[data-testid="stFileUploaderDropzone"] svg{
display:none!important;
}

/* GENERIC FILE IMAGE */

section[data-testid="stFileUploaderDropzone"]::before{

content:"";

width:150px;
height:150px;

margin-bottom:25px;

background-image:url(
"https://cdn-icons-png.flaticon.com/512/3767/3767084.png");

background-size:contain;
background-repeat:no-repeat;
background-position:center;

display:block;
}

section[data-testid="stFileUploaderDropzone"]
[data-testid="stFileUploaderDropzoneInstructions"]{

width:100%!important;

display:flex!important;
flex-direction:column!important;

align-items:center!important;
justify-content:center!important;

text-align:center!important;
margin:auto!important;
}

section[data-testid="stFileUploaderDropzone"] div{

display:flex!important;
flex-direction:column!important;

align-items:center!important;
justify-content:center!important;

text-align:center!important;

color:white!important;
font-size:1.1rem;
}

section[data-testid="stFileUploaderDropzone"] p{

margin-left:0!important;
padding-left:0!important;

text-align:center!important;
}

section[data-testid="stFileUploaderDropzone"] small{

display:block!important;
width:100%!important;

text-align:center!important;

color:#b7c4de!important;
}

/* BUTTON */

section[data-testid="stFileUploaderDropzone"] button{

background:var(--blue)!important;
color:white!important;

border:none!important;
border-radius:10px!important;

font-size:1.4rem!important;
font-weight:700!important;

padding:1rem 4rem!important;

margin-top:1.5rem!important;

transition:.3s;
}

section[data-testid="stFileUploaderDropzone"] button:hover{

background:#6074ff!important;

transform:translateY(-2px);
}

/* =========================
UPLOADED FILE CARD
========================= */

[data-testid="stFileUploaderFile"]{

display:flex!important;

align-items:center!important;

justify-content:space-between!important;

background:#151924!important;

border:1px solid rgba(255,255,255,.08)!important;

border-radius:14px!important;

padding:14px 18px!important;

margin-top:18px!important;

color:white!important;

box-shadow:
0 0 15px rgba(63,92,255,.10);
}

[data-testid="stFileUploaderFile"] span{

color:white!important;

font-size:15px!important;

font-weight:500!important;
}

[data-testid="stFileUploaderDeleteBtn"]{

background:transparent!important;

border:none!important;

color:#ffffff!important;

font-size:20px!important;

cursor:pointer!important;

transition:.3s;
}

[data-testid="stFileUploaderDeleteBtn"]:hover{

color:#ff5f6d!important;

transform:scale(1.15);
}

/* CHAT */

[data-testid="stChatMessage"]{

background:#151924;

border-radius:14px;

padding:14px;

border:1px solid rgba(255,255,255,.05);
}

/* INPUT */

[data-testid="stChatInput"]{

position:fixed;

bottom:12px;
left:50%;

transform:translateX(-50%);

width:min(980px,calc(100% - 2rem));

z-index:1000;
}

[data-testid="stChatInput"] textarea{

background:#111827!important;

color:white!important;

border-radius:999px!important;

border:1px solid rgba(255,255,255,.08)!important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.markdown("""
<h1 class='app-title'>
📘 DocMind AI - Smart Document Assistant
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
Upload PDFs, DOCX, PPTX or TXT files and chat with your documents.
</div>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================

if "kb" not in st.session_state:
    st.session_state.kb=None

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

# =========================
# =========================
# FILE UPLOAD
# =========================

uploaded_files = st.file_uploader(
    "Upload Files",
    type=["pdf", "pptx", "docx", "txt"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if "last_uploaded_files" not in st.session_state:
    st.session_state.last_uploaded_files = None

if uploaded_files:

    current_files = [(file.name, file.size) for file in uploaded_files]

    if st.session_state.last_uploaded_files != current_files:

        with st.spinner("Reading and indexing documents..."):

            blocks = load_documents(uploaded_files)

            kb = KnowledgeBase()

            kb.build(blocks)

            st.session_state.kb = kb

            st.session_state.last_uploaded_files = current_files

            st.session_state.chat_history = []

# =========================
# CHAT HISTORY
# =========================

for msg in st.session_state.chat_history:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if msg["role"] == "assistant" and msg.get("response_time") is not None:
            st.info(f"⚡ Response Time: {msg['response_time']} sec")

# =========================
# CHAT INPUT
# =========================

question = st.chat_input(
    "Ask questions from your documents..."
)

if question:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        if st.session_state.kb is None:

            answer = "Please upload documents first."
            response_time = None

        else:

            engine = AnswerEngine()

            start_time = time.time()

            result = engine.answer(
                question,
                st.session_state.kb
            )

            end_time = time.time()

            response_time = round(end_time - start_time, 2)

            answer = result.answer

        st.markdown(answer)

        if response_time is not None:
            st.info(f"⚡ Response Time: {response_time} sec")

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer,
            "response_time": response_time
        }
    )
    