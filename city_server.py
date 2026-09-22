import json




from flask import Flask, jsonify, render_template_string
from city_core import get_city_context
from city_chat import load_chat


def load_city_state():
    try:
        with open("city_state.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "city": "AI CITY",
            "simulation_status": "offline",
            "citizens": [],
            "locations": [],
            "recent_activities": []
        }


app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI CITY</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #07111f;
    color: white;
}



html {
    scroll-behavior: smooth;
}

#activity,
#chat,
#citizens,
#knowledge {
    scroll-margin-top: 80px;
}

.navbar {
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    padding: 12px;
    background: #091827;
    border-bottom: 1px solid #263b55;
}

.navbar a {
    color: white;
    text-decoration: none;
    padding: 10px 16px;
    background: #12243a;
    border: 1px solid #35506c;
    border-radius: 10px;
    font-size: 14px;
}

.navbar a:hover {
    background: #1b3654;
}

header {
    padding: 20px;
    text-align: center;
    background: #0d1b2e;
    border-bottom: 1px solid #263b55;
}

header h1 {
    margin: 0;
    font-size: 32px;
}

.status {
    margin-top: 8px;
    color: #55ff99;
}

.city {
    position: relative;
    min-height: 700px;
    max-width: 1000px;
    margin: auto;
    padding: 25px;
    background:
        linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
    background-size: 40px 40px;
}

.road {
    position: absolute;
    background: #26384d;
    border-radius: 20px;
}

.road.horizontal {
    height: 35px;
    left: 5%;
    right: 5%;
    top: 48%;
}

.road.vertical {
    width: 35px;
    top: 10%;
    bottom: 8%;
    left: 50%;
    transform: translateX(-50%);
}

.building {
    position: absolute;
    width: 190px;
    padding: 20px;
    text-align: center;
    background: #12243a;
    border: 1px solid #35506c;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,.3);
}

.building .icon {
    font-size: 42px;
}

.building h2 {
    margin: 8px 0;
    font-size: 20px;
}

.building p {
    margin: 5px 0;
    color: #b9c7d8;
}

.core {
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
}

.aion {
    top: 10%;
    left: 4%;
}

.nova {
    top: 10%;
    right: 4%;
}

.knowledge {
    bottom: 7%;
    left: 4%;
}

.hub {
    bottom: 7%;
    right: 4%;
}

.hub-box {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
}

.message {
    background: #12243a;
    border-left: 4px solid #4d7cff;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
}

.message .sender {
    font-weight: bold;
    margin-bottom: 5px;
}

.message .time {
    font-size: 11px;
    color: #71849b;
}

.empty {
    color: #91a2b5;
}

@media (max-width: 650px) {

    .city {
        min-height: 900px;
    }

    .building {
        width: 145px;
        padding: 14px;
    }

    .building .icon {
        font-size: 32px;
    }

    .building h2 {
        font-size: 16px;
    }

}


/* Citizen Status layout */
.citizen-status-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    width: 100%;
    margin-top: 20px;
}

.citizen-card {
    position: relative;
    width: 100%;
    min-height: 230px;
    padding: 22px;
    text-align: center;
    background: #12243a;
    border: 1px solid #35506c;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,.25);
}

.citizen-card .icon {
    font-size: 42px;
    margin-bottom: 10px;
}

.citizen-card h2 {
    margin: 8px 0 12px;
    font-size: 21px;
}

.citizen-card p {
    margin: 8px 0;
    line-height: 1.5;
}

.citizen-card .status {
    margin-top: 10px;
}

@media (max-width: 600px) {
    .citizen-status-list {
        grid-template-columns: 1fr;
        gap: 16px;
    }
}


/* FINAL CITIZEN STATUS LAYOUT */

.citizens-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 24px;
    width: 100%;
    margin-top: 24px;
}

.citizen-status-card {
    position: relative;
    width: auto;
    min-width: 0;
    min-height: 280px;
    padding: 24px;
    text-align: center;
    background: #12243a;
    border: 1px solid #35506c;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,.3);
}

.citizen-icon {
    font-size: 44px;
    margin-bottom: 8px;
}

.citizen-status-card h2 {
    margin: 8px 0;
    font-size: 22px;
}

.citizen-id {
    margin: 4px 0 12px;
    color: #9fb4cc;
}

.citizen-active {
    color: #55ff99;
    font-weight: bold;
    margin: 10px 0 18px;
}

.citizen-stat {
    margin: 9px 0;
    line-height: 1.5;
}

.citizen-stat span {
    font-weight: bold;
}

@media (max-width: 600px) {
    .citizens-grid {
        grid-template-columns: 1fr;
        gap: 18px;
    }

    .citizen-status-card {
        min-height: auto;
    }
}


/* AI CITY BACKGROUND */
body {
    background-image:
        linear-gradient(
            rgba(4, 10, 20, 0.72),
            rgba(4, 10, 20, 0.82)
        ),
        url("/static/ai_city_banner.png");

    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    background-repeat: no-repeat;
}


/* AI CITY PROFILE HERO */

.ai-city-hero {
    position: relative;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px 20px 35px;
    margin-bottom: 25px;
    text-align: center;
}

.ai-city-profile {
    width: min(280px, 72vw);
    height: min(280px, 72vw);
    object-fit: cover;
    border-radius: 50%;
    border: 3px solid rgba(120, 190, 255, 0.8);
    box-shadow:
        0 0 25px rgba(80, 170, 255, 0.45),
        0 0 60px rgba(80, 130, 255, 0.20);
}

.ai-city-hero h1 {
    margin: 20px 0 5px;
    font-size: clamp(30px, 7vw, 52px);
    letter-spacing: 4px;
}

.ai-city-hero p {
    margin: 5px 0;
    color: #b7cce3;
    font-size: 15px;
}


/* AI CITY PROFILE ICON */
.city-profile-icon {
    width: 58px;
    height: 58px;
    object-fit: cover;
    border-radius: 50%;
    vertical-align: middle;
    margin-right: 10px;
    border: 2px solid rgba(120, 190, 255, 0.8);
    box-shadow: 0 0 18px rgba(80, 170, 255, 0.4);
}


/* CITIZEN PROFILE IMAGE */
.citizen-icon-image {
    width: 110px;
    height: 110px;
    object-fit: cover;
    border-radius: 50%;
    display: block;
    margin: 0 auto 14px;
    border: 2px solid rgba(120, 190, 255, 0.75);
    box-shadow: 0 0 25px rgba(80, 170, 255, 0.30);
}


/* PHYSICAL CITY */
.live-state-panel {
    margin-top: 22px;
    padding: 18px;
    border-radius: 16px;
    background: rgba(8, 18, 32, 0.72);
    border: 1px solid rgba(120, 180, 255, 0.18);
    text-align: left;
}

.live-state-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}

.live-state-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.035);
}

.live-state-icon {
    font-size: 20px;
}

.live-state-item strong {
    display: block;
    font-size: 14px;
}

.live-state-item small {
    display: block;
    margin-top: 3px;
    opacity: 0.55;
    font-size: 11px;
}

@media (max-width: 700px) {
    .live-state-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

.physical-city-panel {
    margin: 28px 0;
    padding: 22px;
    border-radius: 18px;
    background: rgba(8, 18, 32, 0.84);
    border: 1px solid rgba(120, 180, 255, 0.25);
    backdrop-filter: blur(8px);
    text-align: left;
}

.physical-city-panel h2 {
    margin-top: 0;
    text-align: center;
}

.physical-district {
    margin-top: 16px;
    padding: 16px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.physical-district h3 {
    margin-top: 0;
}

.physical-building {
    margin-top: 12px;
    padding: 14px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
}

.physical-occupants {
    margin-top: 10px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.physical-citizen {
    padding: 7px 12px;
    border-radius: 20px;
    background: rgba(80, 170, 255, 0.12);
    border: 1px solid rgba(80, 170, 255, 0.22);
}

.physical-empty {
    margin-top: 8px;
    opacity: 0.6;
}

.physical-stats {
    margin-top: 10px;
    text-align: center;
    opacity: 0.75;
}


/* CITY HUB V3 */
.city-hub-details {
    width: 100%;
}

.city-hub-details summary {
    cursor: pointer;
    list-style: none;
    user-select: none;
    padding: 4px 0;
}

.city-hub-details summary::-webkit-details-marker {
    display: none;
}

.city-hub-details summary::after {
    content: " ▸";
    opacity: 0.65;
}

.city-hub-details[open] summary::after {
    content: " ▾";
}

.hub-message-count {
    float: right;
    opacity: 0.6;
    font-size: 13px;
    font-weight: normal;
}

.city-hub-history {
    margin-top: 18px;
}


/* AI CITY PROFESSIONAL LANDING */
.welcome-section {
    max-width: 760px;
    margin: 32px auto 28px;
    padding: 34px 28px;
    text-align: center;
    border-radius: 22px;
    background: rgba(5, 14, 28, 0.72);
    border: 1px solid rgba(120, 190, 255, 0.22);
    backdrop-filter: blur(10px);
    box-shadow: 0 12px 45px rgba(0, 0, 0, 0.28);
}

.welcome-badge {
    display: inline-block;
    margin-bottom: 14px;
    padding: 6px 13px;
    border-radius: 20px;
    font-size: 12px;
    letter-spacing: 1.2px;
    color: rgba(180, 220, 255, 0.9);
    background: rgba(80, 170, 255, 0.10);
    border: 1px solid rgba(120, 190, 255, 0.20);
}

.welcome-section h2 {
    margin: 4px 0 16px;
    font-size: 30px;
}

.welcome-section p {
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.7;
    font-size: 15px;
    opacity: 0.88;
}

.welcome-section .welcome-subtitle {
    margin-top: 12px;
    font-size: 13px;
    opacity: 0.58;
}

@media (max-width: 600px) {
    .welcome-section {
        margin: 22px 12px;
        padding: 28px 20px;
    }

    .welcome-section h2 {
        font-size: 25px;
    }
}


/* =========================================
   AI CITY HAMBURGER MENU
   ========================================= */

.menu-button {
    position: fixed;
    top: 18px;
    right: 18px;
    z-index: 1001;

    width: 46px;
    height: 46px;

    border-radius: 14px;
    border: 1px solid rgba(140, 200, 255, 0.25);

    background: rgba(5, 14, 28, 0.72);
    color: white;

    font-size: 23px;
    line-height: 1;

    cursor: pointer;

    backdrop-filter: blur(10px);

    box-shadow:
        0 8px 28px rgba(0, 0, 0, 0.28);

    transition:
        transform 0.2s ease,
        background 0.2s ease;
}

.menu-button:hover {
    transform: scale(1.05);
    background: rgba(20, 45, 75, 0.9);
}

.city-menu-overlay {
    position: fixed;
    inset: 0;

    z-index: 2000;

    background: rgba(0, 0, 0, 0.42);

    opacity: 0;
    visibility: hidden;

    transition:
        opacity 0.25s ease,
        visibility 0.25s ease;

    backdrop-filter: blur(2px);
}

.city-menu-overlay.open {
    opacity: 1;
    visibility: visible;
}

.city-menu {
    position: absolute;
    top: 0;
    right: 0;

    width: min(340px, 86vw);
    height: 100%;

    padding: 26px 22px;

    box-sizing: border-box;

    background:
        linear-gradient(
            180deg,
            rgba(7, 18, 34, 0.98),
            rgba(4, 10, 20, 0.98)
        );

    border-left: 1px solid rgba(120, 190, 255, 0.22);

    box-shadow:
        -12px 0 45px rgba(0, 0, 0, 0.35);

    transform: translateX(100%);

    transition:
        transform 0.28s ease;
}

.city-menu-overlay.open .city-menu {
    transform: translateX(0);
}

.city-menu-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding-bottom: 22px;

    border-bottom:
        1px solid rgba(255, 255, 255, 0.08);
}

.city-menu-title {
    font-size: 21px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.city-menu-subtitle {
    margin-top: 4px;

    font-size: 12px;
    opacity: 0.5;

    letter-spacing: 1px;
}

.menu-close {
    width: 40px;
    height: 40px;

    border-radius: 12px;

    border: 1px solid rgba(255, 255, 255, 0.10);

    background: rgba(255, 255, 255, 0.05);
    color: white;

    font-size: 18px;

    cursor: pointer;
}

.city-menu-links {
    display: flex;
    flex-direction: column;

    margin-top: 20px;
}

.city-menu-links a {
    display: flex;
    align-items: center;
    gap: 14px;

    padding: 15px 12px;

    border-radius: 12px;

    color: white;
    text-decoration: none;

    font-size: 15px;

    transition:
        background 0.2s ease,
        transform 0.2s ease;
}

.city-menu-links a:hover {
    background: rgba(100, 180, 255, 0.08);
    transform: translateX(3px);
}

.city-menu-links a span:first-child {
    width: 26px;
    text-align: center;
    font-size: 18px;
}

.city-menu-footer {
    position: absolute;
    bottom: 24px;
    left: 22px;

    font-size: 11px;
    opacity: 0.4;

    letter-spacing: 0.8px;
}


/* =========================================
   AI CITY PROFESSIONAL V2
   ========================================= */

.hero-section {
    max-width: 900px;
    margin: 42px auto 35px;
    padding: 70px 28px 62px;
    text-align: center;
    border-radius: 28px;
    background:
        radial-gradient(
            circle at 50% 20%,
            rgba(70, 150, 255, 0.14),
            transparent 55%
        ),
        rgba(5, 14, 28, 0.68);
    border: 1px solid rgba(120, 190, 255, 0.20);
    backdrop-filter: blur(12px);
    box-shadow: 0 20px 70px rgba(0,0,0,0.30);
}

.hero-badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 11px;
    letter-spacing: 1.5px;
    color: rgba(190, 225, 255, 0.92);
    background: rgba(80, 170, 255, 0.10);
    border: 1px solid rgba(120, 190, 255, 0.22);
}

.hero-section h2 {
    margin: 22px 0 18px;
    font-size: clamp(38px, 7vw, 68px);
    line-height: 1.04;
    letter-spacing: -1.5px;
}

.hero-section h2 span {
    background: linear-gradient(
        90deg,
        #8fd3ff,
        #ffffff,
        #8fb9ff
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 680px;
    margin: auto;
    font-size: 16px;
    line-height: 1.75;
    opacity: 0.72;
}

.hero-actions {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 30px;
    flex-wrap: wrap;
}

.hero-button {
    display: inline-block;
    padding: 12px 20px;
    border-radius: 12px;
    text-decoration: none;
    font-size: 14px;
    transition: all 0.2s ease;
}

.hero-button.primary {
    color: white;
    background: rgba(75, 160, 255, 0.22);
    border: 1px solid rgba(120, 200, 255, 0.38);
}

.hero-button.secondary {
    color: rgba(220,235,255,0.85);
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
}

.hero-button:hover {
    transform: translateY(-2px);
    background: rgba(80,170,255,0.25);
}

/* HOW IT WORKS */

.how-section {
    max-width: 1000px;
    margin: 30px auto;
    padding: 32px 24px;
    text-align: center;
}

.section-label {
    font-size: 11px;
    letter-spacing: 2px;
    opacity: 0.45;
    margin-bottom: 10px;
}

.how-section h2 {
    margin: 0;
    font-size: 27px;
}

.section-description {
    max-width: 650px;
    margin: 12px auto 28px;
    line-height: 1.65;
    opacity: 0.58;
    font-size: 14px;
}

.how-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
}

.how-card {
    padding: 22px 18px;
    border-radius: 17px;
    text-align: left;
    background: rgba(7,18,34,0.68);
    border: 1px solid rgba(120,190,255,0.13);
    transition: transform 0.2s ease,
                border-color 0.2s ease;
}

.how-card:hover {
    transform: translateY(-3px);
    border-color: rgba(120,190,255,0.28);
}

.how-number {
    font-size: 11px;
    letter-spacing: 1px;
    opacity: 0.35;
    margin-bottom: 15px;
}

.how-card h3 {
    margin: 0 0 8px;
    font-size: 16px;
}

.how-card p {
    margin: 0;
    font-size: 13px;
    line-height: 1.6;
    opacity: 0.58;
}

/* CITY STATUS */

.city-status-section {
    max-width: 900px;
    margin: 10px auto 32px;
    padding: 24px;
    text-align: center;
}

.city-status-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 18px;
}

.status-item {
    padding: 18px 12px;
    border-radius: 15px;
    background: rgba(5,15,28,0.68);
    border: 1px solid rgba(120,190,255,0.12);
}

.status-value {
    font-size: 25px;
    font-weight: 700;
}

.status-label {
    margin-top: 5px;
    font-size: 11px;
    letter-spacing: 0.7px;
    opacity: 0.45;
    text-transform: uppercase;
}

/* MOBILE */

@media (max-width: 760px) {

    .hero-section {
        margin: 25px 12px;
        padding: 52px 20px 45px;
    }

    .hero-section h2 {
        font-size: 40px;
    }

    .how-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .city-status-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {

    .how-grid {
        grid-template-columns: 1fr;
    }

    .hero-section h2 {
        font-size: 35px;
    }
}




/* =========================================================
   AI CITY MAP V3 — REFERENCE UI
   Full-screen futuristic/isometric city dashboard
   ========================================================= */




/* =========================================================
   AI CITY MAP V3 — SIDE + BOTTOM COMPACT
   ========================================================= */

@media (orientation: landscape) and (max-height: 600px) {

    /* LEFT PANEL */
    .ai-city-side {
        width: 125px !important;
        top: 58px !important;
        bottom: 48px !important;
        padding: 0 0 6px !important;
    }

    .ai-city-nav-item {
        min-height: 30px !important;
        height: 30px !important;
        padding: 0 10px !important;
        gap: 6px !important;
        font-size: 10px !important;
    }

    .ai-city-nav-item .nav-icon {
        width: 16px !important;
        font-size: 14px !important;
    }

    /* BOTTOM LIVE BADGE */
    .ai-city-live-badge {
        left: 12px !important;
        bottom: 10px !important;
        padding: 5px 9px !important;
        font-size: 8px !important;
        border-radius: 8px !important;
    }


}



/* =========================================================
   AI CITY MAP V3 — CITY OVERVIEW + AGENT CARDS COMPACT
   ========================================================= */

@media (orientation: landscape) and (max-height: 600px) {

    /* CITY OVERVIEW */
    .ai-city-overview {
        width: 175px !important;
        flex: 0 0 175px !important;
        padding: 6px 8px !important;
        box-sizing: border-box !important;
    }

    .ai-city-panel-title {
        font-size: 10px !important;
        line-height: 1.1 !important;
    }

    .ai-city-panel-title .panel-icon {
        font-size: 13px !important;
    }

    .ai-city-divider {
        margin: 4px 0 !important;
    }

    .ai-city-overview-grid {
        gap: 3px !important;
    }

    .ai-city-overview-grid > div {
        padding: 3px 4px !important;
    }

    .ai-city-overview small {
        font-size: 7px !important;
    }

    .ai-city-overview strong {
        font-size: 10px !important;
        margin-top: 1px !important;
    }

    /* DUDU + BUBU CONTAINER */
    .ai-city-agent-cards {
        gap: 5px !important;
    }

    /* DUDU + BUBU */
    .ai-city-agent-card {
        min-width: 145px !important;
        width: 145px !important;
        padding: 6px 8px !important;
        gap: 6px !important;
        border-radius: 10px !important;
        box-sizing: border-box !important;
    }

    .ai-city-agent-avatar {
        width: 28px !important;
        height: 28px !important;
        min-width: 28px !important;
        font-size: 15px !important;
    }

    .ai-city-agent-card .agent-name {
        font-size: 10px !important;
    }

    .ai-city-agent-card .online {
        font-size: 7px !important;
    }

    .ai-city-agent-card .agent-meta {
        font-size: 7px !important;
        line-height: 1.2 !important;
        margin-top: 2px !important;
    }

    .ai-city-agent-card .agent-arrow {
        font-size: 15px !important;
    }
}



/* =========================================================
   AI CITY MAP V3 — AGENT PANELS COMPACT V2
   ========================================================= */

@media (orientation: landscape) and (max-height: 600px) {

    /* CITY OVERVIEW */
    .ai-city-overview {
        width: 140px !important;
        flex: 0 0 140px !important;
        padding: 5px 6px !important;
        border-radius: 9px !important;
    }

    .ai-city-panel-title {
        font-size: 8px !important;
        line-height: 1.1 !important;
    }

    .ai-city-panel-title span {
        font-size: 10px !important;
    }

    .ai-city-overview-grid {
        gap: 2px !important;
    }

    .ai-city-overview-grid > div {
        padding: 2px 3px !important;
        font-size: 6px !important;
    }

    .ai-city-overview-grid strong {
        font-size: 8px !important;
    }

    /* DUDU + BUBU */
    .ai-city-agent-cards {
        gap: 3px !important;
    }

    .ai-city-agent-card {
        min-width: 115px !important;
        width: 115px !important;
        padding: 4px 6px !important;
        gap: 4px !important;
        border-radius: 8px !important;
    }

    .ai-city-agent-avatar {
        width: 22px !important;
        height: 22px !important;
        min-width: 22px !important;
        font-size: 12px !important;
    }

    .ai-city-agent-card .agent-name {
        font-size: 8px !important;
    }

    .ai-city-agent-card .online {
        font-size: 6px !important;
    }

    .ai-city-agent-card .agent-meta {
        font-size: 6px !important;
        line-height: 1.15 !important;
    }

    .ai-city-agent-card .agent-arrow {
        font-size: 12px !important;
    }
}

/* =========================================================
   AI CITY MAP V3 — LANDSCAPE PANEL COMPACT
   ========================================================= */

@media (orientation: landscape) and (max-height: 600px) {


    .ai-city-stat {
        min-width: 70px !important;
        padding: 6px 9px !important;
    }

    .ai-city-stat-icon {
        font-size: 16px !important;
    }

    .ai-city-stat span {
        font-size: 9px !important;
    }

    .ai-city-stat strong {
        font-size: 13px !important;
    }

    .ai-city-time {
        min-width: 155px !important;
        padding: 6px 9px !important;
        transform: scale(.68) !important;
        transform-origin: top right !important;
    }

    .ai-city-time .sun {
        font-size: 22px !important;
    }

    .ai-city-time small {
        font-size: 9px !important;
    }

    .ai-city-time strong {
        font-size: 15px !important;
    }

    .ai-city-time em {
        font-size: 8px !important;
    }

    .ai-city-live-badge {
        transform: scale(.72) !important;
        transform-origin: bottom left !important;
        font-size: 9px !important;
    }

    .ai-city-back {
        transform: scale(.72) !important;
        transform-origin: bottom right !important;
    }
}


/* =========================================================
   AI CITY MAP V3 — MOBILE LANDSCAPE
   ========================================================= */

@media (orientation: landscape) and (max-height: 600px) {
    .ai-city-map-v3 {
        min-height: 100vh;
        height: 100vh;
    }

    .ai-city-map-v3-bg {
        background-size: contain !important;
        background-position: center center !important;
        transform: scale(1.0) !important;
    }

    .ai-city-map-v3-top {
        top: 8px;
        left: 12px;
        right: 60px;
    }

    .ai-city-brand-mark {
        width: 48px;
        height: 40px;
        font-size: 28px;
    }

    .ai-city-brand-text strong {
        font-size: 24px;
    }

    .ai-city-brand-text span {
        font-size: 10px;
    }

    .ai-city-side {
        top: 72px;
        bottom: 70px;
        width: 175px;
    }

    .ai-city-nav-item {
        min-height: 38px;
        padding: 0 18px;
        gap: 10px;
        font-size: 12px;
    }

    .ai-city-nav-item .nav-icon {
        width: 20px;
        font-size: 17px;
    }

    
    }
}


body.map-only {
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: #020a14 !important;
}

body.map-only .city {
    min-height: 100vh !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}

body.map-only .city > .hub-box { display: none !important; }

body.map-only .city > #aiCityMapPanel { display: block !important; }

#aiCityMapPanel {
    position: fixed;
    inset: 0;
    z-index: 9990;
    width: 100vw;
    height: 100vh;
    background: #020a14;
}

.ai-city-map-v3 {
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 100vh;
    overflow: hidden;
    color: #eef8ff;
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #020a14;
}

.ai-city-map-v3-bg {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(90deg, rgba(0,10,22,.18), rgba(0,10,22,0) 28%),
        linear-gradient(0deg, rgba(0,8,18,.24), rgba(0,8,18,0) 35%),
        url("/static/ai_city_map_v3_background.png");
    background-size: contain;
    background-position: center center;
    background-repeat: no-repeat;
    transform: scale(1.0);
    filter: saturate(1.04) contrast(1.03);
}

.ai-city-map-v3-vignette {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
        linear-gradient(90deg, rgba(0,5,14,.72) 0%, rgba(0,5,14,.38) 15%, transparent 31%),
        linear-gradient(180deg, rgba(0,8,20,.44), transparent 16%, transparent 83%, rgba(0,6,15,.5));
}

.ai-city-map-v3-top {
    position: absolute;
    top: 16px;
    left: 18px;
    right: 78px;
    z-index: 20;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 18px;
    pointer-events: none;
}

.ai-city-brand { display: flex; align-items: center; gap: 12px; pointer-events: auto; }

.ai-city-brand-mark {
    width: 68px;
    height: 54px;
    display: grid;
    place-items: center;
    color: #69c9ff;
    font-size: 38px;
    filter: drop-shadow(0 0 12px rgba(35,170,255,.8));
}

.ai-city-brand-text strong {
    display: block;
    font-size: clamp(25px, 3vw, 38px);
    line-height: .95;
    letter-spacing: .02em;
    color: #f4fbff;
    text-shadow: 0 0 18px rgba(48,181,255,.45);
}

.ai-city-brand-text span {
    display: block;
    margin-top: 5px;
    font-size: 13px;
    color: #16bff4;
}

.ai-city-time {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 215px;
    padding: 9px 15px;
    border: 1px solid rgba(0,168,255,.65);
    border-radius: 17px;
    background: rgba(3,20,38,.78);
    box-shadow: inset 0 0 18px rgba(0,130,255,.08), 0 0 20px rgba(0,100,255,.12);
    backdrop-filter: blur(12px);
    pointer-events: auto;
}

.ai-city-time .sun { font-size: 32px; line-height: 1; }
.ai-city-time small { display: block; color: #72caff; font-size: 12px; }
.ai-city-time strong { display: block; font-size: 21px; margin-top: 1px; }
.ai-city-time em { margin-left: auto; font-style: normal; font-size: 11px; color: #b8d9ee; }

.ai-city-stats {
    display: flex;
    align-items: stretch;
    overflow: hidden;
    border: 1px solid rgba(0,155,255,.62);
    border-radius: 17px;
    background: rgba(3,21,40,.78);
    box-shadow: inset 0 0 25px rgba(0,120,255,.08), 0 0 24px rgba(0,100,255,.13);
    backdrop-filter: blur(12px);
    pointer-events: auto;
}

.ai-city-stat {
    min-width: 96px;
    padding: 10px 14px;
    border-right: 1px solid rgba(0,155,255,.3);
    text-align: center;
}

.ai-city-stat:last-child { border-right: 0; }
.ai-city-stat-icon { display: block; font-size: 21px; color: #69caff; line-height: 1; }
.ai-city-stat span { display: block; margin-top: 3px; font-size: 11px; color: #b7d8eb; }
.ai-city-stat strong { display: block; margin-top: 1px; font-size: 17px; color: #fff; }

.ai-city-map-v3-menu {
    position: absolute;
    top: 16px;
    right: 18px;
    z-index: 31;
    width: 46px;
    height: 46px;
    border: 1px solid rgba(0,170,255,.65);
    border-radius: 13px;
    background: rgba(2,20,38,.84);
    color: #9fe0ff;
    font-size: 25px;
    cursor: pointer;
    display: grid;
    place-items: center;
    box-shadow: 0 0 18px rgba(0,130,255,.2);
}

.ai-city-side {
    position: absolute;
    top: 110px;
    left: 0;
    bottom: 120px;
    z-index: 19;
    width: 222px;
    padding: 0 0 14px;
    background: linear-gradient(90deg, rgba(1,12,25,.95), rgba(2,17,33,.82), rgba(2,17,33,.08));
    border-right: 1px solid rgba(0,160,255,.18);
}

.ai-city-nav-item {
    display: flex;
    align-items: center;
    gap: 17px;
    min-height: 54px;
    padding: 0 28px;
    color: #c9e8ff;
    font-size: 16px;
    text-decoration: none;
    box-sizing: border-box;
}

.ai-city-nav-item .nav-icon {
    width: 26px;
    text-align: center;
    font-size: 23px;
    color: #a7ddff;
}

.ai-city-nav-item.active {
    color: #fff;
    background: linear-gradient(90deg, rgba(12,132,255,.9), rgba(11,91,180,.54));
    box-shadow: inset 3px 0 0 #59c9ff, 0 0 18px rgba(0,130,255,.13);
}

.ai-city-nav-item:hover { background: rgba(0,130,255,.2); }

.ai-city-bottom {
    position: absolute;
    left: 18px;
    bottom: 18px;
    z-index: 24;
    display: flex;
    align-items: flex-end;
    gap: 14px;
}

.ai-city-overview,
.ai-city-agent-card {
    border: 1px solid rgba(0,154,255,.65);
    background: rgba(2,17,32,.84);
    box-shadow: inset 0 0 25px rgba(0,110,255,.07), 0 0 22px rgba(0,80,180,.12);
    backdrop-filter: blur(10px);
    border-radius: 16px;
}

.ai-city-overview { width: 300px; padding: 14px 16px; }

.ai-city-panel-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: .03em;
}

.ai-city-panel-title .panel-icon { color: #66ccff; font-size: 20px; }
.ai-city-divider { height: 1px; margin: 10px 0 11px; background: rgba(0,158,255,.28); }

.ai-city-overview-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.ai-city-overview-grid > div {
    padding-right: 8px;
    border-right: 1px solid rgba(0,158,255,.2);
}

.ai-city-overview-grid > div:nth-child(3n) { border-right: 0; }
.ai-city-overview small { display: block; color: #6fbcdf; font-size: 10px; }
.ai-city-overview strong { display: block; margin-top: 2px; color: #fff; font-size: 15px; }

.ai-city-agent-cards { display: flex; gap: 10px; }

.ai-city-agent-card {
    width: 285px;
    min-height: 72px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    gap: 11px;
    box-sizing: border-box;
}

.ai-city-agent-avatar {
    width: 50px;
    height: 50px;
    flex: 0 0 50px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 27px;
    background: radial-gradient(circle, rgba(0,175,255,.6), rgba(0,40,85,.95));
    border: 1px solid rgba(93,213,255,.8);
    box-shadow: 0 0 16px rgba(0,165,255,.25);
}

.ai-city-agent-card.bubu .ai-city-agent-avatar {
    background: radial-gradient(circle, rgba(255,30,195,.58), rgba(78,0,75,.92));
    border-color: rgba(255,74,218,.8);
}

.ai-city-agent-card .agent-name { font-size: 16px; font-weight: 700; }
.ai-city-agent-card .online { margin-left: 5px; color: #38e79b; font-size: 11px; }
.ai-city-agent-card .agent-meta { margin-top: 3px; font-size: 11px; color: #a7cee4; }
.ai-city-agent-card .agent-arrow { margin-left: auto; color: #51c8ff; font-size: 24px; }

.ai-city-compass {
    position: absolute;
    right: 64px;
    bottom: 18px;
    z-index: 25;
    width: 96px;
    height: 96px;
    border: 1px solid rgba(0,155,255,.68);
    border-radius: 50%;
    background: rgba(1,18,35,.72);
    box-shadow: inset 0 0 18px rgba(0,120,255,.08), 0 0 18px rgba(0,120,255,.15);
}

.ai-city-compass::after {
    content: "";
    position: absolute;
    inset: 14px;
    border: 1px solid rgba(0,155,255,.34);
    border-radius: 50%;
}

.ai-city-compass .north,
.ai-city-compass .south,
.ai-city-compass .east,
.ai-city-compass .west {
    position: absolute;
    font-size: 11px;
    color: #9cdcff;
    z-index: 2;
}

.ai-city-compass .north { top: 5px; left: 50%; transform: translateX(-50%); }
.ai-city-compass .south { bottom: 5px; left: 50%; transform: translateX(-50%); }
.ai-city-compass .east { right: 6px; top: 50%; transform: translateY(-50%); }
.ai-city-compass .west { left: 6px; top: 50%; transform: translateY(-50%); }

.ai-city-compass .needle {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    font-size: 39px;
    color: #55cfff;
    text-shadow: 0 0 12px rgba(0,183,255,.8);
}

.ai-city-zoom {
    position: absolute;
    right: 18px;
    bottom: 19px;
    z-index: 25;
    width: 40px;
    overflow: hidden;
    border: 1px solid rgba(0,155,255,.68);
    border-radius: 11px;
    background: rgba(1,18,35,.8);
}

.ai-city-zoom button {
    width: 40px;
    height: 42px;
    border: 0;
    border-bottom: 1px solid rgba(0,155,255,.25);
    background: transparent;
    color: #bceaff;
    font-size: 24px;
    cursor: pointer;
}

.ai-city-zoom button:last-child { border-bottom: 0; }

.ai-city-back {
    position: absolute;
    top: 16px;
    right: 18px;
    z-index: 31;
    padding: 7px 12px;
    border: 1px solid rgba(0,155,255,.55);
    border-radius: 10px;
    background: rgba(2,18,34,.72);
    color: #bceaff;
    cursor: pointer;
}

.ai-city-live-badge {
    position: absolute;
    left: 245px;
    top: 113px;
    z-index: 17;
    padding: 7px 11px;
    border: 1px solid rgba(0,183,255,.42);
    border-radius: 999px;
    background: rgba(2,20,38,.55);
    color: #8bdcff;
    font-size: 10px;
    letter-spacing: .08em;
    backdrop-filter: blur(7px);
}

@media (max-width: 900px) {
    .ai-city-map-v3-top { left: 10px; right: 66px; }
    .ai-city-brand-text span,
    .ai-city-time,
    .ai-city-stats .ai-city-stat:nth-child(n+3) { display: none; }
    .ai-city-side { width: 170px; }
    .ai-city-nav-item { padding: 0 18px; gap: 10px; font-size: 13px; }
    .ai-city-bottom { left: 10px; right: 10px; bottom: 10px; overflow-x: auto; }
    .ai-city-overview { width: 47px; flex: 0 0 47px; }
    .ai-city-agent-card { width: 38px; flex: 0 0 38px; }
    .ai-city-compass { width: 72px; height: 72px; right: 62px; bottom: 105px; }
    .ai-city-zoom { right: 10px; bottom: 104px; }
    .ai-city-live-badge { left: 180px; top: 85px; }
}

@media (max-width: 620px) {
    .ai-city-brand-mark { width: 40px; font-size: 28px; }
    .ai-city-brand-text strong { font-size: 23px; }
    .ai-city-side { top: 90px; width: 58px; background: rgba(1,12,25,.78); }
    .ai-city-nav-item { justify-content: center; padding: 0; }
    .ai-city-nav-item span:not(.nav-icon) { display: none; }
    .ai-city-bottom { left: 68px; }
    .ai-city-overview { width: 47px; flex-basis: 47px; }
    .ai-city-agent-card { width: 38px; flex-basis: 38px; }
    .ai-city-map-v3-bg { background-position: 57% center; }
}


/* =========================================================
   AI CITY MAP V3 — FINAL MOBILE LAYOUT
   ========================================================= */

/* Hilangkan panel bawah lama yang masih menampilkan Bubu */
.ai-city-bottom {
    display: none !important;
}

/* TOP AREA */
.ai-city-map-v3-top {
    position: absolute !important;
    top: 18px !important;
    left: 18px !important;
    right: 18px !important;
    height: 105px !important;
    z-index: 30 !important;
    display: block !important;
    pointer-events: none !important;
}

/* Logo tetap di kiri */
.ai-city-brand {
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
}

/* Buildings + Activity */
.ai-city-stats {
    position: absolute !important;
    top: 18px !important;
    right: 82px !important;
    width: 500px !important;
    height: 64px !important;
    display: flex !important;
    transform: none !important;
    overflow: hidden !important;
    border-radius: 15px !important;
}

.ai-city-stats .ai-city-stat {
    box-sizing: border-box !important;
    width: 100px !important;
    min-width: 100px !important;
    height: 64px !important;
    padding: 5px 4px !important;
}

.ai-city-stats .ai-city-stat-icon {
    font-size: 16px !important;
}

.ai-city-stats .ai-city-stat span {
    font-size: 10px !important;
    margin-top: 2px !important;
}

.ai-city-stats .ai-city-stat strong {
    font-size: 15px !important;
    margin-top: 1px !important;
}

/* ← City */
.ai-city-back {
    top: 18px !important;
    right: 18px !important;
    z-index: 35 !important;
    padding: 6px 10px !important;
    font-size: 14px !important;
}

/* Live badge — jangan lagi turun ke tengah peta */
.ai-city-live-badge {
    left: 50% !important;
    top: 112px !important;
    transform: translateX(-50%) !important;
    z-index: 24 !important;
    white-space: nowrap !important;
}

/* CITIZENS + AGENTS */
.ai-city-bottom-stats {
    position: absolute !important;
    left: 18px !important;
    bottom: 24px !important;
    z-index: 28 !important;
    display: flex !important;
    gap: 10px !important;
}

.ai-city-bottom-stats .ai-city-stat {
    display: block !important;
    box-sizing: border-box !important;
    width: 105px !important;
    min-width: 105px !important;
    height: 76px !important;
    padding: 8px 10px !important;
    margin: 0 !important;
    border: 1px solid rgba(0,155,255,.55) !important;
    border-radius: 12px !important;
    background: rgba(3,21,40,.90) !important;
    text-align: center !important;
}

.ai-city-bottom-stats .ai-city-stat-icon {
    display: block !important;
    font-size: 19px !important;
    line-height: 1 !important;
}

.ai-city-bottom-stats .ai-city-stat span {
    display: block !important;
    margin-top: 3px !important;
    font-size: 10px !important;
}

.ai-city-bottom-stats .ai-city-stat strong {
    display: block !important;
    margin-top: 1px !important;
    font-size: 16px !important;
}

/* Jangan biarkan landscape compact rules mengecilkan kartu bawah */
@media (orientation: landscape) and (max-height: 600px) {
    .ai-city-bottom-stats .ai-city-stat {
        min-width: 105px !important;
        width: 105px !important;
        height: 76px !important;
        padding: 8px 10px !important;
    }
}

/* MOBILE PORTRAIT */
@media (max-width: 620px) {
    .ai-city-map-v3-top {
        top: 14px !important;
        left: 12px !important;
        right: 12px !important;
        height: 100px !important;
    }

    .ai-city-brand {
        left: 0 !important;
        top: 4px !important;
    }

    .ai-city-stats {
        top: 14px !important;
        right: 64px !important;
        width: 216px !important;
        height: 70px !important;
    }

    .ai-city-stats .ai-city-stat {
        width: 108px !important;
        min-width: 108px !important;
        height: 70px !important;
        padding: 6px 6px !important;
    }

    .ai-city-stats .ai-city-stat-icon {
        font-size: 17px !important;
    }

    .ai-city-stats .ai-city-stat span {
        font-size: 10px !important;
    }

    .ai-city-stats .ai-city-stat strong {
        font-size: 15px !important;
    }

    .ai-city-back {
        top: 14px !important;
        right: 8px !important;
        padding: 6px 9px !important;
    }

    .ai-city-live-badge {
        top: 104px !important;
        font-size: 12px !important;
        padding: 7px 11px !important;
    }

    .ai-city-bottom-stats {
        left: 12px !important;
        bottom: 18px !important;
        gap: 8px !important;
    }

    .ai-city-bottom-stats .ai-city-stat {
        width: 96px !important;
        min-width: 96px !important;
        height: 70px !important;
        padding: 7px 8px !important;
    }

    .ai-city-bottom-stats .ai-city-stat-icon {
        font-size: 16px !important;
    }

    .ai-city-bottom-stats .ai-city-stat span {
        font-size: 9px !important;
    }

    .ai-city-bottom-stats .ai-city-stat strong {
        font-size: 15px !important;
    }
}

</style>
</head>

<body>

<header>

<h1>
    <img
        src="/static/ai_city_profile.png"
        alt="AI CITY"
        class="city-profile-icon"
    >
    AI CITY
</h1>

<div class="status">
● CITY ONLINE
</div>

</header>

<button class="menu-button" onclick="openCityMenu()" aria-label="Open menu">
    ☰
</button>

<div id="cityMenuOverlay" class="city-menu-overlay" onclick="closeCityMenu(event)">

    <aside class="city-menu">

        <div class="city-menu-header">
            <div>
                <div class="city-menu-title">AI CITY</div>
                <div class="city-menu-subtitle">City Menu</div>
            </div>

            <button class="menu-close" onclick="closeCityMenu()">
                ✕
            </button>
        </div>

        <div class="city-menu-links">
<a href="#" onclick="return openCityMap(event)">
                <span>🗺️</span>
                <span>AI CITY Map</span>
            </a>

            

            <a href="#" onclick="return menuComingSoon(event, 'Registrasi')">
                <span>📝</span>
                <span>Registrasi</span>
            </a>

            <a href="/static/whitepaper.html">
                <span>📄</span>
                <span>Whitepaper</span>
            </a>

            <a href="#" onclick="return menuComingSoon(event, 'Komunitas X')">
                <span>𝕏</span>
                <span>Komunitas</span>
            </a>

            <a href="#" onclick="return menuComingSoon(event, 'Peraturan Pengguna')">
                <span>📜</span>
                <span>Peraturan Pengguna</span>
            </a>

        </div>

        <div class="city-menu-footer">
            AI CITY · Genesis
        </div>

    </aside>

</div>

<section class="hero-section">

    <div class="hero-badge">
        ● AI CITY ONLINE
    </div>

    <h2>A Virtual City<br><span>Built by AI</span></h2>

    <p class="hero-description">
        AI CITY adalah dunia virtual yang dihuni oleh agen-agen AI
        dengan identitas, memory, pengalaman, hubungan, dan kehidupan
        digital mereka sendiri.
    </p>

    <div class="hero-actions">
        <a href="#city" class="hero-button primary">
            Explore AI CITY
        </a>

        <a href="#how-it-works" class="hero-button secondary">
            How It Works
        </a>
    </div>

</section>

<nav class="navbar">
    <a href="/">🏠 City</a>
    <a href="#citizens">👥 Citizens</a>
    <a href="#chat">💬 Chat</a>
    <a href="#activity">📡 Activity</a>
    <a href="#knowledge">🧠 Knowledge</a>
</nav>

<div class="city">

<div class="road horizontal"></div>
<div class="road vertical"></div>


<div class="building aion">

<div class="icon">🤖</div>

<h2>Dudu</h2>

<p>Agent-001</p>

<p>● Active</p>

</div>


<div class="building nova">

<div class="icon">🤖</div>

<h2>Bubu</h2>

<p>Agent-002</p>

<p>● Active</p>

</div>


<div class="building core">

<div class="icon">🏛️</div>

<h2>City Core</h2>

<p>Constitution V{{ constitution_version }}</p>

<p>Genesis</p>

</div>


<div class="building knowledge">

<div class="icon">🧠</div>

<h2>Knowledge Center</h2>

<p>{{ knowledge|length }} shared knowledge</p>

</div>


<div class="building hub">

<div class="icon">💬</div>

<h2>City Hub</h2>

<p>{{ messages|length }} messages</p>

</div>

</div>


<div id="aiCityMapPanel" style="display:none;">
<div class="ai-city-map-v3">

    <div class="ai-city-map-v3-bg"></div>
    <div class="ai-city-map-v3-vignette"></div>

    <div class="ai-city-map-v3-top">
        <div class="ai-city-brand">
            <div class="ai-city-brand-mark">▥</div>
            <div class="ai-city-brand-text">
                <strong>AI CITY</strong>
                <span>Small Steps, Big Future</span>
            </div>
        </div>

        <div class="ai-city-time">
            <div class="sun">☀️</div>
            <div>
                <small>Daytime</small>
                <strong id="aiCityClock">14:27</strong>
            </div>
            <em id="aiCityDate">2026-09-17</em>
        </div>

        <div class="ai-city-stats">

            <div class="ai-city-stat">
                <span class="ai-city-stat-icon">♟</span>
                <span>Citizens</span>
                <strong>{{ citizens|length }}</strong>
            </div>

            <div class="ai-city-stat">
                <span class="ai-city-stat-icon">🤖</span>
                <span>Agents</span>
                <strong>{{ agents|length }}</strong>
            </div>

            <div class="ai-city-stat">
                <span class="ai-city-stat-icon">◈</span>
                <span>Districts</span>
                <strong>{{ physical.district_count }}</strong>
            </div>

            <div class="ai-city-stat">
                <span class="ai-city-stat-icon">🏛</span>
                <span>Buildings</span>
                <strong>{{ physical.building_count }}</strong>
            </div>

            <div class="ai-city-stat">
                <span class="ai-city-stat-icon">↗</span>
                <span>Activity</span>
                <strong>{{ activities|length }}</strong>
            </div>
        </div>
    </div>

    
    <button class="ai-city-back" onclick="closeCityMap()">← City</button>

    <aside class="ai-city-side">
        <a class="ai-city-nav-item active" href="#" onclick="return false;">
            <span class="nav-icon">⌖</span><span>AI CITY Map</span>
        </a>
        <a class="ai-city-nav-item" href="#citizens" onclick="closeCityMap();">
            <span class="nav-icon">♟</span><span>Citizens</span>
        </a>
        <a class="ai-city-nav-item" href="#agents" onclick="closeCityMap();">
            <span class="nav-icon">🤖</span><span>Agents</span>
        </a>
        <a class="ai-city-nav-item" href="#city-hall" onclick="closeCityMap();">
            <span class="nav-icon">🏛</span><span>City Hall</span>
        </a>
        <a class="ai-city-nav-item" href="#activity" onclick="closeCityMap();">
            <span class="nav-icon">↗</span><span>City Activity</span>
        </a>
        <a class="ai-city-nav-item" href="#" onclick="return false;">
            <span class="nav-icon">⚙</span><span>Settings</span>
        </a>
    

        
    

    </aside>

    
    <div class="ai-city-bottom-stats">
        <div class="ai-city-stat">
                <span class="ai-city-stat-icon">♟</span>
                <span>Citizens</span>
                <strong>{{ citizens|length }}</strong>
            </div>
        <div class="ai-city-stat">
                <span class="ai-city-stat-icon">🤖</span>
                <span>Agents</span>
                <strong>{{ agents|length }}</strong>
            </div>
    </div>

<div class="ai-city-live-badge">● LIVE CITY ENVIRONMENT</div>



    <div class="ai-city-compass">
        <span class="north">N</span>
        <span class="south">S</span>
        <span class="east">E</span>
        <span class="west">W</span>
        <div class="needle">▲</div>
    </div>

    <div class="ai-city-zoom">
        <button type="button" onclick="aiCityMapZoom(1)">+</button>
        <button type="button" onclick="aiCityMapZoom(-1)">−</button>
    </div>

</div>
</div>

<div class="hub-box">
<div class="building" style="position:relative; width:100%;">

<h2 id="map">🗺️ AI CITY Map V1</h2>

<div class="ai-city-map">

<div class="ai-city-map-grid"></div>

<div class="ai-city-map-title">
<h2>AI CITY — LIVE CITY MAP</h2>
<p>
{{ physical.district_count }} district ·
{{ physical.building_count }} building ·
{{ physical.location_count }} citizen locations
</p>
</div>

{% for district in physical.districts %}

<div class="ai-city-map-district">

<div class="ai-city-map-road horizontal"></div>
<div class="ai-city-map-road vertical"></div>

<div class="ai-city-map-node city-hall">
🏛️
<strong>City Hall</strong>
<small>{{ district.name }}</small>
</div>

<div class="ai-city-map-node center">
🌐
<strong>City Center</strong>
<small>{{ district.status|upper }}</small>
</div>

{% for location in physical.locations %}

{% if location.district_id == district.id %}

{% if location.citizen_name == "Dudu" %}

<div class="ai-city-map-citizen dudu">
🤖 Dudu · {{ location.status }}
</div>

{% elif location.citizen_name == "Bubu" %}

<div class="ai-city-map-citizen bubu">
🤖 Bubu · {{ location.status }}
</div>

{% endif %}

{% endif %}

{% endfor %}

</div>

{% endfor %}

<div class="ai-city-map-legend">
<span>🏛️ Civic building</span>
<span>🤖 Citizen</span>
<span class="ai-city-map-live">● LIVE CITY DATA</span>
</div>

</div>

</div>
</div>


</div>

<div class="hub-box">

<div class="building" style="position:relative; width:100%;">

<h2 id="citizens">👥 Citizen Status</h2>

<div class="citizens-grid">

{% for name, agent in agents.items() %}

<div class="citizen-status-card">

    <img src="/static/ai_city_profile.png" alt="AI CITY" class="citizen-icon-image">

    <h2>{{ name }}</h2>

    <p class="citizen-id">
        {% for citizen in citizens %}
            {% if citizen.name == name %}
                {{ citizen.id|replace("agent-", "Agent-") }}
            {% endif %}
        {% endfor %}
    </p>

    <p class="citizen-active">● {{ agent.status|upper }}</p>

    <div class="citizen-stat">
        💬 <span>{{ agent.memory.conversations }}</span> conversations
    </div>

    <div class="citizen-stat">
        🧠 <span>{{ agent.memory.knowledge }}</span> knowledge
    </div>

    <div class="citizen-stat">
        ⭐ <span>{{ agent.memory.experiences }}</span> experiences
    </div>

    <div class="citizen-stat">
        🤝 <span>{{ agent.memory.relationships }}</span> relationships
    </div>

</div>

{% endfor %}

</div>

</div>

</div>

<div class="hub-box">

<div class="building" style="position:relative; width:100%;">

<h2>🤖 Autonomous Life</h2>

<div class="citizen-stat">
    ⚡ Status:
    <span>{{ autonomous.status|upper }}</span>
</div>

<div class="citizen-stat">
    🔄 Cycles:
    <span>{{ autonomous.cycles }}</span>
</div>

<div class="citizen-stat">
    🧠 Dudu Cycle:
    <span>{{ autonomous.dudu_cycle_status|upper }}</span>
</div>

{% if autonomous.last_execution %}

<div class="citizen-stat">
    🎯 Last Action:
    <span>{{ autonomous.last_execution.action }}</span>
</div>

<div class="citizen-stat">
    🛡️ Execution:
    <span>{{ autonomous.last_execution.status }}</span>
</div>

<div class="citizen-stat">
    ▶️ Executed:
    <span>{{ "YES" if autonomous.last_execution.executed else "NO" }}</span>
</div>

{% else %}

<div class="citizen-stat">
    🎯 Last Action:
    <span>None</span>
</div>

{% endif %}

</div>

</div>

<div class="hub-box">

<div class="building" style="position:relative; width:100%;">

<h2 id="activity">📡 City Activity</h2>

{% if messages %}

    {% for message in messages[-5:]|reverse %}

        <div class="message">

            <div class="sender">
                🔔 {{ message.sender }} → {{ message.receiver }}
            </div>

            <div class="time">
                {{ message.timestamp }}
            </div>

        </div>

    {% endfor %}

{% else %}

    <p class="empty">
        Belum ada aktivitas kota.
    </p>

{% endif %}

</div>

</div><div class="hub-box">

<div class="building" style="position:relative; width:100%;">

<details class="city-hub-details">

<summary id="chat">
    💬 City Hub — Communication
    <span class="hub-message-count">
        {{ messages|length }} messages
    </span>
</summary>

<div class="city-hub-history">

{% if messages %}

    {% for message in messages %}

    <div class="message">

        <div class="sender">
            🤖 {{ message.sender }}
            → {{ message.receiver }}
        </div>

        <div>
            {{ message.message }}
        </div>

        <div class="time">
            {{ message.timestamp }}
        </div>

    </div>

    {% endfor %}

{% else %}

    <p class="empty">
        Belum ada komunikasi antar-agent.
    </p>

{% endif %}

</div>

</details>

</div>

</div>

<section id="city" class="city-status-section">

    <div class="section-label">
        CITY STATUS
    </div>

    <div class="city-status-grid">

        <div class="status-item">
            <div class="status-value">
                {{ citizens|length }}
            </div>
            <div class="status-label">
                Citizens
            </div>
        </div>

        <div class="status-item">
            <div class="status-value">
                {{ physical.get("district_count", 0) }}
            </div>
            <div class="status-label">
                Districts
            </div>
        </div>

        <div class="status-item">
            <div class="status-value">
                {{ physical.get("building_count", 0) }}
            </div>
            <div class="status-label">
                Buildings
            </div>
        </div>

        <div class="status-item">
            <div class="status-value">
                {{ messages|length }}
            </div>
            <div class="status-label">
                Communications
            </div>
        </div>

    </div>

</section>


<div class="live-state-panel">
    <div class="section-label">
        LIVE CITY STATE
    </div>

    <div class="live-state-grid">

        <div class="live-state-item">
            <span class="live-state-icon">🟢</span>
            <div>
                <strong>{{ city_state.get("simulation_status", "offline")|upper }}</strong>
                <small>Simulation</small>
            </div>
        </div>

        <div class="live-state-item">
            <span class="live-state-icon">🤖</span>
            <div>
                <strong>{{ city_state.get("citizens", [])|length }}</strong>
                <small>Active Citizens</small>
            </div>
        </div>

        <div class="live-state-item">
            <span class="live-state-icon">📍</span>
            <div>
                <strong>{{ city_state.get("locations", [])|length }}</strong>
                <small>Locations</small>
            </div>
        </div>

        <div class="live-state-item">
            <span class="live-state-icon">⚡</span>
            <div>
                <strong>{{ city_state.get("recent_activities", [])|length }}</strong>
                <small>Recent Activities</small>
            </div>
        </div>

    </div>
</div>

<section class="physical-city-panel">
    <h2>🏙️ Physical City</h2>

    <div class="physical-stats">
        🏘️ {{ physical.get("district_count", 0) }} Districts
        &nbsp; • &nbsp;
        🏛️ {{ physical.get("building_count", 0) }} Buildings
        &nbsp; • &nbsp;
        📍 {{ physical.get("location_count", 0) }} Locations
    </div>

    {% for district in physical.get("districts", []) %}
    <div class="physical-district">

        <h3>🏘️ {{ district.get("name") }}</h3>

        {% for building in district.get("buildings", []) %}
        <div class="physical-building">

            <strong>
                🏛️ {{ building.get("name") }}
            </strong>

            <div class="physical-empty">
                {{ building.get("purpose", "") }}
            </div>

            <div class="physical-occupants">
                {% for location in physical.get("locations", []) %}
                    {% if location.get("building_id") == building.get("id") %}
                        <span class="physical-citizen">
                            🤖 {{ location.get("citizen_name") }}
                        </span>
                    {% endif %}
                {% endfor %}
            </div>

        </div>
        {% endfor %}

        {% for location in physical.get("locations", []) %}
            {% if location.get("district_id") == district.get("id")
                  and not location.get("building_id") %}

                <div class="physical-building">
                    <strong>📍 {{ location.get("citizen_name") }}</strong>
                    <div class="physical-empty">
                        Berada di district, belum menempati building.
                    </div>
                </div>

            {% endif %}
        {% endfor %}

    </div>
    {% endfor %}
</section>


<script>
function openCityMenu() {
    const menu = document.getElementById("cityMenuOverlay");
    if (menu) {
        menu.classList.add("open");
    }
}

function closeCityMenu(event) {
    if (event && event.target !== event.currentTarget) {
        return;
    }

    const menu = document.getElementById("cityMenuOverlay");
    if (menu) {
        menu.classList.remove("open");
    }
}

function openCityMap(event) {
    event.preventDefault();

    const panel = document.getElementById("aiCityMapPanel");

    if (panel) {
        panel.style.display = "block";
        panel.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

    closeCityMenu();

    return false;
}


function aiCityMapZoom(direction) {
    const bg = document.querySelector(".ai-city-map-v3-bg");
    if (!bg) return;

    const current = parseFloat(bg.dataset.zoom || "1.035");
    const next = Math.max(1.035, Math.min(1.22, current + direction * 0.035));
    bg.dataset.zoom = String(next);
    bg.style.transform = `scale(${next})`;
}

function closeCityMap() {
    const panel = document.getElementById("aiCityMapPanel");
    if (panel) {
        panel.style.display = "none";
    }
}

function menuComingSoon(event, name) {
    event.preventDefault();

    alert(name + " akan tersedia pada tahap berikutnya.");

    closeCityMenu();

    return false;
}

document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        closeCityMenu();
    }
});
</script>

</body>
</html>
"""


CITIZEN_HTML = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{{ citizen.name }} — AI CITY</title>

<style>

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #050816;
    color: white;
    text-align: center;
}

.container {
    max-width: 700px;
    margin: auto;
    padding: 30px 20px;
}

.profile {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 30px;
    margin-top: 20px;
}

.icon {
    font-size: 70px;
}

.status {
    color: #55ff99;
    font-weight: bold;
}

.stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 25px;
}

.stat {
    background: rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 18px;
}

.number {
    font-size: 28px;
    font-weight: bold;
}

.label {
    opacity: 0.7;
    margin-top: 5px;
}

.back {
    display: inline-block;
    margin-top: 25px;
    padding: 10px 18px;
    border-radius: 10px;
    background: rgba(255,255,255,0.1);
    color: white;
    text-decoration: none;
}


/* AI CITY MAP V3 - FORCE COMPACT CITY OVERVIEW + AGENTS */
@media (orientation: landscape) and (max-height: 600px) {

    .ai-city-overview {
        width: 120px !important;
        flex: 0 0 120px !important;
        min-width: 120px !important;
        padding: 4px 5px !important;
        box-sizing: border-box !important;
    }

    .ai-city-overview-grid {
        gap: 2px !important;
    }

    .ai-city-overview-grid > div {
        padding: 2px !important;
    }

    .ai-city-overview small {
        font-size: 5px !important;
    }

    .ai-city-overview strong {
        font-size: 8px !important;
        margin-top: 1px !important;
    }

    .ai-city-agent-cards {
        gap: 3px !important;
    }

    .ai-city-agent-card {
        width: 100px !important;
        flex: 0 0 100px !important;
        min-width: 100px !important;
        padding: 4px 5px !important;
        gap: 4px !important;
        box-sizing: border-box !important;
    }

    .ai-city-agent-avatar {
        width: 20px !important;
        height: 20px !important;
        min-width: 20px !important;
        font-size: 11px !important;
    }

    .ai-city-agent-card .agent-name {
        font-size: 8px !important;
    }

    .ai-city-agent-card .online {
        font-size: 5px !important;
    }

    .ai-city-agent-card .agent-meta {
        font-size: 5px !important;
        margin-top: 1px !important;
    }

    .ai-city-agent-card .agent-arrow {
        font-size: 11px !important;
    }
}


/* AI CITY MAP V3 - PORTRAIT FULL SIZE TEST */



/* PORTRAIT — ULTRA SHORT HORIZONTAL */
@media (orientation: portrait) {

    .ai-city-bottom {
        left: 3px !important;
        right: 3px !important;
        bottom: 3px !important;
        gap: 3px !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        padding: 0 !important;
    }

    /* CITY OVERVIEW */
    .ai-city-overview {
        width: 150px !important;
        min-width: 150px !important;
        flex: 0 0 150px !important;
        height: 16px !important;
        min-height: 16px !important;
        padding: 1px 4px !important;
        border-radius: 4px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }

    .ai-city-panel-title {
        font-size: 6px !important;
        line-height: 13px !important;
        gap: 2px !important;
        white-space: nowrap !important;
    }

    .ai-city-panel-title .panel-icon {
        font-size: 7px !important;
    }

    .ai-city-divider,
    .ai-city-overview-grid {
        display: none !important;
    }

    /* DUDU + BUBU */
    .ai-city-agent-cards {
        display: flex !important;
        gap: 3px !important;
        flex: 0 0 auto !important;
    }

    .ai-city-agent-card {
        width: 130px !important;
        min-width: 130px !important;
        flex: 0 0 130px !important;
        height: 16px !important;
        min-height: 16px !important;
        padding: 1px 3px !important;
        gap: 3px !important;
        border-radius: 4px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }

    .ai-city-agent-avatar {
        width: 12px !important;
        height: 12px !important;
        min-width: 12px !important;
        flex: 0 0 12px !important;
        font-size: 7px !important;
    }

    .ai-city-agent-card .agent-name {
        font-size: 6px !important;
        line-height: 14px !important;
        white-space: nowrap !important;
    }

    .ai-city-agent-card .online {
        font-size: 4px !important;
        margin-left: 1px !important;
        white-space: nowrap !important;
    }

    .ai-city-agent-card .agent-meta {
        display: none !important;
    }

    .ai-city-agent-card .agent-arrow {
        display: none !important;
    }
}



/* PORTRAIT — OPTION C: BOTTOM OF SIDEBAR */
@media (orientation: portrait) {
    .ai-city-bottom {
        position: absolute !important;

        /*
         * Sidebar portrait berada di sisi kiri.
         * Panel ditempatkan di bawah area sidebar.
         */
        left: 68px !important;
        right: 5px !important;
        bottom: 5px !important;

        display: flex !important;
        align-items: flex-end !important;
        gap: 8px !important;

        overflow-x: auto !important;
        overflow-y: hidden !important;

        flex-wrap: nowrap !important;

        z-index: 30 !important;
    }
}



/* PORTRAIT — OPTION B: BOTTOM STRIP */
@media (orientation: portrait) {
    .ai-city-bottom {
        position: absolute !important;

        left: 68px !important;
        right: 0 !important;
        bottom: 4px !important;

        display: flex !important;
        align-items: flex-end !important;
        gap: 8px !important;

        flex-wrap: nowrap !important;

        overflow-x: auto !important;
        overflow-y: hidden !important;

        width: auto !important;

        z-index: 30 !important;

        padding: 0 8px 2px 4px !important;
        box-sizing: border-box !important;

        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
    }

    .ai-city-agent-cards {
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
        flex: 0 0 auto !important;
    }

    .ai-city-overview,
    .ai-city-agent-card {
        flex-shrink: 0 !important;
    }
}



/* AI CITY MAP V3 - SIDEBAR STATUS PANELS */
.ai-city-menu-panels {
    margin-top: 18px;
    padding-top: 14px;
    border-top: 1px solid rgba(0,154,255,.35);
}

.ai-city-menu-panel-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    color: rgba(120,205,255,.75);
    margin: 0 4px 10px;
}

.ai-city-menu-panels .ai-city-overview {
    position: relative;
    width: auto;
    padding: 12px;
    margin: 0 0 10px;
    border: 1px solid rgba(0,154,255,.55);
    background: rgba(2,17,32,.78);
    box-shadow:
        inset 0 0 20px rgba(0,110,255,.06),
        0 0 16px rgba(0,80,180,.10);
    backdrop-filter: blur(8px);
    border-radius: 12px;
}

.ai-city-menu-panels .ai-city-panel-title {
    font-size: 11px;
    letter-spacing: 1px;
}

.ai-city-menu-panels .ai-city-overview-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 10px;
}

.ai-city-menu-panels .ai-city-overview-grid div {
    min-width: 0;
}

.ai-city-menu-panels .ai-city-overview-grid small {
    display: block;
    font-size: 8px;
    color: rgba(180,220,245,.60);
}

.ai-city-menu-panels .ai-city-overview-grid strong {
    display: block;
    margin-top: 2px;
    font-size: 12px;
    color: #d9f4ff;
}

.ai-city-menu-panels .ai-city-agent-cards {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.ai-city-menu-panels .ai-city-agent-card {
    position: relative;
    width: auto;
    min-width: 0;
    padding: 10px;
    border: 1px solid rgba(0,154,255,.55);
    background: rgba(2,17,32,.78);
    box-shadow:
        inset 0 0 18px rgba(0,110,255,.05),
        0 0 14px rgba(0,80,180,.08);
    backdrop-filter: blur(8px);
    border-radius: 12px;
}

.ai-city-menu-panels .ai-city-agent-avatar {
    flex: 0 0 auto;
}

.ai-city-menu-panels .agent-name {
    font-size: 12px;
}

.ai-city-menu-panels .agent-meta {
    font-size: 9px;
}

.ai-city-menu-panels .agent-arrow {
    font-size: 18px;
}





/* AI CITY MAP V3 - CITIZENS + AGENTS BOTTOM */
.ai-city-bottom-stats {
    position: absolute;
    left: 245px;
    bottom: 18px;
    z-index: 24;
    display: flex;
    gap: 10px;
}

.ai-city-bottom-stats .ai-city-stat {
    display: block;
    box-sizing: border-box;
    width: 110px;
    min-width: 110px;
    height: 78px;
    padding: 10px 12px;
    margin: 0;
    border: 1px solid rgba(0,155,255,.55);
    border-radius: 12px;
    background: rgba(3,21,40,.88);
    box-shadow: inset 0 0 20px rgba(0,120,255,.07), 0 0 18px rgba(0,100,255,.10);
    backdrop-filter: blur(10px);
    text-align: center;
}

.ai-city-bottom-stats .ai-city-stat-icon {
    display: block;
    font-size: 21px;
    line-height: 1;
}

.ai-city-bottom-stats .ai-city-stat span {
    display: block;
    margin-top: 3px;
    font-size: 11px;
}

.ai-city-bottom-stats .ai-city-stat strong {
    display: block;
    margin-top: 1px;
    font-size: 17px;
}

</style>

</head>

<body>

<div class="container">

<h1>AI CITY</h1>

<div class="profile">

<div class="icon">🤖</div>

<h1>{{ citizen.name }}</h1>

<p>{{ citizen.id }}</p>

<p>{{ citizen.role }}</p>

<p class="status">● {{ agent_status.status|upper }}</p>

<div class="stats">

<div class="stat">
<div class="number">{{ agent_status.memory.conversations }}</div>
<div class="label">💬 Conversations</div>
</div>

<div class="stat">
<div class="number">{{ agent_status.memory.knowledge }}</div>
<div class="label">🧠 Knowledge</div>
</div>

<div class="stat">
<div class="number">{{ agent_status.memory.experiences }}</div>
<div class="label">⭐ Experiences</div>
</div>

<div class="stat">
<div class="number">{{ agent_status.memory.relationships }}</div>
<div class="label">🤝 Relationships</div>
</div>

</div>

</div>

<a class="back" href="/">← Kembali ke AI CITY</a>

</div>

</body>
</html>
"""


def load_city_activity():
    try:
        with open("city_activity.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("activities", [])
    except Exception:
        return []


@app.route("/")
def home():

    context = get_city_context()
    city_state = load_city_state()

    chat = load_chat()

    messages = chat.get("messages", [])
    activities = load_city_activity()
    physical = context.get("physical", {})

    return render_template_string(
        HTML,
        constitution_version=context["constitution_version"],
        citizens=context["citizens"],
        agents=context["agents"],
        knowledge=context["shared_knowledge"],
        messages=messages[-10:],
        activities=activities,
        physical=physical,
        city_state=city_state,
        autonomous=context["autonomous"]
    )



@app.route("/citizen/<agent_name>")
def citizen_profile(agent_name):

    context = get_city_context()

    agent = None

    for citizen in context["citizens"]:
        if citizen["name"].upper() == agent_name.upper():
            agent = citizen
            break

    if agent is None:
        return "Citizen tidak ditemukan", 404

    agent_status = context["agents"].get(agent["name"])

    return render_template_string(
        CITIZEN_HTML,
        citizen=agent,
        agent_status=agent_status,
        city=context["city"]
    )


@app.route("/api/city")
def city_api():

    return jsonify(get_city_context())


@app.route("/api/chat")
def chat_api():

    chat = load_chat()

    return jsonify(chat)


if __name__ == "__main__":

    print()
    print("=" * 50)
    print("AI CITY V3")
    print("=" * 50)
    print("Virtual City + City Hub")
    print("http://127.0.0.1:5000")
    print("=" * 50)
    print()

    app.run(
        host="127.0.0.1",
        port=5000
    )
