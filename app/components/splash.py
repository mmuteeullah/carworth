"""Splash screen component."""

import streamlit as st
import time
import base64
from pathlib import Path


def get_logo_base64() -> str:
    """Get logo as base64 for embedding in HTML."""
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def show_splash_screen() -> bool:
    """
    Show splash screen on first load with logo.

    Returns True if splash was shown (first load), False otherwise.
    """
    # Check if this is first load
    if "splash_shown" not in st.session_state:
        st.session_state["splash_shown"] = False

    if not st.session_state["splash_shown"]:
        # Get logo
        logo_b64 = get_logo_base64()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="splash-logo-img" />' if logo_b64 else '<div class="splash-logo">🚗</div>'

        # Show splash screen
        splash = st.empty()

        with splash.container():
            st.markdown(
                f"""
                <style>
                    @keyframes fadeIn {{
                        from {{ opacity: 0; transform: translateY(-20px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                    @keyframes pulse {{
                        0%, 100% {{ transform: scale(1); opacity: 1; }}
                        50% {{ transform: scale(1.05); opacity: 0.9; }}
                    }}
                    @keyframes shimmer {{
                        0% {{ background-position: -200% center; }}
                        100% {{ background-position: 200% center; }}
                    }}
                    .splash-container {{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        min-height: 85vh;
                        text-align: center;
                        animation: fadeIn 0.6s ease-out;
                        background: radial-gradient(ellipse at center, #1e3a5f 0%, #0f172a 70%);
                        margin: -1rem;
                        padding: 2rem;
                        border-radius: 16px;
                    }}
                    .splash-logo {{
                        font-size: 6rem;
                        margin-bottom: 1.5rem;
                        animation: pulse 2s ease-in-out infinite;
                    }}
                    .splash-logo-img {{
                        width: 150px;
                        height: 150px;
                        object-fit: contain;
                        margin-bottom: 1.5rem;
                        animation: pulse 2s ease-in-out infinite;
                        filter: drop-shadow(0 0 30px rgba(59, 130, 246, 0.5));
                    }}
                    .splash-title {{
                        font-size: 3.5rem;
                        font-weight: 800;
                        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #60a5fa 100%);
                        background-size: 200% auto;
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        margin-bottom: 0.5rem;
                        animation: shimmer 3s linear infinite;
                        letter-spacing: -0.02em;
                    }}
                    .splash-subtitle {{
                        font-size: 1.3rem;
                        color: #94a3b8;
                        margin-bottom: 2.5rem;
                        font-weight: 300;
                    }}
                    .splash-loading {{
                        display: flex;
                        gap: 10px;
                        margin-top: 1rem;
                    }}
                    .splash-dot {{
                        width: 14px;
                        height: 14px;
                        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
                        border-radius: 50%;
                        animation: pulse 1.2s ease-in-out infinite;
                        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
                    }}
                    .splash-dot:nth-child(2) {{ animation-delay: 0.2s; }}
                    .splash-dot:nth-child(3) {{ animation-delay: 0.4s; }}
                    .splash-tagline {{
                        margin-top: 3rem;
                        padding: 12px 24px;
                        background: rgba(59, 130, 246, 0.1);
                        border: 1px solid rgba(59, 130, 246, 0.3);
                        border-radius: 30px;
                        color: #60a5fa;
                        font-size: 0.95rem;
                        font-weight: 500;
                    }}
                    .splash-version {{
                        position: fixed;
                        bottom: 2rem;
                        color: #475569;
                        font-size: 0.9rem;
                    }}
                </style>

                <div class="splash-container">
                    {logo_html}
                    <div class="splash-title">CarWorth</div>
                    <div class="splash-subtitle">Used Car Value Calculator for India</div>
                    <div class="splash-loading">
                        <div class="splash-dot"></div>
                        <div class="splash-dot"></div>
                        <div class="splash-dot"></div>
                    </div>
                    <div class="splash-tagline">✨ Know the fair price before you buy</div>
                    <div class="splash-version">v2.0</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Wait briefly
        time.sleep(2)

        # Clear splash and mark as shown
        splash.empty()
        st.session_state["splash_shown"] = True
        return True

    return False
