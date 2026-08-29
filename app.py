import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
import streamlit.components.v1 as components
import time


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Bird Species Observation Analysis",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 🎬 PREMIUM ENTRY INTRO
# ============================================================

if "intro_played" not in st.session_state:

    st.session_state.intro_played = True

    st.html("""
    <style>

    /* ========================================================
       FULL SCREEN INTRO
       ======================================================== */

    .bird-intro {

        position: fixed;

        inset: 0;

        width: 100vw;
        height: 100vh;

        z-index: 999999;

        display: flex;

        align-items: center;
        justify-content: center;

        overflow: hidden;

        background:
            radial-gradient(
                circle at 15% 25%,
                rgba(34,197,94,0.22),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 25%,
                rgba(56,189,248,0.22),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #031B18 0%,
                #063B35 45%,
                #062A42 100%
            );

        animation:
            introExit 0.8s ease
            3.2s forwards;
    }


    /* ========================================================
       GLOW
       ======================================================== */

    .intro-glow {

        position: absolute;

        width: 360px;
        height: 360px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(103,232,249,0.18),
                transparent 68%
            );

        animation:
            glowPulse 3s ease-in-out infinite;
    }


    @keyframes glowPulse {

        0%, 100% {
            transform: scale(0.85);
            opacity: 0.55;
        }

        50% {
            transform: scale(1.12);
            opacity: 1;
        }
    }


    /* ========================================================
       CONTENT
       ======================================================== */

    .intro-content {

        position: relative;

        z-index: 10;

        width: 90%;

        max-width: 1000px;

        text-align: center;
    }


    /* ========================================================
       BADGE
       ======================================================== */

    .intro-badge {

        display: inline-block;

        padding: 9px 18px;

        border-radius: 30px;

        background:
            rgba(255,255,255,0.10);

        border:
            1px solid
            rgba(167,243,208,0.25);

        color: #A7F3D0;

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 1.5px;

        opacity: 0;

        animation:
            introUp 0.7s ease
            0.15s forwards;
    }


    /* ========================================================
       TITLE
       ======================================================== */

    .intro-title {

        margin-top: 25px;

        font-size: clamp(
            38px,
            6vw,
            74px
        );

        line-height: 1.05;

        font-weight: 900;

        color: white;

        letter-spacing: -2px;

        opacity: 0;

        animation:
            introUp 0.9s ease
            0.45s forwards;

        text-shadow:
            0 8px 30px
            rgba(56,189,248,0.20);
    }


    .intro-title-highlight {

        display: inline-block;

        background:
            linear-gradient(
                90deg,
                #86EFAC,
                #67E8F9,
                #93C5FD
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        background-clip: text;

        animation:
            titleGlow 2s ease-in-out infinite;
    }


    @keyframes titleGlow {

        0%, 100% {
            filter:
                drop-shadow(
                    0 0 0px
                    rgba(103,232,249,0)
                );
        }

        50% {
            filter:
                drop-shadow(
                    0 0 18px
                    rgba(103,232,249,0.55)
                );
        }
    }


    /* ========================================================
       SUBTITLE
       ======================================================== */

    .intro-subtitle {

        margin-top: 22px;

        color: #D1FAE5;

        font-size: 17px;

        line-height: 1.7;

        opacity: 0;

        animation:
            introUp 0.8s ease
            0.95s forwards;
    }


    /* ========================================================
       HOOK
       ======================================================== */

    .intro-hook {

        margin-top: 27px;

        color: #67E8F9;

        font-size: 13px;

        font-weight: 800;

        letter-spacing: 2px;

        opacity: 0;

        animation:
            introFade 0.8s ease
            1.45s forwards;
    }


    /* ========================================================
       FLYING BIRDS
       ======================================================== */

    .intro-bird {

        position: absolute;

        font-size: 45px;

        z-index: 5;

        opacity: 0;

        animation:
            birdFly 3s linear infinite;
    }


    .bird-one {

        top: 22%;

        left: -60px;

        animation-delay: 0.8s;
    }


    .bird-two {

        top: 68%;

        left: -60px;

        font-size: 31px;

        animation-delay: 1.8s;
    }


    @keyframes birdFly {

        0% {

            left: -70px;

            opacity: 0;

            transform:
                translateY(0)
                scale(0.8)
                rotate(-5deg);
        }

        10% {

            opacity: 0.75;
        }

        45% {

            transform:
                translateY(-25px)
                scale(1)
                rotate(4deg);
        }

        70% {

            transform:
                translateY(15px)
                scale(1.05)
                rotate(-3deg);
        }

        90% {

            opacity: 0.75;
        }

        100% {

            left: calc(100% + 70px);

            opacity: 0;

            transform:
                translateY(0)
                scale(0.9)
                rotate(0deg);
        }
    }


    /* ========================================================
       PARTICLES
       ======================================================== */

    .intro-particle {

        position: absolute;

        width: 5px;
        height: 5px;

        border-radius: 50%;

        background: #67E8F9;

        box-shadow:
            0 0 12px #67E8F9;

        animation:
            particleFloat 2.8s ease-in-out infinite;
    }


    .particle-1 {
        left: 20%;
        top: 32%;
    }

    .particle-2 {
        left: 31%;
        top: 70%;
        animation-delay: 0.7s;
    }

    .particle-3 {
        right: 22%;
        top: 29%;
        animation-delay: 1.2s;
    }

    .particle-4 {
        right: 16%;
        bottom: 30%;
        animation-delay: 1.7s;
    }


    @keyframes particleFloat {

        0%, 100% {

            transform:
                translateY(0)
                scale(0.8);

            opacity: 0.25;
        }

        50% {

            transform:
                translateY(-14px)
                scale(1.35);

            opacity: 1;
        }
    }


    /* ========================================================
       TEXT ANIMATIONS
       ======================================================== */

    @keyframes introUp {

        from {

            opacity: 0;

            transform:
                translateY(30px);
        }

        to {

            opacity: 1;

            transform:
                translateY(0);
        }
    }


    @keyframes introFade {

        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }


    /* ========================================================
       EXIT
       ======================================================== */

    @keyframes introExit {

        0% {

            opacity: 1;

            visibility: visible;
        }

        100% {

            opacity: 0;

            visibility: hidden;

            pointer-events: none;
        }
    }

    </style>


    <div class="bird-intro">

        <div class="intro-glow"></div>


        <!-- Flying Birds -->

        <div class="intro-bird bird-one">
            🦜
        </div>

        <div class="intro-bird bird-two">
            🕊️
        </div>


        <!-- Particles -->

        <div class="intro-particle particle-1"></div>
        <div class="intro-particle particle-2"></div>
        <div class="intro-particle particle-3"></div>
        <div class="intro-particle particle-4"></div>


        <!-- Content -->

        <div class="intro-content">

            <div class="intro-badge">
                🌿 LIVE BIODIVERSITY ANALYTICS
            </div>


            <div class="intro-title">

                🐦 Welcome to

                <br>

                <span class="intro-title-highlight">
                    Bird Species Observation Analysis
                </span>

            </div>


            <div class="intro-subtitle">

                Explore biodiversity • Discover habitats •
                Understand observation patterns

            </div>


            <div class="intro-hook">

                ✦ OBSERVE&nbsp;&nbsp; • &nbsp;&nbsp;ANALYZE&nbsp;&nbsp; • &nbsp;&nbsp;DISCOVER ✦

            </div>

        </div>

    </div>
    """)

    # Intro duration
    time.sleep(4)

# =========================================================
# CUSTOM CSS - BIRD / NATURE THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(34,197,94,0.08), transparent 25%),
        radial-gradient(circle at 90% 15%, rgba(56,189,248,0.08), transparent 25%),
        #07111f;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* ================= HERO ================= */

/* =========================================================
   PREMIUM BIRD HERO SECTION
   ========================================================= */

.hero {
    position: relative;
    overflow: hidden;

    padding: 42px 45px 38px 45px;

    border-radius: 26px;

    background:
        radial-gradient(
            circle at 88% 20%,
            rgba(56,189,248,0.25),
            transparent 28%
        ),
        radial-gradient(
            circle at 72% 90%,
            rgba(34,197,94,0.20),
            transparent 30%
        ),
        linear-gradient(
            120deg,
            #063b2d 0%,
            #075e54 38%,
            #075985 72%,
            #123b62 100%
        );

    border: 1px solid rgba(125,211,252,0.28);

    box-shadow:
        0 18px 45px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.10);

    margin-bottom: 30px;
}


/* Decorative glow */

.hero::before {
    content: "";

    position: absolute;

    width: 260px;
    height: 260px;

    right: -80px;
    top: -100px;

    border-radius: 50%;

    background: rgba(45,212,191,0.16);

    filter: blur(10px);
}


/* Decorative second glow */

.hero::after {
    content: "";

    position: absolute;

    width: 180px;
    height: 180px;

    left: -90px;
    bottom: -100px;

    border-radius: 50%;

    background: rgba(34,197,94,0.14);

    filter: blur(15px);
}


/* HERO CONTENT */

.hero-content {
    position: relative;
    z-index: 5;

    max-width: 78%;
}


/* SMALL BADGE */

.hero-badge {
    display: inline-flex;
    align-items: center;

    padding: 7px 14px;

    border-radius: 30px;

    background: rgba(255,255,255,0.11);

    border: 1px solid rgba(255,255,255,0.18);

    color: #d1fae5;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.2px;

    margin-bottom: 15px;

    backdrop-filter: blur(8px);
}


/* TITLE */

.hero-title {
    font-size: 44px;
    line-height: 1.08;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -1.2px;
    margin-bottom: 13px;

    animation: heroTitleFloat 4s ease-in-out infinite;
}

@keyframes heroTitleFloat {

    0%, 100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-6px);
    }
}

/* TITLE HIGHLIGHT */

.hero-highlight {
    background: linear-gradient(
        90deg,
        #86efac,
        #67e8f9,
        #93c5fd
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;

    animation: titleGlow 3s ease-in-out infinite;
}

@keyframes titleGlow {

    0%, 100% {
        filter: drop-shadow(0 0 0px rgba(103,232,249,0));
    }

    50% {
        filter: drop-shadow(0 0 14px rgba(103,232,249,0.45));
    }
}

/* SUBTITLE */

.hero-subtitle {
    font-size: 15px;

    line-height: 1.7;

    color: #dbeafe;

    max-width: 780px;

    margin-bottom: 22px;
}


/* TAG CONTAINER */

.hero-tags {
    display: flex;

    flex-wrap: wrap;

    gap: 10px;
}


/* TAG */

.hero-tag {
    display: inline-flex;
    align-items: center;

    padding: 8px 14px;

    border-radius: 30px;

    background: rgba(255,255,255,0.10);

    border: 1px solid rgba(255,255,255,0.18);

    color: #f0fdf4;

    font-size: 12px;

    font-weight: 700;

    backdrop-filter: blur(8px);

    transition: all 0.2s ease;
}


/* TAG HOVER */

.hero-tag:hover {
    background: rgba(255,255,255,0.18);

    transform: translateY(-2px);

    border-color: rgba(125,211,252,0.5);
}


/* BIG BIRD */

.hero-bird {
    position: absolute;

    z-index: 3;

    right: 55px;
    top: 50%;

    transform: translateY(-50%);

    font-size: 125px;

    opacity: 0.18;

    filter:
        drop-shadow(0 15px 25px rgba(0,0,0,0.25));
}


/* BIRD GLOW */

.hero-bird-glow {
    position: absolute;

    z-index: 2;

    right: 40px;
    top: 50%;

    transform: translateY(-50%);

    width: 180px;
    height: 180px;

    border-radius: 50%;

    background: rgba(125,211,252,0.14);

    filter: blur(20px);
}

/* ================= KPI CARDS ================= */

/* =========================================================
   PREMIUM BIRD KPI CARDS
   ========================================================= */

.kpi-card {
    position: relative;
    overflow: hidden;

    min-height: 155px;
    padding: 22px 20px;

    border-radius: 20px;

    background: linear-gradient(
        145deg,
        #162a44 0%,
        #102238 55%,
        #0b1728 100%
    );

    border: 1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.05);

    transition: all 0.25s ease;
}


/* TOP COLOR STRIP */

.kpi-card::before {
    content: "";
    position: absolute;

    top: 0;
    left: 0;
    right: 0;

    height: 5px;

    background: linear-gradient(
        90deg,
        #22c55e,
        #06b6d4,
        #38bdf8,
        #a78bfa,
        #f59e0b
    );
}


/* GLOW */

.kpi-card::after {
    content: "";

    position: absolute;

    width: 110px;
    height: 110px;

    right: -35px;
    top: -35px;

    border-radius: 50%;

    background: rgba(34,211,238,0.12);

    filter: blur(8px);
}


/* ICON */

.kpi-icon {
    position: relative;
    z-index: 2;

    display: flex;
    align-items: center;
    justify-content: center;

    width: 48px;
    height: 48px;

    border-radius: 14px;

    background: linear-gradient(
        135deg,
        #064e3b,
        #075985
    );

    border: 1px solid rgba(56,189,248,0.35);

    font-size: 25px;

    margin-bottom: 13px;

    box-shadow:
        0 5px 18px rgba(0,0,0,0.25);
}


/* KPI TITLE */

.kpi-title {
    position: relative;
    z-index: 2;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.1px;
    text-transform: uppercase;

    color: #9fb6cc;

    margin-bottom: 7px;
}


/* KPI VALUE */

.kpi-value {
    position: relative;
    z-index: 2;

    font-size: 32px;
    line-height: 1;

    font-weight: 900;

    color: #ffffff;

    letter-spacing: -0.5px;

    text-shadow:
        0 3px 12px rgba(56,189,248,0.18);
}


/* HOVER EFFECT */

.kpi-card:hover {
    transform: translateY(-5px);

    border-color: rgba(56,189,248,0.45);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.45),
        0 0 25px rgba(14,165,233,0.12);
}
/* ================= SECTION ================= */

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 30px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 16px;
}

/* ================= INSIGHT ================= */

.insight-box {
    padding: 21px 25px;
    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            rgba(6,78,59,0.45),
            rgba(14,116,144,0.25)
        );

    border-left: 4px solid #38bdf8;

    margin-top: 22px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.18);
}

.insight-title {
    font-size: 17px;
    font-weight: 800;
    color: #f8fafc;
}

.insight-text {
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.7;
    margin-top: 8px;
}

/* ================= SIDEBAR ================= */

/* =========================================================
   PREMIUM SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #071a1f 0%,
        #08252a 45%,
        #06151c 100%
    );

    border-right: 1px solid rgba(52, 211, 153, 0.20);
}

/* Sidebar content */
section[data-testid="stSidebar"] > div {
    padding: 1.2rem 1rem;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
    font-weight: 800 !important;
    letter-spacing: 0.3px;
}

/* Navigation label */
section[data-testid="stSidebar"] label {
    color: #cbd5e1 !important;
}

/* Radio container */
section[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 7px;
}

/* Navigation options */
section[data-testid="stSidebar"] [role="radiogroup"] > label {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 9px 10px;
    margin: 2px 0;
    transition: all 0.2s ease;
}

/* Hover */
section[data-testid="stSidebar"] [role="radiogroup"] > label:hover {
    background: rgba(45, 212, 191, 0.12);
    border-color: rgba(45, 212, 191, 0.30);
    transform: translateX(3px);
}

/* Selected navigation item */
section[data-testid="stSidebar"] [role="radiogroup"] > label:has(
    input:checked
) {
    background: linear-gradient(
        90deg,
        rgba(16, 185, 129, 0.28),
        rgba(14, 165, 233, 0.18)
    );

    border: 1px solid rgba(52, 211, 153, 0.55);

    box-shadow:
        0 0 18px rgba(16, 185, 129, 0.12),
        inset 3px 0 0 #34d399;
}

/* Selected text */
section[data-testid="stSidebar"] [role="radiogroup"] > label:has(
    input:checked
) p {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* Radio buttons */
section[data-testid="stSidebar"] [role="radiogroup"] input {
    accent-color: #34d399;
}

/* Divider */
section[data-testid="stSidebar"] hr {
    border-color: rgba(148,163,184,0.15);
    margin: 20px 0;
}

/* Filter labels */
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSelectbox label {
    color: #d1fae5 !important;
    font-weight: 700 !important;
}

/* Filter boxes */
section[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(52, 211, 153, 0.20);
    border-radius: 11px;
}

/* Filter hover */
section[data-testid="stSidebar"] .stMultiSelect > div > div:hover {
    border-color: rgba(52, 211, 153, 0.55);
}

/* Selected filter tags */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: linear-gradient(
        90deg,
        #059669,
        #0891b2
    ) !important;

    border-radius: 7px !important;
}

/* Tag text */
section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: white !important;
    font-weight: 700 !important;
}

/* Sidebar select text */
section[data-testid="stSidebar"] input {
    color: white !important;
}

/* Sidebar small text */
section[data-testid="stSidebar"] small {
    color: #94a3b8 !important;
}

/* Sidebar scrollbar */
section[data-testid="stSidebar"] ::-webkit-scrollbar {
    width: 6px;
}

section[data-testid="stSidebar"] ::-webkit-scrollbar-track {
    background: #06151c;
}

section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
    background: linear-gradient(
        #10b981,
        #0891b2
    );
    border-radius: 10px;
}

/* ================= DIVIDER ================= */

hr {
    border-color: #243449;
}

/* ================= PLOTLY AREA ================= */

.js-plotly-plot {
    border-radius: 18px;
}
/* ================================
   🐦 BIRD ANALYTICS ANIMATIONS
   ================================ */

/* Smooth page elements */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(14px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Hero floating glow */
@keyframes softGlow {
    0%, 100% {
        filter: drop-shadow(0 0 0px rgba(52, 211, 153, 0));
    }
    50% {
        filter: drop-shadow(0 0 18px rgba(52, 211, 153, 0.25));
    }
}

/* Floating bird */
@keyframes birdFloat {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-8px);
    }
}

/* KPI hover */
@keyframes kpiGlow {
    from {
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    }
    to {
        box-shadow:
            0 14px 35px rgba(14,165,233,0.20),
            0 0 22px rgba(52,211,153,0.12);
    }
}


/* HERO */
div[data-testid="stMarkdownContainer"] {
    animation: fadeUp 0.7s ease-out;
}


/* KPI CARD HOVER */
div[data-testid="stHorizontalBlock"] > div {
    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;
}

div[data-testid="stHorizontalBlock"] > div:hover {
    transform: translateY(-5px);
    animation: kpiGlow 0.25s ease forwards;
}


/* Sidebar navigation hover */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    transition:
        transform 0.2s ease,
        background 0.2s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    transform: translateX(4px);
}


/* Buttons / pills */
button {
    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

button:hover {
    transform: translateY(-2px);
}


/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* =========================================================
   UNIQUE SPECIES KPI - EXPANDABLE HOVER TABLE
   ========================================================= */

.kpi-hover-wrapper {
    position: relative;
    width: 100%;
}


/* ---------------------------------------------------------
   TABLE PANEL - HIDDEN INITIALLY
   --------------------------------------------------------- */

.kpi-hover-panel {

    width: 100%;

    max-height: 0;

    opacity: 0;

    overflow: hidden;

    margin-top: 0;

    padding: 0;

    border-radius: 16px;

    background: linear-gradient(
        145deg,
        #0B2230,
        #0A1927
    );

    border: 1px solid transparent;

    transition:
        max-height 0.35s ease,
        opacity 0.25s ease,
        margin-top 0.25s ease,
        padding 0.25s ease,
        border-color 0.25s ease;

}


/* ---------------------------------------------------------
   SHOW TABLE ON HOVER
   --------------------------------------------------------- */

.kpi-hover-wrapper:hover .kpi-hover-panel {

    max-height: 430px;

    opacity: 1;

    margin-top: 10px;

    padding: 14px;

    border-color: rgba(
        45,
        212,
        191,
        0.40
    );

    box-shadow:
        0 15px 40px rgba(0,0,0,0.35);

}


/* ---------------------------------------------------------
   TABLE SCROLL AREA
   --------------------------------------------------------- */

.species-scroll {

    height: 360px;

    overflow-y: auto;

    overflow-x: hidden;

    border-radius: 10px;

}


/* ---------------------------------------------------------
   TABLE
   --------------------------------------------------------- */

.species-table {

    width: 100%;

    border-collapse: collapse;

    font-size: 11px;

}


/* ---------------------------------------------------------
   TABLE HEADER
   --------------------------------------------------------- */

.species-table thead th {

    position: sticky;

    top: 0;

    z-index: 5;

    background:
        linear-gradient(
            90deg,
            #0D9488,
            #2563EB
        );

    color: white;

    padding: 9px 7px;

    text-align: left;

    font-weight: 800;

    white-space: nowrap;

}


/* ---------------------------------------------------------
   TABLE CELLS
   --------------------------------------------------------- */

.species-table tbody td {

    padding: 8px 7px;

    color: #E2E8F0;

    border-bottom:
        1px solid
        rgba(148,163,184,0.10);

}


/* ---------------------------------------------------------
   ALTERNATE ROWS
   --------------------------------------------------------- */

.species-table tbody tr:nth-child(even) {

    background:
        rgba(255,255,255,0.035);

}


/* ---------------------------------------------------------
   ROW HOVER
   --------------------------------------------------------- */

.species-table tbody tr:hover {

    background:
        rgba(45,212,191,0.12);

}


/* ---------------------------------------------------------
   RANK
   --------------------------------------------------------- */

.species-table tbody td:first-child {

    color: #94A3B8;

    font-weight: 700;

}


/* ---------------------------------------------------------
   SCIENTIFIC NAME
   --------------------------------------------------------- */

.species-table tbody td:nth-child(3) {

    color: #A7F3D0;

    font-style: italic;

}


/* ---------------------------------------------------------
   OBSERVATIONS
   --------------------------------------------------------- */

.species-table tbody td:last-child {

    color: #67E8F9;

    font-weight: 800;

    text-align: right;

}


/* ---------------------------------------------------------
   SCROLLBAR
   --------------------------------------------------------- */

.species-scroll::-webkit-scrollbar {

    width: 6px;

}

.species-scroll::-webkit-scrollbar-track {

    background: #07151F;

}

.species-scroll::-webkit-scrollbar-thumb {

    background:
        linear-gradient(
            #14B8A6,
            #2563EB
        );

    border-radius: 10px;

}
</style>
""", unsafe_allow_html=True)
# =========================================================
# DATABASE CONNECTION
# =========================================================

@st.cache_resource
def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yash1693051043",
        database="bird_species_analysis"
    )


conn = get_connection()


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    query = """
    SELECT *
    FROM bird_observations
    """

    return pd.read_sql(query, conn)


df = load_data()


# =========================================================
# SIDEBAR - DASHBOARD NAVIGATION
# =========================================================
# ============================================================
# SIDEBAR - BIRD ANALYTICS
# ============================================================

# Sidebar styling
st.markdown("""
<style>

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #071a20 0%,
        #08252b 45%,
        #06151c 100%
    );
    border-right: 1px solid rgba(45, 212, 191, 0.20);
}

/* Sidebar padding */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

/* Brand */
.sidebar-brand {
    padding: 8px 6px 18px 6px;
    text-align: left;
}

.sidebar-brand-title {
    font-size: 21px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: 0.2px;
}

.sidebar-brand-subtitle {
    margin-top: 5px;
    font-size: 10px;
    font-weight: 800;
    color: #5eead4;
    letter-spacing: 1.3px;
}

/* Section headings */
.sidebar-section {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin: 8px 0 8px 4px;
}

/* Radio buttons */
[data-testid="stSidebar"] .stRadio > div {
    gap: 7px;
}

[data-testid="stSidebar"] .stRadio label {
    background: rgba(15, 42, 48, 0.70);
    border: 1px solid rgba(71, 106, 112, 0.35);
    border-radius: 11px;
    padding: 8px 10px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(20, 78, 74, 0.75);
    border-color: rgba(45, 212, 191, 0.55);
}

/* Selected radio */
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(
        90deg,
        rgba(5, 150, 105, 0.35),
        rgba(14, 116, 144, 0.35)
    );
    border-color: #2dd4bf;
    box-shadow: 0 0 12px rgba(45, 212, 191, 0.15);
}

/* Filter card */
.filter-box {
    background: linear-gradient(
        135deg,
        rgba(13, 66, 70, 0.55),
        rgba(8, 47, 56, 0.45)
    );
    border: 1px solid rgba(45, 212, 191, 0.20);
    border-radius: 13px;
    padding: 11px 12px;
    margin: 5px 0 12px 0;
}

.filter-title {
    color: #5eead4;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

.filter-subtitle {
    color: #94a3b8;
    font-size: 10px;
    margin-top: 3px;
}

/* =========================================================
   🐦 SINGLE FLYING BIRD IN SIDEBAR
   ========================================================= */

.sidebar-bird-zone {
    position: relative;
    width: 100%;
    height: 95px;
    margin: 2px 0 8px 0;
    overflow: hidden;
    border-radius: 16px;
    
    background:
        radial-gradient(
            circle at 50% 50%,
            rgba(45,212,191,0.10),
            transparent 65%
        );
}


/* Bird */

.sidebar-flying-bird {
    position: absolute;

    left: -45px;
    top: 28px;

    font-size: 30px;

    filter:
        drop-shadow(0 0 8px rgba(45,212,191,0.45));

    animation: sidebarBirdFly 7s linear infinite;
}


/* Flying movement */

@keyframes sidebarBirdFly {

    0% {
        left: -45px;
        top: 30px;
        transform: scaleX(1) rotate(0deg);
        opacity: 0;
    }

    8% {
        opacity: 1;
    }

    25% {
        top: 16px;
        transform: scaleX(1) rotate(-4deg);
    }

    45% {
        top: 34px;
        transform: scaleX(1) rotate(3deg);
    }

    65% {
        top: 12px;
        transform: scaleX(1) rotate(-3deg);
    }

    85% {
        top: 28px;
        opacity: 1;
    }

    100% {
        left: calc(100% + 45px);
        top: 22px;
        transform: scaleX(1) rotate(0deg);
        opacity: 0;
    }
}
/* =========================================================
   🌿 PREMIUM SIDEBAR BIODIVERSITY VISUAL
   ========================================================= */

.sidebar-nature-visual {

    position: relative;

    width: 100%;

    height: 135px;

    margin: 4px 0 18px 0;

    overflow: hidden;

    border-radius: 20px;

    background:
        radial-gradient(
            circle at 50% 45%,
            rgba(45,212,191,0.14),
            transparent 40%
        ),
        linear-gradient(
            135deg,
            rgba(6,78,59,0.20),
            rgba(14,116,144,0.12)
        );

    border: 1px solid rgba(45,212,191,0.14);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.04);

}


/* =========================================================
   GLOW
   ========================================================= */

.nature-glow {

    position: absolute;

    border-radius: 50%;

    filter: blur(12px);

    pointer-events: none;

}


.glow-one {

    width: 70px;

    height: 70px;

    left: 20px;

    top: 20px;

    background: rgba(34,197,94,0.16);

    animation: natureGlowOne 4s ease-in-out infinite;

}


.glow-two {

    width: 90px;

    height: 90px;

    right: -10px;

    bottom: -25px;

    background: rgba(14,165,233,0.13);

    animation: natureGlowTwo 5s ease-in-out infinite;

}


@keyframes natureGlowOne {

    0%, 100% {
        transform: scale(1);
        opacity: 0.45;
    }

    50% {
        transform: scale(1.25);
        opacity: 0.80;
    }

}


@keyframes natureGlowTwo {

    0%, 100% {
        transform: scale(1);
        opacity: 0.35;
    }

    50% {
        transform: scale(1.18);
        opacity: 0.70;
    }

}


/* =========================================================
   ORBITS
   ========================================================= */

.orbit {

    position: absolute;

    left: 50%;

    top: 48%;

    transform: translate(-50%, -50%);

    border: 1px solid rgba(94,234,212,0.18);

    border-radius: 50%;

}


.orbit-one {

    width: 76px;

    height: 76px;

    animation: orbitRotateOne 7s linear infinite;

}


.orbit-two {

    width: 105px;

    height: 105px;

    border-color: rgba(96,165,250,0.12);

    animation: orbitRotateTwo 11s linear infinite reverse;

}


@keyframes orbitRotateOne {

    from {
        transform: translate(-50%, -50%) rotate(0deg);
    }

    to {
        transform: translate(-50%, -50%) rotate(360deg);
    }

}


@keyframes orbitRotateTwo {

    from {
        transform: translate(-50%, -50%) rotate(0deg);
    }

    to {
        transform: translate(-50%, -50%) rotate(360deg);
    }

}


/* =========================================================
   FLOATING LEAVES
   ========================================================= */

.leaf {

    position: absolute;

    font-size: 22px;

    opacity: 0.80;

    filter:
        drop-shadow(
            0 0 7px rgba(45,212,191,0.35)
        );

}


.leaf-one {

    left: 21px;

    top: 48px;

    animation:
        leafFloatOne
        4s ease-in-out infinite;

}


.leaf-two {

    right: 20px;

    top: 23px;

    font-size: 19px;

    animation:
        leafFloatTwo
        5s ease-in-out infinite;

}


.leaf-three {

    left: 48px;

    bottom: 17px;

    font-size: 16px;

    animation:
        leafFloatThree
        4.8s ease-in-out infinite;

}


@keyframes leafFloatOne {

    0%, 100% {
        transform:
            translateY(0)
            rotate(-8deg);
    }

    50% {
        transform:
            translateY(-10px)
            rotate(10deg);
    }

}


@keyframes leafFloatTwo {

    0%, 100% {
        transform:
            translateY(0)
            rotate(8deg);
    }

    50% {
        transform:
            translateY(9px)
            rotate(-10deg);
    }

}


@keyframes leafFloatThree {

    0%, 100% {
        transform:
            translateY(0)
            rotate(0deg);
    }

    50% {
        transform:
            translateY(-7px)
            rotate(12deg);
    }

}


/* =========================================================
   FLOATING FEATHER
   ========================================================= */

.nature-feather {

    position: absolute;

    left: 50%;

    top: 50%;

    transform: translate(-50%, -50%);

    font-size: 39px;

    filter:
        drop-shadow(
            0 0 9px rgba(103,232,249,0.50)
        );

    animation:
        featherFloat
        3.8s ease-in-out infinite;

    z-index: 5;

}


@keyframes featherFloat {

    0%, 100% {

        transform:
            translate(-50%, -50%)
            translateY(0px)
            rotate(-8deg);

    }

    50% {

        transform:
            translate(-50%, -50%)
            translateY(-8px)
            rotate(8deg);

    }

}


/* =========================================================
   GLOWING DOTS
   ========================================================= */

.nature-dot {

    position: absolute;

    width: 5px;

    height: 5px;

    border-radius: 50%;

    background: #5EEAD4;

    box-shadow:
        0 0 8px #5EEAD4;

    animation:
        dotPulse
        2.8s ease-in-out infinite;

}


.dot-one {

    left: 25%;

    top: 24%;

}


.dot-two {

    right: 24%;

    top: 52%;

    animation-delay: 0.8s;

}


.dot-three {

    left: 35%;

    bottom: 22%;

    animation-delay: 1.5s;

}


@keyframes dotPulse {

    0%, 100% {

        opacity: 0.25;

        transform: scale(0.8);

    }

    50% {

        opacity: 1;

        transform: scale(1.35);

    }

}


/* =========================================================
   CAPTION
   ========================================================= */

.nature-caption {

    position: absolute;

    left: 50%;

    bottom: 10px;

    transform: translateX(-50%);

    white-space: nowrap;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: 1.2px;

    color: #99F6E4;

    opacity: 0.82;

}


.nature-caption span {

    display: inline-block;

    margin-right: 5px;

    font-size: 7px;

    animation:
        captionPulse
        1.8s ease-in-out infinite;

}


@keyframes captionPulse {

    0%, 100% {
        opacity: 0.35;
    }

    50% {
        opacity: 1;
    }

}
/* =========================================================
   🐦 ANIMATED BIRD IMAGE SLIDESHOW
   ========================================================= */

.hero-bird-slideshow {

    position: absolute;

    right: 25px;
    top: 50%;

    width: 250px;
    height: 250px;

    transform: translateY(-50%);

    z-index: 3;

    pointer-events: none;

}


/* All bird images */

.hero-bird-slideshow .slide {

    position: absolute;

    inset: 0;

    width: 100%;
    height: 100%;

    object-fit: contain;

    opacity: 0;

    filter:
        drop-shadow(
            0 15px 25px rgba(0,0,0,0.25)
        );

    animation:
        birdSlideShow 16s infinite;

}


/* Different timing */

.hero-bird-slideshow .slide1 {
    animation-delay: 0s;
}

.hero-bird-slideshow .slide2 {
    animation-delay: 4s;
}

.hero-bird-slideshow .slide3 {
    animation-delay: 8s;
}

.hero-bird-slideshow .slide4 {
    animation-delay: 12s;
}


/* =========================================================
   IMAGE TRANSITION
   ========================================================= */

@keyframes birdSlideShow {

    0% {

        opacity: 0;

        transform:
            scale(0.82)
            translateY(12px)
            rotate(-3deg);

    }

    8% {

        opacity: 0.18;

    }

    18% {

        opacity: 0.22;

        transform:
            scale(1)
            translateY(0)
            rotate(0deg);

    }

    25% {

        opacity: 0.20;

    }

    30% {

        opacity: 0;

        transform:
            scale(1.05)
            translateY(-5px)
            rotate(3deg);

    }

    100% {

        opacity: 0;

    }

}
/* =========================================================
   🐦 CLEAR BIRD SLIDESHOW
   Blur → Clear → Hold → Blur → Next
   ========================================================= */

.hero-bird-slideshow {
    position: absolute;
    right: 25px;
    top: 50%;

    width: 270px;
    height: 270px;

    transform: translateY(-50%);

    z-index: 3;
    pointer-events: none;
    overflow: visible;
}


/* Every bird image */

.hero-bird-slideshow .hero-bird-slide {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 245px;
    height: 245px;

    object-fit: contain;

    transform:
        translate(-50%, -50%)
        scale(0.88);

    opacity: 0;

    filter:
        blur(10px)
        saturate(0.85);

    animation:
        birdClearShow 16s infinite;

    transition: none;
}


/* Timing */

.hero-bird-slideshow .slide-1 {
    animation-delay: 0s;
}

.hero-bird-slideshow .slide-2 {
    animation-delay: 4s;
}

.hero-bird-slideshow .slide-3 {
    animation-delay: 8s;
}

.hero-bird-slideshow .slide-4 {
    animation-delay: 12s;
}


/* =========================================================
   BLUR → CLEAR → HOLD → BLUR
   ========================================================= */

@keyframes birdClearShow {

    /* Hidden */

    0% {
        opacity: 0;

        filter:
            blur(12px)
            saturate(0.65);

        transform:
            translate(-50%, -50%)
            scale(0.84);
    }


    /* Blur se enter */

    6% {
        opacity: 0.12;

        filter:
            blur(8px)
            saturate(0.75);

        transform:
            translate(-50%, -50%)
            scale(0.90);
    }


    /* Almost clear */

    12% {
        opacity: 0.90;

        filter:
            blur(2px)
            saturate(0.90);

        transform:
            translate(-50%, -50%)
            scale(0.97);
    }


    /* FULLY CLEAR */

    18% {
        opacity: 1;

        filter:
            blur(0px)
            saturate(1);

        transform:
            translate(-50%, -50%)
            scale(1);
    }


    /* Stay clear */

    22% {
        opacity: 1;

        filter:
            blur(0px)
            saturate(1);

        transform:
            translate(-50%, -50%)
            scale(1);
    }


    /* Stay clear a little longer */

    25% {
        opacity: 0.95;

        filter:
            blur(0px)
            saturate(1);

        transform:
            translate(-50%, -50%)
            scale(1.01);
    }


    /* Start disappearing */

    28% {
        opacity: 0.55;

        filter:
            blur(3px)
            saturate(0.9);

        transform:
            translate(-50%, -50%)
            scale(1.03);
    }


    /* Blur out */

    32% {
        opacity: 0;

        filter:
            blur(12px)
            saturate(0.65);

        transform:
            translate(-50%, -50%)
            scale(1.08);
    }


    /* Wait for next slide */

    100% {
        opacity: 0;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# BRAND
# ============================================================

st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-brand-title">
        🐦 Bird Analytics
    </div>
    <div class="sidebar-brand-subtitle">
        BIODIVERSITY DASHBOARD
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# NAVIGATION
# ============================================================
# ============================================================
# 🐦 SIDEBAR FLYING BIRD
# ============================================================

# ============================================================
# 🌿 SIDEBAR BIODIVERSITY VISUAL
# ============================================================

st.sidebar.html("""
<div class="sidebar-nature-visual">

    <div class="nature-glow glow-one"></div>
    <div class="nature-glow glow-two"></div>

    <div class="orbit orbit-one"></div>
    <div class="orbit orbit-two"></div>

    <div class="leaf leaf-one">🍃</div>
    <div class="leaf leaf-two">🌿</div>
    <div class="leaf leaf-three">🍃</div>

    <div class="nature-feather">🪶</div>

    <div class="nature-dot dot-one"></div>
    <div class="nature-dot dot-two"></div>
    <div class="nature-dot dot-three"></div>

    <div class="nature-caption">
        <span>●</span> LIVE BIODIVERSITY
    </div>

</div>
""")
st.sidebar.markdown(
    '<div class="sidebar-section">🧭 EXPLORE</div>',
    unsafe_allow_html=True
)

selected_page = st.sidebar.radio(
    "",
    [
        "🏠 Overview",
        "🐦 Species Analysis",
        "🌳 Habitat & Location",
        "🌦️ Environmental Analysis",
        "📅 Temporal Analysis",
        "👤 Observation Analysis",
        "🛡️ Conservation Analysis"
    ],
    index=0,
    label_visibility="collapsed"
)


# ============================================================
# DIVIDER
# ============================================================

st.sidebar.markdown(
    "<hr style='border:none;border-top:1px solid rgba(148,163,184,0.18);margin:16px 0;'>",
    unsafe_allow_html=True
)


# ============================================================
# FILTER HEADER
# ============================================================

st.sidebar.markdown("""
<div class="filter-box">
    <div class="filter-title">🎛️ DATA FILTERS</div>
    <div class="filter-subtitle">
        Refine your biodiversity analysis
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

years = sorted(
    df["Year"].dropna().unique()
)

selected_year = st.sidebar.multiselect(
    "📅 Select Year",
    years,
    default=years
)


locations = sorted(
    df["Location_Type"].dropna().unique()
)

selected_location = st.sidebar.multiselect(
    "🌳 Location Type",
    locations,
    default=locations
)


observers = sorted(
    df["Observer"].dropna().unique()
)

selected_observer = st.sidebar.multiselect(
    "👤 Observer",
    observers,
    default=observers
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    df["Year"].isin(selected_year)
    & df["Location_Type"].isin(selected_location)
    & df["Observer"].isin(selected_observer)
].copy()


# =========================================================
# =========================================================
# PAGE 1 - OVERVIEW
# =========================================================
# =========================================================

if selected_page == "🏠 Overview":

    # =========================================================
    # PREMIUM HERO
    # =========================================================

    st.html("""
    <div class="hero">

        <!-- Decorative Bird -->
            <div class="hero-bird-slideshow">

        <img
            src="https://upload.wikimedia.org/wikipedia/commons/9/90/Colorful_Bird.jpg"
            class="hero-bird-slide slide-1"
        >

        <img
            src="https://upload.wikimedia.org/wikipedia/commons/3/36/Bird_with_beautiful_color.jpg"
            class="hero-bird-slide slide-2"
        >

        <img
            src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Bird_on_Flight.jpg"
            class="hero-bird-slide slide-3"
        >

       <img
            src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Apus_apus_flying_(transparent_background).png"
            class="hero-bird-slide slide-4"
        >

        <div class="bird-scene-glow"></div>

        <div class="bird-scene-ring ring-1"></div>
        <div class="bird-scene-ring ring-2"></div>

    </div>


        <!-- Main Content -->
        <div class="hero-content">

            <!-- Badge -->
            <div class="hero-badge">
                🟢 LIVE BIODIVERSITY ANALYTICS
            </div>


            <!-- Title -->
            <div class="hero-title">

                🐦 Bird Species
                <span class="hero-highlight">
                    Observation Analysis
                </span>

            </div>


            <!-- Subtitle -->
            <div class="hero-subtitle">

                Discover bird diversity, habitat patterns and
                observation trends across forest and grassland
                ecosystems through interactive data analytics.

            </div>


            <!-- Tags -->
            <div class="hero-tags">

                <span class="hero-tag">
                    🌿 Biodiversity
                </span>

                <span class="hero-tag">
                    🐦 Species Monitoring
                </span>

                <span class="hero-tag">
                    🌳 Habitat Insights
                </span>

                <span class="hero-tag">
                    📊 Data Analytics
                </span>

            </div>

        </div>

    </div>
    """)

    # -----------------------------------------------------
    # KPI CALCULATIONS
    # -----------------------------------------------------

    total_observations = len(filtered_df)

    unique_species = filtered_df["Scientific_Name"].nunique()

    total_sites = filtered_df["Site_Name"].nunique()

    total_observers = filtered_df["Observer"].nunique()

    avg_temperature = filtered_df["Temperature"].mean()

    # =========================================================
    # PREMIUM KPI CARDS
    # =========================================================
    # ============================================================
    # OBSERVATION SITE DETAILS
    # ============================================================

    site_detail = (
        filtered_df
        .groupby("Site_Name")
        .agg(
            Observations=("Site_Name", "size"),
            Unique_Species=("Scientific_Name", "nunique"),
            Habitats=("Location_Type", "nunique")
        )
        .reset_index()
        .sort_values(
            "Observations",
            ascending=False
        )
        .reset_index(drop=True)
    )

    site_detail.insert(
        0,
        "Rank",
        range(1, len(site_detail) + 1)
    )


    # ============================================================
    # OBSERVER DETAILS
    # ============================================================

    observer_detail = (
        filtered_df
        .groupby("Observer")
        .agg(
            Observations=("Observer", "size"),
            Unique_Species=("Scientific_Name", "nunique"),
            Observation_Sites=("Site_Name", "nunique")
        )
        .reset_index()
        .sort_values(
            "Observations",
            ascending=False
        )
        .reset_index(drop=True)
    )

    observer_detail.insert(
        0,
        "Rank",
        range(1, len(observer_detail) + 1)
    )
    c1, c2, c3, c4, c5 = st.columns(5, gap="medium")

    # ============================================================
    # TOTAL OBSERVATION DETAILS
    # ============================================================

    observation_detail = (
        filtered_df
        .groupby("Common_Name")
        .agg(
            Observations=("Common_Name", "size"),
            Scientific_Name=("Scientific_Name", "first"),
            Habitats=("Location_Type", "nunique"),
            Sites=("Site_Name", "nunique")
        )
        .reset_index()
        .sort_values(
            "Observations",
            ascending=False
        )
        .reset_index(drop=True)
    )

    observation_detail.insert(
        0,
        "Rank",
        range(1, len(observation_detail) + 1)
    )


    observation_rows = ""

    for _, row in observation_detail.iterrows():

        observation_rows += f"""
<tr>

    <td>{int(row["Rank"])}</td>

    <td>{str(row["Common_Name"])}</td>

    <td>{int(row["Observations"]):,}</td>

    <td>{int(row["Habitats"]):,}</td>

    <td>{int(row["Sites"]):,}</td>

</tr>
"""
    # =========================================================
    # KPI 1 - TOTAL OBSERVATIONS
    # =========================================================

       # ============================================================
    # KPI 1 - TOTAL OBSERVATIONS + HOVER TABLE
    # ============================================================

    with c1:

        st.html(f"""
<div class="kpi-hover-wrapper">

    <!-- KPI CARD -->

    <div class="kpi-card">

        <div class="kpi-icon">
            🐦
        </div>

        <div class="kpi-title">
            Total Observations
        </div>

        <div class="kpi-value">
            {total_observations:,}
        </div>

        <div style="
            color:#67E8F9;
            font-size:10px;
            font-weight:700;
            margin-top:8px;
        ">
            Hover to explore observations →
        </div>

    </div>


    <!-- HOVER TABLE -->

    <div class="kpi-hover-panel">

        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:10px;
            margin-bottom:12px;
        ">

            <div style="
                color:#5EEAD4;
                font-size:14px;
                font-weight:800;
            ">
                🐦 Observation Details
            </div>

            <div style="
                background:linear-gradient(
                    90deg,
                    #0D9488,
                    #2563EB
                );

                color:white;

                padding:5px 9px;

                border-radius:8px;

                font-size:10px;

                font-weight:800;

                white-space:nowrap;
            ">
                {total_observations:,} Records
            </div>

        </div>


        <div class="species-scroll">

            <table class="species-table">

                <thead>

                    <tr>

                        <th>#</th>

                        <th>Common Name</th>

                        <th>Obs.</th>

                        <th>Habitat</th>

                        <th>Sites</th>

                    </tr>

                </thead>

                <tbody>

                    {observation_rows}

                </tbody>

            </table>

        </div>

    </div>

</div>
""")

    # ============================================================
    # UNIQUE SPECIES DETAILS FOR KPI HOVER
    # ============================================================

    species_detail = (
        filtered_df
        .groupby(
            ["Common_Name", "Scientific_Name"]
        )
        .size()
        .reset_index(
            name="Observations"
        )
        .sort_values(
            "Observations",
            ascending=False
        )
        .reset_index(drop=True)
    )

    species_detail.insert(
        0,
        "Rank",
        range(1, len(species_detail) + 1)
    )
    # =========================================================
    # KPI 2 - UNIQUE SPECIES
    # =========================================================

    with c2:

        species_rows = ""

        for _, row in species_detail.iterrows():

            species_rows += f"""
            <tr>

                <td>
                    {int(row["Rank"])}
                </td>

                <td>
                    {str(row["Common_Name"])}
                </td>

                <td>
                    <i>{str(row["Scientific_Name"])}</i>
                </td>

                <td>
                    {int(row["Observations"]):,}
                </td>

            </tr>
            """


        st.html(f"""

    <div class="kpi-hover-wrapper">

        <!-- ================= KPI CARD ================= -->

        <div class="kpi-card">

            <div class="kpi-icon">
                🧬
            </div>

            <div class="kpi-title">
                Unique Species
            </div>

            <div class="kpi-value">
                {unique_species:,}
            </div>

            <div style="
                font-size:10px;
                color:#67E8F9;
                margin-top:8px;
                font-weight:700;
            ">
                Hover to explore species →
            </div>

        </div>


        <!-- ================= HOVER TABLE ================= -->

        <div class="kpi-hover-panel">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:12px;
            ">

                <div style="
                    color:#5EEAD4;
                    font-size:14px;
                    font-weight:800;
                ">
                    🧬 Species Details
                </div>

                <div style="
                    color:#FFFFFF;
                    background:linear-gradient(
                        90deg,
                        #0D9488,
                        #2563EB
                    );
                    padding:5px 10px;
                    border-radius:8px;
                    font-size:11px;
                    font-weight:800;
                ">
                    {unique_species} Species
                </div>

            </div>


            <div class="species-scroll">

                <table class="species-table">

                    <thead>

                        <tr>

                            <th>#</th>

                            <th>Common Name</th>

                            <th>Scientific Name</th>

                            <th>Obs.</th>

                        </tr>

                    </thead>

                    <tbody>

                        {species_rows}

                    </tbody>

                </table>

            </div>

        </div>

    </div>
    """)

    # =========================================================
    # KPI 3 - OBSERVATION SITES
    # =========================================================

       # ============================================================
    # KPI 3 - OBSERVATION SITES + HOVER TABLE
    # ============================================================

    site_rows = ""

    for _, row in site_detail.iterrows():

        site_rows += f"""
<tr>

    <td>
        {int(row["Rank"])}
    </td>

    <td>
        {str(row["Site_Name"])}
    </td>

    <td>
        {int(row["Observations"]):,}
    </td>

    <td>
        {int(row["Unique_Species"]):,}
    </td>

    <td>
        {int(row["Habitats"]):,}
    </td>

</tr>
"""


    with c3:

        st.html(f"""
<div class="kpi-hover-wrapper">

    <!-- KPI CARD -->

    <div class="kpi-card">

        <div class="kpi-icon">
            📍
        </div>

        <div class="kpi-title">
            Observation Sites
        </div>

        <div class="kpi-value">
            {total_sites:,}
        </div>

        <div style="
            color:#67E8F9;
            font-size:10px;
            font-weight:700;
            margin-top:8px;
        ">
            Hover to explore sites →
        </div>

    </div>


    <!-- HOVER TABLE -->

    <div class="kpi-hover-panel">

        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:10px;
            margin-bottom:12px;
        ">

            <div style="
                color:#5EEAD4;
                font-size:14px;
                font-weight:800;
            ">
                📍 Observation Site Details
            </div>

            <div style="
                background:linear-gradient(
                    90deg,
                    #0D9488,
                    #2563EB
                );
                color:white;
                padding:5px 9px;
                border-radius:8px;
                font-size:10px;
                font-weight:800;
                white-space:nowrap;
            ">
                {total_sites} Sites
            </div>

        </div>


        <div class="species-scroll">

            <table class="species-table">

                <thead>

                    <tr>
                        <th>#</th>
                        <th>Site Name</th>
                        <th>Obs.</th>
                        <th>Species</th>
                        <th>Habitat</th>
                    </tr>

                </thead>

                <tbody>

                    {site_rows}

                </tbody>

            </table>

        </div>

    </div>

</div>
""")

    # =========================================================
    # KPI 4 - ACTIVE OBSERVERS
    # =========================================================

       # ============================================================
    # KPI 4 - ACTIVE OBSERVERS + HOVER TABLE
    # ============================================================

    observer_rows = ""

    for _, row in observer_detail.iterrows():

        observer_rows += f"""
<tr>

    <td>
        {int(row["Rank"])}
    </td>

    <td>
        {str(row["Observer"])}
    </td>

    <td>
        {int(row["Observations"]):,}
    </td>

    <td>
        {int(row["Unique_Species"]):,}
    </td>

    <td>
        {int(row["Observation_Sites"]):,}
    </td>

</tr>
"""


    with c4:

        st.html(f"""
<div class="kpi-hover-wrapper">

    <!-- KPI CARD -->

    <div class="kpi-card">

        <div class="kpi-icon">
            👤
        </div>

        <div class="kpi-title">
            Active Observers
        </div>

        <div class="kpi-value">
            {total_observers:,}
        </div>

        <div style="
            color:#67E8F9;
            font-size:10px;
            font-weight:700;
            margin-top:8px;
        ">
            Hover to explore observers →
        </div>

    </div>


    <!-- HOVER TABLE -->

    <div class="kpi-hover-panel">

        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:10px;
            margin-bottom:12px;
        ">

            <div style="
                color:#5EEAD4;
                font-size:14px;
                font-weight:800;
            ">
                👤 Observer Details
            </div>

            <div style="
                background:linear-gradient(
                    90deg,
                    #0D9488,
                    #2563EB
                );
                color:white;
                padding:5px 9px;
                border-radius:8px;
                font-size:10px;
                font-weight:800;
                white-space:nowrap;
            ">
                {total_observers} Observers
            </div>

        </div>


        <div class="species-scroll">

            <table class="species-table">

                <thead>

                    <tr>
                        <th>#</th>
                        <th>Observer</th>
                        <th>Obs.</th>
                        <th>Species</th>
                        <th>Sites</th>
                    </tr>

                </thead>

                <tbody>

                    {observer_rows}

                </tbody>

            </table>

        </div>

    </div>

</div>
""")


    # =========================================================
    # KPI 5 - AVERAGE TEMPERATURE
    # =========================================================

    with c5:

        st.html(f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                🌡️
            </div>

            <div class="kpi-title">
                Avg Temperature
            </div>

            <div class="kpi-value">
                {avg_temperature:.1f}°C
            </div>

        </div>
        """)

         # ============================================================
    # MONTHLY OBSERVATION ACTIVITY
    # ============================================================

    st.markdown("## 📅 Monthly Observation Activity")

    st.caption(
        "Track bird observation activity across all months to identify "
        "high-activity and low-activity periods."
    )


    # ------------------------------------------------------------
    # PREPARE MONTHLY DATA
    # ------------------------------------------------------------

    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]


    # Use filtered data so sidebar filters work
    monthly_df = filtered_df.copy()


    # ------------------------------------------------------------
    # CREATE MONTH COLUMN
    # ------------------------------------------------------------

    if "Month" in monthly_df.columns:

        monthly_df["Month"] = (
            monthly_df["Month"]
            .astype(str)
            .str.strip()
            .str[:3]
            .str.title()
        )

    else:

        date_column = None

        possible_date_columns = [
            "Observation Date",
            "Date",
            "ObservationDate",
            "date",
            "DATE"
        ]


        for col in possible_date_columns:

            if col in monthly_df.columns:
                date_column = col
                break


        if date_column is not None:

            monthly_df[date_column] = pd.to_datetime(
                monthly_df[date_column],
                errors="coerce"
            )

            monthly_df["Month"] = (
                monthly_df[date_column]
                .dt.strftime("%b")
            )

        else:

            st.warning(
                "Month/Date column not found in the dataset."
            )

            st.stop()


    # ------------------------------------------------------------
    # COUNT OBSERVATIONS BY MONTH
    # ------------------------------------------------------------

    monthly_counts = (
        monthly_df["Month"]
        .value_counts()
        .reindex(
            month_order,
            fill_value=0
        )
    )


    monthly_data = pd.DataFrame({

        "Month": month_order,

        "Observations": monthly_counts.values

    })


    # ------------------------------------------------------------
    # ACTIVE MONTHS
    # ------------------------------------------------------------

    active_months = monthly_data[
        monthly_data["Observations"] > 0
    ]


    if not active_months.empty:

        highest_row = active_months.loc[
            active_months["Observations"].idxmax()
        ]

        lowest_row = active_months.loc[
            active_months["Observations"].idxmin()
        ]


        highest_month = str(
            highest_row["Month"]
        )

        highest_value = int(
            highest_row["Observations"]
        )


        lowest_month = str(
            lowest_row["Month"]
        )

        lowest_value = int(
            lowest_row["Observations"]
        )

    else:

        highest_month = "N/A"
        highest_value = 0

        lowest_month = "N/A"
        lowest_value = 0


    # ------------------------------------------------------------
    # PROFESSIONAL MONTHLY CHART
    # ------------------------------------------------------------

    fig_monthly = go.Figure()


    # Area + Line
    fig_monthly.add_trace(

        go.Scatter(

            x=monthly_data["Month"],

            y=monthly_data["Observations"],

            mode="lines+markers",

            name="Observations",

            line=dict(
                color="#2DD4BF",
                width=4
            ),

            marker=dict(
                size=9,
                color="#2DD4BF",
                line=dict(
                    color="#FFFFFF",
                    width=1.5
                )
            ),

            fill="tozeroy",

            fillcolor="rgba(45,212,191,0.16)",

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Observations: %{y:,}"
                "<extra></extra>"
            )
        )
    )


    # ------------------------------------------------------------
    # HIGHLIGHT PEAK MONTH
    # ------------------------------------------------------------

    if highest_value > 0:

        fig_monthly.add_trace(

            go.Scatter(

                x=[highest_month],

                y=[highest_value],

                mode="markers+text",

                name="Peak Month",

                marker=dict(
                    size=17,
                    color="#F59E0B",
                    line=dict(
                        color="#FFFFFF",
                        width=2
                    )
                ),

                text=[
                    f"Peak: {highest_value:,}"
                ],

                textposition="top center",

                textfont=dict(
                    color="#FFFFFF",
                    size=12
                ),

                hovertemplate=(
                    f"<b>{highest_month}</b><br>"
                    f"Peak observations: "
                    f"{highest_value:,}"
                    "<extra></extra>"
                )
            )
        )


    # ------------------------------------------------------------
    # CHART LAYOUT
    # ------------------------------------------------------------

    fig_monthly.update_layout(

        title=dict(
            text="<b>Bird Observation Activity by Month</b>",
            x=0.02,
            xanchor="left",
            font=dict(
                size=18,
                color="white"
            )
        ),

        template="plotly_dark",

        paper_bgcolor="#0E1117",

        plot_bgcolor="#0E1117",

        height=480,

        hovermode="x unified",

        xaxis=dict(

            title="Month",

            categoryorder="array",

            categoryarray=month_order,

            tickmode="array",

            tickvals=month_order,

            showgrid=False
        ),

        yaxis=dict(

            title="Number of Observations",

            rangemode="tozero",

            separatethousands=True,

            gridcolor="rgba(255,255,255,0.12)"
        ),

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.02,

            xanchor="right",

            x=1
        ),

        margin=dict(

            l=50,

            r=30,

            t=85,

            b=50
        )
    )


    st.plotly_chart(

        fig_monthly,

        use_container_width=True,

        config={
            "displayModeBar": True,
            "displaylogo": False
        }
    )


       # ============================================================
    # BUSINESS INSIGHTS
    # ============================================================

    if highest_value > 0:

        st.html(f"""
<div style="
    background: linear-gradient(
        135deg,
        rgba(20,184,166,0.14),
        rgba(14,116,144,0.08)
    );
    border: 1px solid rgba(45,212,191,0.28);
    border-left: 5px solid #2DD4BF;
    border-radius: 16px;
    padding: 20px 24px;
    margin-top: 20px;
    margin-bottom: 16px;
">

    <div style="
        color: #5EEAD4;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 12px;
    ">
        💡 BUSINESS INSIGHTS
    </div>

    <div style="
        color: #F8FAFC;
        font-size: 14px;
        line-height: 1.9;
    ">

        <div>
            • <b>Peak observation activity:</b>
            {highest_month} recorded the highest number of
            observations (<b>{highest_value:,}</b>).
        </div>

        <br>

        <div>
            • <b>Lowest active month:</b>
            {lowest_month} recorded the lowest observation
            activity among months with available observations
            (<b>{lowest_value:,}</b>).
        </div>

        <br>

        <div>
            • <b>Seasonal concentration:</b>
            Observation activity is concentrated in specific
            months, indicating that monitoring intensity is not
            evenly distributed throughout the year.
        </div>

        <br>

        <div>
            • <b>Monitoring opportunity:</b>
            Months with lower observation activity may require
            additional field coverage to determine whether lower
            counts are associated with bird activity or reduced
            observation effort.
        </div>

    </div>

</div>
""")


    else:

        st.info(
            "No observation activity is available "
            "for the selected dataset."
        )


    # ============================================================
    # BUSINESS RECOMMENDATIONS
    # ============================================================

    st.html("""
<div style="
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.14),
        rgba(37,99,235,0.08)
    );
    border: 1px solid rgba(96,165,250,0.28);
    border-left: 5px solid #60A5FA;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 25px;
">

    <div style="
        color: #93C5FD;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 12px;
    ">
        🎯 BUSINESS RECOMMENDATIONS
    </div>

    <div style="
        color: #F8FAFC;
        font-size: 14px;
        line-height: 1.9;
    ">

        <div>
            • <b>Prioritize peak months:</b>
            Allocate more field resources during high-activity
            months to maximize species monitoring and data collection.
        </div>

        <br>

        <div>
            • <b>Investigate low-activity periods:</b>
            Review whether low observation counts are associated
            with reduced field visits, environmental conditions,
            or genuinely lower bird activity.
        </div>

        <br>

        <div>
            • <b>Improve year-round coverage:</b>
            Maintain a consistent observation schedule across
            months to reduce seasonal data gaps.
        </div>

        <br>

        <div>
            • <b>Plan conservation activities:</b>
            Use monthly observation patterns to schedule habitat
            monitoring and conservation efforts during periods
            of stronger observation activity.
        </div>

    </div>

</div>
""")
    # ============================================================
    # HABITAT OBSERVATION DISTRIBUTION - PREMIUM
    # ============================================================

    st.markdown("""
    <div class="section-title">
        🌳 Habitat Observation Distribution
    </div>

    <div class="section-subtitle">
        Compare observation activity across different habitats.
    </div>
    """, unsafe_allow_html=True)


    # ============================================================
    # HABITAT DATA
    # ============================================================

    habitat_data = (
        filtered_df
        .groupby("Location_Type")
        .size()
        .reset_index(name="Observation_Count")
        .sort_values(
            "Observation_Count",
            ascending=False
        )
        .reset_index(drop=True)
    )


    if not habitat_data.empty:

        total_habitat_observations = int(
            habitat_data["Observation_Count"].sum()
        )


        # ========================================================
        # CALCULATE SHARE
        # ========================================================

        habitat_data["Share"] = (
            habitat_data["Observation_Count"]
            / total_habitat_observations
            * 100
        )


        # ========================================================
        # HABITAT COLORS
        # ========================================================

        habitat_colors = {
            "Grassland": "#5B6EF5",
            "Forest": "#F15B40",
            "Wetland": "#2EC4B6",
            "Desert": "#F4B942",
            "Urban": "#9B6DCC"
        }

        pie_colors = [
            habitat_colors.get(
                habitat,
                "#26C6B5"
            )
            for habitat in habitat_data["Location_Type"]
        ]


        # ========================================================
        # DONUT CHART
        # ========================================================

        fig_habitat = px.pie(
            habitat_data,
            names="Location_Type",
            values="Observation_Count",
            hole=0.62
        )


        fig_habitat.update_traces(
            marker=dict(
                colors=pie_colors,
                line=dict(
                    color="#0B111B",
                    width=3
                )
            ),

            textposition="outside",

            texttemplate=(
                "<b>%{label}</b><br>"
                "%{percent}"
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Observations: %{value}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )


        # ========================================================
        # CENTER TEXT
        # ========================================================

        fig_habitat.add_annotation(
            text=(
                f"<b>{total_habitat_observations:,}</b>"
                "<br>"
                "<span style='font-size:12px'>"
                "TOTAL OBSERVATIONS"
                "</span>"
            ),

            x=0.5,
            y=0.5,

            showarrow=False,

            font=dict(
                size=22,
                color="white"
            )
        )


        # ========================================================
        # CHART LAYOUT
        # ========================================================

        fig_habitat.update_layout(

            title=dict(
                text="Observation Share by Habitat",
                x=0.02,
                xanchor="left",
                font=dict(
                    size=18,
                    color="white"
                )
            ),

            template="plotly_dark",

            height=430,

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            font=dict(
                color="white"
            ),

            legend=dict(
                title="Habitat",
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=0.78,
                font=dict(
                    size=13
                )
            ),

            margin=dict(
                l=20,
                r=20,
                t=65,
                b=20
            )
        )


        # ========================================================
        # DISPLAY CHART
        # ========================================================

        st.plotly_chart(
            fig_habitat,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # ========================================================
        # FIND TOP HABITAT
        # ========================================================

        top_habitat_row = habitat_data.iloc[0]

        top_habitat = str(
            top_habitat_row["Location_Type"]
        )

        top_habitat_count = int(
            top_habitat_row["Observation_Count"]
        )

        top_habitat_share = float(
            top_habitat_row["Share"]
        )


        # ========================================================
        # FIND LOWEST OBSERVED HABITAT
        # ========================================================

        lowest_habitat_row = habitat_data.iloc[-1]

        lowest_habitat = str(
            lowest_habitat_row["Location_Type"]
        )

        lowest_habitat_count = int(
            lowest_habitat_row["Observation_Count"]
        )

        lowest_habitat_share = float(
            lowest_habitat_row["Share"]
        )

        # ============================================================
        # BUSINESS INSIGHT
        # ============================================================

        insight_html = f"""
<div style="
    background: linear-gradient(135deg, rgba(20,184,166,0.16), rgba(14,116,144,0.10));
    border: 1px solid rgba(45,212,191,0.25);
    border-left: 5px solid #2DD4BF;
    border-radius: 16px;
    padding: 20px 24px;
    margin-top: 18px;
    margin-bottom: 16px;
">

    <div style="
        color: #5EEAD4;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 12px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color: #F8FAFC;
        font-size: 14px;
        line-height: 1.8;
    ">
        • <b>{top_habitat}</b> has the highest observation coverage with
        <b>{top_habitat_count:,}</b> observations
        (<b>{top_habitat_share:.1f}%</b> of total activity).
        <br><br>

        • <b>{lowest_habitat}</b> has the lowest observation coverage with
        <b>{lowest_habitat_count:,}</b> observations
        (<b>{lowest_habitat_share:.1f}%</b>).
        <br><br>

        • Observation activity is concentrated more heavily in
        <b>{top_habitat}</b>, indicating an uneven monitoring distribution
        across habitats.
    </div>

</div>
"""

        st.html(insight_html)


        # ============================================================
        # BUSINESS RECOMMENDATION
        # ============================================================

        recommendation_html = f"""
<div style="
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(37,99,235,0.08));
    border: 1px solid rgba(96,165,250,0.25);
    border-left: 5px solid #60A5FA;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 28px;
">

    <div style="
        color: #93C5FD;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 12px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color: #F8FAFC;
        font-size: 14px;
        line-height: 1.8;
    ">
        • Increase monitoring coverage in
        <b>{lowest_habitat}</b> to reduce the current habitat-level
        observation gap.
        <br><br>

        • Maintain regular monitoring in
        <b>{top_habitat}</b> while expanding surveys in
        under-represented habitats.
        <br><br>

        • Use a balanced sampling strategy across habitats before making
        biodiversity, conservation or resource-allocation decisions.
    </div>

</div>
"""

        st.html(recommendation_html)


    else:

        st.info(
            "No habitat observations are available for the selected filters."
        )
    # ============================================================
    # SPECIES HIGHLIGHTS - COLORFUL RANKING CHART
    # ============================================================

    st.markdown("""
    <div class="section-title">
        🐦 Species Highlights
    </div>

    <div class="section-subtitle">
        Identify the most frequently observed bird species
        in the selected dataset.
    </div>
    """, unsafe_allow_html=True)


    # ------------------------------------------------------------
    # SPECIES DATA
    # ------------------------------------------------------------

    species_data = (
        filtered_df
        .groupby("Common_Name")
        .size()
        .reset_index(name="Observation_Count")
        .sort_values(
            "Observation_Count",
            ascending=False
        )
        .head(10)
        .sort_values(
            "Observation_Count",
            ascending=True
        )
        .reset_index(drop=True)
    )


    if not species_data.empty:

        # --------------------------------------------------------
        # COLOR PALETTE
        # --------------------------------------------------------

        species_colors = [
            "#38D6C5",   # Teal
            "#4CC9F0",   # Cyan
            "#4895EF",   # Blue
            "#4361EE",   # Indigo
            "#7B61FF",   # Purple
            "#9B5DE5",   # Violet
            "#F15BB5",   # Pink
            "#FF6B6B",   # Coral
            "#F4A261",   # Orange
            "#F9C74F"    # Yellow
        ]

        # Reverse so highest gets strongest highlight
        chart_colors = species_colors[-len(species_data):]


        # --------------------------------------------------------
        # HORIZONTAL BAR CHART
        # --------------------------------------------------------

        fig_species = px.bar(
            species_data,
            x="Observation_Count",
            y="Common_Name",
            orientation="h",
            text="Observation_Count"
        )


        fig_species.update_traces(
            marker=dict(
                color=chart_colors,
                line=dict(
                    color="rgba(255,255,255,0.20)",
                    width=1
                ),
            ),

            textposition="outside",

            textfont=dict(
                color="white",
                size=12
            ),

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Observations: %{x:,}"
                "<extra></extra>"
            )
        )


        # --------------------------------------------------------
        # LAYOUT
        # --------------------------------------------------------

        fig_species.update_layout(

            title=dict(
                text="<b>Top 10 Most Observed Bird Species</b>",
                x=0.02,
                xanchor="left",
                font=dict(
                    size=18,
                    color="white"
                )
            ),

            template="plotly_dark",

            height=470,

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            font=dict(
                color="white"
            ),

            xaxis=dict(
                title="Number of Observations",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.10)",
                zeroline=False
            ),

            yaxis=dict(
                title=None,
                showgrid=False,
                categoryorder="array",
                categoryarray=species_data["Common_Name"].tolist()
            ),

            margin=dict(
                l=30,
                r=60,
                t=70,
                b=40
            ),

            showlegend=False
        )


        st.plotly_chart(
            fig_species,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # ========================================================
        # TOP SPECIES DATA
        # ========================================================

        top_species_row = species_data.iloc[-1]

        top_species = str(
            top_species_row["Common_Name"]
        )

        top_species_count = int(
            top_species_row["Observation_Count"]
        )

    # ============================================================
    # SPECIES BUSINESS INSIGHT
    # ============================================================

    top_species_row = species_data.iloc[-1]

    top_species = str(
        top_species_row["Common_Name"]
    )

    top_species_count = int(
        top_species_row["Observation_Count"]
    )

    total_top10 = int(
        species_data["Observation_Count"].sum()
    )

    top_species_share = (
        top_species_count / total_top10 * 100
        if total_top10 > 0
        else 0
    )


    # ============================================================
    # BUSINESS INSIGHT
    # ============================================================

    species_insight_html = f"""<div style="
        background: linear-gradient(
            135deg,
            rgba(20,184,166,0.16),
            rgba(14,116,144,0.10)
        );
        border: 1px solid rgba(45,212,191,0.28);
        border-left: 5px solid #2DD4BF;
        border-radius: 16px;
        padding: 20px 24px;
        margin-top: 18px;
        margin-bottom: 15px;
    ">

        <div style="
            color:#5EEAD4;
            font-size:13px;
            font-weight:800;
            letter-spacing:1px;
            margin-bottom:12px;
        ">
            💡 BUSINESS INSIGHT
        </div>

        <div style="
            color:#F8FAFC;
            font-size:14px;
            line-height:1.8;
        ">

            • <b>{top_species}</b> is the most frequently observed
            species with <b>{top_species_count:,}</b> observations.
            <br><br>

            • Among the Top 10 species,
            <b>{top_species}</b> contributes approximately
            <b>{top_species_share:.1f}%</b> of the recorded observations.
            <br><br>

            • Observation activity is concentrated among a relatively
            small group of frequently observed species.

        </div>

    </div>"""

    st.html(species_insight_html)


    # ============================================================
    # BUSINESS RECOMMENDATION
    # ============================================================

    species_recommendation_html = f"""<div style="
        background: linear-gradient(
            135deg,
            rgba(59,130,246,0.16),
            rgba(37,99,235,0.08)
        );
        border: 1px solid rgba(96,165,250,0.28);
        border-left: 5px solid #60A5FA;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 28px;
    ">

        <div style="
            color:#93C5FD;
            font-size:13px;
            font-weight:800;
            letter-spacing:1px;
            margin-bottom:12px;
        ">
            🎯 BUSINESS RECOMMENDATION
        </div>

        <div style="
            color:#F8FAFC;
            font-size:14px;
            line-height:1.8;
        ">

            • Prioritize <b>{top_species}</b> and other
            high-observation species for regular monitoring.
            <br><br>

            • Conduct targeted surveys for species with lower
            observation counts to identify possible monitoring gaps.
            <br><br>

            • Combine species observations with habitat and
            environmental data before making conservation
            or resource-allocation decisions.

        </div>

    </div>"""

    st.html(species_recommendation_html)
   # =========================================================
# PAGE 2 - SPECIES ANALYSIS
# =========================================================

elif selected_page == "🐦 Species Analysis":

    # =====================================================
    # HERO
    # =====================================================

    st.html("""
    <div class="hero">

        <div class="hero-content">

            <div class="hero-badge">
                🐦 SPECIES INTELLIGENCE
            </div>

            <div class="hero-title">
                Species
                <span class="hero-highlight">
                    Analysis
                </span>
            </div>

            <div class="hero-subtitle">
                Explore species diversity, observation frequency,
                habitat distribution and scientific classification
                across the selected bird observation dataset.
            </div>

            <div class="hero-tags">

                <span class="hero-tag">
                    🐦 Species Diversity
                </span>

                <span class="hero-tag">
                    📊 Observation Frequency
                </span>

                <span class="hero-tag">
                    🌳 Habitat Distribution
                </span>

                <span class="hero-tag">
                    🧬 Classification
                </span>

            </div>

        </div>

        <div class="hero-bird-glow"></div>

        <div class="hero-bird">
            🦜
        </div>

    </div>
    """)


    # =====================================================
    # KPI CALCULATIONS
    # =====================================================

    unique_scientific_species = (
        filtered_df["Scientific_Name"].nunique()
    )

    unique_common_species = (
        filtered_df["Common_Name"].nunique()
    )

    total_species_observations = len(
        filtered_df
    )

    avg_observations_per_species = (
        total_species_observations
        / unique_scientific_species
        if unique_scientific_species > 0
        else 0
    )


    # =====================================================
    # KPI CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.html(f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                🧬
            </div>

            <div class="kpi-title">
                Unique Scientific Species
            </div>

            <div class="kpi-value">
                {unique_scientific_species:,}
            </div>

        </div>
        """)


    with c2:

        st.html(f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                🐦
            </div>

            <div class="kpi-title">
                Unique Common Species
            </div>

            <div class="kpi-value">
                {unique_common_species:,}
            </div>

        </div>
        """)


    with c3:

        st.html(f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                📊
            </div>

            <div class="kpi-title">
                Species Observations
            </div>

            <div class="kpi-value">
                {total_species_observations:,}
            </div>

        </div>
        """)


    with c4:

        st.html(f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                📈
            </div>

            <div class="kpi-title">
                Avg Observations / Species
            </div>

            <div class="kpi-value">
                {avg_observations_per_species:.1f}
            </div>

        </div>
        """)


    # =====================================================
    # SECTION 1 - SPECIES FREQUENCY
    # =====================================================

    st.markdown("""
    <div class="section-title">
        📊 Species Observation Frequency
    </div>

    <div class="section-subtitle">
        Rank species by observation frequency to identify
        the most actively observed birds.
    </div>
    """, unsafe_allow_html=True)


    species_frequency = (
        filtered_df
        .groupby("Common_Name")
        .size()
        .reset_index(
            name="Observation_Count"
        )
        .sort_values(
            "Observation_Count",
            ascending=False
        )
        .head(15)
        .sort_values(
            "Observation_Count",
            ascending=True
        )
        .reset_index(drop=True)
    )


    if not species_frequency.empty:

        # -------------------------------------------------
        # COLORFUL SPECIES CHART
        # -------------------------------------------------

        species_colors = [
            "#38D6C5",
            "#40C9A2",
            "#4CC9F0",
            "#4895EF",
            "#4361EE",
            "#5E60CE",
            "#7B61FF",
            "#9B5DE5",
            "#C77DFF",
            "#E56BDE",
            "#F15BB5",
            "#FF6B8A",
            "#FF7B54",
            "#F4A261",
            "#F9C74F"
        ]

        # Make highest species visually strongest
        chart_colors = (
            species_colors[:len(species_frequency)]
        )


        fig_frequency = px.bar(
            species_frequency,
            x="Observation_Count",
            y="Common_Name",
            orientation="h",
            text="Observation_Count"
        )


        fig_frequency.update_traces(

            marker=dict(
                color=chart_colors,
                line=dict(
                    color="rgba(255,255,255,0.20)",
                    width=1
                )
            ),

            textposition="outside",

            textfont=dict(
                color="white",
                size=12
            ),

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Observations: %{x:,}"
                "<extra></extra>"
            )
        )


        fig_frequency.update_layout(

            title=dict(
                text="<b>Top 15 Most Observed Bird Species</b>",
                x=0.02,
                xanchor="left",
                font=dict(
                    size=18,
                    color="white"
                )
            ),

            template="plotly_dark",

            height=520,

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            font=dict(
                color="white"
            ),

            xaxis=dict(
                title="Number of Observations",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.10)",
                zeroline=False
            ),

            yaxis=dict(
                title=None,
                showgrid=False
            ),

            margin=dict(
                l=30,
                r=70,
                t=70,
                b=45
            ),

            showlegend=False
        )


        st.plotly_chart(
            fig_frequency,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # =================================================
        # TOP SPECIES
        # =================================================

        top_species_row = species_frequency.loc[
            species_frequency["Observation_Count"].idxmax()
        ]

        top_species = str(
            top_species_row["Common_Name"]
        )

        top_species_count = int(
            top_species_row["Observation_Count"]
        )


        total_top15 = int(
            species_frequency["Observation_Count"].sum()
        )

        top_species_share = (
            top_species_count
            / total_top15
            * 100
            if total_top15 > 0
            else 0
        )


        # =================================================
        # BUSINESS INSIGHT
        # =================================================

        species_insight_html = f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.16),
        rgba(14,116,144,0.10)
    );
    border:1px solid rgba(45,212,191,0.28);
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:20px 24px;
    margin-top:18px;
    margin-bottom:15px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:12px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_species}</b> is the most frequently observed
        species with <b>{top_species_count:,}</b> observations.
        <br><br>

        • It contributes approximately
        <b>{top_species_share:.1f}%</b> of observations
        represented by the Top 15 species.
        <br><br>

        • Observation activity is concentrated among a
        relatively small group of frequently recorded species.

    </div>

</div>
"""

        st.html(species_insight_html)


        # =================================================
        # BUSINESS RECOMMENDATION
        # =================================================

        species_recommendation_html = f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.15),
        rgba(37,99,235,0.08)
    );
    border:1px solid rgba(96,165,250,0.28);
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:20px 24px;
    margin-bottom:28px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:12px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Prioritize <b>{top_species}</b> and other
        high-observation species for regular monitoring.
        <br><br>

        • Conduct targeted surveys for lower-observation
        species to identify potential monitoring gaps.
        <br><br>

        • Combine species frequency with habitat and
        environmental information before making conservation
        or resource-allocation decisions.

    </div>

</div>
"""

        st.html(species_recommendation_html)


    else:

        st.info(
            "No species observations are available "
            "for the selected filters."
        )


    # =====================================================
    # SECTION 2 - SPECIES DIVERSITY BY HABITAT
    # =====================================================

    st.markdown("""
    <div class="section-title">
        🌳 Species Diversity by Habitat
    </div>

    <div class="section-subtitle">
        Compare the number of unique species recorded
        across different habitat types.
    </div>
    """, unsafe_allow_html=True)


    habitat_species = (
        filtered_df
        .groupby("Location_Type")["Scientific_Name"]
        .nunique()
        .reset_index(
            name="Unique_Species"
        )
        .sort_values(
            "Unique_Species",
            ascending=False
        )
    )


    if not habitat_species.empty:

        habitat_colors = [
            "#2DD4BF",
            "#F97362",
            "#60A5FA",
            "#A78BFA",
            "#FBBF24"
        ]


        fig_habitat_species = px.bar(
            habitat_species,
            x="Location_Type",
            y="Unique_Species",
            text="Unique_Species"
        )


        fig_habitat_species.update_traces(
            marker=dict(
                color=habitat_colors[
                    :len(habitat_species)
                ],
                line=dict(
                    color="rgba(255,255,255,0.20)",
                    width=1
                )
            ),

            textposition="outside",

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Unique Species: %{y:,}"
                "<extra></extra>"
            )
        )


        fig_habitat_species.update_layout(

            title=dict(
                text="<b>Unique Species Recorded by Habitat</b>",
                x=0.02,
                xanchor="left",
                font=dict(
                    size=18,
                    color="white"
                )
            ),

            template="plotly_dark",

            height=400,

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            font=dict(
                color="white"
            ),

            xaxis=dict(
                title="Habitat",
                showgrid=False
            ),

            yaxis=dict(
                title="Unique Species",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.10)",
                rangemode="tozero"
            ),

            margin=dict(
                l=30,
                r=40,
                t=70,
                b=45
            ),

            showlegend=False
        )


        st.plotly_chart(
            fig_habitat_species,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # =================================================
        # HABITAT DIVERSITY INSIGHT
        # =================================================

        top_habitat_row = habitat_species.iloc[0]

        top_habitat = str(
            top_habitat_row["Location_Type"]
        )

        top_habitat_species = int(
            top_habitat_row["Unique_Species"]
        )


        habitat_insight_html = f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.14),
        rgba(14,116,144,0.08)
    );
    border:1px solid rgba(45,212,191,0.25);
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:19px 23px;
    margin-top:16px;
    margin-bottom:15px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_habitat}</b> has the highest recorded
        species diversity with <b>{top_habitat_species}</b>
        unique species.
        <br><br>

        • Habitat-level species counts can help identify
        areas with broader observed species representation.
        <br><br>

        • Differences in habitat coverage should be considered
        when comparing species diversity.

    </div>

</div>
"""

        st.html(habitat_insight_html)


        # =================================================
        # HABITAT RECOMMENDATION
        # =================================================

        habitat_recommendation_html = f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.14),
        rgba(37,99,235,0.08)
    );
    border:1px solid rgba(96,165,250,0.25);
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:28px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Prioritize detailed species monitoring in
        <b>{top_habitat}</b> while maintaining coverage
        across other habitats.
        <br><br>

        • Expand sampling in habitats with fewer recorded
        species to determine whether the difference reflects
        ecology or monitoring intensity.
        <br><br>

        • Use habitat-level diversity results to support
        biodiversity planning and field-survey prioritization.

    </div>

</div>
"""

        st.html(habitat_recommendation_html)


    else:

        st.info(
            "No habitat diversity data is available "
            "for the selected filters."
        )


    # =====================================================
    # SECTION 3 - SCIENTIFIC CLASSIFICATION
    # =====================================================

    st.markdown("""
    <div class="section-title">
        🧬 Scientific Classification
    </div>

    <div class="section-subtitle">
        Reference table linking common bird names with
        their scientific names.
    </div>
    """, unsafe_allow_html=True)


    classification_data = (
        filtered_df[
            [
                "Common_Name",
                "Scientific_Name"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            "Common_Name"
        )
        .reset_index(drop=True)
    )


    if not classification_data.empty:

        st.dataframe(
            classification_data,
            use_container_width=True,
            hide_index=True,
            height=350
        )

    else:

        st.info(
            "No classification records available."
        )

# ============================================================
# PAGE 3 - HABITAT & LOCATION
# ============================================================

elif selected_page == "🌳 Habitat & Location":

    # ========================================================
    # HERO
    # ========================================================

    st.html("""
<div class="hero">

    <div class="hero-content">

        <div class="hero-badge">
            🌳 HABITAT & LOCATION INTELLIGENCE
        </div>

        <div class="hero-title">
            Habitat & Location
            <span class="hero-highlight">
                Analysis
            </span>
        </div>

        <div class="hero-subtitle">
            Explore observation coverage, species representation,
            habitat distribution and monitoring hotspots across
            the selected dataset.
        </div>

        <div class="hero-tags">

            <span class="hero-tag">
                🌳 Habitat Diversity
            </span>

            <span class="hero-tag">
                📍 Location Coverage
            </span>

            <span class="hero-tag">
                🐦 Species Representation
            </span>

            <span class="hero-tag">
                🗺️ Monitoring Hotspots
            </span>

        </div>

    </div>

    <div class="hero-bird-glow"></div>

    <div class="hero-bird">
        🌳
    </div>

</div>
""")


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_habitats = (
        filtered_df["Location_Type"].nunique()
    )

    total_sites = (
        filtered_df["Site_Name"].nunique()
    )

    total_observations = len(
        filtered_df
    )

    total_species = (
        filtered_df["Scientific_Name"].nunique()
    )

    avg_species_per_habitat = (
        total_species / total_habitats
        if total_habitats > 0
        else 0
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🌳
    </div>

    <div class="kpi-title">
        Habitat Types
    </div>

    <div class="kpi-value">
        {total_habitats:,}
    </div>

</div>
""")


    with c2:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        📍
    </div>

    <div class="kpi-title">
        Observation Sites
    </div>

    <div class="kpi-value">
        {total_sites:,}
    </div>

</div>
""")


    with c3:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🐦
    </div>

    <div class="kpi-title">
        Total Observations
    </div>

    <div class="kpi-value">
        {total_observations:,}
    </div>

</div>
""")


    with c4:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🧬
    </div>

    <div class="kpi-title">
        Species Recorded
    </div>

    <div class="kpi-value">
        {total_species:,}
    </div>

</div>
""")


    with c5:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        📊
    </div>

    <div class="kpi-title">
        Avg Species / Habitat
    </div>

    <div class="kpi-value">
        {avg_species_per_habitat:.1f}
    </div>

</div>
""")


    # ========================================================
    # SECTION 1 - HABITAT SHARE
    # DONUT CHART
    # ========================================================

    st.markdown("""
<div class="section-title">
    🌳 Habitat Observation Distribution
</div>

<div class="section-subtitle">
    Understand how observation activity is distributed across habitats.
</div>
""", unsafe_allow_html=True)


    habitat_data = (
        filtered_df
        .groupby("Location_Type")
        .size()
        .reset_index(
            name="Observation_Count"
        )
        .sort_values(
            "Observation_Count",
            ascending=False
        )
        .reset_index(drop=True)
    )


    if not habitat_data.empty:

        total_habitat_obs = int(
            habitat_data["Observation_Count"].sum()
        )

        habitat_data["Share"] = (
            habitat_data["Observation_Count"]
            / total_habitat_obs
            * 100
        )


        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        habitat_color_map = {
            "Grassland": "#5B6EF5",
            "Forest": "#F15B40",
            "Wetland": "#2EC4B6",
            "Desert": "#F4B942",
            "Urban": "#9B5DE5"
        }

        pie_colors = [
            habitat_color_map.get(
                habitat,
                "#26C6B5"
            )
            for habitat in habitat_data["Location_Type"]
        ]


        # ----------------------------------------------------
        # DONUT
        # ----------------------------------------------------

        fig_habitat = px.pie(
            habitat_data,
            names="Location_Type",
            values="Observation_Count",
            hole=0.62
        )


        fig_habitat.update_traces(

            marker=dict(
                colors=pie_colors,
                line=dict(
                    color="#0B111B",
                    width=3
                )
            ),

            textposition="outside",

            texttemplate=(
                "<b>%{label}</b><br>"
                "%{percent}"
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Observations: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )


        # ----------------------------------------------------
        # CENTER VALUE
        # ----------------------------------------------------

        fig_habitat.add_annotation(
            text=(
                f"<b>{total_habitat_obs:,}</b>"
                "<br>"
                "<span style='font-size:11px'>"
                "OBSERVATIONS"
                "</span>"
            ),
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(
                size=21,
                color="white"
            )
        )


        fig_habitat.update_layout(

            title=dict(
                text="<b>Observation Share by Habitat</b>",
                x=0.02,
                xanchor="left"
            ),

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=430,

            legend=dict(
                title="Habitat",
                orientation="v",
                y=0.5,
                x=0.80
            ),

            margin=dict(
                l=20,
                r=20,
                t=65,
                b=20
            )
        )


        st.plotly_chart(
            fig_habitat,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # ----------------------------------------------------
        # DYNAMIC HABITAT INSIGHT
        # ----------------------------------------------------

        top_habitat = str(
            habitat_data.iloc[0]["Location_Type"]
        )

        top_habitat_count = int(
            habitat_data.iloc[0]["Observation_Count"]
        )

        top_habitat_share = float(
            habitat_data.iloc[0]["Share"]
        )


        lowest_habitat = str(
            habitat_data.iloc[-1]["Location_Type"]
        )

        lowest_habitat_count = int(
            habitat_data.iloc[-1]["Observation_Count"]
        )


        habitat_insight = f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.14),
        rgba(14,116,144,0.08)
    );
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:18px 22px;
    margin-top:16px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_habitat}</b> accounts for
        <b>{top_habitat_count:,}</b> observations
        (<b>{top_habitat_share:.1f}%</b> of total activity).
        <br><br>

        • <b>{lowest_habitat}</b> has the lowest observation
        coverage with <b>{lowest_habitat_count:,}</b> records.
        <br><br>

        • Observation activity is concentrated unevenly
        across habitats.

    </div>

</div>
"""

        st.html(habitat_insight)


        habitat_recommendation = """
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.14),
        rgba(37,99,235,0.07)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:18px 22px;
    margin-top:14px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Increase monitoring coverage in
        <b>under-represented habitats</b>.
        <br><br>

        • Maintain regular surveys in high-activity habitats
        while expanding sampling elsewhere.
        <br><br>

        • Use balanced habitat coverage before making
        biodiversity or resource-allocation decisions.

    </div>

</div>
"""

        st.html(habitat_recommendation)


    else:

        st.info(
            "No habitat observations are available "
            "for the selected filters."
        )


    # ========================================================
    # SECTION 2 - TOP OBSERVATION SITES
    # HORIZONTAL BAR CHART
    # ========================================================

    st.markdown("""
<div class="section-title">
    📍 Observation Site Hotspots
</div>

<div class="section-subtitle">
    Identify monitoring sites contributing the highest number
    of bird observation records.
</div>
""", unsafe_allow_html=True)


    site_data = (
        filtered_df
        .groupby("Site_Name")
        .size()
        .reset_index(
            name="Observation_Count"
        )
        .sort_values(
            "Observation_Count",
            ascending=False
        )
        .head(10)
        .sort_values(
            "Observation_Count",
            ascending=True
        )
        .reset_index(drop=True)
    )


    if not site_data.empty:

        fig_sites = px.bar(
            site_data,
            x="Observation_Count",
            y="Site_Name",
            orientation="h",
            text="Observation_Count"
        )


        fig_sites.update_traces(

            marker=dict(
                color="#F4A261",
                line=dict(
                    color="rgba(255,255,255,0.20)",
                    width=1
                )
            ),

            textposition="outside",

            textfont=dict(
                color="white",
                size=12
            ),

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Observations: %{x:,}"
                "<extra></extra>"
            )
        )


        fig_sites.update_layout(

            title=dict(
                text="<b>Top 10 Observation Sites</b>",
                x=0.02,
                xanchor="left"
            ),

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=450,

            xaxis=dict(
                title="Number of Observations",
                gridcolor="rgba(255,255,255,0.10)"
            ),

            yaxis=dict(
                title=None,
                showgrid=False
            ),

            margin=dict(
                l=30,
                r=60,
                t=65,
                b=45
            ),

            showlegend=False
        )


        st.plotly_chart(
            fig_sites,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # ----------------------------------------------------
        # SITE INSIGHT
        # ----------------------------------------------------

        top_site = str(
            site_data.iloc[-1]["Site_Name"]
        )

        top_site_count = int(
            site_data.iloc[-1]["Observation_Count"]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(244,162,97,0.13),
        rgba(234,88,12,0.07)
    );
    border-left:5px solid #F4A261;
    border-radius:16px;
    padding:18px 22px;
    margin-top:15px;
    margin-bottom:25px;
">

    <div style="
        color:#FDBA74;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_site}</b> is the highest-observation
        monitoring site with <b>{top_site_count:,}</b> records.
        <br><br>

        • High-activity sites represent important locations
        for continued biodiversity monitoring.
        <br><br>

        • Site-level observation concentration can help
        identify potential monitoring hotspots.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.14),
        rgba(37,99,235,0.07)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:18px 22px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Prioritize high-activity sites for regular
        biodiversity monitoring.
        <br><br>

        • Expand sampling across lower-observation sites
        to identify under-monitored areas.
        <br><br>

        • Use site-level observation patterns to optimize
        field-survey scheduling and resource allocation.

    </div>

</div>
""")


    else:

        st.info(
            "No observation site data is available "
            "for the selected filters."
        )


    # ========================================================
    # SECTION 3 - SPECIES COVERAGE BY HABITAT
    # STACKED BAR CHART
    # ========================================================

    st.markdown("""
<div class="section-title">
    🐦 Species Coverage by Habitat
</div>

<div class="section-subtitle">
    Compare how individual bird species are distributed across
    different habitats.
</div>
""", unsafe_allow_html=True)


    species_habitat = (
        filtered_df
        .groupby(
            ["Location_Type", "Common_Name"]
        )
        .size()
        .reset_index(
            name="Observations"
        )
    )


    if not species_habitat.empty:

        # Top 8 species overall
        top_species_list = (
            species_habitat
            .groupby("Common_Name")["Observations"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(8)
            .index
            .tolist()
        )


        species_habitat = species_habitat[
            species_habitat["Common_Name"].isin(
                top_species_list
            )
        ]


        fig_species_habitat = px.bar(
            species_habitat,
            x="Location_Type",
            y="Observations",
            color="Common_Name",
            barmode="stack",
            title="Top Species Distribution Across Habitats"
        )


        fig_species_habitat.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=500,

            xaxis=dict(
                title="Habitat",
                showgrid=False
            ),

            yaxis=dict(
                title="Number of Observations",
                gridcolor="rgba(255,255,255,0.10)"
            ),

            legend=dict(
                title="Bird Species",
                orientation="v"
            ),

            margin=dict(
                l=30,
                r=30,
                t=65,
                b=45
            )
        )


        fig_species_habitat.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>"
                "<b>%{fullData.name}</b><br>"
                "Observations: %{y:,}"
                "<extra></extra>"
            )
        )


        st.plotly_chart(
            fig_species_habitat,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # ====================================================
        # SPECIES-HABITAT INSIGHT
        # ====================================================

        habitat_species_count = (
            filtered_df
            .groupby("Location_Type")[
                "Scientific_Name"
            ]
            .nunique()
            .sort_values(
                ascending=False
            )
        )


        if not habitat_species_count.empty:

            diversity_habitat = str(
                habitat_species_count.index[0]
            )

            diversity_count = int(
                habitat_species_count.iloc[0]
            )


            st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(139,92,246,0.14),
        rgba(76,29,149,0.08)
    );
    border-left:5px solid #A78BFA;
    border-radius:16px;
    padding:18px 22px;
    margin-top:15px;
    margin-bottom:15px;
">

    <div style="
        color:#C4B5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{diversity_habitat}</b> has the highest recorded
        species diversity with <b>{diversity_count}</b>
        unique species.
        <br><br>

        • Species composition differs across habitats,
        providing a useful basis for habitat-specific monitoring.
        <br><br>

        • The chart highlights which species contribute to
        observation activity within each habitat.

    </div>

</div>
""")


            st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.14),
        rgba(37,99,235,0.07)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:18px 22px;
    margin-bottom:30px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Use habitat-specific species patterns to design
        targeted monitoring programs.
        <br><br>

        • Prioritize habitats supporting broader observed
        species representation for detailed biodiversity studies.
        <br><br>

        • Combine species, habitat and site-level results before
        allocating long-term conservation resources.

    </div>

</div>
""")
# =========================================================
# PAGE 4 - ENVIRONMENTAL ANALYSIS
# =========================================================

elif selected_page == "🌦️ Environmental Analysis":

    # =====================================================
    # HERO
    # =====================================================

    st.html("""
<div class="hero">

    <div class="hero-content">

        <div class="hero-badge">
            🌦️ ENVIRONMENTAL INTELLIGENCE
        </div>

        <div class="hero-title">
            Environmental
            <span class="hero-highlight">
                Analysis
            </span>
        </div>

        <div class="hero-subtitle">
            Analyze temperature conditions, habitat-level
            environmental patterns and observation activity
            across the selected bird observation dataset.
        </div>

        <div class="hero-tags">

            <span class="hero-tag">
                🌡️ Temperature Analysis
            </span>

            <span class="hero-tag">
                📈 Observation Activity
            </span>

            <span class="hero-tag">
                🌳 Habitat Comparison
            </span>

            <span class="hero-tag">
                📋 Environmental Data
            </span>

        </div>

    </div>

    <div class="hero-bird-glow"></div>

    <div class="hero-bird">
        🌦️
    </div>

</div>
""")


    # =====================================================
    # PREPARE ENVIRONMENTAL DATA
    # =====================================================

    if "Temperature" not in filtered_df.columns:

        st.error(
            "Temperature column is not available in the dataset."
        )

    else:

        environmental_df = filtered_df.copy()

        # Convert temperature to numeric
        environmental_df["Temperature"] = pd.to_numeric(
            environmental_df["Temperature"],
            errors="coerce"
        )

        # Remove missing temperatures
        environmental_df = environmental_df.dropna(
            subset=["Temperature"]
        )


        # =================================================
        # KPI CALCULATIONS
        # =================================================

        temperature_records = len(
            environmental_df
        )

        avg_temperature = (
            environmental_df["Temperature"].mean()
            if temperature_records > 0
            else 0
        )

        min_temperature = (
            environmental_df["Temperature"].min()
            if temperature_records > 0
            else 0
        )

        max_temperature = (
            environmental_df["Temperature"].max()
            if temperature_records > 0
            else 0
        )

        temperature_range = (
            max_temperature - min_temperature
            if temperature_records > 0
            else 0
        )


        # =================================================
        # KPI CARDS
        # =================================================

        c1, c2, c3, c4 = st.columns(4)


        with c1:

            st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🌡️
    </div>

    <div class="kpi-title">
        Average Temperature
    </div>

    <div class="kpi-value">
        {avg_temperature:.1f}°C
    </div>

</div>
""")


        with c2:

            st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🔽
    </div>

    <div class="kpi-title">
        Minimum Temperature
    </div>

    <div class="kpi-value">
        {min_temperature:.1f}°C
    </div>

</div>
""")


        with c3:

            st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🔼
    </div>

    <div class="kpi-title">
        Maximum Temperature
    </div>

    <div class="kpi-value">
        {max_temperature:.1f}°C
    </div>

</div>
""")


        with c4:

            st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        📏
    </div>

    <div class="kpi-title">
        Temperature Range
    </div>

    <div class="kpi-value">
        {temperature_range:.1f}°C
    </div>

</div>
""")


        # =================================================
        # NO DATA CHECK
        # =================================================

        if environmental_df.empty:

            st.info(
                "No temperature records are available "
                "for the selected filters."
            )

        else:

            # =================================================
            # SECTION 1
            # SCATTER PLOT
            # =================================================

            st.markdown("""
<div class="section-title">
    📈 Temperature vs Observation Activity
</div>

<div class="section-subtitle">
    Examine how observation activity varies across
    recorded temperature conditions.
</div>
""", unsafe_allow_html=True)


            # -----------------------------------------------
            # DATE-BASED DAILY ANALYSIS
            # -----------------------------------------------

            if "Date" in environmental_df.columns:

                environmental_df["Date"] = pd.to_datetime(
                    environmental_df["Date"],
                    errors="coerce"
                )


                daily_data = (
                    environmental_df
                    .dropna(subset=["Date"])
                    .groupby("Date")
                    .agg(
                        Average_Temperature=(
                            "Temperature",
                            "mean"
                        ),
                        Observation_Count=(
                            "Temperature",
                            "size"
                        )
                    )
                    .reset_index()
                    .sort_values("Date")
                )

            else:

                daily_data = pd.DataFrame()


            if not daily_data.empty:

                fig_scatter = px.scatter(
                    daily_data,
                    x="Average_Temperature",
                    y="Observation_Count",
                    size="Observation_Count",
                    color="Average_Temperature",
                    color_continuous_scale=[
                        "#2563EB",
                        "#14B8A6",
                        "#F59E0B",
                        "#EF4444"
                    ],
                    hover_data={
                        "Date": True,
                        "Average_Temperature": ":.1f",
                        "Observation_Count": ":,"
                    },
                    title="Daily Temperature vs Observation Activity"
                )


                fig_scatter.update_traces(
                    marker=dict(
                        opacity=0.82,
                        line=dict(
                            color="white",
                            width=1
                        )
                    )
                )


                fig_scatter.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117",
                    height=450,

                    xaxis=dict(
                        title="Average Temperature (°C)",
                        gridcolor="rgba(255,255,255,0.10)"
                    ),

                    yaxis=dict(
                        title="Daily Observations",
                        gridcolor="rgba(255,255,255,0.10)"
                    ),

                    coloraxis_colorbar=dict(
                        title="Temperature"
                    ),

                    margin=dict(
                        l=45,
                        r=45,
                        t=70,
                        b=50
                    )
                )


                st.plotly_chart(
                    fig_scatter,
                    use_container_width=True,
                    config={
                        "displayModeBar": True,
                        "displaylogo": False
                    }
                )


                # -------------------------------------------
                # PEAK DAY
                # -------------------------------------------

                peak_day = daily_data.loc[
                    daily_data["Observation_Count"].idxmax()
                ]


                peak_date = peak_day["Date"].strftime(
                    "%d %b %Y"
                )

                peak_count = int(
                    peak_day["Observation_Count"]
                )

                peak_temp = float(
                    peak_day["Average_Temperature"]
                )


                # -------------------------------------------
                # SCATTER INSIGHT
                # -------------------------------------------

                st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.14),
        rgba(14,116,144,0.08)
    );
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • The highest daily observation activity occurred on
        <b>{peak_date}</b> with
        <b>{peak_count:,}</b> observations.
        <br><br>

        • The average recorded temperature on that day was
        <b>{peak_temp:.1f}°C</b>.
        <br><br>

        • The scatter plot helps identify the range of
        environmental conditions associated with higher
        observation activity.

    </div>

</div>
""")


                st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.14),
        rgba(37,99,235,0.07)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Use environmental patterns to support field-survey
        planning rather than relying on temperature alone.
        <br><br>

        • Continue collecting observations across different
        temperature conditions to strengthen environmental analysis.
        <br><br>

        • Compare temperature patterns with habitat and species
        information before making monitoring decisions.

    </div>

</div>
""")


            else:

                st.info(
                    "Daily date information is not available, "
                    "so the temperature-activity scatter analysis "
                    "cannot be generated."
                )


            # =================================================
            # SECTION 2
            # AVERAGE TEMPERATURE BY HABITAT
            # =================================================

            st.markdown("""
<div class="section-title">
    🌳 Average Temperature by Habitat
</div>

<div class="section-subtitle">
    Compare average recorded temperature across different habitats.
</div>
""", unsafe_allow_html=True)


            if "Location_Type" in environmental_df.columns:

                habitat_temperature = (
                    environmental_df
                    .groupby("Location_Type")
                    .agg(
                        Average_Temperature=(
                            "Temperature",
                            "mean"
                        ),
                        Observation_Count=(
                            "Temperature",
                            "size"
                        )
                    )
                    .reset_index()
                    .sort_values(
                        "Average_Temperature",
                        ascending=True
                    )
                )


                if not habitat_temperature.empty:

                    fig_habitat_temp = px.bar(
                        habitat_temperature,
                        x="Average_Temperature",
                        y="Location_Type",
                        orientation="h",
                        text="Average_Temperature",
                        color="Average_Temperature",
                        color_continuous_scale=[
                            "#2563EB",
                            "#14B8A6",
                            "#F59E0B",
                            "#EF4444"
                        ],
                        custom_data=[
                            habitat_temperature[
                                "Observation_Count"
                            ]
                        ],
                        title="Average Temperature by Habitat"
                    )


                    fig_habitat_temp.update_traces(
                        texttemplate="%{text:.1f}°C",
                        textposition="outside",
                        hovertemplate=(
                            "<b>%{y}</b><br>"
                            "Average Temperature: %{x:.1f}°C<br>"
                            "Observations: %{customdata[0]:,}"
                            "<extra></extra>"
                        )
                    )


                    fig_habitat_temp.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="#0E1117",
                        plot_bgcolor="#0E1117",
                        height=420,

                        xaxis=dict(
                            title="Average Temperature (°C)",
                            gridcolor="rgba(255,255,255,0.10)"
                        ),

                        yaxis=dict(
                            title="Habitat",
                            showgrid=False
                        ),

                        coloraxis_colorbar=dict(
                            title="Temperature"
                        ),

                        margin=dict(
                            l=40,
                            r=80,
                            t=70,
                            b=50
                        )
                    )


                    st.plotly_chart(
                        fig_habitat_temp,
                        use_container_width=True,
                        config={
                            "displayModeBar": True,
                            "displaylogo": False
                        }
                    )


                    # -----------------------------------------
                    # HABITAT INSIGHT
                    # -----------------------------------------

                    hottest = habitat_temperature.iloc[-1]

                    coolest = habitat_temperature.iloc[0]


                    hottest_habitat = str(
                        hottest["Location_Type"]
                    )

                    hottest_temperature = float(
                        hottest["Average_Temperature"]
                    )

                    coolest_habitat = str(
                        coolest["Location_Type"]
                    )

                    coolest_temperature = float(
                        coolest["Average_Temperature"]
                    )


                    st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.13),
        rgba(14,116,144,0.07)
    );
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{hottest_habitat}</b> has the highest average
        recorded temperature at
        <b>{hottest_temperature:.1f}°C</b>.
        <br><br>

        • <b>{coolest_habitat}</b> has the lowest average
        recorded temperature at
        <b>{coolest_temperature:.1f}°C</b>.
        <br><br>

        • Habitat-level environmental differences provide
        useful context for comparing observation activity.

    </div>

</div>
""")


                    st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Consider habitat-specific environmental conditions
        when planning field surveys.
        <br><br>

        • Maintain monitoring across habitats experiencing
        different temperature conditions.
        <br><br>

        • Combine habitat temperature with species and
        observation volume before making decisions.

    </div>

</div>
""")


            # =================================================
            # SECTION 3
            # TEMPERATURE VARIATION
            # =================================================

            st.markdown("""
<div class="section-title">
    📦 Temperature Variation by Habitat
</div>

<div class="section-subtitle">
    Examine median temperature, spread and potential outliers
    across habitats.
</div>
""", unsafe_allow_html=True)


            if "Location_Type" in environmental_df.columns:

                fig_box = px.box(
                    environmental_df,
                    x="Location_Type",
                    y="Temperature",
                    color="Location_Type",
                    points="outliers",
                    title="Temperature Range and Variation by Habitat"
                )


                fig_box.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117",
                    height=430,

                    xaxis=dict(
                        title="Habitat",
                        showgrid=False
                    ),

                    yaxis=dict(
                        title="Temperature (°C)",
                        gridcolor="rgba(255,255,255,0.10)"
                    ),

                    showlegend=False,

                    margin=dict(
                        l=40,
                        r=40,
                        t=70,
                        b=50
                    )
                )


                st.plotly_chart(
                    fig_box,
                    use_container_width=True,
                    config={
                        "displayModeBar": True,
                        "displaylogo": False
                    }
                )


                # -----------------------------------------
                # VARIATION INSIGHT
                # -----------------------------------------

                st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(244,162,97,0.13),
        rgba(234,88,12,0.07)
    );
    border-left:5px solid #F4A261;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#FDBA74;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • The box plot shows the distribution and variability
        of observed temperatures across habitats.
        <br><br>

        • Wider temperature spreads indicate greater variation
        in recorded environmental conditions.
        <br><br>

        • Potential outliers may represent unusual environmental
        observations and can also be reviewed for data quality.

    </div>

</div>
""")


                st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Investigate unusual temperature records when
        conducting data-quality reviews.
        <br><br>

        • Consider environmental variability while planning
        habitat-level observation schedules.
        <br><br>

        • Combine temperature distribution with observation
        and species data for stronger environmental assessment.

    </div>

</div>
""")


            # =================================================
            # SECTION 4
            # ENVIRONMENTAL DATA TABLE
            # =================================================

            st.markdown("""
<div class="section-title">
    📋 Environmental Data Summary
</div>

<div class="section-subtitle">
    Detailed temperature records from the currently selected dataset.
</div>
""", unsafe_allow_html=True)


            # -------------------------------------------------
            # CREATE TABLE
            # -------------------------------------------------

            table_columns = []


            if "Date" in environmental_df.columns:
                table_columns.append("Date")

            if "Common_Name" in environmental_df.columns:
                table_columns.append("Common_Name")

            if "Scientific_Name" in environmental_df.columns:
                table_columns.append("Scientific_Name")

            if "Location_Type" in environmental_df.columns:
                table_columns.append("Location_Type")

            table_columns.append("Temperature")


            environmental_table = environmental_df[
                table_columns
            ].copy()


            # Date formatting
            if "Date" in environmental_table.columns:

                environmental_table["Date"] = pd.to_datetime(
                    environmental_table["Date"],
                    errors="coerce"
                ).dt.strftime("%d %b %Y")


            # Temperature formatting
            environmental_table["Temperature"] = (
                environmental_table["Temperature"]
                .round(1)
            )


            # Rename columns for presentation
            rename_map = {

                "Date": "Observation Date",

                "Common_Name": "Common Name",

                "Scientific_Name": "Scientific Name",

                "Location_Type": "Habitat",

                "Temperature": "Temperature (°C)"
            }


            environmental_table = (
                environmental_table
                .rename(
                    columns=rename_map
                )
            )


            # -------------------------------------------------
            # DISPLAY TABLE
            # -------------------------------------------------

            st.dataframe(
                environmental_table,
                use_container_width=True,
                hide_index=True,
                height=450
            )


            # =================================================
            # TABLE NOTE
            # =================================================

            st.caption(
                f"Showing {len(environmental_table):,} environmental "
                "records based on the current sidebar filters."
            )
# =========================================================
# PAGE 5 - TEMPORAL ANALYSIS
# =========================================================

elif selected_page == "📅 Temporal Analysis":

    # =====================================================
    # HERO
    # =====================================================

    st.html("""
<div class="hero">

    <div class="hero-content">

        <div class="hero-badge">
            📅 TEMPORAL INTELLIGENCE
        </div>

        <div class="hero-title">
            Temporal
            <span class="hero-highlight">
                Analysis
            </span>
        </div>

        <div class="hero-subtitle">
            Analyze observation activity across months and years,
            identify seasonal patterns and understand changes in
            species diversity and habitat activity.
        </div>

        <div class="hero-tags">

            <span class="hero-tag">
                📅 Seasonal Trends
            </span>

            <span class="hero-tag">
                📈 Observation Activity
            </span>

            <span class="hero-tag">
                🐦 Species Diversity
            </span>

            <span class="hero-tag">
                🌳 Habitat Patterns
            </span>

        </div>

    </div>

    <div class="hero-bird-glow"></div>

    <div class="hero-bird">
        📅
    </div>

</div>
""")


    # =====================================================
    # PREPARE TEMPORAL DATA
    # =====================================================

    temporal_df = filtered_df.copy()

    date_column = None

    possible_date_columns = [
        "Date",
        "Observation Date",
        "ObservationDate",
        "date",
        "DATE"
    ]

    for col in possible_date_columns:

        if col in temporal_df.columns:
            date_column = col
            break


    # =====================================================
    # CREATE MONTH COLUMN
    # =====================================================

    if date_column is not None:

        temporal_df[date_column] = pd.to_datetime(
            temporal_df[date_column],
            errors="coerce"
        )

        temporal_df["Month_Number"] = (
            temporal_df[date_column].dt.month
        )

        temporal_df["Month"] = (
            temporal_df[date_column].dt.strftime("%b")
        )


    elif "Month" in temporal_df.columns:

        temporal_df["Month"] = (
            temporal_df["Month"]
            .astype(str)
            .str.strip()
            .str[:3]
            .str.title()
        )

        month_map = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }

        temporal_df["Month_Number"] = (
            temporal_df["Month"].map(month_map)
        )


    else:

        temporal_df["Month"] = None
        temporal_df["Month_Number"] = None


    # =====================================================
    # MONTH ORDER
    # =====================================================

    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]


    # =====================================================
    # KPI CALCULATIONS
    # =====================================================

    total_temporal_observations = len(
        temporal_df
    )

    active_years = (
        temporal_df["Year"].nunique()
        if "Year" in temporal_df.columns
        else 0
    )

    total_species = (
        temporal_df["Scientific_Name"].nunique()
        if "Scientific_Name" in temporal_df.columns
        else 0
    )


    # Peak month calculation
    if (
        temporal_df["Month"].notna().any()
    ):

        month_counts = (
            temporal_df
            .dropna(subset=["Month"])
            .groupby(
                ["Month_Number", "Month"]
            )
            .size()
            .reset_index(
                name="Observation_Count"
            )
            .sort_values(
                "Month_Number"
            )
        )

    else:

        month_counts = pd.DataFrame()


    if not month_counts.empty:

        peak_month_row = month_counts.loc[
            month_counts[
                "Observation_Count"
            ].idxmax()
        ]

        peak_month = str(
            peak_month_row["Month"]
        )

        peak_month_count = int(
            peak_month_row["Observation_Count"]
        )

    else:

        peak_month = "N/A"
        peak_month_count = 0


    # =====================================================
    # KPI CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        📅
    </div>

    <div class="kpi-title">
        Active Years
    </div>

    <div class="kpi-value">
        {active_years:,}
    </div>

</div>
""")


    with c2:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🐦
    </div>

    <div class="kpi-title">
        Total Observations
    </div>

    <div class="kpi-value">
        {total_temporal_observations:,}
    </div>

</div>
""")


    with c3:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🧬
    </div>

    <div class="kpi-title">
        Species Recorded
    </div>

    <div class="kpi-value">
        {total_species:,}
    </div>

</div>
""")


    with c4:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🔥
    </div>

    <div class="kpi-title">
        Peak Observation Month
    </div>

    <div class="kpi-value">
        {peak_month}
    </div>

</div>
""")


    # =====================================================
    # SECTION 1 - MONTHLY OBSERVATION TREND
    # =====================================================

    st.markdown("""
<div class="section-title">
    📈 Monthly Observation Trend
</div>

<div class="section-subtitle">
    Identify seasonal peaks and low-activity periods in bird observations.
</div>
""", unsafe_allow_html=True)


    if not month_counts.empty:

        monthly_full = (
            month_counts
            .set_index("Month")
            .reindex(
                month_order,
                fill_value=0
            )
            .reset_index()
        )

        # Recalculate actual available count
        monthly_full["Observation_Count"] = (
            month_counts
            .set_index("Month")[
                "Observation_Count"
            ]
            .reindex(
                month_order,
                fill_value=0
            )
            .values
        )


        fig_monthly = px.area(
            monthly_full,
            x="Month",
            y="Observation_Count",
            markers=True,
            title="Bird Observation Activity by Month"
        )


        fig_monthly.update_traces(
            line=dict(
                color="#2DD4BF",
                width=4
            ),
            marker=dict(
                color="#F9C74F",
                size=8,
                line=dict(
                    color="white",
                    width=1
                )
            ),
            fillcolor="rgba(45,212,191,0.18)",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Observations: %{y:,}"
                "<extra></extra>"
            )
        )


        fig_monthly.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=450,

            title=dict(
                text="<b>Bird Observation Activity by Month</b>",
                x=0.02
            ),

            xaxis=dict(
                title="Month",
                categoryorder="array",
                categoryarray=month_order,
                showgrid=False
            ),

            yaxis=dict(
                title="Number of Observations",
                gridcolor="rgba(255,255,255,0.10)",
                rangemode="tozero"
            ),

            margin=dict(
                l=40,
                r=40,
                t=70,
                b=45
            )
        )


        st.plotly_chart(
            fig_monthly,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # =================================================
        # PEAK / LOW MONTH
        # =================================================

        active_months = monthly_full[
            monthly_full["Observation_Count"] > 0
        ]

        if not active_months.empty:

            peak_row = active_months.loc[
                active_months[
                    "Observation_Count"
                ].idxmax()
            ]

            low_row = active_months.loc[
                active_months[
                    "Observation_Count"
                ].idxmin()
            ]

            peak_month_name = str(
                peak_row["Month"]
            )

            peak_count = int(
                peak_row["Observation_Count"]
            )

            low_month_name = str(
                low_row["Month"]
            )

            low_count = int(
                low_row["Observation_Count"]
            )


            st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.14),
        rgba(14,116,144,0.07)
    );
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{peak_month_name}</b> recorded the highest
        observation activity with
        <b>{peak_count:,}</b> observations.
        <br><br>

        • Among months with recorded observations,
        <b>{low_month_name}</b> had the lowest activity with
        <b>{low_count:,}</b> observations.
        <br><br>

        • Observation activity shows a clear seasonal
        concentration in the available dataset.

    </div>

</div>
""")


            st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Increase field-monitoring capacity during
        high-activity months to capture more observations.
        <br><br>

        • Maintain baseline monitoring during lower-activity
        periods to avoid seasonal data gaps.
        <br><br>

        • Use monthly patterns for planning survey schedules,
        field resources and biodiversity-monitoring campaigns.

    </div>

</div>
""")


    else:

        st.info(
            "Monthly date information is not available "
            "for the selected records."
        )


    # =====================================================
    # SECTION 2 - SPECIES DIVERSITY BY MONTH
    # =====================================================

    st.markdown("""
<div class="section-title">
    🐦 Species Diversity by Month
</div>

<div class="section-subtitle">
    Compare the number of unique species recorded during each month.
</div>
""", unsafe_allow_html=True)


    if (
        not temporal_df.empty
        and temporal_df["Month"].notna().any()
        and "Scientific_Name" in temporal_df.columns
    ):

        monthly_species = (
            temporal_df
            .dropna(subset=["Month"])
            .groupby(
                ["Month_Number", "Month"]
            )["Scientific_Name"]
            .nunique()
            .reset_index(
                name="Unique_Species"
            )
            .sort_values(
                "Month_Number"
            )
        )


        monthly_species["Month"] = pd.Categorical(
            monthly_species["Month"],
            categories=month_order,
            ordered=True
        )

        monthly_species = (
            monthly_species
            .sort_values("Month")
        )


        fig_species_month = px.bar(
            monthly_species,
            x="Month",
            y="Unique_Species",
            color="Unique_Species",
            color_continuous_scale=[
                "#2563EB",
                "#14B8A6",
                "#F59E0B"
            ],
            text="Unique_Species",
            title="Unique Bird Species Recorded by Month"
        )


        fig_species_month.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Unique Species: %{y:,}"
                "<extra></extra>"
            )
        )


        fig_species_month.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=430,

            title=dict(
                text="<b>Species Diversity by Month</b>",
                x=0.02
            ),

            xaxis=dict(
                title="Month",
                categoryorder="array",
                categoryarray=month_order,
                showgrid=False
            ),

            yaxis=dict(
                title="Unique Species",
                gridcolor="rgba(255,255,255,0.10)",
                rangemode="tozero"
            ),

            coloraxis_colorbar=dict(
                title="Species"
            ),

            margin=dict(
                l=40,
                r=70,
                t=70,
                b=45
            )
        )


        st.plotly_chart(
            fig_species_month,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        top_diversity = monthly_species.loc[
            monthly_species[
                "Unique_Species"
            ].idxmax()
        ]

        top_diversity_month = str(
            top_diversity["Month"]
        )

        top_diversity_count = int(
            top_diversity["Unique_Species"]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(139,92,246,0.13),
        rgba(76,29,149,0.07)
    );
    border-left:5px solid #A78BFA;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#C4B5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_diversity_month}</b> recorded the highest
        species diversity with
        <b>{top_diversity_count}</b> unique species.
        <br><br>

        • Monthly species diversity provides a useful view
        of seasonal variation in observed biodiversity.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Use high-diversity months to prioritize
        biodiversity surveys and species monitoring.
        <br><br>

        • Maintain sampling during lower-diversity months
        to determine whether differences are ecological
        or related to observation effort.
        <br><br>

        • Combine seasonal species diversity with habitat
        information when planning conservation activities.

    </div>

</div>
""")


    else:

        st.info(
            "Monthly species data is not available."
        )


    # =====================================================
    # SECTION 3 - HABITAT × MONTH HEATMAP
    # =====================================================

    st.markdown("""
<div class="section-title">
    🔥 Habitat Activity Across Months
</div>

<div class="section-subtitle">
    Identify which habitats contribute most to observation
    activity during different months.
</div>
""", unsafe_allow_html=True)


    if (
        "Location_Type" in temporal_df.columns
        and temporal_df["Month"].notna().any()
    ):

        habitat_month = (
            temporal_df
            .dropna(subset=["Month"])
            .groupby(
                [
                    "Location_Type",
                    "Month_Number",
                    "Month"
                ]
            )
            .size()
            .reset_index(
                name="Observations"
            )
        )


        habitat_month["Month"] = pd.Categorical(
            habitat_month["Month"],
            categories=month_order,
            ordered=True
        )


        heatmap_data = (
            habitat_month
            .pivot_table(
                index="Location_Type",
                columns="Month",
                values="Observations",
                aggfunc="sum",
                fill_value=0,
                observed=False
            )
        )


        heatmap_data = heatmap_data.reindex(
            columns=month_order,
            fill_value=0
        )


        fig_heatmap = px.imshow(
            heatmap_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale=[
                "#071A2E",
                "#0E7490",
                "#14B8A6",
                "#F59E0B",
                "#EF4444"
            ],
            title="Observation Activity by Habitat and Month"
        )


        fig_heatmap.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=430,

            title=dict(
                text="<b>Habitat × Month Observation Heatmap</b>",
                x=0.02
            ),

            xaxis=dict(
                title="Month"
            ),

            yaxis=dict(
                title="Habitat"
            ),

            coloraxis_colorbar=dict(
                title="Observations"
            ),

            margin=dict(
                l=40,
                r=70,
                t=70,
                b=45
            )
        )


        st.plotly_chart(
            fig_heatmap,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        # =================================================
        # HEATMAP INSIGHT
        # =================================================

        max_heat_row = habitat_month.loc[
            habitat_month[
                "Observations"
            ].idxmax()
        ]


        heat_habitat = str(
            max_heat_row["Location_Type"]
        )

        heat_month = str(
            max_heat_row["Month"]
        )

        heat_value = int(
            max_heat_row["Observations"]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(244,162,97,0.13),
        rgba(234,88,12,0.07)
    );
    border-left:5px solid #F4A261;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#FDBA74;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • The highest habitat-month observation activity
        occurred in <b>{heat_habitat}</b> during
        <b>{heat_month}</b>, with
        <b>{heat_value:,}</b> observations.
        <br><br>

        • The heatmap highlights seasonal differences
        in observation activity across habitats.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Schedule habitat-specific surveys around
        months with strong observation activity.
        <br><br>

        • Strengthen monitoring in habitat-month combinations
        showing consistently low observation coverage.
        <br><br>

        • Use seasonal habitat patterns to improve field-team
        scheduling and biodiversity-monitoring efficiency.

    </div>

</div>
""")


    else:

        st.info(
            "Habitat or monthly information is not available "
            "for the selected records."
        )


    # =====================================================
    # SECTION 4 - TEMPORAL DATA TABLE
    # =====================================================

    st.markdown("""
<div class="section-title">
    📋 Temporal Data Summary
</div>

<div class="section-subtitle">
    Detailed observation records used for the temporal analysis.
</div>
""", unsafe_allow_html=True)


    # -----------------------------------------------------
    # TABLE COLUMNS
    # -----------------------------------------------------

    table_columns = []

    if date_column is not None:
        table_columns.append(date_column)

    if "Year" in temporal_df.columns:
        table_columns.append("Year")

    if "Month" in temporal_df.columns:
        table_columns.append("Month")

    if "Common_Name" in temporal_df.columns:
        table_columns.append("Common_Name")

    if "Location_Type" in temporal_df.columns:
        table_columns.append("Location_Type")

    if "Temperature" in temporal_df.columns:
        table_columns.append("Temperature")


    temporal_table = temporal_df[
        table_columns
    ].copy()


    # -----------------------------------------------------
    # FORMAT DATE
    # -----------------------------------------------------

    if date_column is not None:

        temporal_table[date_column] = pd.to_datetime(
            temporal_table[date_column],
            errors="coerce"
        ).dt.strftime(
            "%d %b %Y"
        )


    # -----------------------------------------------------
    # FORMAT TEMPERATURE
    # -----------------------------------------------------

    if "Temperature" in temporal_table.columns:

        temporal_table["Temperature"] = (
            pd.to_numeric(
                temporal_table["Temperature"],
                errors="coerce"
            )
            .round(1)
        )


    # -----------------------------------------------------
    # RENAME FOR PRESENTATION
    # -----------------------------------------------------

    rename_map = {

        "Date": "Observation Date",

        "Observation Date": "Observation Date",

        "ObservationDate": "Observation Date",

        "Year": "Year",

        "Month": "Month",

        "Common_Name": "Common Name",

        "Location_Type": "Habitat",

        "Temperature": "Temperature (°C)"
    }


    temporal_table = temporal_table.rename(
        columns=rename_map
    )


    # -----------------------------------------------------
    # DISPLAY TABLE
    # -----------------------------------------------------

    st.dataframe(
        temporal_table,
        use_container_width=True,
        hide_index=True,
        height=450
    )


    st.caption(
        f"Showing {len(temporal_table):,} observation records "
        "based on the current sidebar filters."
    )
    # =========================================================
# =========================================================
# PAGE 6 - OBSERVATION ANALYSIS
# =========================================================

elif selected_page == "👤 Observation Analysis":

    # =====================================================
    # HERO
    # =====================================================

    st.html("""
<div class="hero">

    <div class="hero-content">

        <div class="hero-badge">
            👤 OBSERVER INTELLIGENCE
        </div>

        <div class="hero-title">
            Observation
            <span class="hero-highlight">
                Analysis
            </span>
        </div>

        <div class="hero-subtitle">
            Evaluate observer contribution, species coverage,
            habitat participation and monitoring intensity
            across the selected observation dataset.
        </div>

        <div class="hero-tags">

            <span class="hero-tag">
                👤 Observer Activity
            </span>

            <span class="hero-tag">
                🐦 Species Coverage
            </span>

            <span class="hero-tag">
                🌳 Habitat Contribution
            </span>

            <span class="hero-tag">
                📊 Monitoring Intensity
            </span>

        </div>

    </div>

    <div class="hero-bird-glow"></div>

    <div class="hero-bird">
        👤
    </div>

</div>
""")


    # =====================================================
    # KPI CALCULATIONS
    # =====================================================

    total_observers = (
        filtered_df["Observer"].nunique()
    )

    total_observations = len(
        filtered_df
    )

    avg_observations_per_observer = (
        total_observations / total_observers
        if total_observers > 0
        else 0
    )

    observer_species_count = (
        filtered_df
        .groupby("Observer")["Scientific_Name"]
        .nunique()
    )

    avg_species_per_observer = (
        observer_species_count.mean()
        if not observer_species_count.empty
        else 0
    )


    # =====================================================
    # KPI CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        👤
    </div>

    <div class="kpi-title">
        Total Observers
    </div>

    <div class="kpi-value">
        {total_observers:,}
    </div>

</div>
""")


    with c2:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🐦
    </div>

    <div class="kpi-title">
        Total Observations
    </div>

    <div class="kpi-value">
        {total_observations:,}
    </div>

</div>
""")


    with c3:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        📊
    </div>

    <div class="kpi-title">
        Avg Observations / Observer
    </div>

    <div class="kpi-value">
        {avg_observations_per_observer:.1f}
    </div>

</div>
""")


    with c4:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🧬
    </div>

    <div class="kpi-title">
        Avg Species / Observer
    </div>

    <div class="kpi-value">
        {avg_species_per_observer:.1f}
    </div>

</div>
""")


    # =====================================================
    # SECTION 1
    # OBSERVATIONS BY OBSERVER
    # =====================================================

    st.markdown("""
<div class="section-title">
    👤 Observer Activity
</div>

<div class="section-subtitle">
    Compare the observation contribution of each observer.
</div>
""", unsafe_allow_html=True)


    observer_data = (
        filtered_df
        .groupby("Observer")
        .size()
        .reset_index(
            name="Observation_Count"
        )
        .sort_values(
            "Observation_Count",
            ascending=True
        )
    )


    if not observer_data.empty:

        fig_observer = px.bar(
            observer_data,
            x="Observation_Count",
            y="Observer",
            orientation="h",
            text="Observation_Count",
            color="Observation_Count",
            color_continuous_scale=[
                "#0EA5E9",
                "#14B8A6",
                "#22C55E",
                "#F59E0B"
            ],
            title="Observation Contribution by Observer"
        )


        fig_observer.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Observations: %{x:,}"
                "<extra></extra>"
            )
        )


        fig_observer.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            height=430,

            xaxis=dict(
                title="Number of Observations",
                gridcolor="rgba(255,255,255,0.10)"
            ),

            yaxis=dict(
                title="Observer",
                showgrid=False
            ),

            coloraxis_colorbar=dict(
                title="Observations"
            ),

            margin=dict(
                l=40,
                r=80,
                t=70,
                b=45
            )
        )


        st.plotly_chart(
            fig_observer,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        top_observer_row = observer_data.iloc[-1]

        top_observer = str(
            top_observer_row["Observer"]
        )

        top_observer_count = int(
            top_observer_row["Observation_Count"]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.14),
        rgba(14,116,144,0.07)
    );
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_observer}</b> contributed the highest
        number of observations with
        <b>{top_observer_count:,}</b> records.
        <br><br>

        • Observer contributions indicate differences
        in monitoring participation and field effort.
        <br><br>

        • A highly concentrated contribution pattern may
        indicate dependence on a small number of observers.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Maintain a balanced distribution of field-monitoring
        responsibilities across observers.
        <br><br>

        • Provide targeted support or training where observation
        participation is comparatively low.
        <br><br>

        • Avoid relying excessively on a small number of observers
        for long-term monitoring continuity.

    </div>

</div>
""")


    else:

        st.info(
            "No observer data is available for the selected filters."
        )


    # =====================================================
    # SECTION 2
    # SPECIES COVERAGE BY OBSERVER
    # =====================================================

    st.markdown("""
<div class="section-title">
    🧬 Species Coverage by Observer
</div>

<div class="section-subtitle">
    Compare how many unique bird species each observer has recorded.
</div>
""", unsafe_allow_html=True)


    species_observer = (
        filtered_df
        .groupby("Observer")[
            "Scientific_Name"
        ]
        .nunique()
        .reset_index(
            name="Unique_Species"
        )
        .sort_values(
            "Unique_Species",
            ascending=True
        )
    )


    if not species_observer.empty:

        fig_species_observer = px.bar(
            species_observer,
            x="Unique_Species",
            y="Observer",
            orientation="h",
            text="Unique_Species",
            color="Unique_Species",
            color_continuous_scale=[
                "#8B5CF6",
                "#4F46E5",
                "#0EA5E9",
                "#2DD4BF"
            ],
            title="Species Coverage by Observer"
        )


        fig_species_observer.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Unique Species: %{x:,}"
                "<extra></extra>"
            )
        )


        fig_species_observer.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            height=430,

            xaxis=dict(
                title="Unique Species Recorded",
                gridcolor="rgba(255,255,255,0.10)"
            ),

            yaxis=dict(
                title="Observer",
                showgrid=False
            ),

            coloraxis_colorbar=dict(
                title="Species"
            ),

            margin=dict(
                l=40,
                r=80,
                t=70,
                b=45
            )
        )


        st.plotly_chart(
            fig_species_observer,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        best_species_observer = species_observer.iloc[-1]

        best_observer = str(
            best_species_observer["Observer"]
        )

        best_species_count = int(
            best_species_observer["Unique_Species"]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(139,92,246,0.13),
        rgba(76,29,149,0.07)
    );
    border-left:5px solid #A78BFA;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#C4B5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{best_observer}</b> has the broadest
        species coverage with
        <b>{best_species_count}</b> unique species.
        <br><br>

        • Higher species coverage indicates broader
        observed biodiversity exposure.
        <br><br>

        • Comparing observer coverage helps identify
        differences in field observation breadth.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Share observation methods and best practices
        across observers to improve species coverage.
        <br><br>

        • Use experienced observers to support training
        and field-survey standardization.
        <br><br>

        • Encourage broader species coverage rather than
        focusing only on frequently observed species.

    </div>

</div>
""")


    else:

        st.info(
            "No species coverage data is available."
        )


    # =====================================================
    # SECTION 3
    # OBSERVER × HABITAT CONTRIBUTION
    # =====================================================

    st.markdown("""
<div class="section-title">
    🌳 Observer Contribution by Habitat
</div>

<div class="section-subtitle">
    Understand how observer effort is distributed across habitats.
</div>
""", unsafe_allow_html=True)


    observer_habitat = (
        filtered_df
        .groupby(
            [
                "Observer",
                "Location_Type"
            ]
        )
        .size()
        .reset_index(
            name="Observations"
        )
    )


    if not observer_habitat.empty:

        fig_observer_habitat = px.bar(
            observer_habitat,
            x="Observer",
            y="Observations",
            color="Location_Type",
            barmode="stack",
            text_auto=True,
            title="Observer Observation Volume by Habitat"
        )


        fig_observer_habitat.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=470,

            xaxis=dict(
                title="Observer",
                showgrid=False
            ),

            yaxis=dict(
                title="Number of Observations",
                gridcolor="rgba(255,255,255,0.10)"
            ),

            legend=dict(
                title="Habitat"
            ),

            margin=dict(
                l=40,
                r=40,
                t=70,
                b=50
            )
        )


        st.plotly_chart(
            fig_observer_habitat,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.12),
        rgba(14,116,144,0.06)
    );
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • The stacked bars show how each observer's
        observation contribution is distributed between habitats.
        <br><br>

        • Differences in habitat participation reveal
        where individual observers are contributing field effort.
        <br><br>

        • Balanced observer participation across habitats
        can improve monitoring coverage.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.12),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Assign observation responsibilities to improve
        coverage of habitats with lower monitoring activity.
        <br><br>

        • Rotate field assignments where practical to
        reduce observer-specific habitat bias.
        <br><br>

        • Track observer × habitat contribution regularly
        as part of monitoring-performance reviews.

    </div>

</div>
""")


    else:

        st.info(
            "No observer-habitat data is available."
        )


    # =====================================================
    # SECTION 4
    # OBSERVER × SPECIES HEATMAP
    # =====================================================

    st.markdown("""
<div class="section-title">
    🔥 Observer × Species Coverage
</div>

<div class="section-subtitle">
    Identify which species are most strongly represented
    in each observer's records.
</div>
""", unsafe_allow_html=True)


    observer_species = (
        filtered_df
        .groupby(
            [
                "Observer",
                "Common_Name"
            ]
        )
        .size()
        .reset_index(
            name="Observations"
        )
    )


    if not observer_species.empty:

        # Select top 12 species overall
        top_species_list = (
            observer_species
            .groupby("Common_Name")[
                "Observations"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(12)
            .index
            .tolist()
        )


        heatmap_source = observer_species[
            observer_species["Common_Name"].isin(
                top_species_list
            )
        ]


        heatmap_data = (
            heatmap_source
            .pivot_table(
                index="Observer",
                columns="Common_Name",
                values="Observations",
                aggfunc="sum",
                fill_value=0
            )
        )


        # Order columns by overall observation volume
        ordered_species = (
            heatmap_source
            .groupby("Common_Name")[
                "Observations"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .index
            .tolist()
        )


        heatmap_data = heatmap_data.reindex(
            columns=ordered_species,
            fill_value=0
        )


        fig_heatmap = px.imshow(
            heatmap_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale=[
                "#071A2E",
                "#0E7490",
                "#14B8A6",
                "#F59E0B",
                "#EF4444"
            ],
            title="Observation Intensity by Observer and Species"
        )


        fig_heatmap.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=500,

            xaxis=dict(
                title="Bird Species",
                tickangle=-35
            ),

            yaxis=dict(
                title="Observer"
            ),

            coloraxis_colorbar=dict(
                title="Observations"
            ),

            margin=dict(
                l=40,
                r=70,
                t=70,
                b=110
            )
        )


        st.plotly_chart(
            fig_heatmap,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(244,162,97,0.12),
        rgba(234,88,12,0.06)
    );
    border-left:5px solid #F4A261;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:25px;
">

    <div style="
        color:#FDBA74;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • The heatmap highlights species-observation
        concentration for each observer.
        <br><br>

        • Darker/high-intensity cells indicate stronger
        observation contribution for a species.
        <br><br>

        • The pattern can reveal species specialization
        or differences in observation focus across observers.

    </div>

</div>
""")


    else:

        st.info(
            "No observer-species data is available."
        )


    # =====================================================
    # SECTION 5
    # OBSERVER SUMMARY TABLE
    # =====================================================

    st.markdown("""
<div class="section-title">
    📋 Observer Performance Summary
</div>

<div class="section-subtitle">
    Detailed summary of observation contribution, species coverage
    and monitoring-site participation.
</div>
""", unsafe_allow_html=True)


    observer_summary = (
        filtered_df
        .groupby("Observer")
        .agg(
            Observation_Count=(
                "Observer",
                "size"
            ),

            Unique_Species=(
                "Scientific_Name",
                "nunique"
            ),

            Observation_Sites=(
                "Site_Name",
                "nunique"
            ),

            Habitat_Count=(
                "Location_Type",
                "nunique"
            )
        )
        .reset_index()
        .sort_values(
            "Observation_Count",
            ascending=False
        )
    )


    if not observer_summary.empty:

        observer_summary = observer_summary.rename(
            columns={
                "Observer": "Observer",
                "Observation_Count": "Observations",
                "Unique_Species": "Unique Species",
                "Observation_Sites": "Observation Sites",
                "Habitat_Count": "Habitats Covered"
            }
        )


        st.dataframe(
            observer_summary,
            use_container_width=True,
            hide_index=True,
            height=350
        )


        st.caption(
            f"Showing {len(observer_summary):,} observers "
            "based on the current sidebar filters."
        )

    else:

        st.info(
            "No observer summary is available."
        )
# =========================================================
# PAGE 7 - CONSERVATION ANALYSIS
# =========================================================

elif selected_page == "🛡️ Conservation Analysis":

    # =====================================================
    # HERO
    # =====================================================

    st.html("""
<div class="hero">

    <div class="hero-content">

        <div class="hero-badge">
            🛡️ CONSERVATION INTELLIGENCE
        </div>

        <div class="hero-title">
            Conservation
            <span class="hero-highlight">
                Analysis
            </span>
        </div>

        <div class="hero-subtitle">
            Evaluate biodiversity coverage, species monitoring,
            habitat representation and observation concentration
            to support data-driven conservation planning.
        </div>

        <div class="hero-tags">

            <span class="hero-tag">
                🐦 Species Monitoring
            </span>

            <span class="hero-tag">
                🌳 Habitat Coverage
            </span>

            <span class="hero-tag">
                📍 Site Monitoring
            </span>

            <span class="hero-tag">
                📊 Conservation Intelligence
            </span>

        </div>

    </div>

    <div class="hero-bird-glow"></div>

    <div class="hero-bird">
        🛡️
    </div>

</div>
""")


    # =====================================================
    # KPI CALCULATIONS
    # =====================================================

    total_species = (
        filtered_df["Scientific_Name"].nunique()
    )

    total_observations = len(
        filtered_df
    )

    total_habitats = (
        filtered_df["Location_Type"].nunique()
    )

    total_sites = (
        filtered_df["Site_Name"].nunique()
    )


    # =====================================================
    # KPI CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🐦
    </div>

    <div class="kpi-title">
        Species Monitored
    </div>

    <div class="kpi-value">
        {total_species:,}
    </div>

</div>
""")


    with c2:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        📊
    </div>

    <div class="kpi-title">
        Total Observations
    </div>

    <div class="kpi-value">
        {total_observations:,}
    </div>

</div>
""")


    with c3:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        🌳
    </div>

    <div class="kpi-title">
        Habitats Represented
    </div>

    <div class="kpi-value">
        {total_habitats:,}
    </div>

</div>
""")


    with c4:

        st.html(f"""
<div class="kpi-card">

    <div class="kpi-icon">
        📍
    </div>

    <div class="kpi-title">
        Monitoring Sites
    </div>

    <div class="kpi-value">
        {total_sites:,}
    </div>

</div>
""")


    # =====================================================
    # SECTION 1
    # SPECIES MONITORING COVERAGE
    # =====================================================

    st.markdown("""
<div class="section-title">
    🐦 Species Monitoring Coverage
</div>

<div class="section-subtitle">
    Identify species receiving the highest observation coverage
    in the selected dataset.
</div>
""", unsafe_allow_html=True)


    species_monitoring = (
        filtered_df
        .groupby("Common_Name")
        .size()
        .reset_index(
            name="Observation_Count"
        )
        .sort_values(
            "Observation_Count",
            ascending=False
        )
        .head(10)
        .sort_values(
            "Observation_Count",
            ascending=True
        )
        .reset_index(drop=True)
    )


    if not species_monitoring.empty:

        fig_species_monitoring = px.bar(
            species_monitoring,
            x="Observation_Count",
            y="Common_Name",
            orientation="h",
            text="Observation_Count",
            color="Observation_Count",
            color_continuous_scale=[
                "#0EA5E9",
                "#14B8A6",
                "#22C55E",
                "#F59E0B"
            ],
            title="Top 10 Species by Observation Coverage"
        )


        fig_species_monitoring.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Observations: %{x:,}"
                "<extra></extra>"
            )
        )


        fig_species_monitoring.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            height=470,

            xaxis=dict(
                title="Number of Observations",
                gridcolor="rgba(255,255,255,0.10)"
            ),

            yaxis=dict(
                title=None,
                showgrid=False
            ),

            coloraxis_colorbar=dict(
                title="Observations"
            ),

            margin=dict(
                l=35,
                r=80,
                t=70,
                b=45
            )
        )


        st.plotly_chart(
            fig_species_monitoring,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        top_species_row = species_monitoring.iloc[-1]

        top_species = str(
            top_species_row["Common_Name"]
        )

        top_species_count = int(
            top_species_row["Observation_Count"]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.14),
        rgba(14,116,144,0.07)
    );
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_species}</b> has the highest observation
        coverage with <b>{top_species_count:,}</b> records.
        <br><br>

        • The ranking identifies species receiving the
        greatest level of observation effort.
        <br><br>

        • High observation frequency does not necessarily
        indicate higher population abundance; it reflects
        recorded monitoring activity.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Maintain regular monitoring of highly observed species
        while increasing effort for less-observed species.
        <br><br>

        • Avoid using observation frequency alone as a proxy
        for species population size.
        <br><br>

        • Combine observation frequency with habitat,
        seasonal and environmental information for conservation planning.

    </div>

</div>
""")


    else:

        st.info(
            "No species monitoring data is available."
        )


    # =====================================================
    # SECTION 2
    # HABITAT SPECIES REPRESENTATION
    # =====================================================

    st.markdown("""
<div class="section-title">
    🌳 Habitat Species Representation
</div>

<div class="section-subtitle">
    Compare the number of unique species represented within
    each habitat.
</div>
""", unsafe_allow_html=True)


    habitat_species = (
        filtered_df
        .groupby("Location_Type")[
            "Scientific_Name"
        ]
        .nunique()
        .reset_index(
            name="Unique_Species"
        )
        .sort_values(
            "Unique_Species",
            ascending=True
        )
    )


    if not habitat_species.empty:

        fig_habitat_species = px.bar(
            habitat_species,
            x="Unique_Species",
            y="Location_Type",
            orientation="h",
            text="Unique_Species",
            color="Unique_Species",
            color_continuous_scale=[
                "#2563EB",
                "#14B8A6",
                "#22C55E",
                "#A78BFA"
            ],
            title="Unique Species Recorded Across Habitats"
        )


        fig_habitat_species.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Unique Species: %{x:,}"
                "<extra></extra>"
            )
        )


        fig_habitat_species.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            height=420,

            xaxis=dict(
                title="Unique Species",
                gridcolor="rgba(255,255,255,0.10)"
            ),

            yaxis=dict(
                title="Habitat",
                showgrid=False
            ),

            coloraxis_colorbar=dict(
                title="Species"
            ),

            margin=dict(
                l=40,
                r=80,
                t=70,
                b=45
            )
        )


        st.plotly_chart(
            fig_habitat_species,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        top_habitat_species_row = (
            habitat_species.iloc[-1]
        )

        top_habitat_name = str(
            top_habitat_species_row[
                "Location_Type"
            ]
        )

        top_habitat_species_count = int(
            top_habitat_species_row[
                "Unique_Species"
            ]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(139,92,246,0.13),
        rgba(76,29,149,0.07)
    );
    border-left:5px solid #A78BFA;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#C4B5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_habitat_name}</b> has the highest observed
        species representation with
        <b>{top_habitat_species_count}</b> unique species.
        <br><br>

        • Habitat-level species coverage provides a useful
        view of biodiversity representation across locations.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Maintain strong monitoring coverage in habitats
        supporting broad species representation.
        <br><br>

        • Increase sampling in habitats with lower species
        representation to identify potential observation gaps.
        <br><br>

        • Use habitat-level biodiversity patterns to guide
        field-survey prioritization.

    </div>

</div>
""")


    else:

        st.info(
            "No habitat species data is available."
        )


    # =====================================================
    # SECTION 3
    # OBSERVATION SHARE BY HABITAT
    # DONUT CHART
    # =====================================================

    st.markdown("""
<div class="section-title">
    🍩 Observation Share by Habitat
</div>

<div class="section-subtitle">
    Understand the concentration of observation effort
    across different habitats.
</div>
""", unsafe_allow_html=True)


    habitat_observations = (
        filtered_df
        .groupby("Location_Type")
        .size()
        .reset_index(
            name="Observation_Count"
        )
        .sort_values(
            "Observation_Count",
            ascending=False
        )
        .reset_index(drop=True)
    )


    if not habitat_observations.empty:

        total_habitat_observations = int(
            habitat_observations[
                "Observation_Count"
            ].sum()
        )

        habitat_observations["Share"] = (
            habitat_observations[
                "Observation_Count"
            ]
            / total_habitat_observations
            * 100
        )


        habitat_color_map = {

            "Grassland": "#5B6EF5",

            "Forest": "#F15B40",

            "Wetland": "#2EC4B6",

            "Desert": "#F4B942",

            "Urban": "#9B5DE5"

        }


        pie_colors = [

            habitat_color_map.get(
                habitat,
                "#26C6B5"
            )

            for habitat in
            habitat_observations[
                "Location_Type"
            ]

        ]


        fig_habitat_share = px.pie(
            habitat_observations,
            names="Location_Type",
            values="Observation_Count",
            hole=0.62,
            title="Observation Share by Habitat"
        )


        fig_habitat_share.update_traces(

            marker=dict(
                colors=pie_colors,
                line=dict(
                    color="#0B111B",
                    width=3
                )
            ),

            textposition="outside",

            texttemplate=(
                "<b>%{label}</b><br>"
                "%{percent}"
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Observations: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )


        fig_habitat_share.add_annotation(

            text=(
                f"<b>{total_habitat_observations:,}</b>"
                "<br>"
                "<span style='font-size:11px'>"
                "OBSERVATIONS"
                "</span>"
            ),

            x=0.5,
            y=0.5,

            showarrow=False,

            font=dict(
                size=21,
                color="white"
            )
        )


        fig_habitat_share.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",

            height=430,

            legend=dict(
                title="Habitat",
                orientation="v",
                y=0.5,
                x=0.78
            ),

            margin=dict(
                l=20,
                r=20,
                t=70,
                b=25
            )
        )


        st.plotly_chart(
            fig_habitat_share,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        top_coverage = habitat_observations.iloc[0]

        coverage_habitat = str(
            top_coverage["Location_Type"]
        )

        coverage_count = int(
            top_coverage["Observation_Count"]
        )

        coverage_share = float(
            top_coverage["Share"]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(20,184,166,0.13),
        rgba(14,116,144,0.07)
    );
    border-left:5px solid #2DD4BF;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#5EEAD4;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{coverage_habitat}</b> represents
        <b>{coverage_share:.1f}%</b> of observation activity
        with <b>{coverage_count:,}</b> records.
        <br><br>

        • Observation effort is not distributed equally
        across habitats.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:25px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Increase survey effort in habitats with relatively
        low observation coverage.
        <br><br>

        • Maintain sufficient monitoring in dominant habitats
        while improving representation elsewhere.
        <br><br>

        • Consider monitoring imbalance when interpreting
        habitat-level biodiversity comparisons.

    </div>

</div>
""")


    else:

        st.info(
            "No habitat observation data is available."
        )


    # =====================================================
    # SECTION 4
    # MONITORING SITE COVERAGE
    # =====================================================

    st.markdown("""
<div class="section-title">
    📍 Monitoring Site Coverage
</div>

<div class="section-subtitle">
    Identify observation sites contributing the greatest
    monitoring coverage.
</div>
""", unsafe_allow_html=True)


    site_monitoring = (
        filtered_df
        .groupby("Site_Name")
        .size()
        .reset_index(
            name="Observation_Count"
        )
        .sort_values(
            "Observation_Count",
            ascending=True
        )
        .head(10)
        .reset_index(drop=True)
    )


    if not site_monitoring.empty:

        fig_site_monitoring = px.bar(
            site_monitoring,
            x="Observation_Count",
            y="Site_Name",
            orientation="h",
            text="Observation_Count",
            color="Observation_Count",
            color_continuous_scale=[
                "#0891B2",
                "#14B8A6",
                "#F59E0B"
            ],
            title="Top Monitoring Sites by Observation Volume"
        )


        fig_site_monitoring.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Observations: %{x:,}"
                "<extra></extra>"
            )
        )


        fig_site_monitoring.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            height=450,

            xaxis=dict(
                title="Number of Observations",
                gridcolor="rgba(255,255,255,0.10)"
            ),

            yaxis=dict(
                title="Monitoring Site",
                showgrid=False
            ),

            coloraxis_colorbar=dict(
                title="Observations"
            ),

            margin=dict(
                l=40,
                r=80,
                t=70,
                b=45
            )
        )


        st.plotly_chart(
            fig_site_monitoring,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False
            }
        )


        top_site_row = site_monitoring.iloc[-1]

        top_site = str(
            top_site_row["Site_Name"]
        )

        top_site_count = int(
            top_site_row["Observation_Count"]
        )


        st.html(f"""
<div style="
    background:linear-gradient(
        135deg,
        rgba(244,162,97,0.13),
        rgba(234,88,12,0.07)
    );
    border-left:5px solid #F4A261;
    border-radius:16px;
    padding:19px 23px;
    margin-top:15px;
    margin-bottom:14px;
">

    <div style="
        color:#FDBA74;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        💡 BUSINESS INSIGHT
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • <b>{top_site}</b> has the highest monitoring
        activity with <b>{top_site_count:,}</b> observations.
        <br><br>

        • High-volume monitoring sites represent important
        locations for continued observation effort.

    </div>

</div>
""")


        st.html("""
<div style="
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.13),
        rgba(37,99,235,0.06)
    );
    border-left:5px solid #60A5FA;
    border-radius:16px;
    padding:19px 23px;
    margin-bottom:30px;
">

    <div style="
        color:#93C5FD;
        font-size:13px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        🎯 BUSINESS RECOMMENDATION
    </div>

    <div style="
        color:#F8FAFC;
        font-size:14px;
        line-height:1.8;
    ">

        • Maintain consistent monitoring at high-activity sites.
        <br><br>

        • Expand surveys to lower-activity sites to improve
        spatial coverage.
        <br><br>

        • Review site-level observation concentration regularly
        when planning field resources.

    </div>

</div>
""")


    else:

        st.info(
            "No monitoring site data is available."
        )


    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    st.markdown("""
<div class="section-title">
    📌 Executive Summary
</div>

<div class="section-subtitle">
    Management-level summary of biodiversity monitoring coverage
    based on the current dashboard filters.
</div>
""", unsafe_allow_html=True)


    # -----------------------------------------------------
    # EXECUTIVE METRICS
    # -----------------------------------------------------

    top_species_name = (
        str(species_monitoring.iloc[-1]["Common_Name"])
        if not species_monitoring.empty
        else "N/A"
    )

    top_species_value = (
        int(species_monitoring.iloc[-1]["Observation_Count"])
        if not species_monitoring.empty
        else 0
    )


    top_habitat_name_summary = (
        str(habitat_observations.iloc[0]["Location_Type"])
        if not habitat_observations.empty
        else "N/A"
    )

    top_habitat_share_summary = (
        float(habitat_observations.iloc[0]["Share"])
        if not habitat_observations.empty
        else 0
    )


    top_site_name_summary = (
        str(site_monitoring.iloc[-1]["Site_Name"])
        if not site_monitoring.empty
        else "N/A"
    )

    top_site_value_summary = (
        int(site_monitoring.iloc[-1]["Observation_Count"])
        if not site_monitoring.empty
        else 0
    )


    # -----------------------------------------------------
    # SUMMARY CARD
    # -----------------------------------------------------

    executive_summary_html = f"""
<div style="
    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(45,212,191,0.18),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #082F35 0%,
            #0B3B42 45%,
            #0E3B5E 100%
        );

    border:1px solid rgba(94,234,212,0.25);

    border-radius:22px;

    padding:28px 30px;

    margin-top:10px;

    box-shadow:
        0 15px 40px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.08);
">


    <div style="
        display:flex;
        align-items:center;
        gap:12px;
        margin-bottom:18px;
    ">

        <div style="
            width:42px;
            height:42px;
            border-radius:12px;
            background:linear-gradient(
                135deg,
                #0D9488,
                #2563EB
            );
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:22px;
        ">
            📌
        </div>

        <div>

            <div style="
                color:#F8FAFC;
                font-size:21px;
                font-weight:900;
            ">
                Conservation Monitoring Overview
            </div>

            <div style="
                color:#94A3B8;
                font-size:12px;
                margin-top:3px;
            ">
                Current filtered dataset
            </div>

        </div>

    </div>


    <div style="
        color:#E2E8F0;
        font-size:14px;
        line-height:1.9;
    ">

        <b>Coverage:</b>
        The current analysis includes
        <b>{total_species:,} species</b>,
        <b>{total_observations:,} observations</b>,
        <b>{total_habitats:,} habitats</b> and
        <b>{total_sites:,} monitoring sites.</b>

        <br><br>

        <b>Species Focus:</b>
        <b>{top_species_name}</b> has the highest observation
        coverage with <b>{top_species_value:,}</b> records.

        <br><br>

        <b>Habitat Focus:</b>
        <b>{top_habitat_name_summary}</b> represents
        <b>{top_habitat_share_summary:.1f}%</b>
        of total observation activity.

        <br><br>

        <b>Monitoring Hotspot:</b>
        <b>{top_site_name_summary}</b> contributes
        <b>{top_site_value_summary:,}</b> observations,
        making it the highest-volume monitoring site.

        <br><br>

        <b>Management Implication:</b>
        Observation coverage is concentrated around
        particular species, habitats and monitoring locations.
        Conservation decisions should therefore consider
        monitoring intensity alongside biodiversity patterns.

    </div>


    <div style="
        margin-top:22px;
        padding-top:18px;
        border-top:1px solid rgba(148,163,184,0.18);
    ">

        <div style="
            color:#5EEAD4;
            font-size:12px;
            font-weight:800;
            letter-spacing:1px;
            margin-bottom:10px;
        ">
            🎯 PRIORITY ACTIONS
        </div>

        <div style="
            color:#F8FAFC;
            font-size:14px;
            line-height:1.9;
        ">

            • Strengthen monitoring in under-represented
            habitats and lower-observation sites.
            <br>

            • Maintain consistent monitoring of highly observed
            species without treating observation frequency as
            a direct measure of abundance.
            <br>

            • Use balanced species, habitat and site coverage
            to support future conservation planning.

        </div>

    </div>


</div>
"""

    st.html(executive_summary_html)


    # =====================================================
    # EXECUTIVE FOOTNOTE
    # =====================================================

    st.caption(
        "Executive Summary reflects the currently selected "
        "Year, Location Type and Observer filters."
    )