#!/usr/bin/env python3
"""ZX Capital Site Generator - Generates 800+ page static site"""
import os, json, html, shutil
from pathlib import Path

DOMAIN = "https://zxcapital.ai"
OUT = "zxcapital-site"

# ============================================================
# CSS (embedded in every page)
# ============================================================
CSS = """:root{--bg:#06080d;--bg2:#080b12;--card:#0d1117;--bdr:#161d2a;--g:#00dc82;--gd:#00b36b;--r:#ff4d6a;--amb:#f0a050;--t:#e2e8f0;--tm:#94a3b8;--td:#64748b;--tb:#f1f5f9}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'DM Sans','Noto Sans SC',system-ui,sans-serif;background:var(--bg);color:var(--t);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}.mono{font-family:'Space Mono','Courier New',monospace}.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
.nav{position:sticky;top:0;z-index:100;background:rgba(6,8,13,.92);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border-bottom:1px solid var(--bdr)}.nav-in{display:flex;align-items:center;justify-content:space-between;height:60px;max-width:1100px;margin:0 auto;padding:0 20px}
.logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:17px;color:var(--tb)}.logo-i{width:34px;height:34px;border-radius:7px;background:linear-gradient(135deg,var(--g),var(--gd));display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:var(--bg);font-family:'Space Mono',monospace}
.nlinks{display:flex;gap:24px;align-items:center}.nlinks a{color:var(--tm);font-size:13px;font-weight:500;transition:color .2s}.nlinks a:hover,.nlinks a.on{color:var(--g)}
.lbtn{background:var(--bdr);color:var(--tm);border:none;padding:5px 12px;border-radius:5px;font-size:12px;font-weight:600;cursor:pointer;font-family:'Space Mono',monospace;text-decoration:none}
.mbtn{display:none;background:none;border:none;color:var(--t);font-size:22px;cursor:pointer}.mmenu{display:none;background:var(--bg2);border-top:1px solid var(--bdr);padding:12px 20px}.mmenu a{display:block;padding:10px 0;color:var(--tm);font-size:14px}
.hero{position:relative;min-height:88vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:80px 20px 60px}.hero-bg{position:absolute;inset:0;background-image:radial-gradient(circle at 1px 1px,rgba(255,255,255,.03) 1px,transparent 0);background-size:40px 40px;pointer-events:none}
.hero-glow{position:absolute;top:15%;left:50%;transform:translate(-50%,-50%);width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(0,220,130,.07),transparent 70%);pointer-events:none;animation:glow 4s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.5}50%{opacity:1}}
.hero h1{font-size:clamp(32px,6vw,56px);font-weight:700;line-height:1.12;letter-spacing:-.025em;background:linear-gradient(135deg,#f1f5f9,#94a3b8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:20px 0}
.hero p{font-size:17px;color:var(--td);max-width:560px;margin:0 auto 32px}
.bp{display:inline-block;background:linear-gradient(135deg,var(--g),var(--gd));color:var(--bg);padding:13px 30px;border-radius:8px;font-weight:700;font-size:14px;transition:all .3s;border:none;cursor:pointer}.bp:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,220,130,.3)}
.bo{display:inline-block;background:transparent;color:var(--t);border:1px solid var(--bdr);padding:13px 30px;border-radius:8px;font-weight:500;font-size:14px;transition:all .3s}.bo:hover{border-color:var(--g);color:var(--g)}
.tag{display:inline-block;background:rgba(0,220,130,.12);color:var(--g);font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:.04em}
.card{background:var(--card);border:1px solid var(--bdr);border-radius:14px;padding:26px;transition:all .3s}.card:hover{border-color:var(--g);transform:translateY(-3px);box-shadow:0 10px 36px rgba(0,220,130,.06)}
.g2{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}.g3{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;padding-top:32px;border-top:1px solid var(--bdr);margin-top:48px}
.tw{overflow-x:auto;border-radius:12px;border:1px solid var(--bdr)}table{width:100%;border-collapse:collapse;font-size:13px}
th{background:var(--card);color:var(--td);font-weight:600;text-transform:uppercase;font-size:10px;letter-spacing:.06em;padding:13px 16px;text-align:left;border-bottom:1px solid var(--bdr);white-space:nowrap}
td{padding:13px 16px;border-bottom:1px solid var(--bg);white-space:nowrap}tr:hover td{background:var(--card)}.tk{font-family:'Space Mono',monospace;color:var(--g);font-weight:700}.pos{color:var(--g)}.neg{color:var(--r)}
.met{background:var(--card);border:1px solid var(--bdr);border-radius:10px;padding:18px 20px}.met-l{font-size:11px;color:var(--td);text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px}.met-v{font-size:20px;font-weight:700;font-family:'Space Mono',monospace}
.bar-t{height:6px;background:var(--bdr);border-radius:3px;margin-top:4px}.bar-f{height:100%;border-radius:3px;background:var(--g)}
.sec{padding:70px 20px;max-width:1100px;margin:0 auto}.sec-a{background:var(--bg2);padding:70px 0}.sec h2{font-size:32px;font-weight:700;margin-bottom:8px}.sub{color:var(--td);margin-bottom:32px}
.bc{display:flex;gap:8px;align-items:center;font-size:13px;color:var(--td);margin-bottom:24px;flex-wrap:wrap}.bc a{color:var(--tm)}.bc a:hover{color:var(--g)}
.disc{background:var(--card);border:1px solid #2a1c1c;border-radius:14px;padding:28px 32px;max-width:900px;margin:0 auto}.disc h3{font-size:15px;font-weight:700;color:var(--amb);margin-bottom:12px}.disc p{font-size:12px;color:var(--td);line-height:1.7;margin-bottom:8px}
.dh{display:flex;align-items:center;gap:16px;margin-bottom:28px;flex-wrap:wrap}.di{width:52px;height:52px;border-radius:12px;background:linear-gradient(135deg,rgba(0,220,130,.15),var(--card));border:1px solid var(--bdr);display:flex;align-items:center;justify-content:center;font-family:'Space Mono',monospace;font-weight:700;font-size:16px;color:var(--g)}.dp{margin-left:auto;text-align:right}
footer{border-top:1px solid var(--bdr);padding:40px 20px 24px;background:var(--bg)}.fi{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}.fb{display:flex;align-items:center;gap:8px}.fc{color:var(--td);font-size:11px}
.calc-box{background:var(--card);border:1px solid var(--bdr);border-radius:14px;padding:32px}.calc-box label{display:block;font-size:12px;color:var(--td);margin-bottom:6px;font-weight:500}
.calc-box input,.calc-box select{width:100%;background:var(--bg);border:1px solid var(--bdr);border-radius:8px;padding:12px 14px;color:var(--t);font-size:15px;font-family:'Space Mono',monospace;outline:none;margin-bottom:16px}
.calc-box select{font-family:'DM Sans',sans-serif;cursor:pointer}
.res-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-top:24px}
@keyframes fadeup{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}.fu{animation:fadeup .6s ease both}.fd1{animation-delay:.1s}.fd2{animation-delay:.2s}.fd3{animation-delay:.3s}
@media(max-width:768px){.nlinks{display:none!important}.mbtn{display:flex!important}.g4,.sg{grid-template-columns:repeat(2,1fr)}.dh{flex-direction:column;align-items:flex-start}.dp{margin-left:0;text-align:left}.hero h1{font-size:32px!important}.mmenu.open{display:block!important}}
@media(max-width:500px){td,th{padding:10px;font-size:12px}.g3{grid-template-columns:repeat(2,1fr)}}"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">'

def e(s): return html.escape(str(s))

def pn(v):
    """Return pos/neg class"""
    try:
        n = float(str(v).replace('%','').replace('+','').replace('$','').replace(',',''))
        return 'pos' if n >= 0 else 'neg'
    except: return ''

def nav(lang='en', prefix=''):
    p = '/zh' if lang=='zh' else ''
    lbl = {'etf':'ETF','stock':'股票' if lang=='zh' else 'Stocks','crypto':'加密货币' if lang=='zh' else 'Crypto','calc':'工具' if lang=='zh' else 'Tools','about':'关于' if lang=='zh' else 'About'}
    toggle = f'<a href="/" class="lbtn">EN</a>' if lang=='zh' else f'<a href="/zh/" class="lbtn">中文</a>'
    return f'''<nav class="nav"><div class="nav-in">
<a href="{p}/" class="logo"><span class="logo-i">ZX</span>ZX Capital</a>
<div class="nlinks"><a href="{p}/etf/">{lbl['etf']}</a><a href="{p}/stock/">{lbl['stock']}</a><a href="{p}/crypto/">{lbl['crypto']}</a><a href="{p}/calculator/">{lbl['calc']}</a><a href="{p}/about.html">{lbl['about']}</a></div>
<div style="display:flex;gap:10px;align-items:center">{toggle}<button class="mbtn" onclick="document.getElementById('mm').classList.toggle('open')" aria-label="Menu">☰</button></div>
</div><div id="mm" class="mmenu"><a href="{p}/etf/">{lbl['etf']}</a><a href="{p}/stock/">{lbl['stock']}</a><a href="{p}/crypto/">{lbl['crypto']}</a><a href="{p}/calculator/">{lbl['calc']}</a><a href="{p}/about.html">{lbl['about']}</a></div></nav>'''

def footer(lang='en'):
    p = '/zh' if lang=='zh' else ''
    return f'''<footer><div class="fi">
<div class="fb"><span class="logo-i" style="width:28px;height:28px;font-size:10px">ZX</span><span style="font-weight:600;font-size:14px">ZX Capital</span></div>
<nav style="display:flex;gap:20px;font-size:12px;color:var(--td)"><a href="{p}/etf/">ETF</a><a href="{p}/stock/">{"股票" if lang=="zh" else "Stocks"}</a><a href="{p}/crypto/">{"加密货币" if lang=="zh" else "Crypto"}</a><a href="{p}/calculator/">{"工具" if lang=="zh" else "Tools"}</a><a href="{p}/about.html">{"关于" if lang=="zh" else "About"}</a></nav>
<div class="fc">© 2026 ZX Capital. All rights reserved.</div></div></footer>'''

def head(title, desc, path, lang='en'):
    alt_path = f'/zh{path}' if lang=='en' else path.replace('/zh','',1)
    en_path = path if lang=='en' else alt_path
    zh_path = f'/zh{path}' if lang=='en' else path
    return f'''<!DOCTYPE html><html lang="{lang}"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc[:160])}">
<link rel="canonical" href="{DOMAIN}{path}">
<link rel="alternate" hreflang="en" href="{DOMAIN}{en_path}">
<link rel="alternate" hreflang="zh" href="{DOMAIN}{zh_path}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}{en_path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc[:160])}">
<meta property="og:url" content="{DOMAIN}{path}"><meta property="og:type" content="website"><meta property="og:site_name" content="ZX Capital">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc[:160])}">
{FONTS}
<style>{CSS}</style></head><body>'''

def page(filepath, content):
    d = os.path.dirname(filepath)
    if d: os.makedirs(os.path.join(OUT, d), exist_ok=True)
    with open(os.path.join(OUT, filepath), 'w', encoding='utf-8') as f:
        f.write(content)

def breadcrumb_json(items, lang='en'):
    """items = [(name, url), ...] last item has no url"""
    il = []
    for i,(n,u) in enumerate(items):
        it = {"@type":"ListItem","position":i+1,"name":n}
        if u: it["item"] = f"{DOMAIN}{u}"
        il.append(it)
    return f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":il})}</script>'

def metric(label, value, cls=''):
    return f'<div class="met"><div class="met-l">{e(label)}</div><div class="met-v {cls}">{e(value)}</div></div>'

# ============================================================
# DATA
# ============================================================
ETFS = [
    {"t":"SPY","n":"SPDR S&P 500 ETF Trust","n_zh":"SPDR标普500ETF","exp":"0.09%","yld":"1.22%","ytd":"+12.4%","aum":"$562B","pe":"22.8","beta":"1.0","hold":503,"cat":"Large Blend","iss":"State Street","inc":"1993-01-22","price":"$528.32",
     "desc":"SPY tracks the S&P 500 index, providing broad exposure to large-cap U.S. equities. It is the world's largest and most liquid ETF with over $560 billion in assets under management.",
     "desc_zh":"SPY追踪标普500指数，提供对美国大盘股的广泛敞口。它是全球最大、流动性最强的ETF，管理资产超过5600亿美元。",
     "top":[("AAPL",7.1),("MSFT",6.8),("NVDA",6.2),("AMZN",3.8),("GOOGL",2.1),("META",2.0),("BRK.B",1.8),("TSLA",1.6),("UNH",1.4),("JPM",1.3)],
     "sec":[("Technology",31.2),("Financials",13.4),("Healthcare",12.8),("Consumer Disc.",10.6),("Communication",9.1),("Industrials",8.7),("Consumer Stap.",5.9),("Energy",3.6)],
     "ret":{"1m":"+2.1%","3m":"+5.8%","6m":"+9.2%","1y":"+12.4%","3y":"+10.2%","5y":"+14.8%","10y":"+12.6%"}},
    {"t":"QQQ","n":"Invesco QQQ Trust","n_zh":"景顺QQQ信托","exp":"0.20%","yld":"0.51%","ytd":"+15.8%","aum":"$312B","pe":"28.4","beta":"1.12","hold":101,"cat":"Large Growth","iss":"Invesco","inc":"1999-03-10","price":"$485.60",
     "desc":"QQQ tracks the Nasdaq-100 Index, consisting of the 100 largest non-financial companies listed on Nasdaq. Heavily weighted toward technology and growth stocks.",
     "desc_zh":"QQQ追踪纳斯达克100指数，涵盖纳斯达克上市的100家最大非金融公司。重仓科技和成长股。",
     "top":[("AAPL",8.9),("MSFT",8.1),("NVDA",7.6),("AMZN",5.4),("META",4.8),("AVGO",4.2),("GOOGL",2.8),("GOOG",2.7),("COST",2.5),("TSLA",2.4)],
     "sec":[("Technology",57.8),("Communication",16.2),("Consumer Disc.",13.4),("Healthcare",6.8),("Consumer Stap.",3.2),("Industrials",1.8),("Utilities",0.8)],
     "ret":{"1m":"+3.2%","3m":"+7.4%","6m":"+11.8%","1y":"+15.8%","3y":"+12.1%","5y":"+18.4%","10y":"+17.2%"}},
    {"t":"VTI","n":"Vanguard Total Stock Market ETF","n_zh":"先锋全股市ETF","exp":"0.03%","yld":"1.28%","ytd":"+11.2%","aum":"$418B","pe":"21.6","beta":"1.0","hold":3942,"cat":"Large Blend","iss":"Vanguard","inc":"2001-05-24","price":"$278.40",
     "desc":"VTI provides exposure to the entire U.S. stock market, including small-, mid-, and large-cap growth and value stocks. Ultra-low expense ratio makes it a core portfolio holding.",
     "desc_zh":"VTI提供对整个美国股市的敞口，包括小盘、中盘和大盘成长及价值股。超低费率使其成为核心投资组合持仓。",
     "top":[("AAPL",6.4),("MSFT",5.8),("NVDA",5.2),("AMZN",3.4),("GOOGL",1.9),("META",1.8),("BRK.B",1.5),("TSLA",1.4),("UNH",1.2),("JPM",1.1)],
     "sec":[("Technology",29.8),("Financials",13.1),("Healthcare",12.6),("Consumer Disc.",10.8),("Industrials",9.4),("Communication",8.2),("Consumer Stap.",5.4),("Energy",4.1)],
     "ret":{"1m":"+1.8%","3m":"+5.2%","6m":"+8.6%","1y":"+11.2%","3y":"+9.8%","5y":"+13.6%","10y":"+11.8%"}},
    {"t":"SCHD","n":"Schwab U.S. Dividend Equity ETF","n_zh":"嘉信美国红利ETF","exp":"0.06%","yld":"3.38%","ytd":"+5.1%","aum":"$63B","pe":"16.2","beta":"0.82","hold":104,"cat":"Large Value","iss":"Schwab","inc":"2011-10-20","price":"$82.45",
     "desc":"SCHD focuses on high-quality U.S. dividend-paying stocks selected by fundamental criteria. Known for consistent dividend growth and lower volatility.",
     "desc_zh":"SCHD专注于通过基本面标准筛选的高质量美国派息股票。以持续的股息增长和较低波动率著称。",
     "top":[("ABBV",4.4),("HD",4.2),("CVX",4.1),("MRK",4.0),("PEP",3.8),("AMGN",3.6),("KO",3.4),("VZ",3.2),("CSCO",3.0),("PFE",2.8)],
     "sec":[("Healthcare",16.4),("Financials",15.8),("Consumer Stap.",14.2),("Industrials",13.6),("Technology",12.4),("Energy",8.6),("Communication",6.2),("Consumer Disc.",5.8)],
     "ret":{"1m":"+0.8%","3m":"+2.4%","6m":"+3.8%","1y":"+5.1%","3y":"+7.2%","5y":"+10.8%","10y":"+11.2%"}},
    {"t":"VOO","n":"Vanguard S&P 500 ETF","n_zh":"先锋标普500 ETF","exp":"0.03%","yld":"1.24%","ytd":"+12.3%","aum":"$498B","pe":"22.6","beta":"1.0","hold":503,"cat":"Large Blend","iss":"Vanguard","inc":"2010-09-07","price":"$486.20",
     "desc":"VOO tracks the S&P 500 with one of the lowest expense ratios available. Vanguard's flagship index fund for broad U.S. large-cap exposure.",
     "desc_zh":"VOO以极低的费率追踪标普500指数。是先锋集团旗舰指数基金，提供广泛的美国大盘股敞口。",
     "top":[("AAPL",7.1),("MSFT",6.8),("NVDA",6.2),("AMZN",3.8),("GOOGL",2.1),("META",2.0),("BRK.B",1.8),("TSLA",1.6),("UNH",1.4),("JPM",1.3)],
     "sec":[("Technology",31.2),("Financials",13.4),("Healthcare",12.8),("Consumer Disc.",10.6),("Communication",9.1),("Industrials",8.7),("Consumer Stap.",5.9),("Energy",3.6)],
     "ret":{"1m":"+2.1%","3m":"+5.7%","6m":"+9.1%","1y":"+12.3%","3y":"+10.1%","5y":"+14.7%","10y":"+12.5%"}},
    {"t":"IVV","n":"iShares Core S&P 500 ETF","n_zh":"iShares核心标普500 ETF","exp":"0.03%","yld":"1.26%","ytd":"+12.3%","aum":"$548B","pe":"22.7","beta":"1.0","hold":503,"cat":"Large Blend","iss":"BlackRock","inc":"2000-05-15","price":"$582.80",
     "desc":"IVV is BlackRock's core S&P 500 tracking ETF with an ultra-low expense ratio. One of the three largest ETFs by assets under management globally.",
     "desc_zh":"IVV是贝莱德核心标普500追踪ETF，费率极低。按管理资产规模排名全球前三。",
     "top":[("AAPL",7.1),("MSFT",6.8),("NVDA",6.2),("AMZN",3.8),("GOOGL",2.1),("META",2.0),("BRK.B",1.8),("TSLA",1.6),("UNH",1.4),("JPM",1.3)],
     "sec":[("Technology",31.2),("Financials",13.4),("Healthcare",12.8),("Consumer Disc.",10.6),("Communication",9.1),("Industrials",8.7),("Consumer Stap.",5.9),("Energy",3.6)],
     "ret":{"1m":"+2.1%","3m":"+5.8%","6m":"+9.2%","1y":"+12.3%","3y":"+10.2%","5y":"+14.7%","10y":"+12.5%"}},
    {"t":"VGT","n":"Vanguard Information Technology ETF","n_zh":"先锋信息技术ETF","exp":"0.10%","yld":"0.58%","ytd":"+16.2%","aum":"$78B","pe":"30.2","beta":"1.18","hold":316,"cat":"Technology","iss":"Vanguard","inc":"2004-01-26","price":"$582.10",
     "desc":"VGT provides targeted exposure to the U.S. information technology sector. Includes hardware, software, and semiconductor companies.",
     "desc_zh":"VGT提供对美国信息技术行业的集中敞口，涵盖硬件、软件和半导体公司。",
     "top":[("AAPL",16.8),("MSFT",15.2),("NVDA",14.6),("AVGO",5.8),("CRM",2.4),("ACN",2.2),("ADBE",2.0),("AMD",1.8),("CSCO",1.6),("ORCL",1.5)],
     "sec":[("Software",36.4),("Semiconductors",28.6),("Hardware",18.2),("IT Services",16.8)],
     "ret":{"1m":"+3.4%","3m":"+8.2%","6m":"+13.1%","1y":"+16.2%","3y":"+11.8%","5y":"+19.4%","10y":"+18.6%"}},
    {"t":"ARKK","n":"ARK Innovation ETF","n_zh":"ARK创新ETF","exp":"0.75%","yld":"0.00%","ytd":"-2.4%","aum":"$6.8B","pe":"N/A","beta":"1.62","hold":35,"cat":"Large Growth","iss":"ARK Invest","inc":"2014-10-31","price":"$48.20",
     "desc":"ARKK is an actively managed ETF focused on disruptive innovation across genomics, automation, AI, fintech, and next-gen internet. High risk, high potential return.",
     "desc_zh":"ARKK是一只主动管理的ETF，专注于基因组学、自动化、AI、金融科技和下一代互联网领域的颠覆性创新。",
     "top":[("TSLA",10.2),("COIN",8.4),("ROKU",6.8),("SHOP",5.6),("SQ",5.2),("RBLX",4.8),("U",4.4),("PLTR",4.2),("TWLO",3.8),("ZM",3.6)],
     "sec":[("Technology",38.4),("Communication",22.6),("Healthcare",18.2),("Financials",12.4),("Consumer Disc.",8.4)],
     "ret":{"1m":"-1.2%","3m":"-3.4%","6m":"-0.8%","1y":"-2.4%","3y":"-18.6%","5y":"+2.4%","10y":"N/A"}},
    # More ETFs - adding 72 more
    {"t":"XLK","n":"Technology Select Sector SPDR","n_zh":"科技精选行业SPDR","exp":"0.09%","yld":"0.62%","ytd":"+15.4%","aum":"$72B","pe":"29.8","beta":"1.16","hold":64,"cat":"Technology","iss":"State Street","inc":"1998-12-16","price":"$228.40",
     "desc":"XLK tracks the Technology Select Sector Index, providing concentrated exposure to S&P 500 tech companies including Apple, Microsoft, and Nvidia.",
     "desc_zh":"XLK追踪科技精选行业指数，集中投资标普500科技公司。",
     "top":[("AAPL",21.2),("MSFT",19.8),("NVDA",18.4),("AVGO",5.2),("CRM",2.6),("ACN",2.4),("ADBE",2.2),("AMD",2.0),("CSCO",1.8),("ORCL",1.6)],
     "sec":[("Software",34.2),("Semiconductors",30.8),("Hardware",19.6),("IT Services",15.4)],
     "ret":{"1m":"+3.2%","3m":"+7.8%","6m":"+12.4%","1y":"+15.4%","3y":"+11.2%","5y":"+18.8%","10y":"+17.4%"}},
    {"t":"XLF","n":"Financial Select Sector SPDR","n_zh":"金融精选行业SPDR","exp":"0.09%","yld":"1.42%","ytd":"+8.6%","aum":"$42B","pe":"15.4","beta":"1.08","hold":72,"cat":"Financials","iss":"State Street","inc":"1998-12-16","price":"$44.80",
     "desc":"XLF provides exposure to U.S. financial sector companies including banks, insurance, and capital markets firms within the S&P 500.",
     "desc_zh":"XLF提供对美国金融行业的敞口，包括银行、保险和资本市场公司。",
     "top":[("BRK.B",13.2),("JPM",10.4),("V",7.8),("MA",6.4),("BAC",4.2),("WFC",3.6),("GS",3.2),("MS",2.8),("SCHW",2.4),("AXP",2.2)],
     "sec":[("Banks",28.4),("Capital Markets",22.6),("Insurance",18.4),("Financial Services",16.2),("Consumer Finance",14.4)],
     "ret":{"1m":"+1.8%","3m":"+4.2%","6m":"+6.8%","1y":"+8.6%","3y":"+9.4%","5y":"+11.2%","10y":"+10.8%"}},
    {"t":"XLE","n":"Energy Select Sector SPDR","n_zh":"能源精选行业SPDR","exp":"0.09%","yld":"3.28%","ytd":"-4.2%","aum":"$36B","pe":"12.4","beta":"1.22","hold":23,"cat":"Energy","iss":"State Street","inc":"1998-12-16","price":"$82.60",
     "desc":"XLE tracks the energy sector of the S&P 500, heavily weighted in integrated oil & gas and exploration companies.",
     "desc_zh":"XLE追踪标普500能源板块，主要投资于综合油气和勘探公司。",
     "top":[("XOM",22.8),("CVX",16.4),("COP",8.2),("EOG",5.4),("SLB",4.8),("MPC",4.2),("PSX",3.6),("PXD",3.2),("VLO",2.8),("OXY",2.6)],
     "sec":[("Integrated Oil & Gas",42.6),("Exploration & Production",24.8),("Refining",16.4),("Oil Services",12.2),("Pipeline",4.0)],
     "ret":{"1m":"-1.4%","3m":"-2.8%","6m":"-3.2%","1y":"-4.2%","3y":"+12.4%","5y":"+8.6%","10y":"+4.2%"}},
    {"t":"XLV","n":"Health Care Select Sector SPDR","n_zh":"医疗健康精选行业SPDR","exp":"0.09%","yld":"1.52%","ytd":"+4.8%","aum":"$38B","pe":"18.6","beta":"0.72","hold":60,"cat":"Healthcare","iss":"State Street","inc":"1998-12-16","price":"$148.20",
     "desc":"XLV provides exposure to S&P 500 healthcare companies including pharmaceuticals, biotech, medical devices, and health insurance.",
     "desc_zh":"XLV提供对标普500医疗健康公司的敞口，涵盖制药、生物科技、医疗器械和健康保险。",
     "top":[("LLY",12.4),("UNH",10.8),("JNJ",7.2),("MRK",5.8),("ABBV",5.4),("TMO",4.6),("ABT",4.2),("PFE",3.8),("DHR",3.4),("AMGN",3.2)],
     "sec":[("Pharma",36.8),("Health Insurance",18.4),("Medical Devices",16.2),("Biotech",14.6),("Life Sciences",14.0)],
     "ret":{"1m":"+0.6%","3m":"+2.4%","6m":"+3.6%","1y":"+4.8%","3y":"+6.2%","5y":"+8.4%","10y":"+10.2%"}},
    {"t":"DIA","n":"SPDR Dow Jones Industrial Average ETF","n_zh":"SPDR道琼斯工业平均ETF","exp":"0.16%","yld":"1.68%","ytd":"+8.2%","aum":"$36B","pe":"20.4","beta":"0.92","hold":30,"cat":"Large Value","iss":"State Street","inc":"1998-01-14","price":"$428.60",
     "desc":"DIA tracks the Dow Jones Industrial Average, consisting of 30 blue-chip U.S. stocks. A price-weighted index of America's largest companies.",
     "desc_zh":"DIA追踪道琼斯工业平均指数，由30只美国蓝筹股组成。",
     "top":[("UNH",9.8),("GS",7.4),("MSFT",6.2),("HD",5.8),("CAT",5.4),("AMGN",5.2),("V",4.8),("CRM",4.4),("MCD",4.2),("BA",3.8)],
     "sec":[("Healthcare",18.4),("Technology",17.6),("Financials",16.8),("Industrials",14.2),("Consumer Disc.",12.4),("Consumer Stap.",8.6)],
     "ret":{"1m":"+1.4%","3m":"+4.2%","6m":"+6.4%","1y":"+8.2%","3y":"+8.6%","5y":"+10.4%","10y":"+10.8%"}},
    {"t":"IWM","n":"iShares Russell 2000 ETF","n_zh":"iShares罗素2000 ETF","exp":"0.19%","yld":"1.14%","ytd":"+4.6%","aum":"$72B","pe":"24.8","beta":"1.24","hold":1974,"cat":"Small Blend","iss":"BlackRock","inc":"2000-05-22","price":"$218.40",
     "desc":"IWM tracks the Russell 2000 Index of small-cap U.S. stocks. Provides diversified exposure to smaller, growth-oriented companies.",
     "desc_zh":"IWM追踪罗素2000小盘股指数，提供对较小型成长导向公司的多元化敞口。",
     "top":[("SMCI",1.2),("ONTO",0.8),("SWAV",0.7),("FN",0.6),("CRDO",0.6),("CEIX",0.5),("LNTH",0.5),("CVNA",0.5),("ANF",0.5),("AFRM",0.4)],
     "sec":[("Healthcare",16.2),("Financials",15.8),("Industrials",15.4),("Technology",14.2),("Consumer Disc.",12.8),("Energy",6.4),("Real Estate",5.8)],
     "ret":{"1m":"+0.8%","3m":"+2.2%","6m":"+3.4%","1y":"+4.6%","3y":"+3.2%","5y":"+7.8%","10y":"+8.4%"}},
    {"t":"EFA","n":"iShares MSCI EAFE ETF","n_zh":"iShares MSCI EAFE ETF","exp":"0.32%","yld":"2.86%","ytd":"+6.8%","aum":"$62B","pe":"14.8","beta":"0.88","hold":782,"cat":"Foreign Large Blend","iss":"BlackRock","inc":"2001-08-14","price":"$82.40",
     "desc":"EFA tracks developed market stocks outside the U.S. and Canada, covering Europe, Australasia, and the Far East.",
     "desc_zh":"EFA追踪美国和加拿大以外的发达市场股票，覆盖欧洲、澳大拉西亚和远东地区。",
     "top":[("ASML",2.4),("NOVO",2.2),("SAP",1.8),("NESN",1.6),("SHEL",1.4),("AZN",1.4),("ROG",1.2),("LVMH",1.2),("TM",1.0),("HSBA",1.0)],
     "sec":[("Financials",18.6),("Industrials",14.8),("Healthcare",13.2),("Consumer Disc.",11.4),("Technology",10.8),("Consumer Stap.",9.6),("Materials",7.2)],
     "ret":{"1m":"+1.2%","3m":"+3.4%","6m":"+5.2%","1y":"+6.8%","3y":"+4.6%","5y":"+6.2%","10y":"+5.4%"}},
    {"t":"EEM","n":"iShares MSCI Emerging Markets ETF","n_zh":"iShares MSCI新兴市场ETF","exp":"0.68%","yld":"2.12%","ytd":"+3.2%","aum":"$22B","pe":"12.6","beta":"0.96","hold":1386,"cat":"Diversified Emerging","iss":"BlackRock","inc":"2003-04-07","price":"$42.80",
     "desc":"EEM provides exposure to large and mid-cap emerging market stocks across China, India, Taiwan, South Korea, and Brazil.",
     "desc_zh":"EEM提供对中国、印度、台湾、韩国和巴西等新兴市场大中盘股的敞口。",
     "top":[("TSM",8.4),("TCEHY",4.2),("BABA",3.1),("SMSN",2.8),("RELIANCE",1.4),("INFY",1.2),("PDD",1.1),("JD",0.9),("VALE",0.8),("ITUB",0.7)],
     "sec":[("Technology",22.4),("Financials",20.8),("Consumer Disc.",14.6),("Communication",10.2),("Materials",8.4),("Energy",6.8),("Industrials",6.2)],
     "ret":{"1m":"+0.4%","3m":"+1.8%","6m":"+2.4%","1y":"+3.2%","3y":"+1.4%","5y":"+3.6%","10y":"+4.2%"}},
    {"t":"AGG","n":"iShares Core U.S. Aggregate Bond ETF","n_zh":"iShares核心美国综合债券ETF","exp":"0.03%","yld":"4.28%","ytd":"+1.8%","aum":"$118B","pe":"N/A","beta":"0.04","hold":11942,"cat":"Intermediate Core Bond","iss":"BlackRock","inc":"2003-09-22","price":"$98.60",
     "desc":"AGG tracks the Bloomberg U.S. Aggregate Bond Index, providing broad exposure to U.S. investment-grade bonds. Core fixed-income holding.",
     "desc_zh":"AGG追踪彭博美国综合债券指数，提供对美国投资级债券的广泛敞口。是核心固收持仓选择。",
     "top":[],
     "sec":[("Treasury",42.6),("MBS",26.4),("Corporate",18.2),("Agency",8.4),("ABS",4.4)],
     "ret":{"1m":"+0.2%","3m":"+0.6%","6m":"+1.2%","1y":"+1.8%","3y":"-2.4%","5y":"+0.8%","10y":"+1.6%"}},
    {"t":"BND","n":"Vanguard Total Bond Market ETF","n_zh":"先锋全债市ETF","exp":"0.03%","yld":"4.32%","ytd":"+1.6%","aum":"$112B","pe":"N/A","beta":"0.04","hold":10148,"cat":"Intermediate Core Bond","iss":"Vanguard","inc":"2007-04-03","price":"$72.40",
     "desc":"BND tracks the Bloomberg U.S. Aggregate Float Adjusted Index. Vanguard's flagship bond ETF with broad U.S. fixed-income exposure.",
     "desc_zh":"BND追踪彭博美国综合浮动调整指数。先锋旗舰债券ETF。",
     "top":[],"sec":[("Treasury",44.2),("MBS",24.8),("Corporate",17.6),("Agency",8.2),("ABS",5.2)],
     "ret":{"1m":"+0.2%","3m":"+0.5%","6m":"+1.0%","1y":"+1.6%","3y":"-2.6%","5y":"+0.6%","10y":"+1.4%"}},
    {"t":"GLD","n":"SPDR Gold Shares","n_zh":"SPDR黄金ETF","exp":"0.40%","yld":"0.00%","ytd":"+14.8%","aum":"$68B","pe":"N/A","beta":"0.08","hold":1,"cat":"Commodities","iss":"State Street","inc":"2004-11-18","price":"$248.60",
     "desc":"GLD is backed by physical gold bullion held in vaults. The world's largest physically backed gold ETF, providing direct exposure to gold prices.",
     "desc_zh":"GLD以保管库中的实物金条作为支撑。全球最大的实物黄金ETF，提供对金价的直接敞口。",
     "top":[],"sec":[("Gold",100.0)],
     "ret":{"1m":"+4.2%","3m":"+8.6%","6m":"+12.4%","1y":"+14.8%","3y":"+8.2%","5y":"+10.6%","10y":"+6.8%"}},
    {"t":"TLT","n":"iShares 20+ Year Treasury Bond ETF","n_zh":"iShares 20+年国债ETF","exp":"0.15%","yld":"4.42%","ytd":"-2.8%","aum":"$48B","pe":"N/A","beta":"0.18","hold":42,"cat":"Long Government","iss":"BlackRock","inc":"2002-07-22","price":"$88.40",
     "desc":"TLT provides exposure to U.S. Treasury bonds with remaining maturities greater than 20 years. Highly sensitive to interest rate changes.",
     "desc_zh":"TLT提供对剩余期限超过20年的美国国债的敞口。对利率变化高度敏感。",
     "top":[],"sec":[("Long-Term Treasury",100.0)],
     "ret":{"1m":"-0.8%","3m":"-1.4%","6m":"-2.2%","1y":"-2.8%","3y":"-12.4%","5y":"-4.6%","10y":"-0.8%"}},
    {"t":"VNQ","n":"Vanguard Real Estate ETF","n_zh":"先锋房地产ETF","exp":"0.12%","yld":"3.82%","ytd":"+2.4%","aum":"$34B","pe":"32.4","beta":"0.92","hold":156,"cat":"Real Estate","iss":"Vanguard","inc":"2004-09-23","price":"$86.20",
     "desc":"VNQ tracks the MSCI US Investable Market Real Estate 25/50 Index. Provides diversified REIT exposure across commercial, residential, and specialty real estate.",
     "desc_zh":"VNQ追踪MSCI美国可投资市场房地产指数，提供多元化的REITs敞口。",
     "top":[("PLD",8.2),("AMT",6.4),("EQIX",5.8),("CCI",4.2),("SPG",3.6),("PSA",3.4),("O",3.2),("DLR",2.8),("WELL",2.6),("VICI",2.4)],
     "sec":[("Specialized REITs",32.4),("Industrial",14.8),("Residential",14.2),("Retail",12.6),("Office",8.4),("Healthcare",8.2),("Diversified",9.4)],
     "ret":{"1m":"+0.4%","3m":"+1.2%","6m":"+1.8%","1y":"+2.4%","3y":"-4.2%","5y":"+4.8%","10y":"+6.4%"}},
    {"t":"VXUS","n":"Vanguard Total International Stock ETF","n_zh":"先锋全国际股市ETF","exp":"0.07%","yld":"2.92%","ytd":"+5.8%","aum":"$72B","pe":"14.2","beta":"0.86","hold":8526,"cat":"Foreign Large Blend","iss":"Vanguard","inc":"2011-01-26","price":"$60.40",
     "desc":"VXUS provides exposure to stocks in developed and emerging markets outside the U.S. Covers over 8,000 stocks across 49 countries.",
     "desc_zh":"VXUS提供对美国以外发达市场和新兴市场股票的敞口，覆盖49个国家超过8000只股票。",
     "top":[("TSM",2.2),("ASML",1.4),("NOVO",1.2),("SAP",1.0),("NESN",0.9),("SHEL",0.8),("TCEHY",0.8),("AZN",0.7),("ROG",0.7),("SMSN",0.7)],
     "sec":[("Financials",18.4),("Industrials",13.6),("Technology",12.8),("Consumer Disc.",11.2),("Healthcare",10.4),("Consumer Stap.",8.6),("Materials",7.4)],
     "ret":{"1m":"+1.0%","3m":"+2.8%","6m":"+4.4%","1y":"+5.8%","3y":"+3.4%","5y":"+5.2%","10y":"+4.8%"}},
    {"t":"VIG","n":"Vanguard Dividend Appreciation ETF","n_zh":"先锋股息增长ETF","exp":"0.06%","yld":"1.72%","ytd":"+9.4%","aum":"$88B","pe":"21.8","beta":"0.86","hold":316,"cat":"Large Blend","iss":"Vanguard","inc":"2006-04-21","price":"$192.40",
     "desc":"VIG focuses on companies with a track record of increasing dividends for at least 10 consecutive years. Quality-oriented dividend growth strategy.",
     "desc_zh":"VIG专注于连续至少10年增加股息的公司。以质量为导向的股息增长策略。",
     "top":[("AAPL",4.8),("MSFT",4.4),("JPM",3.8),("UNH",3.4),("V",3.2),("MA",2.8),("HD",2.6),("PG",2.4),("AVGO",2.2),("JNJ",2.0)],
     "sec":[("Technology",24.6),("Financials",18.4),("Healthcare",16.2),("Industrials",14.8),("Consumer Disc.",10.4),("Consumer Stap.",8.2)],
     "ret":{"1m":"+1.6%","3m":"+4.4%","6m":"+7.2%","1y":"+9.4%","3y":"+8.6%","5y":"+11.2%","10y":"+10.8%"}},
    {"t":"JEPI","n":"JPMorgan Equity Premium Income ETF","n_zh":"摩根大通股权溢价收入ETF","exp":"0.35%","yld":"7.12%","ytd":"+4.2%","aum":"$36B","pe":"16.8","beta":"0.62","hold":120,"cat":"Large Value","iss":"JPMorgan","inc":"2020-05-20","price":"$58.40",
     "desc":"JEPI generates income through a combination of equity holdings and selling call options on the S&P 500. Popular for monthly income seekers.",
     "desc_zh":"JEPI通过持有股票和卖出标普500看涨期权的组合来产生收入。深受寻求月度收入的投资者欢迎。",
     "top":[("MSFT",2.4),("AMZN",1.8),("AAPL",1.6),("META",1.4),("GOOGL",1.2),("PG",1.0),("UNH",1.0),("HD",0.9),("V",0.9),("JNJ",0.8)],
     "sec":[("Technology",18.4),("Healthcare",14.6),("Financials",14.2),("Consumer Disc.",12.8),("Industrials",11.4),("Consumer Stap.",8.4)],
     "ret":{"1m":"+0.6%","3m":"+1.8%","6m":"+2.8%","1y":"+4.2%","3y":"+5.8%","5y":"N/A","10y":"N/A"}},
    {"t":"JEPQ","n":"JPMorgan Nasdaq Equity Premium Income ETF","n_zh":"摩根大通纳斯达克股权溢价收入ETF","exp":"0.35%","yld":"8.42%","ytd":"+6.8%","aum":"$18B","pe":"24.2","beta":"0.74","hold":82,"cat":"Large Growth","iss":"JPMorgan","inc":"2022-05-03","price":"$54.60",
     "desc":"JEPQ generates income by investing in Nasdaq-100 stocks while selling call options. Higher income potential with tech sector growth exposure.",
     "desc_zh":"JEPQ通过投资纳斯达克100股票并卖出看涨期权来产生收入。兼具高收入潜力和科技行业成长敞口。",
     "top":[("AAPL",8.2),("MSFT",7.4),("NVDA",6.8),("AMZN",5.2),("META",4.6),("AVGO",3.8),("GOOGL",2.6),("GOOG",2.4),("COST",2.2),("TSLA",2.0)],
     "sec":[("Technology",52.4),("Communication",16.8),("Consumer Disc.",14.2),("Healthcare",8.4),("Consumer Stap.",4.6)],
     "ret":{"1m":"+1.2%","3m":"+3.2%","6m":"+5.0%","1y":"+6.8%","3y":"N/A","5y":"N/A","10y":"N/A"}},
    {"t":"SOXX","n":"iShares Semiconductor ETF","n_zh":"iShares半导体ETF","exp":"0.35%","yld":"0.62%","ytd":"+18.4%","aum":"$14B","pe":"26.8","beta":"1.42","hold":30,"cat":"Technology","iss":"BlackRock","inc":"2001-07-10","price":"$262.40",
     "desc":"SOXX tracks the ICE Semiconductor Index, providing targeted exposure to U.S. semiconductor companies driving AI and computing innovation.",
     "desc_zh":"SOXX追踪ICE半导体指数，集中投资于推动AI和计算创新的美国半导体公司。",
     "top":[("NVDA",9.8),("AVGO",9.2),("AMD",7.4),("QCOM",6.8),("TXN",6.2),("INTC",4.8),("MRVL",4.4),("ADI",4.2),("MU",4.0),("LRCX",3.8)],
     "sec":[("Semiconductors",68.4),("Semiconductor Equipment",22.6),("EDA/IP",9.0)],
     "ret":{"1m":"+4.2%","3m":"+9.8%","6m":"+14.6%","1y":"+18.4%","3y":"+14.2%","5y":"+24.6%","10y":"+22.8%"}},
    {"t":"GDX","n":"VanEck Gold Miners ETF","n_zh":"VanEck黄金矿业ETF","exp":"0.51%","yld":"1.52%","ytd":"+22.4%","aum":"$14B","pe":"18.6","beta":"0.42","hold":52,"cat":"Equity Precious Metals","iss":"VanEck","inc":"2006-05-16","price":"$42.80",
     "desc":"GDX tracks the NYSE Arca Gold Miners Index, investing in gold mining companies. Leveraged play on gold prices with mining company operations.",
     "desc_zh":"GDX追踪纽约证券交易所Arca黄金矿业指数，投资于黄金开采公司。",
     "top":[("NEM",12.4),("GOLD",10.8),("AEM",8.2),("FNV",6.4),("WPM",6.2),("RGLD",4.8),("AGI",4.2),("KGC",3.8),("AU",3.4),("IAG",3.0)],
     "sec":[("Gold Mining",82.4),("Silver Mining",8.6),("Precious Metals Streaming",9.0)],
     "ret":{"1m":"+6.2%","3m":"+12.8%","6m":"+18.4%","1y":"+22.4%","3y":"+4.6%","5y":"+8.2%","10y":"+4.4%"}},
    {"t":"XBI","n":"SPDR S&P Biotech ETF","n_zh":"SPDR标普生物科技ETF","exp":"0.35%","yld":"0.00%","ytd":"+2.8%","aum":"$7.2B","pe":"N/A","beta":"1.18","hold":142,"cat":"Health","iss":"State Street","inc":"2006-01-31","price":"$92.40",
     "desc":"XBI is an equal-weighted biotech ETF providing exposure to S&P Biotechnology Select Industry Index. Higher allocation to small-cap biotech.",
     "desc_zh":"XBI是一只等权重生物科技ETF，提供对标普生物科技精选行业指数的敞口。",
     "top":[("VKTX",1.2),("MRNA",1.1),("REGN",1.0),("VRTX",1.0),("IONS",0.9),("PCVX",0.9),("ALNY",0.8),("BMRN",0.8),("EXAS",0.8),("SRPT",0.7)],
     "sec":[("Biotech",72.4),("Pharma",18.6),("Life Sciences",9.0)],
     "ret":{"1m":"+0.4%","3m":"+1.2%","6m":"+2.0%","1y":"+2.8%","3y":"-8.4%","5y":"+2.6%","10y":"+4.2%"}},
    {"t":"IBIT","n":"iShares Bitcoin Trust ETF","n_zh":"iShares比特币信托ETF","exp":"0.12%","yld":"0.00%","ytd":"+8.6%","aum":"$52B","pe":"N/A","beta":"1.82","hold":1,"cat":"Digital Assets","iss":"BlackRock","inc":"2024-01-11","price":"$54.20",
     "desc":"IBIT is BlackRock's spot Bitcoin ETF, providing direct exposure to Bitcoin price movements. The largest Bitcoin ETF by assets under management.",
     "desc_zh":"IBIT是贝莱德的现货比特币ETF，提供对比特币价格走势的直接敞口。按管理资产规模为最大的比特币ETF。",
     "top":[],"sec":[("Bitcoin",100.0)],
     "ret":{"1m":"+3.8%","3m":"+6.4%","6m":"+7.2%","1y":"+8.6%","3y":"N/A","5y":"N/A","10y":"N/A"}},
    {"t":"RSP","n":"Invesco S&P 500 Equal Weight ETF","n_zh":"景顺标普500等权重ETF","exp":"0.20%","yld":"1.48%","ytd":"+6.8%","aum":"$68B","pe":"18.4","beta":"0.96","hold":503,"cat":"Large Blend","iss":"Invesco","inc":"2003-04-24","price":"$174.20",
     "desc":"RSP holds the same S&P 500 stocks but in equal weights rather than cap-weighted. Reduces concentration risk in mega-cap tech stocks.",
     "desc_zh":"RSP持有相同的标普500股票但采用等权重。降低了超大型科技股的集中风险。",
     "top":[],
     "sec":[("Industrials",14.8),("Financials",14.4),("Healthcare",13.2),("Technology",12.6),("Consumer Disc.",11.8),("Consumer Stap.",7.4),("Real Estate",6.2)],
     "ret":{"1m":"+1.2%","3m":"+3.4%","6m":"+5.2%","1y":"+6.8%","3y":"+7.2%","5y":"+10.4%","10y":"+9.8%"}},
    {"t":"QUAL","n":"iShares MSCI USA Quality Factor ETF","n_zh":"iShares MSCI美国质量因子ETF","exp":"0.15%","yld":"1.18%","ytd":"+11.8%","aum":"$42B","pe":"23.4","beta":"0.94","hold":124,"cat":"Large Blend","iss":"BlackRock","inc":"2013-07-16","price":"$172.80",
     "desc":"QUAL targets U.S. stocks with high return on equity, stable earnings growth, and low financial leverage. Quality factor investing approach.",
     "desc_zh":"QUAL瞄准具有高净资产收益率、稳定盈利增长和低财务杠杆的美国股票。",
     "top":[("AAPL",8.2),("MSFT",7.6),("NVDA",6.4),("META",4.2),("V",3.4),("MA",2.8),("JNJ",2.4),("PG",2.2),("AVGO",2.0),("UNH",1.8)],
     "sec":[("Technology",32.4),("Healthcare",14.8),("Financials",13.2),("Communication",10.6),("Consumer Disc.",9.4),("Industrials",8.6)],
     "ret":{"1m":"+2.0%","3m":"+5.4%","6m":"+8.8%","1y":"+11.8%","3y":"+9.6%","5y":"+13.4%","10y":"+12.2%"}},
    {"t":"SMH","n":"VanEck Semiconductor ETF","n_zh":"VanEck半导体ETF","exp":"0.35%","yld":"0.48%","ytd":"+19.2%","aum":"$22B","pe":"28.4","beta":"1.48","hold":25,"cat":"Technology","iss":"VanEck","inc":"2011-12-20","price":"$284.60",
     "desc":"SMH is a concentrated semiconductor ETF tracking the MVIS US Listed Semiconductor 25 Index. Heavy allocation to top chip makers.",
     "desc_zh":"SMH是一只集中投资的半导体ETF，追踪MVIS美国上市半导体25指数。",
     "top":[("NVDA",20.4),("TSM",12.8),("AVGO",8.6),("AMD",5.4),("QCOM",4.8),("TXN",4.4),("ASML",4.2),("INTC",3.8),("MU",3.4),("LRCX",3.2)],
     "sec":[("Semiconductors",72.4),("Semiconductor Equipment",18.6),("EDA/IP",9.0)],
     "ret":{"1m":"+4.6%","3m":"+10.2%","6m":"+15.4%","1y":"+19.2%","3y":"+15.8%","5y":"+26.4%","10y":"+24.2%"}},
]

# Add more ETFs programmatically
_more_etfs = [
    ("XLI","Industrial Select Sector SPDR","工业精选行业SPDR","0.09%","1.24%","+7.4%","$18B","20.2","1.04",78,"Industrials","State Street","1998-12-16","$128.40","Tracks S&P 500 industrial sector companies.","追踪标普500工业板块。"),
    ("XLP","Consumer Staples Select Sector SPDR","必需消费品精选行业SPDR","0.09%","2.48%","+4.2%","$16B","22.4","0.62",36,"Consumer Staples","State Street","1998-12-16","$78.60","Provides exposure to S&P 500 consumer staples companies.","提供对标普500必需消费品公司的敞口。"),
    ("XLU","Utilities Select Sector SPDR","公用事业精选行业SPDR","0.09%","2.92%","+3.6%","$14B","18.8","0.48",30,"Utilities","State Street","1998-12-16","$72.40","Tracks the utilities sector of the S&P 500.","追踪标普500公用事业板块。"),
    ("XLB","Materials Select Sector SPDR","材料精选行业SPDR","0.09%","1.68%","+2.8%","$6B","16.4","0.98",28,"Materials","State Street","1998-12-16","$88.20","Provides exposure to S&P 500 materials sector.","提供对标普500材料板块的敞口。"),
    ("XLC","Communication Services Select Sector SPDR","通信服务精选行业SPDR","0.09%","0.72%","+14.2%","$18B","20.8","1.08",24,"Communication","State Street","2018-06-18","$86.40","Tracks S&P 500 communication services companies.","追踪标普500通信服务公司。"),
    ("XLRE","Real Estate Select Sector SPDR","房地产精选行业SPDR","0.09%","3.42%","+1.8%","$6B","34.2","0.86",30,"Real Estate","State Street","2015-10-07","$42.80","Provides exposure to S&P 500 REITs and real estate companies.","提供对标普500 REITs和房地产公司的敞口。"),
    ("IWF","iShares Russell 1000 Growth ETF","iShares罗素1000成长ETF","0.19%","0.52%","+14.8%","$88B","32.4","1.14",426,"Large Growth","BlackRock","2000-05-22","$342.60","Tracks Russell 1000 Growth Index of large-cap U.S. growth stocks.","追踪罗素1000成长指数。"),
    ("IWD","iShares Russell 1000 Value ETF","iShares罗素1000价值ETF","0.19%","1.82%","+6.2%","$58B","16.8","0.92",842,"Large Value","BlackRock","2000-05-22","$178.40","Tracks Russell 1000 Value Index of large-cap U.S. value stocks.","追踪罗素1000价值指数。"),
    ("VEA","Vanguard FTSE Developed Markets ETF","先锋富时发达市场ETF","0.05%","3.04%","+6.2%","$112B","14.6","0.84",4042,"Foreign Large Blend","Vanguard","2007-07-20","$52.40","Low-cost exposure to developed market stocks outside the U.S.","低成本投资美国以外的发达市场股票。"),
    ("VWO","Vanguard FTSE Emerging Markets ETF","先锋富时新兴市场ETF","0.08%","2.82%","+3.8%","$82B","12.8","0.92",5824,"Diversified Emerging","Vanguard","2005-03-04","$44.20","Broad exposure to emerging market stocks at a very low cost.","以极低成本广泛投资新兴市场股票。"),
    ("VYM","Vanguard High Dividend Yield ETF","先锋高红利ETF","0.06%","2.82%","+6.4%","$62B","16.4","0.84",442,"Large Value","Vanguard","2006-11-10","$118.40","Focuses on high dividend yield U.S. stocks.","专注于高股息收益率的美国股票。"),
    ("DGRO","iShares Core Dividend Growth ETF","iShares核心股息增长ETF","0.08%","2.18%","+7.8%","$28B","18.2","0.86",416,"Large Blend","BlackRock","2014-06-10","$58.40","Tracks U.S. stocks with sustained dividend growth history.","追踪具有持续股息增长历史的美国股票。"),
    ("SPLG","SPDR Portfolio S&P 500 ETF","SPDR投资组合标普500 ETF","0.02%","1.24%","+12.2%","$38B","22.6","1.0",503,"Large Blend","State Street","2005-11-08","$64.80","Ultra-low cost S&P 500 tracker from SPDR.","SPDR旗下超低费率标普500追踪基金。"),
    ("SPYG","SPDR Portfolio S&P 500 Growth ETF","SPDR投资组合标普500成长ETF","0.04%","0.68%","+14.4%","$24B","28.6","1.08",236,"Large Growth","State Street","2000-09-25","$78.40","Tracks S&P 500 growth companies at very low cost.","以极低费率追踪标普500成长公司。"),
    ("SPYV","SPDR Portfolio S&P 500 Value ETF","SPDR投资组合标普500价值ETF","0.04%","1.92%","+5.8%","$22B","16.2","0.94",436,"Large Value","State Street","2000-09-25","$48.60","Tracks S&P 500 value companies at very low cost.","以极低费率追踪标普500价值公司。"),
    ("VTV","Vanguard Value ETF","先锋价值ETF","0.04%","2.24%","+6.8%","$118B","17.4","0.88",342,"Large Value","Vanguard","2004-01-26","$164.20","Tracks CRSP US Large Cap Value Index with low expense.","以低费率追踪CRSP美国大盘价值指数。"),
    ("VUG","Vanguard Growth ETF","先锋成长ETF","0.04%","0.48%","+15.2%","$118B","32.8","1.12",218,"Large Growth","Vanguard","2004-01-26","$368.40","Tracks CRSP US Large Cap Growth Index.","追踪CRSP美国大盘成长指数。"),
    ("IJR","iShares Core S&P Small-Cap ETF","iShares核心标普小盘ETF","0.06%","1.28%","+3.8%","$82B","22.4","1.18",602,"Small Blend","BlackRock","2000-05-22","$108.40","Tracks S&P SmallCap 600 Index.","追踪标普小盘600指数。"),
    ("IJH","iShares Core S&P Mid-Cap ETF","iShares核心标普中盘ETF","0.05%","1.18%","+5.4%","$82B","18.6","1.08",402,"Mid-Cap Blend","BlackRock","2000-05-22","$288.40","Tracks S&P MidCap 400 Index.","追踪标普中盘400指数。"),
    ("MDY","SPDR S&P Midcap 400 ETF Trust","SPDR标普中盘400 ETF","0.23%","1.22%","+5.2%","$22B","18.4","1.06",402,"Mid-Cap Blend","State Street","1995-05-04","$528.40","Tracks S&P MidCap 400 for mid-cap U.S. stock exposure.","追踪标普中盘400指数。"),
    ("SDY","SPDR S&P Dividend ETF","SPDR标普红利ETF","0.35%","2.42%","+4.8%","$22B","17.8","0.82",132,"Large Value","State Street","2005-11-08","$138.40","Tracks S&P High Yield Dividend Aristocrats Index.","追踪标普高收益红利贵族指数。"),
    ("DVY","iShares Select Dividend ETF","iShares精选红利ETF","0.38%","3.28%","+3.2%","$22B","14.8","0.78",98,"Large Value","BlackRock","2003-11-03","$124.60","Focuses on high-yielding U.S. stocks.","专注于高收益率美国股票。"),
    ("PFF","iShares Preferred & Income Securities ETF","iShares优先股及收入证券ETF","0.46%","5.82%","+2.4%","$14B","N/A","0.24",482,"Preferred Stock","BlackRock","2007-03-26","$32.40","Provides exposure to U.S. preferred stocks.","提供对美国优先股的敞口。"),
    ("VCSH","Vanguard Short-Term Corporate Bond ETF","先锋短期公司债ETF","0.04%","4.62%","+1.4%","$42B","N/A","0.12",2284,"Short-Term Bond","Vanguard","2009-11-19","$78.40","Tracks short-term U.S. corporate bonds.","追踪美国短期公司债。"),
    ("VCIT","Vanguard Intermediate-Term Corporate Bond ETF","先锋中期公司债ETF","0.04%","4.82%","+1.8%","$48B","N/A","0.18",2042,"Corporate Bond","Vanguard","2009-11-19","$82.60","Tracks intermediate-term U.S. corporate bonds.","追踪美国中期公司债。"),
    ("TIP","iShares TIPS Bond ETF","iShares通胀保护债券ETF","0.19%","4.22%","+0.8%","$22B","N/A","0.06",52,"Inflation-Protected","BlackRock","2003-12-04","$108.40","Tracks U.S. Treasury inflation-protected securities.","追踪美国国债通胀保护证券。"),
    ("LQD","iShares iBoxx $ Investment Grade Corporate Bond ETF","iShares投资级公司债ETF","0.14%","4.92%","+1.2%","$34B","N/A","0.16",2684,"Corporate Bond","BlackRock","2002-07-22","$108.60","Tracks U.S. investment-grade corporate bonds.","追踪美国投资级公司债。"),
    ("HYG","iShares iBoxx $ High Yield Corporate Bond ETF","iShares高收益公司债ETF","0.49%","6.42%","+2.2%","$18B","N/A","0.28",1242,"High Yield Bond","BlackRock","2007-04-04","$78.40","Tracks U.S. high-yield corporate bonds.","追踪美国高收益公司债。"),
    ("SLV","iShares Silver Trust","iShares白银信托","0.50%","0.00%","+18.6%","$12B","N/A","0.12",1,"Commodities","BlackRock","2006-04-21","$28.40","Backed by physical silver. Direct silver price exposure.","以实物白银支撑，提供白银价格直接敞口。"),
    ("USO","United States Oil Fund","美国石油基金","0.60%","0.00%","-8.4%","$2.8B","N/A","0.48",1,"Commodities","USCF","2006-04-10","$68.40","Tracks WTI crude oil futures.","追踪WTI原油期货。"),
    ("BNDX","Vanguard Total International Bond ETF","先锋全国际债券ETF","0.07%","3.82%","+1.2%","$48B","N/A","0.06",6842,"World Bond","Vanguard","2013-05-31","$48.60","Broad international bond exposure hedged to USD.","广泛的国际债券敞口，对冲至美元。"),
    ("EMB","iShares J.P. Morgan USD Emerging Markets Bond ETF","iShares新兴市场债券ETF","0.39%","5.82%","+2.8%","$14B","N/A","0.32",584,"Emerging Markets Bond","BlackRock","2007-12-17","$88.40","Tracks USD-denominated emerging market government bonds.","追踪以美元计价的新兴市场政府债券。"),
    ("ETHE","iShares Ethereum Trust ETF","iShares以太坊信托ETF","0.12%","0.00%","+4.2%","$8.4B","N/A","1.96",1,"Digital Assets","BlackRock","2024-07-23","$22.40","Spot Ethereum ETF from BlackRock.","贝莱德旗下现货以太坊ETF。"),
    ("ARKW","ARK Next Generation Internet ETF","ARK下一代互联网ETF","0.88%","0.00%","+1.8%","$1.4B","N/A","1.48",38,"Technology","ARK Invest","2014-09-30","$78.40","Actively managed ETF focused on next-gen internet companies.","专注于下一代互联网公司的主动管理ETF。"),
    ("ARKG","ARK Genomic Revolution ETF","ARK基因组革命ETF","0.75%","0.00%","-4.2%","$1.8B","N/A","1.24",32,"Health","ARK Invest","2014-10-31","$32.40","Focused on genomics, CRISPR, and biotech innovation.","专注于基因组学、CRISPR和生物科技创新。"),
    ("IBB","iShares Biotechnology ETF","iShares生物科技ETF","0.44%","0.22%","+3.4%","$8.2B","24.6","1.02",282,"Health","BlackRock","2001-02-05","$142.60","Tracks the ICE Biotechnology Index.","追踪ICE生物科技指数。"),
    ("KWEB","KraneShares CSI China Internet ETF","KraneShares中国互联网ETF","0.68%","0.42%","+8.4%","$6.8B","22.4","0.82",42,"China","KraneShares","2013-07-31","$32.40","Tracks Chinese internet and tech companies.","追踪中国互联网和科技公司。"),
    ("FXI","iShares China Large-Cap ETF","iShares中国大盘ETF","0.74%","2.18%","+6.2%","$6.4B","10.8","0.78",50,"China","BlackRock","2004-10-05","$28.60","Tracks the 50 largest Chinese stocks.","追踪50只最大的中国股票。"),
    ("INDA","iShares MSCI India ETF","iShares MSCI印度ETF","0.64%","0.42%","+2.4%","$8.2B","24.8","0.82",142,"India","BlackRock","2012-02-02","$52.40","Tracks large and mid-cap Indian stocks.","追踪印度大中盘股。"),
    ("EWJ","iShares MSCI Japan ETF","iShares MSCI日本ETF","0.50%","1.82%","+4.8%","$14B","14.2","0.72",238,"Japan","BlackRock","1996-03-12","$68.40","Tracks large and mid-cap Japanese stocks.","追踪日本大中盘股。"),
    ("EWZ","iShares MSCI Brazil ETF","iShares MSCI巴西ETF","0.58%","8.42%","-2.4%","$4.8B","8.2","1.12",52,"Brazil","BlackRock","2000-07-10","$28.40","Tracks large and mid-cap Brazilian stocks.","追踪巴西大中盘股。"),
    ("EWG","iShares MSCI Germany ETF","iShares MSCI德国ETF","0.50%","2.62%","+8.4%","$2.8B","12.8","0.92",62,"Germany","BlackRock","1996-03-12","$32.60","Tracks large and mid-cap German stocks.","追踪德国大中盘股。"),
    ("EWU","iShares MSCI United Kingdom ETF","iShares MSCI英国ETF","0.50%","3.82%","+5.2%","$2.4B","11.4","0.82",82,"UK","BlackRock","1996-03-12","$34.80","Tracks large and mid-cap UK stocks.","追踪英国大中盘股。"),
    ("NOBL","ProShares S&P 500 Dividend Aristocrats","ProShares标普500红利贵族","0.35%","2.04%","+5.6%","$12B","20.4","0.84",68,"Large Value","ProShares","2013-10-09","$98.40","Tracks S&P 500 companies with 25+ years of dividend increases.","追踪连续25年以上增加股息的标普500公司。"),
    ("MTUM","iShares MSCI USA Momentum Factor ETF","iShares MSCI美国动量因子ETF","0.15%","0.82%","+16.4%","$14B","26.8","1.12",124,"Large Growth","BlackRock","2013-04-16","$202.40","Targets U.S. stocks exhibiting strong price momentum.","瞄准展现强劲价格动量的美国股票。"),
    ("USMV","iShares MSCI USA Min Vol Factor ETF","iShares MSCI美国最低波动率ETF","0.15%","1.62%","+6.2%","$28B","20.4","0.72",176,"Large Blend","BlackRock","2011-10-18","$82.40","Targets lower volatility U.S. stocks.","瞄准较低波动率的美国股票。"),
    ("SPTM","SPDR Portfolio S&P 1500 Composite Stock Market ETF","SPDR投资组合标普1500复合ETF","0.03%","1.22%","+10.8%","$8B","22.2","1.0",1502,"Large Blend","State Street","2000-10-04","$68.40","Ultra-low cost total U.S. market tracker.","超低费率美国全市场追踪基金。"),
    ("ARKF","ARK Fintech Innovation ETF","ARK金融科技创新ETF","0.75%","0.00%","+2.8%","$0.8B","N/A","1.36",36,"Financials","ARK Invest","2019-02-04","$24.60","Focused on fintech, blockchain, and digital payment innovation.","专注于金融科技、区块链和数字支付创新。"),
    ("MCHI","iShares MSCI China ETF","iShares MSCI中国ETF","0.58%","1.82%","+7.2%","$5.8B","12.4","0.82",628,"China","BlackRock","2011-03-29","$48.20","Broad exposure to Chinese large and mid-cap stocks.","广泛投资中国大中盘股。"),
]

for t,n,nz,exp,yld,ytd,aum,pe,beta,hold,cat,iss,inc,price,desc,desc_zh in _more_etfs:
    ETFS.append({"t":t,"n":n,"n_zh":nz,"exp":exp,"yld":yld,"ytd":ytd,"aum":aum,"pe":pe,"beta":beta,"hold":hold,"cat":cat,"iss":iss,"inc":inc,"price":price,
     "desc":desc,"desc_zh":desc_zh,
     "top":[],"sec":[("Primary",60.0),("Secondary",25.0),("Other",15.0)],
     "ret":{"1m":"+1.0%","3m":"+2.5%","6m":"+4.0%","1y":ytd,"3y":"+6.0%","5y":"+8.0%","10y":"+7.0%"}})

print(f"ETF data: {len(ETFS)} ETFs")

# ============================================================
# STOCKS DATA
# ============================================================
STOCKS = [
    {"t":"AAPL","n":"Apple Inc.","n_zh":"苹果公司","p":"$228.52","ch":"+1.34%","sec":"Technology","ind":"Consumer Electronics","emp":"164K","founded":"1976","hq":"Cupertino, CA","ceo":"Tim Cook","mcap":"$3.48T","pe":"33.2","ps":"8.9","pb":"52.4","rev":"$391B","rg":"+6.1%","eps":"$6.88","dy":"1.0%","beta":"1.21",
     "desc":"Apple designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The iPhone, Mac, iPad, Apple Watch, and services ecosystem generate over $390B in annual revenue.",
     "desc_zh":"苹果公司设计、制造和销售智能手机、个人电脑、平板电脑、可穿戴设备。iPhone、Mac、iPad、Apple Watch及服务生态系统年收入超过3900亿美元。",
     "qr":[("Q1'26","$124.3B",120),("Q4'25","$94.9B",92),("Q3'25","$85.8B",83),("Q2'25","$90.8B",88)]},
    {"t":"NVDA","n":"NVIDIA Corporation","n_zh":"英伟达","p":"$878.40","ch":"+2.86%","sec":"Technology","ind":"Semiconductors","emp":"32K","founded":"1993","hq":"Santa Clara, CA","ceo":"Jensen Huang","mcap":"$2.16T","pe":"62.4","ps":"36.2","pb":"48.6","rev":"$60.9B","rg":"+122%","eps":"$14.08","dy":"0.02%","beta":"1.68",
     "desc":"NVIDIA designs GPUs and accelerated computing platforms that power AI, gaming, data centers, and autonomous vehicles. The undisputed leader in AI training hardware.",
     "desc_zh":"英伟达设计GPU和加速计算平台，为AI、游戏、数据中心和自动驾驶提供算力。AI训练硬件的无可争议的领导者。",
     "qr":[("Q4'26","$22.1B",120),("Q3'26","$18.1B",98),("Q2'26","$13.5B",73),("Q1'26","$7.2B",39)]},
    {"t":"MSFT","n":"Microsoft Corporation","n_zh":"微软","p":"$428.60","ch":"+0.82%","sec":"Technology","ind":"Software","emp":"221K","founded":"1975","hq":"Redmond, WA","ceo":"Satya Nadella","mcap":"$3.18T","pe":"36.8","ps":"13.6","pb":"12.4","rev":"$236B","rg":"+16%","eps":"$11.64","dy":"0.72%","beta":"0.92",
     "desc":"Microsoft develops software, cloud computing (Azure), and AI solutions. Azure, Office 365, LinkedIn, and Xbox drive diversified revenue streams.",
     "desc_zh":"微软开发软件、云计算(Azure)和AI解决方案。Azure、Office 365、LinkedIn和Xbox推动多元化收入。",
     "qr":[("Q2'26","$69.6B",120),("Q1'26","$65.6B",113),("Q4'25","$56.5B",97),("Q3'25","$52.9B",91)]},
    {"t":"GOOGL","n":"Alphabet Inc.","n_zh":"谷歌母公司Alphabet","p":"$178.40","ch":"+1.12%","sec":"Communication","ind":"Internet Services","emp":"182K","founded":"1998","hq":"Mountain View, CA","ceo":"Sundar Pichai","mcap":"$2.18T","pe":"24.6","ps":"7.2","pb":"6.8","rev":"$340B","rg":"+14%","eps":"$7.26","dy":"0.48%","beta":"1.06",
     "desc":"Alphabet operates Google Search, YouTube, Android, Google Cloud, and Waymo. Dominant in digital advertising with growing cloud and AI revenue.",
     "desc_zh":"Alphabet运营谷歌搜索、YouTube、Android、谷歌云和Waymo。数字广告领域占据主导地位，云和AI收入持续增长。",
     "qr":[("Q4'25","$96.5B",120),("Q3'25","$88.3B",110),("Q2'25","$84.7B",105),("Q1'25","$80.5B",100)]},
    {"t":"AMZN","n":"Amazon.com Inc.","n_zh":"亚马逊","p":"$198.60","ch":"+1.56%","sec":"Consumer Disc.","ind":"E-Commerce","emp":"1540K","founded":"1994","hq":"Seattle, WA","ceo":"Andy Jassy","mcap":"$2.06T","pe":"58.4","ps":"3.4","pb":"8.2","rev":"$604B","rg":"+12%","eps":"$3.40","dy":"0.00%","beta":"1.18",
     "desc":"Amazon operates the world's largest e-commerce platform, AWS cloud computing, Prime Video, and advertising business. AWS is the leading cloud provider globally.",
     "desc_zh":"亚马逊运营全球最大的电子商务平台、AWS云计算、Prime Video和广告业务。AWS是全球领先的云服务提供商。",
     "qr":[("Q4'25","$170.0B",120),("Q3'25","$158.9B",112),("Q2'25","$148.0B",104),("Q1'25","$143.3B",101)]},
    {"t":"META","n":"Meta Platforms Inc.","n_zh":"Meta平台(脸书)","p":"$568.40","ch":"+2.14%","sec":"Communication","ind":"Social Media","emp":"72K","founded":"2004","hq":"Menlo Park, CA","ceo":"Mark Zuckerberg","mcap":"$1.44T","pe":"28.4","ps":"9.6","pb":"8.4","rev":"$150B","rg":"+22%","eps":"$20.00","dy":"0.36%","beta":"1.24",
     "desc":"Meta operates Facebook, Instagram, WhatsApp, and Messenger, serving over 3.9 billion monthly users. Heavily investing in AI and metaverse technology.",
     "desc_zh":"Meta运营Facebook、Instagram、WhatsApp和Messenger，月活用户超39亿。大力投资AI和元宇宙技术。",
     "qr":[("Q4'25","$42.0B",120),("Q3'25","$40.6B",116),("Q2'25","$39.1B",112),("Q1'25","$36.5B",104)]},
    {"t":"TSLA","n":"Tesla Inc.","n_zh":"特斯拉","p":"$248.40","ch":"-1.82%","sec":"Consumer Disc.","ind":"Auto Manufacturers","emp":"128K","founded":"2003","hq":"Austin, TX","ceo":"Elon Musk","mcap":"$782B","pe":"68.4","ps":"8.2","pb":"14.6","rev":"$96.8B","rg":"+8%","eps":"$3.63","dy":"0.00%","beta":"2.04",
     "desc":"Tesla designs, manufactures, and sells electric vehicles, energy storage, and solar products. Leader in EV market with growing energy and AI robotaxi business.",
     "desc_zh":"特斯拉设计、制造和销售电动汽车、储能和太阳能产品。电动汽车市场领导者，能源和AI自动驾驶出租车业务持续增长。",
     "qr":[("Q4'25","$25.7B",120),("Q3'25","$25.2B",118),("Q2'25","$24.9B",116),("Q1'25","$21.3B",100)]},
    {"t":"JPM","n":"JPMorgan Chase & Co.","n_zh":"摩根大通","p":"$228.40","ch":"+0.64%","sec":"Financials","ind":"Banks","emp":"309K","founded":"1799","hq":"New York, NY","ceo":"Jamie Dimon","mcap":"$658B","pe":"12.8","ps":"3.8","pb":"2.2","rev":"$172B","rg":"+10%","eps":"$17.84","dy":"2.12%","beta":"1.08",
     "desc":"JPMorgan Chase is the largest U.S. bank by assets. Diversified across investment banking, consumer banking, asset management, and commercial banking.",
     "desc_zh":"摩根大通是按资产计美国最大的银行。业务横跨投资银行、消费银行、资产管理和商业银行。",
     "qr":[("Q4'25","$44.2B",120),("Q3'25","$42.8B",116),("Q2'25","$41.3B",112),("Q1'25","$40.1B",109)]},
]

# More stocks
_more_stocks = [
    ("BRK.B","Berkshire Hathaway","伯克希尔·哈撒韦","$448.60","+0.42%","Financials","Conglomerates","396K","1839","Omaha, NE","Warren Buffett","$982B","22.4","2.8","1.6","$364B","+8%","$20.02","0.00%","0.62"),
    ("V","Visa Inc.","Visa","$308.40","+0.86%","Financials","Payment Services","30K","1958","San Francisco, CA","Ryan McInerney","$612B","32.4","18.6","14.8","$34.8B","+10%","$9.52","0.74%","0.96"),
    ("UNH","UnitedHealth Group","联合健康集团","$548.60","-0.42%","Healthcare","Health Insurance","400K","1977","Minnetonka, MN","Andrew Witty","$502B","22.8","1.4","6.8","$372B","+12%","$24.04","1.42%","0.72"),
    ("JNJ","Johnson & Johnson","强生","$158.40","+0.28%","Healthcare","Pharma","132K","1886","New Brunswick, NJ","Joaquin Duato","$382B","16.4","4.6","6.2","$85.2B","+4%","$9.66","2.82%","0.52"),
    ("WMT","Walmart Inc.","沃尔玛","$82.40","+0.62%","Consumer Stap.","Retail","2100K","1962","Bentonville, AR","Doug McMillon","$662B","36.8","1.0","8.2","$648B","+6%","$2.24","1.08%","0.52"),
    ("XOM","Exxon Mobil","埃克森美孚","$108.60","-0.84%","Energy","Oil & Gas","62K","1870","Spring, TX","Darren Woods","$448B","12.4","1.2","2.0","$344B","-4%","$8.76","3.42%","0.82"),
    ("MA","Mastercard","万事达卡","$528.40","+0.92%","Financials","Payment Services","33K","1966","Purchase, NY","Michael Miebach","$482B","36.8","22.4","68.2","$27.4B","+12%","$14.36","0.52%","1.02"),
    ("PG","Procter & Gamble","宝洁","$168.40","+0.18%","Consumer Stap.","Consumer Products","107K","1837","Cincinnati, OH","Jon Moeller","$398B","26.4","4.8","8.2","$84.0B","+2%","$6.38","2.34%","0.42"),
    ("HD","Home Depot","家得宝","$382.40","+0.46%","Consumer Disc.","Home Improvement","475K","1978","Atlanta, GA","Ted Decker","$382B","24.8","2.4","162.4","$157B","+4%","$15.42","2.28%","1.02"),
    ("CVX","Chevron","雪佛龙","$152.40","-0.62%","Energy","Oil & Gas","43K","1879","San Ramon, CA","Mike Wirth","$282B","14.2","1.4","2.0","$196B","-6%","$10.72","4.08%","0.92"),
    ("MRK","Merck & Co.","默克","$128.40","+0.34%","Healthcare","Pharma","68K","1891","Rahway, NJ","Robert Davis","$324B","24.6","5.4","7.2","$60.1B","+8%","$5.22","2.42%","0.42"),
    ("ABBV","AbbVie","艾伯维","$178.40","+0.52%","Healthcare","Pharma","50K","2013","North Chicago, IL","Robert Michael","$314B","22.8","5.6","32.4","$56.3B","+6%","$7.82","3.62%","0.62"),
    ("KO","Coca-Cola","可口可乐","$62.40","+0.16%","Consumer Stap.","Beverages","79K","1886","Atlanta, GA","James Quincey","$268B","24.2","6.0","10.4","$45.8B","+4%","$2.58","2.86%","0.58"),
    ("PEP","PepsiCo","百事","$148.60","-0.22%","Consumer Stap.","Beverages","315K","1898","Purchase, NY","Ramon Laguarta","$202B","22.8","2.4","12.8","$91.5B","+2%","$6.52","3.12%","0.58"),
    ("COST","Costco","好市多","$948.40","+1.04%","Consumer Stap.","Retail","316K","1983","Issaquah, WA","Ron Vachris","$420B","52.4","1.8","16.8","$254B","+8%","$18.08","0.52%","0.82"),
    ("AVGO","Broadcom","博通","$192.40","+2.42%","Technology","Semiconductors","20K","1961","San Jose, CA","Hock Tan","$892B","68.4","16.8","12.4","$52.4B","+44%","$2.81","1.22%","1.28"),
    ("LLY","Eli Lilly","礼来","$862.40","+1.86%","Healthcare","Pharma","43K","1876","Indianapolis, IN","David Ricks","$818B","82.4","22.4","52.6","$41.3B","+32%","$10.46","0.62%","0.42"),
    ("TMO","Thermo Fisher Scientific","赛默飞世尔","$548.60","+0.42%","Healthcare","Life Sciences","125K","1956","Waltham, MA","Marc Casper","$208B","32.4","4.8","4.2","$42.9B","+2%","$16.92","0.22%","0.82"),
    ("MCD","McDonald's","麦当劳","$298.40","+0.28%","Consumer Disc.","Restaurants","150K","1940","Chicago, IL","Chris Kempczinski","$212B","24.6","8.4","N/A","$25.5B","+4%","$12.14","2.22%","0.72"),
    ("CSCO","Cisco Systems","思科","$58.40","+0.42%","Technology","Networking","84K","1984","San Jose, CA","Chuck Robbins","$238B","18.4","4.4","5.2","$54.2B","+6%","$3.18","2.68%","0.92"),
    ("CRM","Salesforce","Salesforce","$298.40","+1.24%","Technology","Software","73K","1999","San Francisco, CA","Marc Benioff","$288B","42.6","8.4","4.8","$34.9B","+10%","$7.01","0.52%","1.18"),
    ("ACN","Accenture","埃森哲","$328.40","+0.36%","Technology","IT Services","738K","1989","Dublin, Ireland","Julie Sweet","$208B","28.4","3.2","8.2","$64.9B","+4%","$11.56","1.52%","1.12"),
    ("ABT","Abbott Laboratories","雅培","$118.40","+0.28%","Healthcare","Medical Devices","114K","1888","Abbott Park, IL","Robert Ford","$202B","28.6","4.8","5.4","$40.1B","+6%","$4.14","1.82%","0.72"),
    ("NFLX","Netflix","奈飞","$948.60","+2.14%","Communication","Streaming","13K","1997","Los Gatos, CA","Ted Sarandos","$408B","42.4","10.8","14.2","$38.4B","+16%","$22.36","0.00%","1.42"),
    ("AMD","Advanced Micro Devices","超威半导体","$168.40","+3.14%","Technology","Semiconductors","26K","1969","Santa Clara, CA","Lisa Su","$268B","48.6","10.4","4.8","$25.8B","+18%","$3.46","0.00%","1.62"),
    ("INTC","Intel Corporation","英特尔","$22.40","-1.82%","Technology","Semiconductors","110K","1968","Santa Clara, CA","Pat Gelsinger","$94B","N/A","1.7","1.2","$54.2B","-8%","$-0.42","1.42%","1.12"),
    ("QCOM","Qualcomm","高通","$178.40","+1.42%","Technology","Semiconductors","51K","1985","San Diego, CA","Cristiano Amon","$198B","18.6","5.2","8.4","$38.6B","+8%","$9.58","1.82%","1.32"),
    ("TXN","Texas Instruments","德州仪器","$188.40","+0.62%","Technology","Semiconductors","34K","1951","Dallas, TX","Haviv Ilan","$174B","32.4","10.4","12.6","$16.8B","-4%","$5.81","2.62%","1.08"),
    ("ORCL","Oracle Corporation","甲骨文","$178.40","+1.86%","Technology","Software","164K","1977","Austin, TX","Safra Catz","$492B","38.4","9.4","48.2","$52.8B","+12%","$4.64","1.08%","1.02"),
    ("IBM","IBM","IBM","$228.40","+0.42%","Technology","IT Services","288K","1911","Armonk, NY","Arvind Krishna","$212B","22.8","3.4","8.2","$62.4B","+4%","$10.02","3.12%","0.82"),
    ("ADBE","Adobe","Adobe","$448.40","+1.24%","Technology","Software","30K","1982","San Jose, CA","Shantanu Narayen","$198B","42.6","10.2","18.4","$19.4B","+10%","$10.52","0.00%","1.28"),
    ("PYPL","PayPal","PayPal","$78.40","+1.62%","Financials","Digital Payments","26K","1998","San Jose, CA","Alex Chriss","$82B","18.4","2.6","4.2","$31.8B","+8%","$4.26","0.00%","1.42"),
    ("UBER","Uber Technologies","优步","$78.60","+1.86%","Technology","Ride-Sharing","32K","2009","San Francisco, CA","Dara Khosrowshahi","$162B","68.4","4.2","14.6","$40.1B","+16%","$1.15","0.00%","1.52"),
    ("COIN","Coinbase Global","Coinbase","$248.40","+4.28%","Financials","Crypto Exchange","3500","2012","San Francisco, CA","Brian Armstrong","$62B","32.4","8.2","6.4","$7.6B","+84%","$7.66","0.00%","2.82"),
    ("PLTR","Palantir Technologies","Palantir","$28.40","+3.42%","Technology","Software","3800","2003","Denver, CO","Alex Karp","$62B","168.4","24.2","18.4","$2.6B","+24%","$0.17","0.00%","2.12"),
    ("SNOW","Snowflake","Snowflake","$178.40","+2.28%","Technology","Cloud Computing","5900","2012","Bozeman, MT","Sridhar Ramaswamy","$58B","N/A","18.4","8.2","$3.2B","+28%","$-0.42","0.00%","1.82"),
    ("NET","Cloudflare","Cloudflare","$108.40","+2.86%","Technology","Cloud Networking","3800","2009","San Francisco, CA","Matthew Prince","$36B","N/A","22.4","32.6","$1.6B","+30%","$-0.02","0.00%","1.72"),
    ("CRWD","CrowdStrike","CrowdStrike","$368.40","+1.86%","Technology","Cybersecurity","8800","2011","Austin, TX","George Kurtz","$88B","68.4","22.4","28.6","$3.9B","+32%","$5.39","0.00%","1.42"),
    ("PANW","Palo Alto Networks","Palo Alto Networks","$188.40","+1.42%","Technology","Cybersecurity","15K","2005","Santa Clara, CA","Nikesh Arora","$62B","52.4","8.8","22.4","$7.1B","+16%","$3.61","0.00%","1.28"),
    ("NOW","ServiceNow","ServiceNow","$898.40","+1.62%","Technology","Software","22K","2004","Santa Clara, CA","Bill McDermott","$182B","72.4","18.8","28.4","$10.0B","+22%","$12.42","0.00%","1.12"),
    ("GM","General Motors","通用汽车","$48.60","+0.82%","Consumer Disc.","Auto Manufacturers","163K","1908","Detroit, MI","Mary Barra","$54B","6.2","0.3","1.2","$172B","+4%","$7.84","0.82%","1.24"),
    ("F","Ford Motor","福特汽车","$11.20","-0.42%","Consumer Disc.","Auto Manufacturers","177K","1903","Dearborn, MI","Jim Farley","$44B","8.4","0.3","1.4","$176B","+2%","$1.33","4.82%","1.32"),
    ("BA","Boeing","波音","$188.40","-0.62%","Industrials","Aerospace","171K","1916","Arlington, VA","Kelly Ortberg","$112B","N/A","1.4","N/A","$78.1B","+12%","$-4.42","0.00%","1.42"),
    ("CAT","Caterpillar","卡特彼勒","$378.40","+0.42%","Industrials","Machinery","114K","1925","Irving, TX","Jim Umpleby","$182B","18.4","2.8","14.2","$65.7B","+2%","$20.56","1.52%","1.08"),
    ("GE","GE Aerospace","通用电气航空","$198.40","+0.86%","Industrials","Aerospace","52K","1892","Cincinnati, OH","Larry Culp","$214B","38.4","5.6","12.8","$38.2B","+18%","$5.16","0.58%","1.12"),
    ("RTX","RTX Corporation","RTX(雷神技术)","$128.40","+0.28%","Industrials","Defense","185K","1922","Arlington, VA","Christopher Calio","$168B","32.4","2.4","3.2","$71.6B","+8%","$3.96","2.02%","0.68"),
    ("LMT","Lockheed Martin","洛克希德·马丁","$468.40","+0.42%","Industrials","Defense","116K","1926","Bethesda, MD","Jim Taiclet","$112B","18.4","1.6","14.2","$71.0B","+6%","$25.46","2.52%","0.48"),
    ("HON","Honeywell","霍尼韦尔","$208.40","+0.34%","Industrials","Conglomerates","97K","1906","Charlotte, NC","Vimal Kapur","$138B","22.4","3.6","7.2","$36.7B","+4%","$9.30","1.98%","0.92"),
    ("NEE","NextEra Energy","NextEra能源","$78.40","+0.52%","Utilities","Utilities","15K","1925","Juno Beach, FL","John Ketchum","$158B","28.4","7.8","3.4","$24.8B","+10%","$2.76","2.52%","0.52"),
    ("PLD","Prologis","Prologis","$118.40","+0.28%","Real Estate","Industrial REITs","2300","1983","San Francisco, CA","Hamid Moghadam","$108B","42.4","14.2","2.2","$8.1B","+8%","$2.79","3.22%","0.82"),
    ("AMT","American Tower","美国电塔","$208.40","+0.42%","Real Estate","Cell Tower REITs","6100","1995","Boston, MA","Steven Vondran","$96B","38.4","8.4","12.8","$11.1B","+4%","$5.42","2.92%","0.72"),
    ("BX","Blackstone","黑石集团","$168.40","+1.42%","Financials","Asset Management","4700","1985","New York, NY","Steve Schwarzman","$202B","42.4","28.6","18.4","$7.2B","+18%","$3.98","2.28%","1.42"),
    ("GOLD","Barrick Gold","巴里克黄金","$22.40","+2.86%","Materials","Gold Mining","21K","1983","Toronto, Canada","Mark Bristow","$38B","16.4","4.2","1.8","$9.1B","+12%","$1.37","2.04%","0.42"),
    ("NEM","Newmont Corp","纽蒙特矿业","$52.40","+2.42%","Materials","Gold Mining","31K","1916","Denver, CO","Tom Palmer","$62B","18.2","5.4","1.6","$11.5B","+14%","$2.88","1.82%","0.48"),
    ("FSLR","First Solar","第一太阳能","$188.40","+1.86%","Technology","Solar Energy","7200","1999","Tempe, AZ","Mark Widmar","$20B","14.8","4.8","2.4","$4.2B","+28%","$12.73","0.00%","1.42"),
]

for t,n,nz,p,ch,sec,ind,emp,founded,hq,ceo,mcap,pe,ps,pb,rev,rg,eps,dy,beta in _more_stocks:
    STOCKS.append({"t":t,"n":n,"n_zh":nz,"p":p,"ch":ch,"sec":sec,"ind":ind,"emp":emp,"founded":founded,"hq":hq,"ceo":ceo,"mcap":mcap,"pe":pe,"ps":ps,"pb":pb,"rev":rev,"rg":rg,"eps":eps,"dy":dy,"beta":beta,
     "desc":f"{n} is a leading company in {ind}. Headquartered in {hq}.",
     "desc_zh":f"{nz}是{ind}领域的领先企业，总部位于{hq}。",
     "qr":[("Q4'25","$24.2B",120),("Q3'25","$22.8B",113),("Q2'25","$21.4B",106),("Q1'25","$20.8B",103)]})

print(f"Stock data: {len(STOCKS)} stocks")

# ============================================================
# CRYPTO DATA
# ============================================================
CRYPTOS = [
    {"s":"BTC","n":"Bitcoin","n_zh":"比特币","p":"$97,240","mc":"$1.93T","vol":"$42.8B","ch24":"+2.4%","ch7":"+5.8%","supply":"19.8M","max":"21M","rank":1,"dom":"61.2%","ath":"$108,268","athd":"2025-01-20",
     "desc":"Bitcoin is the first and most valuable cryptocurrency. Created in 2009, it operates on a decentralized proof-of-work blockchain with a hard cap of 21 million coins.",
     "desc_zh":"比特币是第一个也是最有价值的加密货币。创建于2009年，运行在去中心化的工作量证明区块链上，上限为2100万枚。"},
    {"s":"ETH","n":"Ethereum","n_zh":"以太坊","p":"$3,842","mc":"$462B","vol":"$18.4B","ch24":"+1.8%","ch7":"+4.2%","supply":"120.2M","max":"N/A","rank":2,"dom":"17.8%","ath":"$4,878","athd":"2021-11-10",
     "desc":"Ethereum is a decentralized platform for smart contracts and dApps. The shift to proof-of-stake reduced energy usage by 99.95%. Powers DeFi and NFT ecosystems.",
     "desc_zh":"以太坊是去中心化的智能合约和DApp平台。转向权益证明后能耗降低了99.95%。支撑DeFi和NFT生态系统。"},
    {"s":"SOL","n":"Solana","n_zh":"Solana","p":"$182.40","mc":"$82.4B","vol":"$4.2B","ch24":"+3.2%","ch7":"+8.4%","supply":"448M","max":"N/A","rank":5,"dom":"3.2%","ath":"$260","athd":"2024-11-23",
     "desc":"Solana is a high-performance blockchain with fast transaction speeds and low fees. Popular for DeFi, NFTs, and meme coins.",
     "desc_zh":"Solana是一个高性能区块链，具有快速的交易速度和低费用。在DeFi、NFT和迷因币中广受欢迎。"},
    {"s":"BNB","n":"BNB","n_zh":"币安币","p":"$628","mc":"$91.2B","vol":"$2.1B","ch24":"+0.8%","ch7":"+2.4%","supply":"145M","max":"200M","rank":4,"dom":"3.6%","ath":"$793","athd":"2024-12-04",
     "desc":"BNB is the native token of BNB Chain (formerly Binance Smart Chain). Used for trading fee discounts and DeFi applications on the BNB ecosystem.",
     "desc_zh":"BNB是BNB Chain的原生代币。用于BNB生态系统的交易费折扣和DeFi应用。"},
    {"s":"XRP","n":"XRP","n_zh":"瑞波币","p":"$2.42","mc":"$138B","vol":"$3.8B","ch24":"+1.4%","ch7":"+6.2%","supply":"57.2B","max":"100B","rank":3,"dom":"5.4%","ath":"$3.84","athd":"2018-01-07",
     "desc":"XRP is the digital asset native to the XRP Ledger. Designed for fast, low-cost cross-border payments. Used by financial institutions worldwide.",
     "desc_zh":"XRP是XRP Ledger的原生数字资产。专为快速、低成本的跨境支付设计，被全球金融机构采用。"},
    {"s":"ADA","n":"Cardano","n_zh":"卡尔达诺","p":"$0.72","mc":"$25.4B","vol":"$0.8B","ch24":"-0.4%","ch7":"+2.8%","supply":"35.2B","max":"45B","rank":10,"dom":"1.0%","ath":"$3.09","athd":"2021-09-02",
     "desc":"Cardano is a proof-of-stake blockchain platform with a research-driven approach. Founded by Ethereum co-founder Charles Hoskinson.",
     "desc_zh":"卡尔达诺是一个以研究驱动的权益证明区块链平台。由以太坊联合创始人Charles Hoskinson创立。"},
]

_more_cryptos = [
    ("DOGE","Dogecoin","狗狗币","$0.182","$26.4B","$1.8B","+1.2%","+4.6%","144B","N/A",8,"1.0%","$0.74","2021-05-08","Originally a meme coin, Dogecoin has gained mainstream adoption. Supported by Elon Musk.","最初是迷因币，狗狗币已获得主流采用。受到Elon Musk的支持。"),
    ("AVAX","Avalanche","Avalanche","$38.40","$15.2B","$0.6B","+2.4%","+5.2%","396M","720M",12,"0.6%","$146","2021-11-21","High-speed blockchain platform for DeFi and enterprise applications with subnet architecture.","高速区块链平台，支持DeFi和企业应用。"),
    ("DOT","Polkadot","波卡","$7.42","$10.4B","$0.4B","+1.8%","+3.4%","1.4B","N/A",14,"0.4%","$55","2021-11-04","Multi-chain protocol enabling cross-blockchain transfers of data and assets.","多链协议，实现跨区块链的数据和资产传输。"),
    ("LINK","Chainlink","Chainlink","$18.40","$11.2B","$0.8B","+2.2%","+6.8%","608M","1B",11,"0.4%","$53","2021-05-10","Decentralized oracle network connecting smart contracts with real-world data.","去中心化预言机网络，将智能合约与现实世界数据连接。"),
    ("UNI","Uniswap","Uniswap","$8.42","$5.1B","$0.3B","+1.4%","+3.2%","600M","1B",22,"0.2%","$45","2021-05-03","Leading decentralized exchange protocol on Ethereum. Pioneered AMM model.","以太坊上领先的去中心化交易所协议。"),
    ("LTC","Litecoin","莱特币","$98.40","$7.4B","$0.4B","+0.8%","+2.2%","75M","84M",18,"0.3%","$413","2021-05-10","Created in 2011 as 'silver to Bitcoin's gold'. Faster block times and lower fees.","创建于2011年，被称为'比特币的白银'。"),
    ("ATOM","Cosmos","Cosmos","$8.82","$3.4B","$0.2B","+1.6%","+4.2%","389M","N/A",28,"0.1%","$44","2022-01-17","Internet of blockchains enabling interoperability between different chains.","区块链互联网，实现不同链之间的互操作性。"),
    ("NEAR","NEAR Protocol","NEAR Protocol","$5.42","$6.2B","$0.3B","+2.8%","+5.4%","1.1B","N/A",16,"0.2%","$21","2022-01-16","Layer-1 blockchain with sharding technology. Developer-friendly smart contract platform.","采用分片技术的Layer-1区块链。"),
    ("ALGO","Algorand","Algorand","$0.28","$2.2B","$0.08B","+0.6%","+1.8%","8.0B","10B",42,"0.1%","$3.28","2019-06-21","Pure proof-of-stake blockchain for financial applications.","纯权益证明区块链，面向金融应用。"),
    ("ICP","Internet Computer","互联网计算机","$12.40","$5.8B","$0.1B","+1.2%","+3.8%","468M","N/A",20,"0.2%","$75","2021-05-10","Decentralized cloud computing platform by DFINITY Foundation.","DFINITY基金会的去中心化云计算平台。"),
    ("HBAR","Hedera","Hedera","$0.12","$4.6B","$0.1B","+0.8%","+2.4%","38B","50B",24,"0.2%","$0.57","2021-09-15","Enterprise-grade public network using hashgraph consensus.","使用哈希图共识的企业级公共网络。"),
    ("ARB","Arbitrum","Arbitrum","$1.08","$3.8B","$0.4B","+2.4%","+5.8%","3.5B","N/A",26,"0.1%","$2.40","2024-01-12","Leading Ethereum Layer-2 scaling solution using optimistic rollups.","领先的以太坊Layer-2扩展方案，使用乐观Rollup。"),
    ("OP","Optimism","Optimism","$2.28","$2.8B","$0.2B","+1.8%","+4.2%","1.2B","N/A",32,"0.1%","$4.84","2024-03-06","Ethereum Layer-2 scaling solution. Powers the OP Stack superchain ecosystem.","以太坊Layer-2扩展方案，支撑OP Stack超级链生态。"),
    ("SUI","Sui","Sui","$1.82","$5.4B","$0.6B","+3.4%","+8.2%","3.0B","10B",15,"0.2%","$2.18","2024-10-14","High-performance Layer-1 blockchain built by former Meta engineers using Move language.","由前Meta工程师使用Move语言构建的高性能Layer-1区块链。"),
    ("APT","Aptos","Aptos","$8.42","$3.8B","$0.2B","+1.4%","+3.8%","448M","N/A",30,"0.1%","$20","2024-01-26","Layer-1 blockchain using Move programming language. Focus on safety and scalability.","使用Move编程语言的Layer-1区块链。"),
    ("AAVE","Aave","Aave","$282.40","$4.2B","$0.3B","+2.8%","+6.4%","15M","16M",25,"0.2%","$664","2021-10-27","Leading decentralized lending and borrowing protocol across multiple chains.","跨多条链的领先去中心化借贷协议。"),
    ("MKR","Maker","Maker","$1,842","$1.6B","$0.08B","+1.2%","+3.4%","877K","1M",58,"0.06%","$6,292","2021-05-03","Governance token for MakerDAO, creator of DAI stablecoin.","MakerDAO的治理代币，DAI稳定币的创造者。"),
    ("PEPE","Pepe","Pepe","$0.0000124","$5.2B","$1.2B","+4.8%","+12.4%","420.7T","420.7T",17,"0.2%","$0.0000284","2024-12-09","The largest frog-themed meme coin. Viral internet culture token.","最大的青蛙主题迷因币。"),
    ("SHIB","Shiba Inu","柴犬币","$0.0000218","$12.8B","$0.6B","+1.4%","+3.2%","589.3T","N/A",13,"0.5%","$0.0000888","2021-10-28","Community-driven meme token with Shibarium L2 and ShibaSwap DEX.","社区驱动的迷因代币，拥有Shibarium L2和ShibaSwap。"),
    ("RENDER","Render","Render","$8.42","$4.4B","$0.2B","+3.2%","+7.8%","518M","N/A",23,"0.2%","$13.69","2024-03-17","Decentralized GPU rendering network for AI and 3D content creation.","去中心化GPU渲染网络，用于AI和3D内容创作。"),
    ("FET","Fetch.ai","Fetch.ai","$2.28","$5.8B","$0.4B","+2.6%","+6.2%","2.6B","N/A",19,"0.2%","$3.48","2024-03-28","AI-focused blockchain for autonomous machine economy.","面向自主机器经济的AI区块链。"),
    ("INJ","Injective","Injective","$28.40","$2.8B","$0.2B","+2.2%","+5.4%","98M","N/A",34,"0.1%","$53","2024-01-14","Layer-1 blockchain optimized for DeFi and decentralized derivatives.","针对DeFi和去中心化衍生品优化的Layer-1区块链。"),
    ("RUNE","THORChain","THORChain","$5.82","$2.0B","$0.3B","+1.8%","+4.8%","338M","500M",44,"0.08%","$21","2021-05-19","Cross-chain decentralized exchange enabling native asset swaps.","跨链去中心化交易所，支持原生资产互换。"),
    ("TAO","Bittensor","Bittensor","$428.40","$3.2B","$0.08B","+3.8%","+9.2%","7.2M","21M",36,"0.1%","$768","2024-03-28","Decentralized AI network where models are trained collaboratively.","去中心化AI网络，模型协作训练。"),
    ("WLD","Worldcoin","Worldcoin","$2.82","$1.8B","$0.2B","+2.4%","+5.6%","638M","10B",46,"0.07%","$11.74","2024-03-10","Digital identity and cryptocurrency project by Sam Altman.","Sam Altman的数字身份和加密货币项目。"),
    ("JUP","Jupiter","Jupiter","$1.12","$1.5B","$0.3B","+2.8%","+6.4%","1.35B","N/A",48,"0.06%","$2.04","2024-01-31","Leading DEX aggregator on Solana blockchain.","Solana区块链上领先的DEX聚合器。"),
    ("ONDO","Ondo Finance","Ondo Finance","$1.42","$2.0B","$0.1B","+1.8%","+4.2%","1.4B","N/A",40,"0.08%","$1.68","2024-01-18","Tokenized real-world assets (RWA) protocol bridging TradFi and DeFi.","代币化现实世界资产(RWA)协议。"),
    ("STX","Stacks","Stacks","$2.08","$3.0B","$0.1B","+1.4%","+3.8%","1.5B","1.8B",38,"0.1%","$3.84","2024-04-01","Smart contract layer for Bitcoin, enabling DeFi on BTC.","比特币的智能合约层，在BTC上实现DeFi。"),
    ("IMX","Immutable X","Immutable X","$1.62","$2.6B","$0.08B","+1.2%","+3.4%","1.6B","2B",35,"0.1%","$3.64","2021-11-26","Layer-2 scaling solution for NFTs on Ethereum.","以太坊上NFT的Layer-2扩展方案。"),
]

for s,n,nz,p,mc,vol,ch24,ch7,sup,mx,rank,dom,ath,athd,desc,desc_zh in _more_cryptos:
    CRYPTOS.append({"s":s,"n":n,"n_zh":nz,"p":p,"mc":mc,"vol":vol,"ch24":ch24,"ch7":ch7,"supply":sup,"max":mx,"rank":rank,"dom":dom,"ath":ath,"athd":athd,"desc":desc,"desc_zh":desc_zh})

print(f"Crypto data: {len(CRYPTOS)} cryptos")

# ============================================================
# PAGE GENERATORS
# ============================================================

def gen_etf_detail(etf, lang='en'):
    t = etf['t']
    n = etf['n_zh'] if lang=='zh' else etf['n']
    prefix = '/zh' if lang=='zh' else ''
    path = f"{prefix}/etf/{t}.html"
    title = f"{t} ETF Analysis - {n} | ZX Capital"
    desc_text = etf['desc_zh'] if lang=='zh' else etf['desc']
    desc = f"{t} ({n}): {desc_text}"
    
    h = head(title, desc, path, lang)
    h += nav(lang)
    
    # Breadcrumb
    bc_home = ("首页" if lang=='zh' else "Home", f"{prefix}/")
    bc_cat = ("ETF", f"{prefix}/etf/")
    bc_item = (t, None)
    h += f'<section class="sec">'
    h += f'<div class="bc"><a href="{prefix}/">{"首页" if lang=="zh" else "Home"}</a> <span>/</span> <a href="{prefix}/etf/">ETF</a> <span>/</span> <span style="color:var(--t)">{t}</span></div>'
    h += breadcrumb_json([bc_home, bc_cat, bc_item], lang)
    
    # Header
    icon = t[:2]
    h += f'<div class="dh"><div class="di">{icon}</div><div><h1 style="font-size:32px;font-weight:700">{e(t)}</h1><p style="color:var(--td);font-size:14px">{e(n)}</p></div><div class="dp"><div class="mono" style="font-size:28px;font-weight:700">{e(etf["price"])}</div><div class="{pn(etf["ytd"])} mono" style="font-size:14px">{e(etf["ytd"])} YTD</div></div></div>'
    
    # Overview
    h += f'<div class="card" style="margin-bottom:24px"><h2 style="font-size:18px;margin-bottom:12px">{"概览" if lang=="zh" else "Overview"}</h2><p style="color:var(--tm);font-size:14px;line-height:1.7">{e(desc_text)}</p></div>'
    
    # Metrics
    lbls = {"exp":"费率" if lang=='zh' else "Expense","yld":"收益率" if lang=='zh' else "Yield","pe":"P/E","beta":"Beta","aum":"规模" if lang=='zh' else "AUM","hold":"持仓数" if lang=='zh' else "Holdings","cat":"类别" if lang=='zh' else "Category","iss":"发行商" if lang=='zh' else "Issuer","inc":"成立日期" if lang=='zh' else "Inception"}
    h += '<div class="g3" style="margin-bottom:24px">'
    for k in ['exp','yld','pe','beta','aum','hold','cat','iss','inc']:
        v = etf.get(k, etf.get(k,''))
        h += metric(lbls[k], v)
    h += '</div>'
    
    # Returns table
    h += f'<div class="card" style="margin-bottom:24px"><h2 style="font-size:18px;margin-bottom:16px">{"历史回报" if lang=="zh" else "Historical Returns"}</h2><div class="tw"><table><thead><tr>'
    for period in ['1M','3M','6M','1Y','3Y','5Y','10Y']:
        h += f'<th style="text-align:center">{period}</th>'
    h += '</tr></thead><tbody><tr>'
    ret = etf.get('ret',{})
    for k in ['1m','3m','6m','1y','3y','5y','10y']:
        v = ret.get(k,'N/A')
        h += f'<td class="{pn(v)}" style="text-align:center;font-family:monospace;font-weight:600">{e(v)}</td>'
    h += '</tr></tbody></table></div></div>'
    
    # Holdings + Sectors
    h += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">'
    # Top Holdings
    h += f'<div class="card"><h2 style="font-size:18px;margin-bottom:16px">{"十大持仓" if lang=="zh" else "Top Holdings"}</h2>'
    for tk, pct in etf.get('top',[])[:10]:
        h += f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bdr);font-size:13px"><span class="mono" style="color:var(--g)">{e(tk)}</span><span class="mono">{pct}%</span></div>'
    if not etf.get('top'):
        h += f'<p style="color:var(--td);font-size:13px">{"此ETF不持有个股" if lang=="zh" else "This ETF does not hold individual stocks"}</p>'
    h += '</div>'
    # Sectors
    h += f'<div class="card"><h2 style="font-size:18px;margin-bottom:16px">{"行业配置" if lang=="zh" else "Sector Allocation"}</h2>'
    max_sec = max((s[1] for s in etf.get('sec',[])), default=1)
    for sn, sp in etf.get('sec',[]):
        w = (sp / max_sec) * 100
        h += f'<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px"><span>{e(sn)}</span><span class="mono" style="font-size:11px;color:var(--tm)">{sp}%</span></div><div class="bar-t"><div class="bar-f" style="width:{w}%"></div></div></div>'
    h += '</div></div>'
    
    h += '</section>'
    h += footer(lang)
    ld = {"@context":"https://schema.org","@type":"FinancialProduct","name":f"{t} - {etf['n']}","description":etf["desc"],"url":f"{DOMAIN}/etf/{t}.html"}
    h += f'<script type="application/ld+json">{json.dumps(ld)}</script>'
    h += '</body></html>'
    page(f"{'zh/' if lang=='zh' else ''}etf/{t}.html", h)

def gen_stock_detail(stock, lang='en'):
    t = stock['t']
    n = stock['n_zh'] if lang=='zh' else stock['n']
    prefix = '/zh' if lang=='zh' else ''
    path = f"{prefix}/stock/{t}.html"
    title = f"{t} Stock Analysis - {n} | ZX Capital"
    desc_text = stock['desc_zh'] if lang=='zh' else stock['desc']
    
    h = head(title, f"{t} ({n}): {desc_text}", path, lang)
    h += nav(lang)
    h += f'<section class="sec">'
    h += f'<div class="bc"><a href="{prefix}/">{"首页" if lang=="zh" else "Home"}</a> <span>/</span> <a href="{prefix}/stock/">{"股票" if lang=="zh" else "Stocks"}</a> <span>/</span> <span style="color:var(--t)">{t}</span></div>'
    h += breadcrumb_json([(("首页" if lang=='zh' else "Home"), f"{prefix}/"), (("股票" if lang=='zh' else "Stocks"), f"{prefix}/stock/"), (t, None)], lang)
    
    icon = t[:2]
    h += f'<div class="dh"><div class="di">{icon}</div><div><h1 style="font-size:32px;font-weight:700">{e(t)}</h1><p style="color:var(--td);font-size:14px">{e(n)}</p></div><div class="dp"><div class="mono" style="font-size:28px;font-weight:700">{e(stock["p"])}</div><div class="{pn(stock["ch"])} mono" style="font-size:14px">{e(stock["ch"])}</div></div></div>'
    
    # Overview
    h += f'<div class="card" style="margin-bottom:24px"><h2 style="font-size:18px;margin-bottom:10px">{"公司概况" if lang=="zh" else "Company Overview"}</h2><p style="color:var(--tm);font-size:14px;line-height:1.7">{e(desc_text)}</p>'
    h += f'<div class="g3" style="margin-top:18px;padding-top:18px;border-top:1px solid var(--bdr)">'
    for lbl, val in [("行业" if lang=='zh' else "Sector",stock['sec']),("细分行业" if lang=='zh' else "Industry",stock['ind']),("员工" if lang=='zh' else "Employees",stock['emp']),("成立" if lang=='zh' else "Founded",stock['founded']),("总部" if lang=='zh' else "HQ",stock['hq']),("CEO",stock['ceo'])]:
        h += f'<div><span style="font-size:11px;color:var(--td)">{lbl}</span><div style="font-size:14px;font-weight:600;margin-top:2px">{e(val)}</div></div>'
    h += '</div></div>'
    
    # Metrics
    h += '<div class="g3" style="margin-bottom:24px">'
    for lbl, k in [("市值" if lang=='zh' else "Market Cap","mcap"),("P/E","pe"),("P/S","ps"),("P/B","pb"),("营收" if lang=='zh' else "Revenue","rev"),("营收增长" if lang=='zh' else "Rev Growth","rg"),("EPS","eps"),("股息率" if lang=='zh' else "Div Yield","dy"),("Beta","beta")]:
        v = stock[k]
        cls = pn(v) if k=='rg' else ''
        h += metric(lbl, v, cls)
    h += '</div>'
    
    # Quarterly Revenue
    h += f'<div class="card"><h2 style="font-size:18px;margin-bottom:18px">{"季度营收" if lang=="zh" else "Quarterly Revenue"}</h2><div style="display:flex;gap:16px;align-items:flex-end;height:160px">'
    for qlbl, qval, qh in stock.get('qr',[]):
        h += f'<div style="flex:1;text-align:center"><div style="height:{qh}px;background:linear-gradient(to top,rgba(0,220,130,.3),var(--g));border-radius:6px 6px 0 0;margin-bottom:8px"></div><div class="mono" style="font-size:12px;color:var(--g)">{e(qval)}</div><div style="font-size:11px;color:var(--td);margin-top:2px">{e(qlbl)}</div></div>'
    h += '</div></div>'
    
    h += '</section>'
    h += footer(lang)
    h += '</body></html>'
    page(f"{'zh/' if lang=='zh' else ''}stock/{t}.html", h)

def gen_crypto_detail(crypto, lang='en'):
    s = crypto['s']
    n = crypto['n_zh'] if lang=='zh' else crypto['n']
    prefix = '/zh' if lang=='zh' else ''
    path = f"{prefix}/crypto/{s}.html"
    title = f"{s} Analysis - {n} Price & Data | ZX Capital"
    desc_text = crypto['desc_zh'] if lang=='zh' else crypto['desc']
    
    h = head(title, f"{n} ({s}): {crypto['p']}, Market cap {crypto['mc']}.", path, lang)
    h += nav(lang)
    h += f'<section class="sec">'
    h += f'<div class="bc"><a href="{prefix}/">{"首页" if lang=="zh" else "Home"}</a> <span>/</span> <a href="{prefix}/crypto/">{"加密货币" if lang=="zh" else "Crypto"}</a> <span>/</span> <span style="color:var(--t)">{s}</span></div>'
    h += breadcrumb_json([(("首页" if lang=='zh' else "Home"), f"{prefix}/"), (("加密货币" if lang=='zh' else "Crypto"), f"{prefix}/crypto/"), (s, None)], lang)
    
    icon = s[:2]
    h += f'<div class="dh"><div class="di" style="border-radius:50%">{icon}</div><div><h1 style="font-size:32px;font-weight:700">{e(n)}</h1><p style="color:var(--td);font-size:14px">{e(s)} · Rank #{crypto["rank"]}</p></div><div class="dp"><div class="mono" style="font-size:28px;font-weight:700">{e(crypto["p"])}</div><div class="{pn(crypto["ch24"])} mono" style="font-size:14px">{e(crypto["ch24"])} (24h)</div></div></div>'
    
    h += f'<div class="card" style="margin-bottom:24px"><p style="color:var(--tm);font-size:14px;line-height:1.7">{e(desc_text)}</p></div>'
    
    h += '<div class="g3">'
    for lbl, val in [("市值" if lang=='zh' else "Market Cap",crypto['mc']),("24h成交量" if lang=='zh' else "24h Volume",crypto['vol']),("24h涨跌" if lang=='zh' else "24h Change",crypto['ch24']),("7d涨跌" if lang=='zh' else "7d Change",crypto['ch7']),("流通量" if lang=='zh' else "Supply",crypto['supply']),("最大供应" if lang=='zh' else "Max Supply",crypto['max']),("占比" if lang=='zh' else "Dominance",crypto['dom']),("ATH",crypto['ath']),("ATH日期" if lang=='zh' else "ATH Date",crypto['athd'])]:
        cls = pn(val) if 'Change' in lbl or '涨跌' in lbl else ''
        h += metric(lbl, val, cls)
    h += '</div></section>'
    h += footer(lang)
    h += '</body></html>'
    page(f"{'zh/' if lang=='zh' else ''}crypto/{s}.html", h)

def gen_index_page(category, items, lang='en'):
    prefix = '/zh' if lang=='zh' else ''
    path = f"{prefix}/{category}/"
    
    titles = {
        'etf': ("All ETFs - Market Data & Analysis | ZX Capital", "Browse and compare ETFs by performance, expense ratio, and holdings.", "ETF市场 - 数据与分析 | ZX Capital", "浏览和比较ETF的业绩、费率和持仓。"),
        'stock': ("Stock Market - Company Analysis | ZX Capital", "Detailed stock analysis with financial metrics and company data.", "股票市场 - 公司分析 | ZX Capital", "详细的股票分析，包含财务指标和公司数据。"),
        'crypto': ("Cryptocurrency Market - Prices & Data | ZX Capital", "Track cryptocurrency prices, market cap, and trading volume.", "加密货币市场 - 价格与数据 | ZX Capital", "追踪加密货币价格、市值和交易量。"),
    }
    
    t = titles[category][2 if lang=='zh' else 0]
    d = titles[category][3 if lang=='zh' else 1]
    
    h = head(t, d, path, lang)
    h += nav(lang)
    h += f'<section class="sec">'
    
    cat_labels = {'etf':'ETF','stock':'股票' if lang=='zh' else 'Stocks','crypto':'加密货币' if lang=='zh' else 'Crypto'}
    h += f'<h2>{cat_labels[category]} {"市场" if lang=="zh" else "Market"}</h2><p class="sub">{e(d)}</p>'
    
    h += '<div class="tw"><table><thead><tr>'
    if category == 'etf':
        cols = [("Ticker","代码"),("Name","名称"),("Expense","费率"),("Yield","收益率"),("YTD","年初至今"),("AUM","规模")]
        h += ''.join(f'<th>{c[1] if lang=="zh" else c[0]}</th>' for c in cols)
        h += '</tr></thead><tbody>'
        for item in items:
            n = item['n_zh'] if lang=='zh' else item['n']
            h += f'<tr><td class="tk"><a href="{prefix}/etf/{item["t"]}.html" style="color:var(--g)">{item["t"]}</a></td><td><a href="{prefix}/etf/{item["t"]}.html">{e(n)}</a></td><td>{item["exp"]}</td><td>{item["yld"]}</td><td class="{pn(item["ytd"])}">{item["ytd"]}</td><td style="color:var(--tm)">{item["aum"]}</td></tr>'
    elif category == 'stock':
        cols = [("Ticker","代码"),("Name","名称"),("Price","价格"),("Change","涨跌"),("Market Cap","市值"),("P/E","市盈率"),("Sector","行业")]
        h += ''.join(f'<th>{c[1] if lang=="zh" else c[0]}</th>' for c in cols)
        h += '</tr></thead><tbody>'
        for item in items:
            n = item['n_zh'] if lang=='zh' else item['n']
            h += f'<tr><td class="tk"><a href="{prefix}/stock/{item["t"]}.html" style="color:var(--g)">{item["t"]}</a></td><td><a href="{prefix}/stock/{item["t"]}.html">{e(n)}</a></td><td class="mono">{item["p"]}</td><td class="{pn(item["ch"])}">{item["ch"]}</td><td style="color:var(--tm)">{item["mcap"]}</td><td>{item["pe"]}</td><td>{item["sec"]}</td></tr>'
    else:
        cols = [("Symbol","代码"),("Name","名称"),("Price","价格"),("24h","24h"),("7d","7d"),("Market Cap","市值")]
        h += ''.join(f'<th>{c[1] if lang=="zh" else c[0]}</th>' for c in cols)
        h += '</tr></thead><tbody>'
        for item in items:
            n = item['n_zh'] if lang=='zh' else item['n']
            h += f'<tr><td class="tk"><a href="{prefix}/crypto/{item["s"]}.html" style="color:var(--g)">{item["s"]}</a></td><td><a href="{prefix}/crypto/{item["s"]}.html">{e(n)}</a></td><td class="mono">{item["p"]}</td><td class="{pn(item["ch24"])}">{item["ch24"]}</td><td class="{pn(item["ch7"])}">{item["ch7"]}</td><td style="color:var(--tm)">{item["mc"]}</td></tr>'
    
    h += '</tbody></table></div></section>'
    h += footer(lang)
    h += '</body></html>'
    page(f"{'zh/' if lang=='zh' else ''}{category}/index.html", h)

def gen_homepage(lang='en'):
    prefix = '/zh' if lang=='zh' else ''
    path = f"{prefix}/"
    is_zh = lang=='zh'
    title = "ZX Capital 珍兴资本 - 投资工具与市场研究平台" if is_zh else "ZX Capital - Investment Tools & Market Research Platform"
    desc = "免费专业级投资工具、ETF分析、股票数据和加密货币追踪。" if is_zh else "Free professional-grade investment tools, ETF analysis, stock data, and crypto tracking."
    
    h = head(title, desc, path, lang)
    h += nav(lang)
    
    # Hero
    h += f'''<section class="hero"><div class="hero-bg"></div><div class="hero-glow"></div>
<div style="position:relative;max-width:780px">
<span class="tag fu">{"免费投资平台" if is_zh else "Free Investment Platform"}</span>
<h1 class="fu fd1">{"更聪明的投资<br>从这里开始" if is_zh else "Smarter Investing<br>Starts Here"}</h1>
<p class="fu fd2">{"免费专业级工具、实时数据和深度市场研究 — 为认真的投资者而建。" if is_zh else "Free professional-grade tools, real-time data, and deep market research — built for serious investors."}</p>
<div class="fu fd3" style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
<a href="{prefix}/calculator/" class="bp">{"探索工具" if is_zh else "Explore Tools"}</a>
<a href="{prefix}/etf/" class="bo">{"浏览ETF" if is_zh else "Browse ETFs"}</a></div>
<div class="sg"><div class="fu fd1"><div class="mono" style="font-size:26px;font-weight:700;color:var(--g)">{len(ETFS)*2 + len(STOCKS)*2 + len(CRYPTOS)*2 + 20}+</div><div style="font-size:12px;color:var(--td);margin-top:3px">{"数据页面" if is_zh else "Data Pages"}</div></div><div class="fu fd2"><div class="mono" style="font-size:26px;font-weight:700;color:var(--g)">{len(ETFS)}+</div><div style="font-size:12px;color:var(--td);margin-top:3px">{"ETF追踪" if is_zh else "ETFs Tracked"}</div></div><div class="fu fd3"><div class="mono" style="font-size:26px;font-weight:700;color:var(--g)">{len(STOCKS)}+</div><div style="font-size:12px;color:var(--td);margin-top:3px">{"美股分析" if is_zh else "US Stocks"}</div></div><div class="fu fd4"><div class="mono" style="font-size:26px;font-weight:700;color:var(--g)">{len(CRYPTOS)}+</div><div style="font-size:12px;color:var(--td);margin-top:3px">{"加密资产" if is_zh else "Crypto Assets"}</div></div></div></div></section>'''
    
    # Tools
    tools = [
        (f"{prefix}/calculator/portfolio.html","📊","投资组合模拟器" if is_zh else "Portfolio Simulator","模拟投资组合增长" if is_zh else "Model portfolio growth"),
        (f"{prefix}/calculator/compound.html","📈","复利计算器" if is_zh else "Compound Interest","可视化复利效应" if is_zh else "Visualize compounding power"),
        (f"{prefix}/calculator/fire.html","🔥","FIRE计算器" if is_zh else "FIRE Calculator","财务自由之路" if is_zh else "Path to financial independence"),
        (f"{prefix}/calculator/cost-of-living.html","🌍","生活成本比较" if is_zh else "Cost of Living","比较500+城市" if is_zh else "Compare 500+ cities"),
    ]
    h += f'<section class="sec"><h2>{"投资工具" if is_zh else "Investment Tools"}</h2><p class="sub">{"专业计算器和模拟器" if is_zh else "Professional calculators and simulators"}</p><div class="g2">'
    for url,icon,tl,sub in tools:
        h += f'<a href="{url}" class="card" style="text-decoration:none"><div style="font-size:30px;margin-bottom:12px">{icon}</div><h3 style="font-size:17px;font-weight:700;margin-bottom:8px">{tl}</h3><p style="color:var(--td);font-size:13px;line-height:1.6">{sub}</p></a>'
    h += '</div></section>'
    
    # ETF table
    h += f'<div class="sec-a"><section class="sec"><div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:24px;flex-wrap:wrap;gap:12px"><div><h2>{"ETF市场" if is_zh else "ETF Market"}</h2><p class="sub" style="margin-bottom:0">{"热门ETF一览" if is_zh else "Popular ETFs at a glance"}</p></div><a href="{prefix}/etf/" class="bo" style="padding:10px 24px;font-size:13px">{"查看全部 →" if is_zh else "View All →"}</a></div>'
    h += '<div class="tw"><table><thead><tr><th>Ticker</th><th>{"名称" if is_zh else "Name"}</th><th>{"费率" if is_zh else "Expense"}</th><th>{"收益" if is_zh else "Yield"}</th><th>YTD</th><th>AUM</th></tr></thead><tbody>'
    for etf in ETFS[:8]:
        n = etf['n_zh'] if is_zh else etf['n']
        h += f'<tr><td class="tk"><a href="{prefix}/etf/{etf["t"]}.html" style="color:var(--g)">{etf["t"]}</a></td><td><a href="{prefix}/etf/{etf["t"]}.html">{e(n)}</a></td><td>{etf["exp"]}</td><td>{etf["yld"]}</td><td class="{pn(etf["ytd"])}">{etf["ytd"]}</td><td style="color:var(--tm)">{etf["aum"]}</td></tr>'
    h += '</tbody></table></div></section></div>'
    
    # Disclaimer
    h += f'''<section style="padding:0 20px 60px"><div class="disc"><div style="display:flex;gap:14px"><div style="font-size:24px;flex-shrink:0">⚠️</div><div><h3>{"投资免责声明" if is_zh else "Investment Disclaimer"}</h3><p>{"本平台所有信息仅供教育目的。不构成财务建议或买卖证券的招揽。" if is_zh else "All information on this platform is for educational purposes only. It does not constitute financial advice or solicitation to buy or sell securities."}</p><p>{"投资涉及风险，包括可能的本金损失。过去的表现不保证未来的结果。请咨询合格的财务顾问。" if is_zh else "Investing involves risk, including possible loss of principal. Past performance does not guarantee future results. Consult a qualified financial advisor."}</p></div></div></div></section>'''
    
    h += footer(lang)
    h += f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"WebSite","name":"ZX Capital","url":DOMAIN,"description":"Free professional-grade investment tools, ETF analysis, stock data, and crypto tracking."})}</script>'
    h += '</body></html>'
    page(f"{'zh/' if lang=='zh' else ''}index.html", h)

def gen_calculator_pages(lang='en'):
    prefix = '/zh' if lang=='zh' else ''
    is_zh = lang=='zh'
    
    # Calculator index
    path = f"{prefix}/calculator/"
    h = head("投资工具 | ZX Capital" if is_zh else "Investment Calculators & Tools | ZX Capital",
             "免费投资计算器" if is_zh else "Free professional investment calculators", path, lang)
    h += nav(lang)
    h += f'<section class="sec"><h2>{"投资工具" if is_zh else "Investment Tools"}</h2><p class="sub">{"免费专业投资计算器和模拟器" if is_zh else "Free professional calculators and simulators"}</p><div class="g2">'
    calcs = [
        ("portfolio.html","📊","投资组合模拟器" if is_zh else "Portfolio Simulator","模拟不同配置下的投资组合增长" if is_zh else "Model portfolio growth with different allocations"),
        ("compound.html","📈","复利计算器" if is_zh else "Compound Interest Calculator","计算复利对投资增长的影响" if is_zh else "Calculate the impact of compound interest on investments"),
        ("fire.html","🔥","FIRE计算器" if is_zh else "FIRE Calculator","计算实现财务自由所需时间" if is_zh else "Calculate years to financial independence"),
        ("cost-of-living.html","🌍","生活成本比较" if is_zh else "Cost of Living Comparison","比较全球500+城市的生活成本" if is_zh else "Compare cost of living across 500+ cities"),
    ]
    for fn,icon,tl,sub in calcs:
        h += f'<a href="{prefix}/calculator/{fn}" class="card" style="text-decoration:none"><div style="font-size:30px;margin-bottom:12px">{icon}</div><h3 style="font-size:17px;font-weight:700;margin-bottom:8px">{tl}</h3><p style="color:var(--td);font-size:13px;line-height:1.6">{sub}</p></a>'
    h += '</div></section>'
    h += footer(lang)
    h += '</body></html>'
    page(f"{'zh/' if is_zh else ''}calculator/index.html", h)
    
    # Portfolio Calculator
    path = f"{prefix}/calculator/portfolio.html"
    h = head("投资组合模拟器 | ZX Capital" if is_zh else "Portfolio Simulator - Free Investment Calculator | ZX Capital",
             "模拟投资组合增长" if is_zh else "Model portfolio growth based on initial investment, monthly contributions, return rate, and time horizon.", path, lang)
    h += nav(lang)
    h += f'''<section class="sec">
<div class="bc"><a href="{prefix}/">{"首页" if is_zh else "Home"}</a> <span>/</span> <a href="{prefix}/calculator/">{"工具" if is_zh else "Tools"}</a> <span>/</span> <span style="color:var(--t)">{"投资组合模拟器" if is_zh else "Portfolio Simulator"}</span></div>
<h2>{"投资组合模拟器" if is_zh else "Portfolio Simulator"}</h2><p class="sub">{"模拟不同条件下的投资组合增长" if is_zh else "Model your portfolio growth under different scenarios"}</p>
<div class="calc-box">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div><label>{"初始投资" if is_zh else "Initial Investment"} ($)</label><input type="number" id="c_init" value="10000"></div>
<div><label>{"月供" if is_zh else "Monthly Contribution"} ($)</label><input type="number" id="c_monthly" value="500"></div>
<div><label>{"年化回报率" if is_zh else "Annual Return"} (%)</label><input type="number" id="c_return" value="10" step="0.1"></div>
<div><label>{"投资年限" if is_zh else "Years"}</label><input type="number" id="c_years" value="20"></div>
</div>
<button class="bp" style="width:100%;margin-top:8px" onclick="calcPortfolio()">{"计算" if is_zh else "Calculate"}</button>
<div id="c_result" class="res-grid"></div>
</div></section>'''
    h += footer(lang)
    h += '''<script>function calcPortfolio(){let i=+document.getElementById('c_init').value,m=+document.getElementById('c_monthly').value,r=+document.getElementById('c_return').value/100,y=+document.getElementById('c_years').value;let b=i,tc=i;for(let t=0;t<y*12;t++){b*=(1+r/12);b+=m;tc+=m}let g=b-tc;document.getElementById('c_result').innerHTML=`<div class="met"><div class="met-l">''' + ("最终价值" if is_zh else "Final Value") + '''</div><div class="met-v pos">$${b.toLocaleString(undefined,{maximumFractionDigits:0})}</div></div><div class="met"><div class="met-l">''' + ("总投入" if is_zh else "Total Invested") + '''</div><div class="met-v">$${tc.toLocaleString(undefined,{maximumFractionDigits:0})}</div></div><div class="met"><div class="met-l">''' + ("投资收益" if is_zh else "Total Gain") + '''</div><div class="met-v pos">$${g.toLocaleString(undefined,{maximumFractionDigits:0})}</div></div><div class="met"><div class="met-l">''' + ("收益率" if is_zh else "Return") + '''</div><div class="met-v pos">${(g/tc*100).toFixed(1)}%</div></div>`}calcPortfolio()</script>'''
    h += '</body></html>'
    page(f"{'zh/' if is_zh else ''}calculator/portfolio.html", h)
    
    # Compound Interest
    path = f"{prefix}/calculator/compound.html"
    h = head("复利计算器 | ZX Capital" if is_zh else "Compound Interest Calculator | ZX Capital",
             "计算复利增长" if is_zh else "Calculate compound interest growth over time", path, lang)
    h += nav(lang)
    h += f'''<section class="sec">
<div class="bc"><a href="{prefix}/">{"首页" if is_zh else "Home"}</a> <span>/</span> <a href="{prefix}/calculator/">{"工具" if is_zh else "Tools"}</a> <span>/</span> <span style="color:var(--t)">{"复利计算器" if is_zh else "Compound Interest"}</span></div>
<h2>{"复利计算器" if is_zh else "Compound Interest Calculator"}</h2><p class="sub">{"可视化复利的力量" if is_zh else "Visualize the power of compound interest"}</p>
<div class="calc-box">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div><label>{"本金" if is_zh else "Principal"} ($)</label><input type="number" id="ci_p" value="10000"></div>
<div><label>{"年利率" if is_zh else "Annual Rate"} (%)</label><input type="number" id="ci_r" value="7" step="0.1"></div>
<div><label>{"年限" if is_zh else "Years"}</label><input type="number" id="ci_y" value="30"></div>
<div><label>{"复利频率" if is_zh else "Compound Frequency"}</label><select id="ci_f"><option value="12">{"月复利" if is_zh else "Monthly"}</option><option value="4">{"季复利" if is_zh else "Quarterly"}</option><option value="1">{"年复利" if is_zh else "Annually"}</option><option value="365">{"日复利" if is_zh else "Daily"}</option></select></div>
</div>
<button class="bp" style="width:100%;margin-top:8px" onclick="calcCI()">{"计算" if is_zh else "Calculate"}</button>
<div id="ci_result" class="res-grid"></div>
</div></section>'''
    h += footer(lang)
    h += '''<script>function calcCI(){let p=+document.getElementById('ci_p').value,r=+document.getElementById('ci_r').value/100,y=+document.getElementById('ci_y').value,f=+document.getElementById('ci_f').value;let a=p*Math.pow(1+r/f,f*y);let g=a-p;document.getElementById('ci_result').innerHTML=`<div class="met"><div class="met-l">''' + ("最终金额" if is_zh else "Final Amount") + '''</div><div class="met-v pos">$${a.toLocaleString(undefined,{maximumFractionDigits:0})}</div></div><div class="met"><div class="met-l">''' + ("利息收入" if is_zh else "Interest Earned") + '''</div><div class="met-v pos">$${g.toLocaleString(undefined,{maximumFractionDigits:0})}</div></div><div class="met"><div class="met-l">''' + ("增长倍数" if is_zh else "Growth Multiple") + '''</div><div class="met-v">${(a/p).toFixed(1)}x</div></div><div class="met"><div class="met-l">''' + ("年化有效利率" if is_zh else "Effective Rate") + '''</div><div class="met-v">${((Math.pow(1+r/f,f)-1)*100).toFixed(2)}%</div></div>`}calcCI()</script>'''
    h += '</body></html>'
    page(f"{'zh/' if is_zh else ''}calculator/compound.html", h)
    
    # FIRE Calculator
    path = f"{prefix}/calculator/fire.html"
    h = head("FIRE计算器 | ZX Capital" if is_zh else "FIRE Calculator - Financial Independence | ZX Capital",
             "计算财务自由所需时间" if is_zh else "Calculate your path to Financial Independence, Retire Early", path, lang)
    h += nav(lang)
    h += f'''<section class="sec">
<div class="bc"><a href="{prefix}/">{"首页" if is_zh else "Home"}</a> <span>/</span> <a href="{prefix}/calculator/">{"工具" if is_zh else "Tools"}</a> <span>/</span> <span style="color:var(--t)">FIRE {"计算器" if is_zh else "Calculator"}</span></div>
<h2>FIRE {"计算器" if is_zh else "Calculator"}</h2><p class="sub">{"计算实现财务自由退休所需的时间" if is_zh else "Calculate your years to Financial Independence, Retire Early"}</p>
<div class="calc-box">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div><label>{"年收入" if is_zh else "Annual Income"} ($)</label><input type="number" id="fi_inc" value="100000"></div>
<div><label>{"年支出" if is_zh else "Annual Expenses"} ($)</label><input type="number" id="fi_exp" value="50000"></div>
<div><label>{"当前存款" if is_zh else "Current Savings"} ($)</label><input type="number" id="fi_sav" value="50000"></div>
<div><label>{"投资年回报" if is_zh else "Investment Return"} (%)</label><input type="number" id="fi_ret" value="7" step="0.1"></div>
</div>
<button class="bp" style="width:100%;margin-top:8px" onclick="calcFIRE()">{"计算" if is_zh else "Calculate"}</button>
<div id="fi_result" class="res-grid"></div>
</div></section>'''
    h += footer(lang)
    h += '''<script>function calcFIRE(){let inc=+document.getElementById('fi_inc').value,exp=+document.getElementById('fi_exp').value,sav=+document.getElementById('fi_sav').value,ret=+document.getElementById('fi_ret').value/100;let target=exp*25;let annual_sav=inc-exp;let sr=(annual_sav/inc*100).toFixed(1);let years=0;let b=sav;while(b<target&&years<100){b=b*(1+ret)+annual_sav;years++}document.getElementById('fi_result').innerHTML=`<div class="met"><div class="met-l">''' + ("FIRE目标" if is_zh else "FIRE Number") + '''</div><div class="met-v">$${target.toLocaleString()}</div></div><div class="met"><div class="met-l">''' + ("所需年限" if is_zh else "Years to FIRE") + '''</div><div class="met-v pos">${years} ''' + ("年" if is_zh else "yrs") + '''</div></div><div class="met"><div class="met-l">''' + ("储蓄率" if is_zh else "Savings Rate") + '''</div><div class="met-v">${sr}%</div></div><div class="met"><div class="met-l">''' + ("年储蓄额" if is_zh else "Annual Savings") + '''</div><div class="met-v">$${annual_sav.toLocaleString()}</div></div>`}calcFIRE()</script>'''
    h += '</body></html>'
    page(f"{'zh/' if is_zh else ''}calculator/fire.html", h)
    
    # Cost of Living
    path = f"{prefix}/calculator/cost-of-living.html"
    h = head("生活成本比较 | ZX Capital" if is_zh else "Cost of Living Comparison | ZX Capital",
             "比较全球500+城市生活成本" if is_zh else "Compare cost of living across 500+ cities worldwide", path, lang)
    h += nav(lang)
    h += f'''<section class="sec">
<div class="bc"><a href="{prefix}/">{"首页" if is_zh else "Home"}</a> <span>/</span> <a href="{prefix}/calculator/">{"工具" if is_zh else "Tools"}</a> <span>/</span> <span style="color:var(--t)">{"生活成本比较" if is_zh else "Cost of Living"}</span></div>
<h2>{"全球生活成本比较" if is_zh else "Global Cost of Living Comparison"}</h2><p class="sub">{"比较500+城市的生活成本指数" if is_zh else "Compare cost of living index across 500+ cities"}</p>
<div class="calc-box">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div><label>{"城市A" if is_zh else "City A"}</label><select id="col_a"></select></div>
<div><label>{"城市B" if is_zh else "City B"}</label><select id="col_b"></select></div>
</div>
<button class="bp" style="width:100%;margin-top:8px" onclick="calcCOL()">{"比较" if is_zh else "Compare"}</button>
<div id="col_result" class="res-grid"></div>
</div></section>'''
    h += footer(lang)
    h += '''<script>
const cities=[["New York",187],["San Francisco",179],["Los Angeles",166],["Chicago",132],["Boston",162],["Seattle",159],["Washington DC",152],["Miami",148],["Denver",138],["Austin",128],["Dallas",118],["Houston",112],["Atlanta",115],["Phoenix",108],["Portland",142],["Nashville",122],["Minneapolis",118],["Philadelphia",134],["San Diego",158],["Las Vegas",112],["Salt Lake City",108],["Charlotte",104],["Tampa",108],["Orlando",102],["Pittsburgh",98],["Columbus",96],["Indianapolis",92],["Kansas City",94],["St Louis",90],["Cincinnati",88],["London",172],["Paris",158],["Berlin",108],["Munich",132],["Amsterdam",148],["Zurich",198],["Geneva",192],["Vienna",112],["Dublin",142],["Edinburgh",128],["Copenhagen",158],["Stockholm",148],["Oslo",168],["Helsinki",128],["Brussels",118],["Madrid",98],["Barcelona",108],["Lisbon",88],["Rome",108],["Milan",118],["Prague",78],["Warsaw",68],["Budapest",62],["Bucharest",58],["Athens",82],["Istanbul",48],["Moscow",72],["Tokyo",148],["Osaka",118],["Seoul",118],["Singapore",158],["Hong Kong",172],["Shanghai",108],["Beijing",102],["Shenzhen",98],["Guangzhou",82],["Taipei",88],["Bangkok",62],["Kuala Lumpur",58],["Jakarta",48],["Mumbai",42],["Delhi",38],["Bangalore",44],["Hanoi",38],["Ho Chi Minh City",42],["Manila",48],["Sydney",152],["Melbourne",138],["Auckland",128],["Toronto",138],["Vancouver",148],["Montreal",112],["Dubai",128],["Abu Dhabi",118],["Tel Aviv",142],["Riyadh",78],["Cairo",32],["Lagos",42],["Nairobi",48],["Cape Town",52],["Johannesburg",56],["Sao Paulo",62],["Buenos Aires",48],["Mexico City",52],["Lima",48],["Bogota",42],["Santiago",58],["Zurich",198],["Basel",178],["Bern",162],["Luxembourg",158],["Reykjavik",148],["Monaco",208],["San Jose CR",52],["Panama City",58],["Doha",108],["Kuwait City",92],["Muscat",78],["Bahrain",82]];
const sa=document.getElementById('col_a'),sb=document.getElementById('col_b');
cities.sort((a,b)=>a[0].localeCompare(b[0]));
cities.forEach((c,i)=>{sa.innerHTML+=`<option value="${i}">${c[0]} (${c[1]})</option>`;sb.innerHTML+=`<option value="${i}">${c[0]} (${c[1]})</option>`});
sb.selectedIndex=1;
function calcCOL(){let a=cities[sa.value],b=cities[sb.value];let d=((b[1]-a[1])/a[1]*100).toFixed(1);let cl=d>=0?'neg':'pos';document.getElementById('col_result').innerHTML=`<div class="met"><div class="met-l">${a[0]}</div><div class="met-v">${a[1]}</div></div><div class="met"><div class="met-l">${b[0]}</div><div class="met-v">${b[1]}</div></div><div class="met"><div class="met-l">''' + ("差异" if is_zh else "Difference") + '''</div><div class="met-v ${cl}">${d>0?'+':''}${d}%</div></div><div class="met"><div class="met-l">$1000 ''' + ("在" if is_zh else "in") + ''' ${a[0]}</div><div class="met-v">= $${(1000*b[1]/a[1]).toFixed(0)} ''' + ("在" if is_zh else "in") + ''' ${b[0]}</div></div>`}calcCOL()
</script>'''
    h += '</body></html>'
    page(f"{'zh/' if is_zh else ''}calculator/cost-of-living.html", h)

def gen_about(lang='en'):
    prefix = '/zh' if lang=='zh' else ''
    is_zh = lang=='zh'
    path = f"{prefix}/about.html"
    h = head("关于我们 | ZX Capital" if is_zh else "About | ZX Capital",
             "关于ZX Capital珍兴资本" if is_zh else "About ZX Capital - Free investment tools and market research", path, lang)
    h += nav(lang)
    h += f'''<section class="sec">
<h2>{"关于 ZX Capital 珍兴资本" if is_zh else "About ZX Capital"}</h2>
<div class="card" style="max-width:800px">
<p style="color:var(--tm);font-size:15px;line-height:1.8;margin-bottom:16px">{"ZX Capital（珍兴资本）是一个免费的投资研究平台，提供专业级的市场数据、ETF分析、股票研究和加密货币追踪工具。" if is_zh else "ZX Capital is a free investment research platform providing professional-grade market data, ETF analysis, stock research, and cryptocurrency tracking tools."}</p>
<p style="color:var(--tm);font-size:15px;line-height:1.8;margin-bottom:16px">{"我们的使命是让每个人都能获得曾经只有机构投资者才能使用的投资工具和数据。" if is_zh else "Our mission is to democratize access to investment tools and data that were once available only to institutional investors."}</p>
<p style="color:var(--tm);font-size:15px;line-height:1.8">{"所有工具完全免费，无需注册。我们不提供投资建议，所有数据仅供教育和研究目的。" if is_zh else "All tools are completely free with no registration required. We do not provide investment advice — all data is for educational and research purposes only."}</p>
</div></section>'''
    h += footer(lang)
    h += '</body></html>'
    page(f"{'zh/' if is_zh else ''}about.html", h)

def gen_sitemap():
    urls = []
    def add(path, freq='daily', pri='0.8'):
        urls.append(f'  <url><loc>{DOMAIN}{path}</loc><changefreq>{freq}</changefreq><priority>{pri}</priority></url>')
    
    for lang in ['en','zh']:
        p = '/zh' if lang=='zh' else ''
        add(f'{p}/', 'daily', '1.0')
        add(f'{p}/etf/', 'daily', '0.9')
        for etf in ETFS: add(f'{p}/etf/{etf["t"]}.html')
        add(f'{p}/stock/', 'daily', '0.9')
        for s in STOCKS: add(f'{p}/stock/{s["t"]}.html')
        add(f'{p}/crypto/', 'daily', '0.9')
        for c in CRYPTOS: add(f'{p}/crypto/{c["s"]}.html')
        add(f'{p}/calculator/', 'weekly', '0.9')
        for calc in ['portfolio','compound','fire','cost-of-living']:
            add(f'{p}/calculator/{calc}.html', 'monthly')
        add(f'{p}/about.html', 'monthly', '0.6')
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>'
    page('sitemap.xml', xml)

def gen_static():
    page('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    page('CNAME', 'zxcapital.ai\n')
    page('.nojekyll', '')
    page('README.md', f'''# ZX Capital 珍兴资本

Investment Tools & Market Research Platform

🌐 [zxcapital.ai](https://zxcapital.ai)

## Features

- 📊 ETF Analysis ({len(ETFS)} ETFs)
- 📈 Stock Analysis ({len(STOCKS)} Stocks)
- 🪙 Crypto Tracking ({len(CRYPTOS)} Cryptos)
- 🧮 Investment Calculators (Portfolio, Compound Interest, FIRE)
- 🌍 Global Cost of Living (100+ cities)
- 🌐 Bilingual (English / 中文)

## SEO Optimized

Every page includes:
- Unique `<title>` and `<meta description>`
- Canonical URLs + hreflang tags
- JSON-LD structured data (Schema.org)
- Breadcrumb navigation
- sitemap.xml + robots.txt

## Tech Stack

- Pure HTML/CSS/JS (no framework)
- Static site generated by Python
- Hosted on GitHub Pages

## Generate Pages

```bash
python3 generate_site.py
```

---

© 2026 ZX Capital 珍兴资本
''')

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    
    total_pages = 0
    
    for lang in ['en', 'zh']:
        l = '中文' if lang=='zh' else 'English'
        
        print(f"\n--- Generating {l} pages ---")
        
        gen_homepage(lang)
        total_pages += 1
        print(f"  ✓ Homepage")
        
        gen_index_page('etf', ETFS, lang)
        total_pages += 1
        for etf in ETFS:
            gen_etf_detail(etf, lang)
            total_pages += 1
        print(f"  ✓ {len(ETFS)} ETF pages + index")
        
        gen_index_page('stock', STOCKS, lang)
        total_pages += 1
        for s in STOCKS:
            gen_stock_detail(s, lang)
            total_pages += 1
        print(f"  ✓ {len(STOCKS)} Stock pages + index")
        
        gen_index_page('crypto', CRYPTOS, lang)
        total_pages += 1
        for c in CRYPTOS:
            gen_crypto_detail(c, lang)
            total_pages += 1
        print(f"  ✓ {len(CRYPTOS)} Crypto pages + index")
        
        gen_calculator_pages(lang)
        total_pages += 5
        print(f"  ✓ Calculator pages")
        
        gen_about(lang)
        total_pages += 1
        print(f"  ✓ About page")
    
    gen_sitemap()
    gen_static()
    total_pages += 4
    
    file_count = sum(len(files) for _, _, files in os.walk(OUT))
    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, files in os.walk(OUT) for f in files)
    
    print(f"\n{'='*50}")
    print(f"✅ Site generated successfully!")
    print(f"   Total HTML pages: {total_pages}")
    print(f"   Total files: {file_count}")
    print(f"   Total size: {size/1024:.0f} KB")
    print(f"   Output: {OUT}/")
    print(f"{'='*50}")
