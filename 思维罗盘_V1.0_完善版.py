import random
import math
import time
import os
import sqlite3
import json
import csv
import io
from datetime import datetime
from collections import Counter
from html import escape

import streamlit as st
import plotly.graph_objects as go


# =========================================================
# App
# =========================================================
APP_TITLE = "思维罗盘｜大学生高阶思维能力测评与成长管理系统"
APP_SUBTITLE = "看见你的思维优势，找到下一步成长方向"
AI_REPORT_VERSION = 4

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    /* ---------- Global ---------- */
    :root {
        --ink: #192033;
        --sub: #687086;
        --purple: #6C63FF;
        --purple2: #8D7CFF;
        --blue: #4C8DFF;
        --cyan: #4BC8D9;
        --bg: #F7F8FC;
        --card: rgba(255,255,255,.92);
        --line: rgba(31,39,66,.10);
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(108,99,255,.10), transparent 26rem),
            radial-gradient(circle at 95% 5%, rgba(76,141,255,.09), transparent 25rem),
            linear-gradient(180deg, #FBFCFF 0%, #F7F8FC 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2.2rem;
        padding-bottom: 3.5rem;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    /* ---------- Hero ---------- */
    .brand-pill {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .38rem .72rem;
        border-radius: 999px;
        background: rgba(108,99,255,.10);
        border: 1px solid rgba(108,99,255,.14);
        color: #5C54DE;
        font-weight: 700;
        font-size: .88rem;
        margin-bottom: 1rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.4rem 2.55rem;
        border-radius: 28px;
        background:
            linear-gradient(135deg, rgba(255,255,255,.98), rgba(248,249,255,.94));
        border: 1px solid rgba(108,99,255,.12);
        box-shadow: 0 18px 55px rgba(39,48,87,.08);
        margin-bottom: 1.25rem;
    }

    .hero::after {
        content: "✦";
        position: absolute;
        right: 2.2rem;
        top: 1.2rem;
        font-size: 7rem;
        color: rgba(108,99,255,.08);
        transform: rotate(12deg);
    }

    .hero-title {
        font-size: clamp(2.15rem, 4vw, 3.8rem);
        line-height: 1.07;
        margin: 0 0 .9rem 0;
        font-weight: 850;
        color: #171D31;
    }

    .hero-gradient {
        background: linear-gradient(90deg, #6C63FF, #4C8DFF, #4BC8D9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        line-height: 1.85;
        color: #687086;
        max-width: 760px;
        margin-bottom: 0;
    }

    /* ---------- Small feature cards ---------- */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: .85rem;
        margin: 1.15rem 0 1.3rem;
    }

    .feature-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(38,46,80,.04);
    }

    .feature-icon {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(108,99,255,.15), rgba(76,141,255,.10));
        font-size: 1.2rem;
        margin-bottom: .65rem;
    }

    .feature-value {
        font-size: 1.23rem;
        font-weight: 800;
        color: #1D2439;
        margin-bottom: .08rem;
    }

    .feature-label {
        color: #7A8195;
        font-size: .91rem;
    }

    /* ---------- Intro / tips ---------- */
    .soft-panel {
        background: rgba(255,255,255,.82);
        border: 1px solid rgba(31,39,66,.08);
        border-radius: 18px;
        padding: 1.05rem 1.15rem;
        margin: .85rem 0 1.1rem;
    }

    .soft-panel strong {
        color: #3F47A7;
    }

    /* ---------- Survey ---------- */
    .survey-top {
        background: rgba(255,255,255,.88);
        border: 1px solid rgba(31,39,66,.08);
        border-radius: 20px;
        padding: 1.15rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 26px rgba(38,46,80,.04);
    }

    .survey-title {
        font-size: 1.65rem;
        font-weight: 820;
        margin-bottom: .18rem;
    }

    .survey-meta {
        color: #7A8195;
        font-size: .93rem;
    }

    .q-card {
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 20px;
        padding: 1.2rem 1.3rem .7rem 1.3rem;
        margin: .85rem 0;
        box-shadow: 0 7px 20px rgba(38,46,80,.035);
    }

    .q-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 34px;
        height: 34px;
        padding: 0 .55rem;
        border-radius: 11px;
        background: linear-gradient(135deg, #7168FF, #5B8EFF);
        color: white;
        font-weight: 800;
        font-size: .88rem;
        margin-right: .55rem;
    }

    .q-text {
        display: inline;
        font-size: 1.04rem;
        line-height: 1.78;
        font-weight: 650;
        color: #222A3F;
    }

    div[role="radiogroup"] {
        gap: .2rem;
    }

    div[data-testid="stRadio"] label {
        padding: .28rem .15rem;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stDownloadButton > button {
        border-radius: 14px !important;
        min-height: 2.9rem;
        font-weight: 750 !important;
        border: 1px solid rgba(108,99,255,.16) !important;
        transition: .18s ease !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6C63FF, #5C8DFF) !important;
        color: white !important;
        border: 0 !important;
        box-shadow: 0 9px 24px rgba(108,99,255,.22) !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
    }

    /* ---------- Results ---------- */
    .result-hero {
        padding: 1.85rem 2rem;
        border-radius: 25px;
        background: linear-gradient(135deg, #222946, #343D70 60%, #535CC3);
        color: white;
        box-shadow: 0 18px 50px rgba(30,36,74,.18);
        margin-bottom: 1.15rem;
    }

    .result-hero .eyebrow {
        opacity: .76;
        font-size: .88rem;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: .45rem;
    }

    .result-hero .title {
        font-size: 2rem;
        font-weight: 850;
        margin-bottom: .25rem;
    }

    .result-hero .desc {
        opacity: .82;
        line-height: 1.7;
    }

    .score-box {
        background: rgba(255,255,255,.95);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 22px;
        text-align: center;
        padding: 1.35rem 1.1rem;
        min-height: 178px;
        box-shadow: 0 10px 32px rgba(38,46,80,.055);
    }

    .score-label {
        color: #7A8195;
        font-size: .9rem;
    }

    .score-number {
        font-size: 3.15rem;
        font-weight: 900;
        line-height: 1.06;
        margin: .3rem 0 .2rem;
        background: linear-gradient(90deg, #6C63FF, #4C8DFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .score-level {
        display: inline-flex;
        padding: .28rem .7rem;
        border-radius: 999px;
        background: rgba(108,99,255,.10);
        color: #5B54D7;
        font-size: .87rem;
        font-weight: 780;
    }

    .mini-result {
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 22px;
        padding: 1.25rem 1.3rem;
        min-height: 178px;
        box-shadow: 0 10px 32px rgba(38,46,80,.055);
    }

    .mini-icon {
        font-size: 1.35rem;
        margin-bottom: .42rem;
    }

    .mini-label {
        color: #7A8195;
        font-size: .88rem;
    }

    .mini-title {
        font-size: 1.13rem;
        font-weight: 820;
        margin: .2rem 0;
        color: #20273C;
    }

    .mini-score {
        color: #5E67C8;
        font-weight: 800;
        font-size: .93rem;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: .55rem;
        margin: 1.75rem 0 .72rem;
        font-size: 1.35rem;
        font-weight: 850;
        color: #1F263A;
    }

    .section-icon {
        width: 34px;
        height: 34px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 11px;
        background: rgba(108,99,255,.10);
    }

    .dimension-card {
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin-bottom: .7rem;
        box-shadow: 0 7px 22px rgba(38,46,80,.035);
    }

    .dim-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: .35rem;
    }

    .dim-name {
        display: flex;
        align-items: center;
        gap: .55rem;
        font-weight: 820;
        color: #20273C;
    }

    .dim-score {
        font-weight: 850;
        color: #5E67C8;
        white-space: nowrap;
    }

    .dim-desc {
        color: #6E758A;
        line-height: 1.7;
        font-size: .94rem;
    }

    .advice-card {
        background: linear-gradient(135deg, rgba(108,99,255,.07), rgba(76,141,255,.055));
        border: 1px solid rgba(108,99,255,.12);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin: .65rem 0;
    }

    .behavior-card {
        background: rgba(255,255,255,.94);
        border-left: 4px solid #7A73FF;
        border-radius: 14px;
        padding: .85rem 1rem;
        margin: .6rem 0;
        box-shadow: 0 6px 18px rgba(38,46,80,.03);
    }

    .ai-report-wrap {
        background:
            radial-gradient(circle at 95% 5%, rgba(108,99,255,.10), transparent 18rem),
            linear-gradient(135deg, rgba(255,255,255,.98), rgba(248,249,255,.96));
        border: 1px solid rgba(108,99,255,.14);
        border-radius: 22px;
        padding: 1.25rem 1.35rem .45rem 1.35rem;
        margin: .7rem 0 1rem;
        box-shadow: 0 12px 34px rgba(55,60,110,.06);
    }


    div[data-testid="stMarkdownContainer"] h3 {
        margin-top: 1.45rem;
        margin-bottom: .72rem;
    }

    div[data-testid="stMarkdownContainer"] h4 {
        margin-top: 1.25rem;
        margin-bottom: .5rem;
        color: #293152;
    }

    div[data-testid="stMarkdownContainer"] hr {
        margin: 1rem 0 1.15rem;
        border-color: rgba(31,39,66,.09);
    }

    div[data-testid="stMarkdownContainer"] ol > li,
    div[data-testid="stMarkdownContainer"] ul > li {
        margin-bottom: .42rem;
        line-height: 1.72;
    }

    .ai-report-kicker {
        display: inline-flex;
        align-items: center;
        gap: .4rem;
        padding: .28rem .62rem;
        border-radius: 999px;
        background: rgba(108,99,255,.10);
        color: #5E57D8;
        font-size: .82rem;
        font-weight: 780;
        margin-bottom: .65rem;
    }

    .muted {
        color: #7A8195;
        font-size: .9rem;
    }


    /* ---------- System navigation / management ---------- */
    .system-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .system-badge {
        display: inline-flex;
        align-items: center;
        gap: .4rem;
        padding: .38rem .72rem;
        border-radius: 999px;
        background: rgba(76,141,255,.09);
        border: 1px solid rgba(76,141,255,.14);
        color: #4C65B5;
        font-weight: 750;
        font-size: .84rem;
    }

    .profile-card {
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 20px;
        padding: 1.1rem 1.25rem;
        margin: .8rem 0 1rem;
        box-shadow: 0 8px 24px rgba(38,46,80,.04);
    }

    .profile-name {
        font-size: 1.25rem;
        font-weight: 850;
        color: #20273C;
    }

    .profile-meta {
        color: #727A90;
        margin-top: .25rem;
        line-height: 1.7;
    }

    .admin-header {
        padding: 1.45rem 1.55rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #222946, #343D70 60%, #535CC3);
        color: white;
        margin-bottom: 1rem;
    }

    .admin-header .title {
        font-size: 1.8rem;
        font-weight: 850;
        margin-bottom: .25rem;
    }

    .admin-header .desc {
        opacity: .8;
    }

    .stat-card {
        background: rgba(255,255,255,.95);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(38,46,80,.04);
        min-height: 115px;
    }

    .stat-value {
        font-size: 1.85rem;
        font-weight: 900;
        color: #4F5FC2;
        line-height: 1.2;
    }

    .stat-label {
        color: #7A8195;
        font-size: .88rem;
        margin-top: .2rem;
    }

    .history-card {
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(31,39,66,.09);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin: .6rem 0;
        box-shadow: 0 7px 20px rgba(38,46,80,.035);
    }

    @media (max-width: 780px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
        .hero {
            padding: 1.55rem 1.25rem;
        }
        .hero::after {
            display: none;
        }
        .block-container {
            padding-top: 1.2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


QUESTIONS = [
    {"dimension": "批判性思维能力", "text": "在面对生成式 AI 提供的信息时，我会有意识地判断其准确性和可靠性。", "reverse": False},
    {"dimension": "创造性思维能力", "text": "使用 AI 时，我常常会被它给出的现成思路限制，很难再从新的角度产生自己的想法。", "reverse": True},
    {"dimension": "问题解决能力", "text": "遇到复杂学习任务时，我会先利用 AI 拆解问题，再把大目标分成可执行的小步骤。", "reverse": False},
    {"dimension": "自我调节学习能力", "text": "使用 AI 前，我通常不会事先设定清晰的学习目标、时间安排或使用边界。", "reverse": True},
    {"dimension": "人机协同能力", "text": "使用各类数字工具（含 AI）时，我会针对自己的需求设计合适的提问或操作方式。", "reverse": False},
    {"dimension": "元认知能力", "text": "看到 AI 给出的解释或答案后，我有时会直接觉得自己已经懂了，而不会再检查自己是否真正理解。", "reverse": True},
    {"dimension": "计算思维能力", "text": "在分析问题时，我会先用 AI 帮我提取关键变量及其关系，再构建解决框架。", "reverse": False},
    {"dimension": "批判性思维能力", "text": "当 AI 的回答看起来比较合理时，我通常会直接接受，而不会再与其他来源进行核对。", "reverse": True},
    {"dimension": "创造性思维能力", "text": "我经常将 AI 生成的不同元素进行组合、重构，以创造出新的内容。", "reverse": False},
    {"dimension": "问题解决能力", "text": "当原有方法无效时，我往往会依赖 AI 给出的第一个方案，而不会主动比较其他解题策略。", "reverse": True},
    {"dimension": "自我调节学习能力", "text": "发现 AI 反馈效率不高时，我会主动调整提示词或更换学习策略。", "reverse": False},
    {"dimension": "人机协同能力", "text": "当 AI 的结果不理想时，我通常会直接接受或放弃，而很少继续补充信息、调整提示或切换工具。", "reverse": True},
    {"dimension": "元认知能力", "text": "我大致清楚自己在哪些知识或能力上比较薄弱，并会利用 AI 进行针对性训练。", "reverse": False},
    {"dimension": "计算思维能力", "text": "面对多步骤任务时，我更倾向于让 AI 直接给出最终结果，而很少自己梳理清楚操作流程和逻辑关系。", "reverse": True},
    {"dimension": "批判性思维能力", "text": "我能识别出 AI 生成内容中逻辑不清晰或证据不足的部分。", "reverse": False},
    {"dimension": "创造性思维能力", "text": "对于 AI 给出的内容，我通常只是做少量修改，很少进一步重组并形成真正属于自己的新表达或新方案。", "reverse": True},
    {"dimension": "问题解决能力", "text": "面对真实情境问题（课程设计、项目实践等），我能综合 AI 建议与多方信息，拟定可行方案。", "reverse": False},
    {"dimension": "自我调节学习能力", "text": "完成 AI 辅助学习任务后，我很少回顾 AI 输出与实际效果之间的差距，也很少据此调整下一步学习方法。", "reverse": True},
    {"dimension": "人机协同能力", "text": "我善于把 AI 给出的建议与自己的想法结合，形成更完善的解决方案或作品。", "reverse": False},
    {"dimension": "元认知能力", "text": "完成一项 AI 辅助任务后，我通常不会专门反思哪些地方真正有效、哪些地方只是表面上完成了任务。", "reverse": True},
    {"dimension": "计算思维能力", "text": "遇到重复性学习任务时，我会利用 AI 生成脚本、公式或宏命令，实现自动化处理。", "reverse": False},
    {"dimension": "批判性思维能力", "text": "即使 AI 已经给出了一个现成答案，我通常也不会再独立追问问题的本质或重新思考其推理过程。", "reverse": True},
    {"dimension": "创造性思维能力", "text": "AI 提供的灵感能够帮助我打破思维定势，从新的角度思考问题。", "reverse": False},
]

DIMENSIONS = [
    "批判性思维能力",
    "创造性思维能力",
    "问题解决能力",
    "自我调节学习能力",
    "人机协同能力",
    "元认知能力",
    "计算思维能力",
]

DIMENSION_INFO = {
    "批判性思维能力": {
        "icon": "🔎",
        "short": "辨别、核验与独立判断",
        "meaning": "你是否会核验 AI 信息、识别逻辑与证据问题，并保持独立判断。",
        "tips": [
            "对重要结论至少找 1 个独立来源进行交叉验证。",
            "看到答案时追问：证据是什么？有没有反例？还有没有其他解释？",
            "让 AI 列出自身答案中可能存在的漏洞，再由你做最后判断。",
        ],
    },
    "创造性思维能力": {
        "icon": "✨",
        "short": "发散、重组与新想法",
        "meaning": "你能否借助 AI 打破思维定势、重组信息，并形成有自己特色的新想法。",
        "tips": [
            "同一问题尝试 3 种不同视角，再自行筛选与重组。",
            "不要停留在第一个答案，比较多个版本后再形成自己的方案。",
            "把两个原本不相关的概念、案例或方法重新连接，练习组合创新。",
        ],
    },
    "问题解决能力": {
        "icon": "🧩",
        "short": "拆解、比较与落地",
        "meaning": "你能否拆解复杂任务、比较多种路径，并把 AI 建议转化为可执行方案。",
        "tips": [
            "复杂任务先写清目标、约束、步骤和验证标准。",
            "遇到卡点时，让 AI 提供多种路径并比较各自利弊。",
            "方案完成后检查资源、时间、风险和替代方案。",
        ],
    },
    "自我调节学习能力": {
        "icon": "🎯",
        "short": "目标、监控与复盘",
        "meaning": "你是否能在使用 AI 前设定目标，在过程中调整策略，并在结束后复盘。",
        "tips": [
            "使用 AI 前先写下本次任务目标和必须自己完成的部分。",
            "给 AI 使用设置时间边界，避免一直停留在对话中。",
            "任务结束后记录：AI 帮助了什么、干扰了什么、下次怎么改。",
        ],
    },
    "人机协同能力": {
        "icon": "🤝",
        "short": "提问、调整与协作",
        "meaning": "你能否通过提问、补充信息和工具切换，让 AI 真正服务于自己的目标。",
        "tips": [
            "提问时明确任务目标、背景信息、限制条件和输出格式。",
            "第一次结果不理想时，指出具体问题并逐步补充上下文。",
            "让 AI 负责发散与整理，你负责判断、取舍和最终负责。",
        ],
    },
    "元认知能力": {
        "icon": "🪞",
        "short": "觉察、理解与自我检查",
        "meaning": "你是否清楚自己会什么、不会什么，并能检查“我是否真的理解”。",
        "tips": [
            "学完后关闭 AI，用自己的话复述核心内容。",
            "让 AI 出递进问题进行自测，但先由自己独立作答。",
            "建立知识薄弱清单，记录反复出错的概念和步骤。",
        ],
    },
    "计算思维能力": {
        "icon": "⚙️",
        "short": "变量、流程与自动化",
        "meaning": "你能否识别变量关系、设计流程，并把重复任务转化为规则或自动化步骤。",
        "tips": [
            "遇到复杂问题先梳理输入、处理步骤和输出。",
            "把多步骤任务写成流程或伪代码，再检查逻辑遗漏。",
            "对重复操作主动寻找可复用模板、公式、脚本或自动化方式。",
        ],
    },
}


def mean(values):
    return sum(values) / len(values) if values else 0.0


def to_ten_point(likert_mean):
    return round((likert_mean - 1) / 4 * 10, 2)


def score_level(score):
    if score >= 9.0:
        return "卓越"
    if score >= 8.0:
        return "优秀"
    if score >= 7.0:
        return "良好"
    if score >= 6.0:
        return "中上"
    if score >= 5.0:
        return "中等"
    if score >= 4.0:
        return "发展中"
    return "成长空间较大"


def dimension_status(score):
    if score >= 8.5:
        return "优势突出"
    if score >= 7.0:
        return "表现良好"
    if score >= 5.5:
        return "基础稳定"
    if score >= 4.0:
        return "仍有提升空间"
    return "建议优先加强"


def overall_interpretation(score, spread):
    if score >= 8.5:
        base = "你的整体表现处于较高水平，说明你在 AI 辅助学习中已经形成较成熟的判断、调节与协作习惯。"
    elif score >= 7.0:
        base = "你的整体表现较好，多数高阶思维环节已经能够主动使用，下一步可以继续提升稳定性与迁移能力。"
    elif score >= 5.5:
        base = "你的整体表现处于中等偏上水平，已经具备一定的高阶思维习惯，但部分能力在复杂任务中还不够稳定。"
    elif score >= 4.0:
        base = "你的高阶思维能力正在发展中。你已经表现出部分有效做法，下一步需要把零散习惯逐渐变成稳定策略。"
    else:
        base = "当前结果显示，你在 AI 辅助学习中的高阶思维策略使用相对有限，适合先从最需要加强的 1—2 个方向开始。"

    if spread < 1.2:
        structure = " 七个维度之间差距较小，整体结构比较均衡。"
    elif spread < 2.5:
        structure = " 不同维度之间存在一定差异，你已经形成部分优势，同时也有明确的提升方向。"
    else:
        structure = " 不同维度之间差异较明显，优先补强短板会比平均用力更有效。"

    return base + structure


def make_alternating_order():
    positive = [i for i, q in enumerate(QUESTIONS) if not q["reverse"]]
    negative = [i for i, q in enumerate(QUESTIONS) if q["reverse"]]
    random.shuffle(positive)
    random.shuffle(negative)

    order = []
    for i in range(max(len(positive), len(negative))):
        if i < len(positive):
            order.append(positive[i])
        if i < len(negative):
            order.append(negative[i])
    return order


def save_answer(idx):
    widget_key = f"_widget_q_{idx}"
    if widget_key in st.session_state:
        st.session_state.answers[idx] = st.session_state[widget_key]


def build_scores():
    dim_raw = {d: [] for d in DIMENSIONS}
    item_results = []

    for idx, q in enumerate(QUESTIONS):
        raw_value = st.session_state.answers.get(idx)
        if raw_value is None:
            continue

        scored_value = 6 - raw_value if q["reverse"] else raw_value
        dim_raw[q["dimension"]].append(scored_value)

        item_results.append(
            {
                "index": idx,
                "dimension": q["dimension"],
                "text": q["text"],
                "raw_likert": raw_value,
                "scored_likert": scored_value,
            }
        )

    dim_scores = {d: to_ten_point(mean(dim_raw[d])) for d in DIMENSIONS}
    overall = round(mean(list(dim_scores.values())), 2)
    return overall, dim_scores, item_results


def response_quality():
    answers = list(st.session_state.answers.values())
    if not answers:
        return []

    notices = []
    counts = Counter(answers)
    most_common_ratio = max(counts.values()) / len(answers)

    if len(answers) >= 15 and most_common_ratio >= 0.80:
        notices.append("你的选择较为集中，建议结合真实学习经历再次确认部分题目。")

    if "survey_start_time" in st.session_state and len(answers) == len(QUESTIONS):
        elapsed = time.time() - st.session_state.survey_start_time
        if elapsed < 60:
            notices.append("本次完成速度较快，若有题目未仔细阅读，可以重新测评后再对比结果。")

    return notices


def build_report_text(overall, dim_scores, item_results):
    ranked = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    strengths = ranked[:2]
    priorities = ranked[-2:]
    lowest_items = sorted(
        item_results,
        key=lambda x: (x["scored_likert"], x["index"])
    )[:3]

    lines = [
        f"{APP_TITLE}｜个人报告",
        "=" * 34,
        f"综合得分：{overall:.2f}/10",
        f"综合表现：{score_level(overall)}",
        "",
        "一、能力画像",
    ]

    for d in DIMENSIONS:
        lines.append(f"- {d}：{dim_scores[d]:.2f}/10")

    lines.extend(["", "二、优势方向"])
    for d, s in strengths:
        lines.append(f"- {d}（{s:.2f}/10）：{DIMENSION_INFO[d]['meaning']}")

    lines.extend(["", "三、优先提升方向"])
    for d, s in priorities:
        lines.append(f"- {d}（{s:.2f}/10）")
        for tip in DIMENSION_INFO[d]["tips"]:
            lines.append(f"  · {tip}")

    lines.extend(["", "四、值得关注的具体行为"])
    for x in lowest_items:
        lines.append(f"- [{x['dimension']}] {x['text']}")

    lines.extend(
        [
            "",
            "说明：",
            "本报告反映的是你在 AI 辅助学习情境中的自我感知与行为倾向，可用于自我了解和学习改进。",
        ]
    )

    return "\n".join(lines)


LIKERT_LABELS = {
    1: "完全不符合",
    2: "比较不符合",
    3: "一般",
    4: "比较符合",
    5: "完全符合",
}


def get_app_secret(name, default=None):
    """优先读取 Streamlit Secrets，其次读取环境变量。"""
    try:
        value = st.secrets.get(name, None)
        if value:
            return value
    except Exception:
        pass
    return os.getenv(name, default)


def item_strength_label(scored_likert):
    """内部用于给 AI 理解题项方向，不直接展示评分机制。"""
    if scored_likert >= 4.5:
        return "明显优势"
    if scored_likert >= 3.5:
        return "较稳定"
    if scored_likert >= 2.5:
        return "中性/不稳定"
    if scored_likert >= 1.5:
        return "需要提升"
    return "优先关注"


def build_ai_assessment_context(overall, dim_scores, item_results):
    ranked = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)

    lines = [
        "【综合结果】",
        f"综合思维指数：{overall:.2f}/10",
        f"综合表现：{score_level(overall)}",
        "",
        "【七维得分】",
    ]

    for d, s in ranked:
        lines.append(f"- {d}：{s:.2f}/10")

    lines.extend(
        [
            "",
            "【逐题作答】",
            "说明：下面的“能力表现强度”已经按题目含义统一为 1—5，5 表示该能力行为更稳定，1 表示更需要关注。",
        ]
    )

    for i, x in enumerate(item_results, start=1):
        raw = x["raw_likert"]
        scored = x["scored_likert"]
        lines.append(
            f"{i}. 维度：{x['dimension']}；"
            f"题目：{x['text']}；"
            f"用户选择：{raw}/5（{LIKERT_LABELS[raw]}）；"
            f"能力表现强度：{scored}/5（{item_strength_label(scored)}）"
        )

    return "\n".join(lines)


def build_local_personalized_report(overall, dim_scores, item_results):
    """
    AI 服务不可用时的兜底报告。
    仍然依据逐题选择生成，不会只看总分。
    """
    ranked_dims = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    strong_items = sorted(
        item_results,
        key=lambda x: (-x["scored_likert"], -dim_scores[x["dimension"]], x["index"])
    )[:4]
    weak_items = sorted(
        item_results,
        key=lambda x: (x["scored_likert"], dim_scores[x["dimension"]], x["index"])
    )[:4]

    # 找同一维度内部差异较大的维度
    by_dim = {d: [] for d in DIMENSIONS}
    for x in item_results:
        by_dim[x["dimension"]].append(x["scored_likert"])

    mixed_dims = []
    for d, vals in by_dim.items():
        if vals and max(vals) - min(vals) >= 2:
            mixed_dims.append((d, max(vals) - min(vals)))
    mixed_dims.sort(key=lambda x: x[1], reverse=True)

    strongest_dim = ranked_dims[0]
    weakest_dim = ranked_dims[-1]

    lines = [
        "### 一句话画像",
        (
            f"你的综合思维指数为 **{overall:.2f}/10**。从逐题作答看，你目前最稳定的方向是"
            f" **{strongest_dim[0]}**，而 **{weakest_dim[0]}** 更值得优先投入训练。"
            "与只看总分相比，你的具体题目表现显示出更细的“强项—短板”组合。"
        ),
        "",
        "### 你已经做得比较好的地方",
    ]

    for x in strong_items[:3]:
        lines.append(
            f"- 在“{x['text']}”这一行为上，你的作答表现较强。"
            f"这说明你在 **{x['dimension']}** 中已经形成了较稳定的有效习惯，建议继续保持并迁移到更复杂的任务。"
        )

    lines.extend(["", "### 最值得关注的具体表现"])

    for x in weak_items[:3]:
        tip = DIMENSION_INFO[x["dimension"]]["tips"][0]
        lines.append(
            f"- 对于“{x['text']}”，你的选择提示这一行为目前还不够稳定。"
            f"建议下一次遇到类似学习任务时，先执行一个固定动作：**{tip}**"
        )

    if mixed_dims:
        d = mixed_dims[0][0]
        vals = [x for x in item_results if x["dimension"] == d]
        high = max(vals, key=lambda x: x["scored_likert"])
        low = min(vals, key=lambda x: x["scored_likert"])
        lines.extend(
            [
                "",
                "### 一个容易被总分忽略的细节",
                (
                    f"你的 **{d}** 并不是简单的“强”或“弱”。例如，你在“{high['text']}”上的表现较好，"
                    f"但在“{low['text']}”上相对不足。这意味着更适合做**针对具体行为的训练**，"
                    "而不是笼统地说“提升这个维度”。"
                ),
            ]
        )

    lines.extend(["", "### 给你的针对性建议", ""])
    used_dims = []
    for x in weak_items:
        d = x["dimension"]
        if d in used_dims:
            continue
        used_dims.append(d)
        tips = DIMENSION_INFO[d]["tips"]
        n = len(used_dims)

        # 每条建议使用独立四级标题和独立段落，避免 Markdown 把下一条建议接在上一行后面
        lines.extend(
            [
                f"#### {n}. {DIMENSION_INFO[d]['icon']} {d}",
                "",
                f"**对应你的具体表现：** “{x['text']}”",
                "",
                f"**下一次可以直接做：** {tips[0]}",
                "",
                f"**进一步训练：** {tips[1]}",
                "",
                "---",
                "",
            ]
        )

        if len(used_dims) >= 4:
            break

    lines.extend(
        [
            "",
            "### 下一次使用 AI 时，先做这三件事",
            "",
            "1. **先自己想 2–3 分钟**：写下目标、已有思路和最不确定的地方，再打开 AI。",
            "",
            "2. **不要只问最终答案**：让 AI 给出多个思路、证据和可能出错的位置，再由你判断。",
            "",
            "3. **结束时做一次脱离 AI 的检查**：用自己的话复述、重做或解释核心过程，确认真正掌握。",
        ]
    )

    return "\n".join(lines)


def generate_ai_personalized_report(overall, dim_scores, item_results):
    """
    返回 (report, source)
    source 为 "openai" 或 "fallback"
    """
    api_key = get_app_secret("OPENAI_API_KEY")
    model = get_app_secret("OPENAI_MODEL", "gpt-5.6-luna")

    if not api_key:
        return build_local_personalized_report(overall, dim_scores, item_results), "fallback"

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        assessment_context = build_ai_assessment_context(
            overall, dim_scores, item_results
        )

        instructions = """
你是一名面向大学生的“高阶思维学习策略顾问”。你的任务是依据一份生成式AI学习情境下的高阶思维测评结果，
生成真正个性化、可执行的中文反馈。

重要要求：
1. 综合分只是背景，分析重点必须落在“每一道题具体选择了什么”。
2. 必须综合七维得分与23个逐题作答，不能只重复最低维度或最高维度。
3. 至少具体引用或清晰改述 8 个题项的作答表现，覆盖优势、短板和中等表现。
4. 如果同一维度内不同题项高低不一致，要指出这种“维度内部差异”，解释为什么总分会掩盖它。
5. 每条提升建议都要明确对应到用户的某个具体作答行为，避免“多思考、多练习”这类空泛建议。
6. 不要向用户提到“正向题、反向题、反向计分、内部评分规则”等测评设计细节。
7. 不做人格、心理、医学或能力诊断。用“从本次作答看”“可能”“更倾向于”等审慎表述。
8. 语气专业、清晰、有鼓励性，但不要夸张吹捧。
9. 不要重新计算或修改系统给出的分数。
10. 输出使用 Markdown，控制在约 1200—1800 个中文字。

请严格按以下结构输出：
## 你的核心思维画像
用 2—3 段解释整体能力结构，不只是复述分数。

## 从具体作答看，你的 3 个优势
每个优势都写：
- 具体表现证据
- 说明了什么
- 如何继续强化

## 最值得优先改变的 3 个具体习惯
每项必须指出对应的具体题目行为，并解释为什么值得优先改变。

## 一个容易被总分忽略的细节
寻找同一维度内部不一致、或跨维度的有趣组合，并给出解释。

## 给你的针对性建议
给出 4 条具体建议。
格式必须严格使用下面这种结构，并且每一条建议前后都要有空行：

### 1. 建议标题
**对应的本次作答：** ……

**下一次具体怎么做：** ……

**可以直接复制的 AI 提问示例：** ……

### 2. 建议标题
……

最终展示给用户的这一部分标题必须写成“## 给你的针对性建议”，标题中不要出现“4个”“四条”等具体数量。\n四条建议必须各自成为独立小节，绝对不要把“2.”、“3.”、“4.”接在上一条建议的同一行或同一段中。

## 7天微型训练计划
每天一个很小、可以真的执行的任务，必须与该用户的低分题项相关。
第1天到第7天分别独立成行，日期之间留空行，避免挤在同一段。

最后增加一句简短提醒：本报告用于自我了解与学习改进，不代表标准化诊断。
""".strip()

        user_input = f"""
请根据以下测评数据生成个性化深度报告。

{assessment_context}

请特别注意：
- 用户选择“完全不符合/比较不符合/一般/比较符合/完全符合”所对应的具体行为差异；
- 建议要随着某一道题的实际选择而变化；
- 不要只根据七维总分套模板；
- 不要在最终报告中暴露任何内部计分方式。
""".strip()

        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=user_input,
            reasoning={"effort": "low"},
            max_output_tokens=2600,
        )

        report = (response.output_text or "").strip()
        if not report:
            raise RuntimeError("模型未返回文本")

        return report, "openai"

    except Exception:
        return build_local_personalized_report(overall, dim_scores, item_results), "fallback"


def assessment_signature():
    """用于避免 Streamlit 每次 rerun 都重新调用 AI；版本升级时自动刷新旧报告。"""
    return (AI_REPORT_VERSION, tuple(sorted(st.session_state.answers.items())))



# =========================================================

# =========================================================
# Local database / system management
# =========================================================
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sixiangluopan.db")
ADMIN_PASSWORD = get_app_secret("ADMIN_PASSWORD", "123456")


def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_no TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            school TEXT DEFAULT '',
            major TEXT DEFAULT '',
            grade TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            assessed_at TEXT NOT NULL,
            overall REAL NOT NULL,
            dim_scores TEXT NOT NULL,
            answers TEXT NOT NULL,
            report TEXT DEFAULT '',
            report_source TEXT DEFAULT '',
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()
    conn.close()


def upsert_student(student_no, name, school, major, grade):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = db_connect()
    conn.execute(
        """
        INSERT INTO students(student_no, name, school, major, grade, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(student_no) DO UPDATE SET
            name=excluded.name,
            school=excluded.school,
            major=excluded.major,
            grade=excluded.grade,
            updated_at=excluded.updated_at
        """,
        (student_no.strip(), name.strip(), school.strip(), major.strip(), grade.strip(), now, now),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM students WHERE student_no = ?", (student_no.strip(),)
    ).fetchone()
    conn.close()
    return dict(row)


def get_student_by_no(student_no):
    conn = db_connect()
    row = conn.execute(
        "SELECT * FROM students WHERE student_no = ?", (student_no.strip(),)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_student(student_id):
    conn = db_connect()
    row = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def save_assessment(student_id, overall, dim_scores, answers, report, report_source):
    assessed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = db_connect()
    cur = conn.execute(
        """
        INSERT INTO assessments(
            student_id, assessed_at, overall, dim_scores, answers, report, report_source
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            assessed_at,
            float(overall),
            json.dumps(dim_scores, ensure_ascii=False),
            json.dumps(answers, ensure_ascii=False),
            report,
            report_source,
        ),
    )
    conn.commit()
    assessment_id = cur.lastrowid
    conn.close()
    return assessment_id


def get_student_assessments(student_id):
    conn = db_connect()
    rows = conn.execute(
        """
        SELECT * FROM assessments
        WHERE student_id = ?
        ORDER BY assessed_at DESC, id DESC
        """,
        (student_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_assessment(assessment_id):
    """获取单次测评详情，并同时带出学生档案信息。"""
    conn = db_connect()
    row = conn.execute(
        """
        SELECT a.*,
               s.student_no,
               s.name,
               s.school,
               s.major,
               s.grade
        FROM assessments a
        JOIN students s ON a.student_id = s.id
        WHERE a.id = ?
        """,
        (assessment_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_students():
    conn = db_connect()
    rows = conn.execute(
        """
        SELECT s.*,
               COUNT(a.id) AS assessment_count,
               MAX(a.assessed_at) AS last_assessed_at
        FROM students s
        LEFT JOIN assessments a ON s.id = a.student_id
        GROUP BY s.id
        ORDER BY s.updated_at DESC, s.id DESC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_assessments():
    conn = db_connect()
    rows = conn.execute(
        """
        SELECT a.*, s.student_no, s.name, s.school, s.major, s.grade
        FROM assessments a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.assessed_at DESC, a.id DESC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_student(student_id):
    conn = db_connect()
    conn.execute("DELETE FROM assessments WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()


def update_student(student_id, student_no, name, school, major, grade):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = db_connect()
    try:
        conn.execute(
            """
            UPDATE students
            SET student_no=?, name=?, school=?, major=?, grade=?, updated_at=?
            WHERE id=?
            """,
            (
                student_no.strip(),
                name.strip(),
                school.strip(),
                major.strip(),
                grade.strip(),
                now,
                student_id,
            ),
        )
        conn.commit()
        return True, ""
    except sqlite3.IntegrityError:
        return False, "学号已存在，请更换学号。"
    finally:
        conn.close()


def make_csv(rows, columns):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([label for _, label in columns])
    for row in rows:
        writer.writerow([row.get(key, "") for key, _ in columns])
    return output.getvalue().encode("utf-8-sig")


def assessment_rows_for_export(rows):
    result = []
    for row in rows:
        dims = json.loads(row["dim_scores"])
        result.append(
            {
                "测评编号": row["id"],
                "学号": row["student_no"],
                "姓名": row["name"],
                "学校": row["school"],
                "专业": row["major"],
                "年级": row["grade"],
                "测评时间": row["assessed_at"],
                "综合思维指数": row["overall"],
                **{d: dims.get(d, "") for d in DIMENSIONS},
            }
        )
    return result


init_db()


# =========================================================
# State
# =========================================================
if "stage" not in st.session_state:
    st.session_state.stage = "intro"

if "page" not in st.session_state:
    st.session_state.page = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "question_order" not in st.session_state:
    st.session_state.question_order = make_alternating_order()

if "ai_report" not in st.session_state:
    st.session_state.ai_report = None

if "ai_report_signature" not in st.session_state:
    st.session_state.ai_report_signature = None

if "ai_report_source" not in st.session_state:
    st.session_state.ai_report_source = None

if "saved_assessment_id" not in st.session_state:
    st.session_state.saved_assessment_id = None

if "student_id" not in st.session_state:
    st.session_state.student_id = None

if "admin_authed" not in st.session_state:
    st.session_state.admin_authed = False

if "history_selected_id" not in st.session_state:
    st.session_state.history_selected_id = None


def reset_survey_state():
    for key in list(st.session_state.keys()):
        if key.startswith("_widget_q_"):
            del st.session_state[key]

    st.session_state.page = 0
    st.session_state.answers = {}
    st.session_state.question_order = make_alternating_order()
    st.session_state.ai_report = None
    st.session_state.ai_report_signature = None
    st.session_state.ai_report_source = None
    st.session_state.saved_assessment_id = None
    st.session_state.pop("survey_start_time", None)


def student_header():
    student = get_student(st.session_state.student_id) if st.session_state.student_id else None
    if not student:
        return

    st.markdown(
        f"""
        <div class="profile-card">
            <div class="profile-name">🧑‍🎓 {escape(student["name"])}</div>
            <div class="profile-meta">
                学号：{escape(student["student_no"])}
                &nbsp; · &nbsp; {escape(student["school"] or "未填写学校")}
                &nbsp; · &nbsp; {escape(student["major"] or "未填写专业")}
                &nbsp; · &nbsp; {escape(student["grade"] or "未填写年级")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_student_navigation():
    if not st.session_state.student_id:
        return

    st.markdown('<div class="system-badge">✦ 学生端</div>', unsafe_allow_html=True)
    n1, n2, n3, n4 = st.columns(4)

    with n1:
        if st.button("📝 开始测评", use_container_width=True):
            reset_survey_state()
            st.session_state.stage = "survey"
            st.session_state.survey_start_time = time.time()
            st.rerun()

    with n2:
        if st.button("📈 成长记录", use_container_width=True):
            st.session_state.stage = "history"
            st.rerun()

    with n3:
        if st.button("👤 我的档案", use_container_width=True):
            st.session_state.stage = "profile"
            st.rerun()

    with n4:
        if st.button("退出学生端", use_container_width=True):
            st.session_state.student_id = None
            st.session_state.stage = "intro"
            reset_survey_state()
            st.rerun()


# =========================================================
# Home / Student Profile
# =========================================================
if st.session_state.stage == "intro":
    if st.session_state.student_id:
        student_header()
        show_student_navigation()

        st.markdown("")
        st.markdown(
            """
            <div class="hero">
                <div class="brand-pill">✦ THINKING COMPASS · V1.0</div>
                <div class="hero-title">
                    欢迎回到<br>
                    <span class="hero-gradient">思维罗盘</span>
                </div>
                <p class="hero-subtitle">
                    查看你的历史测评，持续追踪七维高阶思维能力变化，
                    或重新完成测评获得最新的能力画像与行动建议。
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        history = get_student_assessments(st.session_state.student_id)
        if history:
            latest = history[0]
            st.markdown(
                f"""
                <div class="soft-panel">
                    <strong>最近一次测评</strong><br>
                    综合思维指数：<strong>{latest["overall"]:.2f}/10</strong>
                    &nbsp; · &nbsp; 测评时间：{latest["assessed_at"]}
                    &nbsp; · &nbsp; 累计测评：{len(history)} 次
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("你还没有测评记录，点击“开始测评”即可建立第一份思维画像。")

    else:
        st.markdown(
            f"""
            <div class="hero">
                <div class="brand-pill">✦ AI × HIGHER-ORDER THINKING · V1.0</div>
                <div class="hero-title">
                    思维罗盘<br>
                    <span class="hero-gradient">高阶思维能力测评与成长管理</span>
                </div>
                <p class="hero-subtitle">
                    {APP_SUBTITLE}。通过与你日常 AI 学习行为有关的陈述，
                    了解你在判断、创造、解决问题、自我调节与人机协作等方面的特点，
                    并通过历史记录持续观察自己的成长变化。
                </p>
            </div>

            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">◈</div>
                    <div class="feature-value">23 题</div>
                    <div class="feature-label">轻量完成，不增加额外负担</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">◷</div>
                    <div class="feature-value">约 4–6 分钟</div>
                    <div class="feature-label">依据最近一段时间的真实状态作答</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">✦</div>
                    <div class="feature-value">7 维画像</div>
                    <div class="feature-label">结果不只是一项总分</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="soft-panel">
                <strong>第一步：建立学生档案</strong><br>
                输入基本信息后即可开始测评。系统会保存测评结果，
                便于后续查看历史变化；个人信息仅用于本地系统中的测评记录管理。
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            student_no = st.text_input("学号 / 学生编号", placeholder="例如：20260001")
            name = st.text_input("姓名", placeholder="请输入姓名")
            school = st.text_input("学校", placeholder="请输入学校名称")
        with c2:
            major = st.text_input("专业", placeholder="请输入专业")
            grade = st.selectbox(
                "年级",
                ["本科一年级", "本科二年级", "本科三年级", "本科四年级",
                 "硕士研究生", "博士研究生", "专科一年级", "专科二年级",
                 "专科三年级", "其他"],
            )

            existing = get_student_by_no(student_no) if student_no.strip() else None
            if existing:
                st.caption(
                    f"已找到该学生档案：{existing['name']}。开始测评后将更新本次基本信息，并保留历史测评记录。"
                )

        st.write("")
        consent = st.checkbox("我会根据真实情况认真作答，并同意保存本次测评记录。")

        a, b = st.columns([1.5, 1])
        with a:
            if st.button(
                "建立档案并开始测评  →",
                type="primary",
                use_container_width=True,
                disabled=not consent,
            ):
                if not student_no.strip() or not name.strip():
                    st.error("请至少填写学号/学生编号和姓名。")
                else:
                    student = upsert_student(
                        student_no, name, school, major, grade
                    )
                    st.session_state.student_id = student["id"]
                    reset_survey_state()
                    st.session_state.stage = "survey"
                    st.session_state.survey_start_time = time.time()
                    st.rerun()

        with b:
            if st.button("管理员入口", use_container_width=True):
                st.session_state.stage = "admin"
                st.rerun()

        st.markdown("### 你将获得")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("🔷 **综合思维指数**：0–10 分的整体表现")
            st.markdown("🕸️ **七维能力雷达图**：一眼看清能力结构")
            st.markdown("🏅 **优势方向**：发现最值得保留的思维习惯")
        with c2:
            st.markdown("🧭 **提升方向**：找到最值得优先改善的能力")
            st.markdown("📝 **行为级反馈**：定位到具体学习习惯")
            st.markdown("📈 **成长记录**：保存每次测评并观察变化")


# =========================================================
# Student Profile
# =========================================================
elif st.session_state.stage == "profile":
    if not st.session_state.student_id:
        st.session_state.stage = "intro"
        st.rerun()

    student_header()
    show_student_navigation()

    student = get_student(st.session_state.student_id)
    st.markdown(
        '<div class="section-title"><span class="section-icon">👤</span>我的档案</div>',
        unsafe_allow_html=True,
    )

    with st.form("student_profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            p_no = st.text_input("学号 / 学生编号", value=student["student_no"])
            p_name = st.text_input("姓名", value=student["name"])
            p_school = st.text_input("学校", value=student["school"])
        with c2:
            p_major = st.text_input("专业", value=student["major"])
            grade_options = [
                "本科一年级", "本科二年级", "本科三年级", "本科四年级",
                "硕士研究生", "博士研究生", "专科一年级", "专科二年级",
                "专科三年级", "其他"
            ]
            p_grade = st.selectbox(
                "年级",
                grade_options,
                index=grade_options.index(student["grade"])
                if student["grade"] in grade_options else len(grade_options) - 1,
            )
        submitted = st.form_submit_button("保存档案", type="primary", use_container_width=True)

    if submitted:
        if not p_no.strip() or not p_name.strip():
            st.error("学号/学生编号和姓名不能为空。")
        else:
            ok, msg = update_student(
                student["id"], p_no, p_name, p_school, p_major, p_grade
            )
            if ok:
                updated = get_student_by_no(p_no)
                st.session_state.student_id = updated["id"]
                st.success("档案已更新。")
                st.rerun()
            else:
                st.error(msg)

    history = get_student_assessments(st.session_state.student_id)
    st.markdown("### 档案概览")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{len(history)}</div><div class="stat-label">累计测评次数</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        latest_score = history[0]["overall"] if history else 0
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{latest_score:.2f}</div><div class="stat-label">最近综合思维指数</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        first_score = history[-1]["overall"] if history else 0
        change = latest_score - first_score if history else 0
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{change:+.2f}</div><div class="stat-label">相对首次变化</div></div>',
            unsafe_allow_html=True,
        )


# =========================================================
# Student History / Growth
# =========================================================
elif st.session_state.stage == "history":
    if not st.session_state.student_id:
        st.session_state.stage = "intro"
        st.rerun()

    student_header()
    show_student_navigation()

    history = get_student_assessments(st.session_state.student_id)

    st.markdown(
        '<div class="section-title"><span class="section-icon">📈</span>成长记录</div>',
        unsafe_allow_html=True,
    )

    if not history:
        st.info("暂时没有测评记录。完成第一次测评后，这里会自动生成成长档案。")
    else:
        # 历史趋势：按时间正序
        ordered = list(reversed(history))
        dates = [x["assessed_at"][:10] for x in ordered]
        overall_values = [x["overall"] for x in ordered]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=overall_values,
                mode="lines+markers",
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate="%{x}<br>综合指数：%{y:.2f}<extra></extra>",
            )
        )
        fig.update_layout(
            title="综合思维指数成长趋势",
            yaxis=dict(range=[0, 10], title="综合思维指数"),
            xaxis=dict(title="测评日期"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=360,
            margin=dict(l=40, r=30, t=55, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 七维能力变化")
        latest = json.loads(history[0]["dim_scores"])
        first = json.loads(history[-1]["dim_scores"])

        delta_rows = []
        for d in DIMENSIONS:
            delta_rows.append(
                {
                    "维度": d,
                    "首次": round(first.get(d, 0), 2),
                    "最近": round(latest.get(d, 0), 2),
                    "变化": round(latest.get(d, 0) - first.get(d, 0), 2),
                }
            )
        st.dataframe(delta_rows, use_container_width=True, hide_index=True)

        st.markdown("### 历史测评")
        for row in history:
            dims = json.loads(row["dim_scores"])
            with st.expander(
                f'{row["assessed_at"]}  ·  综合指数 {row["overall"]:.2f}/10'
            ):
                st.write(
                    f"优势方向：{max(dims.items(), key=lambda x: x[1])[0]}  ·  "
                    f"优先提升：{min(dims.items(), key=lambda x: x[1])[0]}"
                )
                if row["report"]:
                    st.download_button(
                        "下载本次报告",
                        data=row["report"].encode("utf-8-sig"),
                        file_name=f"思维罗盘_个人报告_{row['assessed_at'][:10]}.txt",
                        mime="text/plain",
                        key=f"history_download_{row['id']}",
                    )

        # 下载成长数据
        growth_rows = []
        for row in history:
            dims = json.loads(row["dim_scores"])
            growth_rows.append(
                {
                    "测评时间": row["assessed_at"],
                    "综合思维指数": row["overall"],
                    **{d: dims.get(d, "") for d in DIMENSIONS},
                }
            )
        st.download_button(
            "📥 导出我的成长数据",
            data=make_csv(
                growth_rows,
                [(k, k) for k in growth_rows[0].keys()],
            ),
            file_name="思维罗盘_个人成长记录.csv",
            mime="text/csv",
            use_container_width=True,
        )


# =========================================================
# Survey
# =========================================================
elif st.session_state.stage == "survey":
    if not st.session_state.student_id:
        st.session_state.stage = "intro"
        st.rerun()

    student_header()

    QUESTIONS_PER_PAGE = 5
    total_pages = math.ceil(len(QUESTIONS) / QUESTIONS_PER_PAGE)
    page = st.session_state.page

    start = page * QUESTIONS_PER_PAGE
    end = min(start + QUESTIONS_PER_PAGE, len(QUESTIONS))
    current_indices = st.session_state.question_order[start:end]
    answered_count = len(st.session_state.answers)

    st.markdown(
        f"""
        <div class="survey-top">
            <div class="survey-title">✦ 思维罗盘 · 高阶思维测评</div>
            <div class="survey-meta">
                第 {page + 1} / {total_pages} 页 · 已完成 {answered_count} / {len(QUESTIONS)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(answered_count / len(QUESTIONS))
    st.caption("请逐题阅读，选择最接近你真实情况的一项。")

    LABELS = {
        1: "1 · 完全不符合",
        2: "2 · 比较不符合",
        3: "3 · 一般",
        4: "4 · 比较符合",
        5: "5 · 完全符合",
    }

    for position, idx in enumerate(current_indices, start=start + 1):
        q = QUESTIONS[idx]
        widget_key = f"_widget_q_{idx}"

        if idx in st.session_state.answers and widget_key not in st.session_state:
            st.session_state[widget_key] = st.session_state.answers[idx]

        st.markdown(
            f"""
            <div class="q-card">
                <span class="q-number">Q{position}</span>
                <span class="q-text">{escape(q["text"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.radio(
            label=f"第 {position} 题",
            options=[1, 2, 3, 4, 5],
            index=None,
            format_func=lambda x: LABELS[x],
            key=widget_key,
            on_change=save_answer,
            args=(idx,),
            horizontal=True,
            label_visibility="collapsed",
        )

    page_complete = all(idx in st.session_state.answers for idx in current_indices)

    left, spacer, right = st.columns([1, 1.4, 1.6])

    with left:
        if page > 0:
            if st.button("← 返回上一页", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

    with right:
        if page < total_pages - 1:
            if st.button(
                "继续下一页 →",
                type="primary",
                use_container_width=True,
                disabled=not page_complete,
            ):
                st.session_state.page += 1
                st.rerun()
        else:
            all_complete = len(st.session_state.answers) == len(QUESTIONS)
            if st.button(
                "查看我的思维画像 ✦",
                type="primary",
                use_container_width=True,
                disabled=not all_complete,
            ):
                st.session_state.stage = "result"
                st.rerun()

    if not page_complete:
        st.caption("完成本页全部题目后即可继续。")


# =========================================================
# Result
# =========================================================
elif st.session_state.stage == "result":
    if not st.session_state.student_id:
        st.session_state.stage = "intro"
        st.rerun()

    student_header()
    overall, dim_scores, item_results = build_scores()
    ranked = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    strongest = ranked[0]
    weakest = ranked[-1]
    spread = strongest[1] - weakest[1]

    st.markdown(
        f"""
        <div class="result-hero">
            <div class="eyebrow">YOUR THINKING PROFILE</div>
            <div class="title">✦ 你的思维画像已经生成</div>
            <div class="desc">
                这份结果展示的是你在 AI 辅助学习情境中的思维特点。
                重点不是追求“满分”，而是看清自己的优势与下一步成长方向。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    notices = response_quality()
    for text_notice in notices:
        st.info("💡 " + text_notice)

    c1, c2, c3 = st.columns([1.05, 1, 1])

    with c1:
        st.markdown(
            f"""
            <div class="score-box">
                <div class="score-label">综合思维指数</div>
                <div class="score-number">{overall:.2f}</div>
                <div class="score-level">{score_level(overall)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        info = DIMENSION_INFO[strongest[0]]
        st.markdown(
            f"""
            <div class="mini-result">
                <div class="mini-icon">🏅 {info["icon"]}</div>
                <div class="mini-label">优势最突出的方向</div>
                <div class="mini-title">{escape(strongest[0])}</div>
                <div class="mini-score">{strongest[1]:.2f} / 10</div>
                <div class="muted">{escape(info["short"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        info = DIMENSION_INFO[weakest[0]]
        st.markdown(
            f"""
            <div class="mini-result">
                <div class="mini-icon">🧭 {info["icon"]}</div>
                <div class="mini-label">最值得优先提升</div>
                <div class="mini-title">{escape(weakest[0])}</div>
                <div class="mini-score">{weakest[1]:.2f} / 10</div>
                <div class="muted">{escape(info["short"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title"><span class="section-icon">◈</span>综合解读</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="soft-panel">
            {escape(overall_interpretation(overall, spread))}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title"><span class="section-icon">🕸️</span>七维能力画像</div>',
        unsafe_allow_html=True,
    )

    labels = DIMENSIONS + [DIMENSIONS[0]]
    values = [dim_scores[d] for d in DIMENSIONS] + [dim_scores[DIMENSIONS[0]]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill="toself",
            line=dict(color="#6C63FF", width=3),
            fillcolor="rgba(108,99,255,.17)",
            marker=dict(size=6, color="#4C8DFF"),
            hovertemplate="%{theta}<br>%{r:.2f}/10<extra></extra>",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickvals=[0, 2, 4, 6, 8, 10],
                gridcolor="rgba(31,39,66,.10)",
                linecolor="rgba(31,39,66,.08)",
                tickfont=dict(color="#8890A3", size=10),
            ),
            angularaxis=dict(
                gridcolor="rgba(31,39,66,.08)",
                tickfont=dict(color="#3D455A", size=12),
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=520,
        margin=dict(l=55, r=55, t=35, b=35),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title"><span class="section-icon">✦</span>每个维度怎么看</div>',
        unsafe_allow_html=True,
    )

    for d, s in ranked:
        info = DIMENSION_INFO[d]
        st.markdown(
            f"""
            <div class="dimension-card">
                <div class="dim-row">
                    <div class="dim-name"><span>{info["icon"]}</span>{escape(d)}</div>
                    <div class="dim-score">{s:.2f} / 10 · {dimension_status(s)}</div>
                </div>
                <div class="dim-desc">{escape(info["meaning"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title"><span class="section-icon">🏅</span>你的优势</div>',
        unsafe_allow_html=True,
    )
    for d, s in ranked[:2]:
        info = DIMENSION_INFO[d]
        st.markdown(
            f"""
            <div class="advice-card">
                <strong>{info["icon"]} {escape(d)} · {s:.2f}/10</strong><br>
                <span class="muted">{escape(info["meaning"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title"><span class="section-icon">🧭</span>下一步优先提升</div>',
        unsafe_allow_html=True,
    )

    for d, s in ranked[-2:][::-1]:
        info = DIMENSION_INFO[d]
        st.markdown(
            f"""
            <div class="advice-card">
                <strong>{info["icon"]} {escape(d)} · {s:.2f}/10</strong><br>
                <span class="muted">{escape(info["meaning"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for tip in info["tips"]:
            st.markdown(f"- {tip}")

    st.markdown(
        '<div class="section-title"><span class="section-icon">📝</span>最值得关注的具体习惯</div>',
        unsafe_allow_html=True,
    )

    lowest_items = sorted(
        item_results,
        key=lambda x: (
            x["scored_likert"],
            dim_scores[x["dimension"]],
            x["index"],
        ),
    )[:5]

    for x in lowest_items:
        st.markdown(
            f"""
            <div class="behavior-card">
                <strong>{DIMENSION_INFO[x["dimension"]]["icon"]} {escape(x["dimension"])}</strong><br>
                <span class="muted">{escape(x["text"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title"><span class="section-icon">✦</span>AI 个性化深度报告</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="ai-report-wrap">
            <div class="ai-report-kicker">✦ PERSONALIZED AI INSIGHT</div>
            <div class="dim-desc">
                这部分不会只看综合分。系统会结合七维能力结构，以及你在每一道题上的具体选择，
                识别“同一维度内哪些行为已经稳定、哪些行为仍然薄弱”，再生成更针对性的建议。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_signature = assessment_signature()

    if (
        st.session_state.ai_report is None
        or st.session_state.ai_report_signature != current_signature
    ):
        with st.spinner("正在结合你的 23 道具体作答生成个性化深度报告…"):
            ai_report, ai_source = generate_ai_personalized_report(
                overall, dim_scores, item_results
            )
            st.session_state.ai_report = ai_report
            st.session_state.ai_report_source = ai_source
            st.session_state.ai_report_signature = current_signature

    st.markdown(st.session_state.ai_report)

    if st.session_state.ai_report_source == "fallback":
        st.caption(
            "当前已生成基于逐题作答的个性化报告。配置 AI 服务后，系统会进一步进行跨题关联分析与更丰富的个性化解释。"
        )

    base_report_text = build_report_text(overall, dim_scores, item_results)
    report_text = (
        base_report_text
        + "\n\n"
        + "=" * 34
        + "\nAI 个性化深度报告\n"
        + "=" * 34
        + "\n"
        + st.session_state.ai_report
    )

    # 只保存一次本次测评
    if st.session_state.saved_assessment_id is None:
        st.session_state.saved_assessment_id = save_assessment(
            st.session_state.student_id,
            overall,
            dim_scores,
            st.session_state.answers,
            report_text,
            st.session_state.ai_report_source or "fallback",
        )

    st.markdown(
        f'<div class="soft-panel"><strong>✓ 本次测评已保存</strong><br>测评编号：{st.session_state.saved_assessment_id} · 可在“成长记录”中查看历史变化。</div>',
        unsafe_allow_html=True,
    )

    st.download_button(
        "下载完整测评报告 ↓",
        data=report_text.encode("utf-8-sig"),
        file_name="思维罗盘_生成式AI高阶思维能力测评_完整报告.txt",
        mime="text/plain",
        use_container_width=True,
    )

    b1, b2 = st.columns(2)
    with b1:
        if st.button("📈 查看成长记录", use_container_width=True):
            st.session_state.stage = "history"
            st.rerun()
    with b2:
        if st.button("重新测评", use_container_width=True):
            reset_survey_state()
            st.session_state.stage = "survey"
            st.session_state.survey_start_time = time.time()
            st.rerun()

    st.caption(
        "本测评用于了解 AI 辅助学习情境中的思维特点与学习行为，可作为自我了解与学习改进的参考。"
    )


# =========================================================
# Admin
# =========================================================
elif st.session_state.stage == "admin":
    st.markdown(
        """
        <div class="admin-header">
            <div class="title">✦ 思维罗盘 · 管理后台</div>
            <div class="desc">学生档案、测评记录与群体数据管理</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.admin_authed:
        st.markdown("### 管理员登录")
        password = st.text_input("管理员密码", type="password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("登录管理后台", type="primary", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_authed = True
                    st.rerun()
                else:
                    st.error("密码不正确。")
        with c2:
            if st.button("返回学生端", use_container_width=True):
                st.session_state.stage = "intro"
                st.rerun()
    else:
        a1, a2, a3 = st.columns(3)
        students = get_all_students()
        assessments = get_all_assessments()

        with a1:
            st.markdown(
                f'<div class="stat-card"><div class="stat-value">{len(students)}</div><div class="stat-label">学生人数</div></div>',
                unsafe_allow_html=True,
            )
        with a2:
            st.markdown(
                f'<div class="stat-card"><div class="stat-value">{len(assessments)}</div><div class="stat-label">累计测评次数</div></div>',
                unsafe_allow_html=True,
            )
        with a3:
            avg_score = mean([x["overall"] for x in assessments]) if assessments else 0
            st.markdown(
                f'<div class="stat-card"><div class="stat-value">{avg_score:.2f}</div><div class="stat-label">平均综合思维指数</div></div>',
                unsafe_allow_html=True,
            )

        st.write("")
        tabs = st.tabs(["👥 学生管理", "📊 测评统计", "📋 测评记录"])

        # Student management
        with tabs[0]:
            st.markdown("### 学生档案")
            keyword = st.text_input(
                "搜索学生",
                placeholder="可输入学号、姓名、学校或专业",
                key="admin_student_keyword",
            ).strip().lower()

            grade_filter = st.selectbox(
                "年级筛选",
                ["全部"] + sorted(
                    {x["grade"] for x in students if x["grade"]},
                    key=str,
                ),
            )

            filtered_students = []
            for s in students:
                haystack = " ".join(
                    [
                        s["student_no"],
                        s["name"],
                        s["school"],
                        s["major"],
                    ]
                ).lower()
                if keyword and keyword not in haystack:
                    continue
                if grade_filter != "全部" and s["grade"] != grade_filter:
                    continue
                filtered_students.append(s)

            table_rows = [
                {
                    "学号": s["student_no"],
                    "姓名": s["name"],
                    "学校": s["school"],
                    "专业": s["major"],
                    "年级": s["grade"],
                    "测评次数": s["assessment_count"],
                    "最近测评": s["last_assessed_at"] or "暂无",
                }
                for s in filtered_students
            ]
            st.dataframe(table_rows, use_container_width=True, hide_index=True)

            if filtered_students:
                selected_no = st.selectbox(
                    "选择需要管理的学生",
                    [s["student_no"] for s in filtered_students],
                )
                selected = next(
                    s for s in filtered_students if s["student_no"] == selected_no
                )

                with st.expander("✏️ 编辑学生档案", expanded=False):
                    with st.form(f"edit_student_{selected['id']}"):
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            e_no = st.text_input("学号", value=selected["student_no"])
                            e_name = st.text_input("姓名", value=selected["name"])
                            e_school = st.text_input("学校", value=selected["school"])
                        with ec2:
                            e_major = st.text_input("专业", value=selected["major"])
                            e_grade = st.text_input("年级", value=selected["grade"])
                        save_edit = st.form_submit_button(
                            "保存修改", type="primary", use_container_width=True
                        )

                    if save_edit:
                        ok, msg = update_student(
                            selected["id"],
                            e_no,
                            e_name,
                            e_school,
                            e_major,
                            e_grade,
                        )
                        if ok:
                            st.success("学生档案已更新。")
                            st.rerun()
                        else:
                            st.error(msg)

                with st.expander("🗑️ 删除学生档案", expanded=False):
                    st.warning(
                        "删除学生后，该学生的全部历史测评记录也会被删除，此操作不可恢复。"
                    )
                    confirm_delete = st.checkbox(
                        "我确认删除该学生及其历史测评记录",
                        key=f"confirm_delete_{selected['id']}",
                    )
                    if st.button(
                        "确认删除",
                        disabled=not confirm_delete,
                        key=f"delete_student_{selected['id']}",
                    ):
                        delete_student(selected["id"])
                        st.success("学生档案及相关测评记录已删除。")
                        st.rerun()

            if students:
                export_students = []
                for s in students:
                    export_students.append(
                        {
                            "学号": s["student_no"],
                            "姓名": s["name"],
                            "学校": s["school"],
                            "专业": s["major"],
                            "年级": s["grade"],
                            "测评次数": s["assessment_count"],
                            "最近测评": s["last_assessed_at"] or "",
                        }
                    )
                st.download_button(
                    "📥 导出学生档案 CSV",
                    data=make_csv(
                        export_students,
                        [(k, k) for k in export_students[0].keys()],
                    ),
                    file_name="思维罗盘_学生档案.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        # Statistics
        with tabs[1]:
            st.markdown("### 群体能力概览")
            if not assessments:
                st.info("暂无测评数据。")
            else:
                dim_means = {}
                for d in DIMENSIONS:
                    vals = [
                        json.loads(a["dim_scores"]).get(d, 0)
                        for a in assessments
                    ]
                    dim_means[d] = round(mean(vals), 2)

                stat_rows = [
                    {"维度": d, "群体平均得分": dim_means[d]}
                    for d in DIMENSIONS
                ]
                st.dataframe(stat_rows, use_container_width=True, hide_index=True)

                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        x=list(dim_means.keys()),
                        y=list(dim_means.values()),
                        text=list(dim_means.values()),
                        textposition="outside",
                    )
                )
                fig.update_layout(
                    title="七维高阶思维群体平均水平",
                    yaxis=dict(range=[0, 10], title="平均得分"),
                    xaxis=dict(tickangle=-20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=420,
                    margin=dict(l=45, r=25, t=55, b=100),
                )
                st.plotly_chart(fig, use_container_width=True)

                # 学校/年级的简单统计
                st.markdown("### 分组概览")
                group_rows = []
                groups = sorted({a["grade"] for a in assessments if a["grade"]})
                for g in groups:
                    vals = [a["overall"] for a in assessments if a["grade"] == g]
                    group_rows.append(
                        {
                            "年级": g,
                            "测评人数": len(vals),
                            "平均综合指数": round(mean(vals), 2),
                        }
                    )
                st.dataframe(group_rows, use_container_width=True, hide_index=True)

        # Assessment records
        with tabs[2]:
            st.markdown("### 全部测评记录")
            if not assessments:
                st.info("暂无测评记录。")
            else:
                record_rows = [
                    {
                        "测评编号": a["id"],
                        "学号": a["student_no"],
                        "姓名": a["name"],
                        "学校": a["school"],
                        "专业": a["major"],
                        "年级": a["grade"],
                        "测评时间": a["assessed_at"],
                        "综合指数": a["overall"],
                    }
                    for a in assessments
                ]
                st.dataframe(record_rows, use_container_width=True, hide_index=True)

                export_rows = assessment_rows_for_export(assessments)
                st.download_button(
                    "📥 导出全部测评数据 CSV",
                    data=make_csv(
                        export_rows,
                        [(k, k) for k in export_rows[0].keys()],
                    ),
                    file_name="思维罗盘_全部测评数据.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

                selected_assessment_id = st.selectbox(
                    "查看某次测评详情",
                    [a["id"] for a in assessments],
                    format_func=lambda x: next(
                        f'{a["assessed_at"]} · {a["name"]} · {a["overall"]:.2f}/10'
                        for a in assessments if a["id"] == x
                    ),
                )
                detail = get_assessment(selected_assessment_id)
                if detail:
                    dims = json.loads(detail["dim_scores"])
                    st.markdown("#### 测评结果")
                    detail_rows = [
                        {"维度": d, "得分": round(dims.get(d, 0), 2)}
                        for d in DIMENSIONS
                    ]
                    st.dataframe(
                        detail_rows,
                        use_container_width=True,
                        hide_index=True,
                    )

                    if detail["report"]:
                        st.download_button(
                            "下载该学生完整报告",
                            data=detail["report"].encode("utf-8-sig"),
                            file_name=f"思维罗盘_{detail.get('name', '学生')}_{detail['assessed_at'][:10]}_报告.txt",
                            mime="text/plain",
                            key=f"admin_report_{detail['id']}",
                        )

        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("返回学生端", use_container_width=True):
                st.session_state.admin_authed = False
                st.session_state.stage = "intro"
                st.rerun()
        with c2:
            if st.button("管理员退出", use_container_width=True):
                st.session_state.admin_authed = False
                st.session_state.stage = "admin"
                st.rerun()
