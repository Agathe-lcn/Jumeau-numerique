import json

with open('salles_R1.json', encoding='utf-8') as f:
    salles_data = json.load(f)

with open('graph_R1.json', encoding='utf-8') as f:
    graph_data = json.load(f)

with open('images_b64.json', encoding='utf-8') as f:
    images_b64 = json.load(f)

LOGO_B64 = images_b64['logo']
WELCOME_B64 = images_b64['welcome']

html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ensIIE — Jumeau Numérique 3D & Orientation Indoor (R+1)</title>
    <script src="three.min.js"></script>
    <script src="OrbitControls.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg:         #0a0e1a;
            --surface:    rgba(14, 20, 36, 0.96);
            --surface2:   rgba(20, 28, 50, 0.85);
            --border:     rgba(255,255,255,0.08);
            --border2:    rgba(255,255,255,0.14);
            --blue:       #2563eb;
            --blue-light: #38bdf8;
            --blue-dim:   rgba(37,99,235,0.18);
            --green:      #10b981;
            --green-dim:  rgba(16,185,129,0.16);
            --red:        #ef4444;
            --cyan:       #06b6d4;
            --orange:     #f97316;
            --purple:     #a855f7;
            --yellow:     #eab308;
            --text:       #f8fafc;
            --text2:      #94a3b8;
            --text3:      #cbd5e1;
            --sidebar-w:  360px;
        }}
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{
            width: 100%; height: 100%;
            font-family: 'Inter', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            overflow: hidden;
        }}
        #app {{ display: flex; width: 100vw; height: 100vh; position: relative; }}

        /* ── Welcome Splash Screen ────────────────────────────────────────── */
        #welcome-modal {{
            position: fixed;
            inset: 0;
            z-index: 99999;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(10, 14, 26, 0.94);
            transition: opacity 0.5s ease, visibility 0.5s ease;
            overflow: hidden;
        }}
        #welcome-bg {{
            position: absolute;
            inset: 0;
            width: 100%; height: 100%;
            object-fit: cover;
            z-index: 0;
            filter: brightness(0.32) saturate(0.85);
        }}
        #welcome-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(10,14,26,0.75) 0%, rgba(10,14,26,0.55) 100%);
            z-index: 1;
        }}
        #welcome-modal.hidden {{
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }}
        .welcome-box {{
            background: rgba(14, 20, 36, 0.96);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 20px;
            padding: 38px 42px;
            max-width: 520px;
            width: 90%;
            text-align: center;
            box-shadow: 0 30px 70px rgba(0,0,0,0.8);
            animation: welcomePop 0.4s ease-out;
            position: relative;
            z-index: 2;
        }}
        @keyframes welcomePop {{
            0% {{ transform: scale(0.92); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        .welcome-logo {{
            height: 58px;
            background: #ffffff;
            padding: 7px 16px;
            border-radius: 10px;
            margin-bottom: 18px;
            display: inline-block;
            box-shadow: 0 6px 22px rgba(0,0,0,0.35);
            object-fit: contain;
        }}
        .welcome-title {{
            font-size: 26px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        .welcome-sub {{
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 26px;
            line-height: 1.5;
        }}
        .btn-welcome {{
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 15px 30px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45);
        }}
        .btn-welcome:hover {{
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            transform: translateY(-2px);
            box-shadow: 0 10px 28px rgba(37, 99, 235, 0.55);
        }}

        /* ── Sidebar ─────────────────────────────────────────────────────── */
        #sidebar {{
            width: var(--sidebar-w);
            height: 100%;
            background: var(--surface);
            border-right: 1px solid var(--border2);
            display: flex;
            flex-direction: column;
            z-index: 20;
            box-shadow: 6px 0 28px rgba(0,0,0,0.55);
            overflow: hidden;
        }}

        /* Brand */
        #brand {{
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
            flex-shrink: 0;
        }}
        .brand-logo-img {{
            height: 36px;
            background: #ffffff;
            padding: 4px 8px;
            border-radius: 6px;
            object-fit: contain;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}
        #brand-title {{
            font-size: 13px;
            font-weight: 700;
            color: var(--text);
            line-height: 1.3;
        }}
        #brand-sub {{
            font-size: 11px;
            font-weight: 400;
            color: var(--text2);
        }}

        /* Tabs */
        #tabs {{
            display: flex;
            border-bottom: 1px solid var(--border);
            padding: 0 6px;
            flex-shrink: 0;
            background: rgba(10, 14, 26, 0.4);
        }}
        .tab {{
            flex: 1;
            padding: 12px 4px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text2);
            background: none;
            border: none;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.15s;
            letter-spacing: 0.2px;
            text-align: center;
        }}
        .tab:hover {{ color: var(--text); }}
        .tab.active {{
            color: var(--blue-light);
            border-bottom-color: var(--blue);
            font-weight: 700;
        }}

        /* Pinned Salles Header (Search + Filter Chips) */
        #salles-fixed-header {{
            flex-shrink: 0;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 10px 14px 8px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        #search-wrap {{
            position: relative;
            width: 100%;
        }}
        #search {{
            width: 100%;
            background: var(--surface2);
            border: 1px solid var(--border2);
            border-radius: 8px;
            padding: 8px 12px 8px 34px;
            color: var(--text);
            font-size: 12px;
            font-family: inherit;
            outline: none;
            transition: border-color 0.15s;
        }}
        #search:focus {{ border-color: var(--blue-light); }}
        #search-icon {{
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            width: 14px; height: 14px;
            color: var(--text2);
        }}

        /* Filters */
        #filters {{
            display: flex;
            gap: 5px;
            overflow-x: auto;
            padding-bottom: 2px;
            scrollbar-width: none;
        }}
        #filters::-webkit-scrollbar {{ display: none; }}
        .chip {{
            background: rgba(255,255,255,0.04);
            border: 1px solid var(--border);
            color: var(--text2);
            padding: 5px 9px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 500;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .chip:hover {{ color: var(--text); border-color: var(--border2); }}
        .chip.active {{
            background: var(--blue-dim);
            border-color: var(--blue-light);
            color: var(--blue-light);
            font-weight: 600;
        }}

        #filter-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: var(--text2);
            padding: 0 2px;
        }}
        .btn-clear-card {{
            background: none;
            border: none;
            color: var(--blue-light);
            cursor: pointer;
            font-size: 11px;
            font-weight: 600;
        }}
        .btn-clear-card:hover {{ text-decoration: underline; }}

        /* Scrollable content areas */
        .pane {{
            flex: 1;
            overflow-y: auto;
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            scrollbar-width: thin;
            scrollbar-color: rgba(255,255,255,0.1) transparent;
        }}
        .pane::-webkit-scrollbar {{ width: 4px; }}
        .pane::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.12); border-radius: 4px; }}

        /* Card */
        .card {{
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 13px;
        }}
        .card-title {{
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text2);
            margin-bottom: 8px;
        }}

        /* Room photo */
        #room-photo-wrap {{
            display: none;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 10px;
            position: relative;
            cursor: zoom-in;
            border: 1px solid rgba(255,255,255,0.12);
        }}
        #room-photo {{
            width: 100%;
            height: 130px;
            object-fit: cover;
            display: block;
            transition: transform 0.2s;
        }}
        #room-photo:hover {{ transform: scale(1.02); }}
        #room-photo-label {{
            position: absolute;
            bottom: 0; left: 0; right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            padding: 6px 8px;
            font-size: 10px;
            color: rgba(255,255,255,0.85);
        }}

        #room-name {{
            font-size: 16px;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 2px;
        }}
        #room-type {{
            font-size: 11px;
            color: var(--text2);
            margin-bottom: 8px;
        }}
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 8px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .status-badge.libre {{ background: var(--green-dim); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }}
        .status-badge.occupe {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }}
        .dot {{ width: 5px; height: 5px; border-radius: 50%; background: currentColor; }}

        /* Meta grid */
        .meta-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 8px;
        }}
        .meta-cell {{
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            border-radius: 7px;
            padding: 7px 9px;
        }}
        .meta-label {{ font-size: 9px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; }}
        .meta-val {{ font-size: 12px; font-weight: 700; color: var(--text); margin-top: 1px; }}

        /* Occupant */
        #occupant-card {{
            display: none;
            background: var(--green-dim);
            border: 1px solid rgba(16,185,129,0.25);
            border-radius: 8px;
            padding: 8px 10px;
            margin-bottom: 8px;
        }}
        #occupant-label {{ font-size: 9px; font-weight: 700; color: #34d399; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 3px; }}
        #occupant-name {{ font-size: 12px; font-weight: 700; color: var(--text); }}
        #occupant-role {{ font-size: 10px; color: var(--text2); margin-top: 2px; }}

        /* Schedule */
        .sched-item {{
            padding: 6px 9px;
            border-radius: 6px;
            border-left: 3px solid #475569;
            background: rgba(255,255,255,0.02);
            font-size: 11px;
            margin-bottom: 4px;
        }}
        .sched-item.current {{ border-left-color: #ef4444; background: rgba(239,68,68,0.12); }}
        .sched-item.free {{ border-left-color: #10b981; background: var(--green-dim); }}
        .sched-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .sched-time {{ font-weight: 600; color: var(--text3); font-size: 10px; }}
        .sched-status {{ font-weight: 700; font-size: 10px; }}
        .sched-desc {{ color: var(--text2); margin-top: 2px; font-size: 10px; }}

        /* Room Browse List */
        .room-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 10px;
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .room-row:hover {{
            background: rgba(37,99,235,0.12);
            border-color: rgba(56,189,248,0.3);
        }}
        .room-row.active {{
            background: rgba(37,99,235,0.22);
            border-color: #38bdf8;
        }}
        .room-tag {{
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 600;
        }}

        /* ── Itinéraire Tab & Turn-by-Turn Guidance ──────────────────────────── */
        .form-label {{ font-size: 11px; font-weight: 600; color: var(--text2); margin-bottom: 4px; }}
        .form-select {{
            width: 100%;
            background: rgba(10,14,26,0.85);
            border: 1px solid var(--border2);
            border-radius: 8px;
            padding: 8px 10px;
            color: var(--text);
            font-size: 12px;
            font-family: inherit;
            outline: none;
            cursor: pointer;
            margin-bottom: 10px;
        }}
        .form-select:focus {{ border-color: var(--blue-light); }}
        .btn-primary {{
            width: 100%;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            border: none;
            border-radius: 9px;
            padding: 11px;
            color: #fff;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        }}
        .btn-primary:hover {{ background: linear-gradient(135deg, #3b82f6, #2563eb); }}

        #route-summary {{
            display: none;
            margin-top: 10px;
            padding: 12px;
            background: rgba(16,185,129,0.14);
            border: 1px solid rgba(16,185,129,0.3);
            border-radius: 9px;
            flex-direction: column;
            gap: 4px;
        }}
        #route-summary.visible {{ display: flex; }}
        #clear-route {{
            background: none;
            border: 1px solid var(--border2);
            border-radius: 7px;
            padding: 7px 10px;
            color: var(--text2);
            font-size: 11px;
            cursor: pointer;
            margin-top: 8px;
            transition: all 0.15s;
            width: 100%;
        }}
        #clear-route:hover {{ border-color: var(--red); color: #f87171; }}

        /* Turn-by-Turn Steps */
        #route-steps-container {{
            margin-top: 10px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .step-card {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 9px 11px;
            background: rgba(255,255,255,0.025);
            border: 1px solid var(--border);
            border-radius: 9px;
            transition: background 0.15s;
        }}
        .step-icon {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
            flex-shrink: 0;
            font-weight: 700;
        }}
        .step-icon.start {{ background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(16,185,129,0.35); }}
        .step-icon.straight {{ background: rgba(56,189,248,0.2); color: #38bdf8; border: 1px solid rgba(56,189,248,0.35); }}
        .step-icon.left {{ background: rgba(249,115,22,0.2); color: #fb923c; border: 1px solid rgba(249,115,22,0.35); }}
        .step-icon.right {{ background: rgba(234,179,8,0.2); color: #facc15; border: 1px solid rgba(234,179,8,0.35); }}
        .step-icon.dest {{ background: rgba(168,85,247,0.25); color: #c084fc; border: 1px solid rgba(168,85,247,0.4); }}
        .step-content {{ flex: 1; }}
        .step-action {{ font-size: 12px; font-weight: 700; color: var(--text); line-height: 1.2; }}
        .step-desc {{ font-size: 11px; color: var(--text2); margin-top: 2px; }}
        .step-dist {{
            font-size: 10px;
            font-weight: 700;
            color: var(--blue-light);
            background: rgba(56,189,248,0.12);
            padding: 3px 7px;
            border-radius: 5px;
            white-space: nowrap;
        }}

        /* ── 3D Viewport ──────────────────────────────────────────────────────── */
        #viewport {{
            flex: 1;
            height: 100%;
            position: relative;
            background: radial-gradient(ellipse at 55% 35%, #0d1e42 0%, #0a0e1a 80%);
        }}
        #canvas-3d {{ width: 100%; height: 100%; display: block; }}

        /* Top bar */
        #topbar {{
            position: absolute;
            top: 14px; left: 16px; right: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            pointer-events: none;
            z-index: 10;
        }}
        .topbar-pill {{
            pointer-events: auto;
            background: var(--surface);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border2);
            border-radius: 10px;
            padding: 6px 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }}
        .topbar-divider {{ width: 1px; height: 20px; background: var(--border2); }}
        .floor-badge {{
            background: var(--blue-dim);
            color: var(--blue-light);
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 5px;
            border: 1px solid rgba(59,130,246,0.3);
        }}

        #topbar-right {{
            pointer-events: auto;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .pmr-btn {{
            background: var(--surface);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border2);
            border-radius: 8px;
            padding: 8px 14px;
            color: var(--text2);
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 7px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
        }}
        .pmr-btn:hover {{ color: var(--text); border-color: rgba(255,255,255,0.25); }}
        .pmr-btn.active {{
            background: #2563eb;
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 4px 16px rgba(37,99,235,0.45);
        }}
        .icon-btn {{
            pointer-events: auto;
            width: 38px; height: 38px;
            background: var(--surface);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border2);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.15s;
            color: var(--text2);
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
        }}
        .icon-btn:hover {{ border-color: rgba(255,255,255,0.25); color: var(--text); }}

        /* Tooltip */
        #tooltip {{
            position: absolute;
            display: none;
            background: rgba(14, 20, 36, 0.95);
            border: 1px solid var(--border2);
            color: var(--text);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            pointer-events: none;
            z-index: 50;
            white-space: nowrap;
            box-shadow: 0 6px 16px rgba(0,0,0,0.5);
        }}

        /* Bottom Legend Overlay with Totally Distinct Colors */
        #legend {{
            position: absolute;
            bottom: 16px; right: 16px;
            background: var(--surface);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border2);
            border-radius: 10px;
            padding: 8px 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            pointer-events: none;
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        }}
        .leg-item {{ display: flex; align-items: center; gap: 5px; font-size: 11px; color: var(--text2); }}
        .leg-dot {{ width: 8px; height: 8px; border-radius: 2px; }}
        .leg-sep {{ width: 1px; height: 14px; background: var(--border); }}

        /* Lightbox */
        #lightbox {{
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.92);
            z-index: 9999;
            justify-content: center;
            align-items: center;
            cursor: zoom-out;
        }}
        #lightbox.open {{ display: flex; }}
        #lightbox img {{ max-width: 90vw; max-height: 88vh; border-radius: 10px; box-shadow: 0 30px 60px rgba(0,0,0,0.8); }}
    </style>
</head>
<body>
<div id="app">

    <!-- ── Welcome Modal ────────────────────────────────────────────────── -->
    <div id="welcome-modal">
        <img id="welcome-bg" src="{WELCOME_B64}" alt="">
        <div id="welcome-overlay"></div>
        <div class="welcome-box">
            <img src="{LOGO_B64}" class="welcome-logo" alt="Logo ensIIE">
            <h1 class="welcome-title">Bienvenue à l'ensIIE</h1>
            <p class="welcome-sub">Jumeau Numérique 3D & Navigation Indoor — Étage R+1</p>
            <button id="btn-enter" class="btn-welcome" onclick="enterPlan()">Accéder au Plan 3D →</button>
        </div>
    </div>

    <!-- ── Sidebar ─────────────────────────────────────────────────────────── -->
    <div id="sidebar">

        <!-- Brand -->
        <div id="brand">
            <img src="{LOGO_B64}" class="brand-logo-img" alt="ensIIE">
            <div>
                <div id="brand-title">Plan Interactif 3D</div>
                <div id="brand-sub">Bâtiment principal — Étage R+1</div>
            </div>
        </div>

        <!-- Tabs -->
        <div id="tabs">
            <button class="tab active" data-tab="salles">Salles</button>
            <button class="tab" data-tab="itineraire">Itinéraire</button>
            <button class="tab" data-tab="infos">Légende & Infos</button>
        </div>

        <!-- ── PANE: Salles ────────────────────────────────────────────── -->
        <div id="pane-salles" style="display:flex; flex-direction:column; flex:1; overflow:hidden;">
            <!-- Fixed Pinned Header for Salles -->
            <div id="salles-fixed-header">
                <div id="search-wrap">
                    <svg id="search-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="9" cy="9" r="6"/><path d="M15 15l-3-3"/>
                    </svg>
                    <input id="search" type="text" placeholder="Rechercher salle, amphi, bureau, prof…">
                </div>
                <div id="filters">
                    <button class="chip active" data-filter="all">Tous (48)</button>
                    <button class="chip" data-filter="amphi">Amphis (3)</button>
                    <button class="chip" data-filter="tp">Salles TP (4)</button>
                    <button class="chip" data-filter="td">Salles TD (10)</button>
                    <button class="chip" data-filter="bureau">Bureaux (18)</button>
                    <button class="chip" data-filter="libre">Libres</button>
                </div>
                <div id="filter-meta">
                    <span id="room-count">48 espaces</span>
                    <button id="btn-close-fiche" class="btn-clear-card" style="display:none;" onclick="deselectRoom()">✕ Fermer la fiche</button>
                </div>
            </div>

            <!-- Scrollable Content Body -->
            <div class="pane">
                <!-- Room Details Card -->
                <div class="card" id="room-details-card" style="display:none;">
                    <div id="room-photo-wrap">
                        <img id="room-photo" src="" alt="">
                        <div id="room-photo-label">📷 Cliquez pour zoomer la photo</div>
                    </div>

                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <div id="room-name">Salle</div>
                            <div id="room-type">Type</div>
                        </div>
                        <button onclick="deselectRoom()" style="background:none; border:none; color:var(--text2); cursor:pointer; font-size:14px; padding:2px 6px;">✕</button>
                    </div>
                    <div id="room-status" class="status-badge occupe"><span class="dot"></span><span id="room-status-text">Occupé</span></div>

                    <div class="meta-grid">
                        <div class="meta-cell">
                            <div class="meta-label">Surface</div>
                            <div class="meta-val" id="room-surface">—</div>
                        </div>
                        <div class="meta-cell">
                            <div class="meta-label">Capacité</div>
                            <div class="meta-val" id="room-capacity">—</div>
                        </div>
                    </div>

                    <div id="occupant-card">
                        <div id="occupant-label">Responsable / Enseignant</div>
                        <div id="occupant-name"></div>
                        <div id="occupant-role"></div>
                    </div>

                    <button class="btn-primary" id="btn-route-to-room" style="margin-top:4px; padding:8px 10px; font-size:11px;" onclick="routeToCurrentRoom()">
                        📍 Y aller depuis l'entrée
                    </button>

                    <div class="card-title" style="margin-top:12px;">Emploi du temps — Aujourd'hui</div>
                    <div id="schedule"></div>
                </div>

                <!-- Room Directory List (shown when no room selected, or below card) -->
                <div id="room-directory" style="display:flex; flex-direction:column; gap:5px;"></div>
            </div>
        </div>

        <!-- ── PANE: Itinéraire ────────────────────────────────────────── -->
        <div id="pane-itineraire" class="pane" style="display:none;">
            <div class="card">
                <div class="card-title">Calcul d'itinéraire indoor</div>

                <div class="form-label">Point de départ</div>
                <select id="select-start" class="form-select"></select>

                <div class="form-label">Destination</div>
                <select id="select-end" class="form-select"></select>

                <button class="btn-primary" id="btn-route">Tracer le chemin 3D</button>

                <!-- Route Summary Banner -->
                <div id="route-summary">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span id="route-dist" style="font-weight:700; color:#34d399; font-size:13px;"></span>
                        <span id="route-time" style="font-size:11px; color:#cbd5e1; font-weight:600;"></span>
                    </div>
                    <div id="route-pmr-badge" style="font-size:10px; color:#60a5fa; display:none;">♿ Trajet adapté PMR (Ascenseur)</div>
                </div>

                <!-- Turn-by-Turn Navigation Steps -->
                <div id="route-steps-container"></div>

                <button id="clear-route" style="display:none;">Effacer le chemin</button>
            </div>

            <div class="card" style="border-color:rgba(37,99,235,0.25);">
                <div class="card-title">Réseau de circulation officiel</div>
                <div style="font-size:12px; color:var(--text2); line-height:1.6;">
                    Le tracé suit exclusivement les <b>couloirs</b> d'après le plan d'évacuation officiel du bâtiment principal. Aucune salle fermée n'est traversée.
                    <br><br>
                    <span id="pmr-note" style="color:var(--text3);">Mode standard : escaliers et couloirs piétons.</span>
                </div>
            </div>
        </div>

        <!-- ── PANE: Infos ─────────────────────────────────────────────── -->
        <div id="pane-infos" class="pane" style="display:none;">
            <div class="card">
                <div class="card-title">Code Couleur des Espaces</div>
                <div style="display:flex; flex-direction:column; gap:9px; font-size:12px; color:var(--text2);">
                    <div style="display:flex;align-items:center;gap:10px;"><span style="width:14px;height:14px;background:#ef4444;border-radius:3px;flex-shrink:0;"></span> <b>Amphithéâtres</b> (101, 102, 123)</div>
                    <div style="display:flex;align-items:center;gap:10px;"><span style="width:14px;height:14px;background:#06b6d4;border-radius:3px;flex-shrink:0;"></span> <b>Salles de TP</b> (127, 130, 131, 133)</div>
                    <div style="display:flex;align-items:center;gap:10px;"><span style="width:14px;height:14px;background:#f97316;border-radius:3px;flex-shrink:0;"></span> <b>Salles de TD</b> (121, 122, 126, 135, 136…)</div>
                    <div style="display:flex;align-items:center;gap:10px;"><span style="width:14px;height:14px;background:#10b981;border-radius:3px;flex-shrink:0;"></span> <b>Bureaux Enseignants</b> (18 bureaux)</div>
                    <div style="display:flex;align-items:center;gap:10px;"><span style="width:14px;height:14px;background:#a855f7;border-radius:3px;flex-shrink:0;"></span> <b>Rotonde 103</b> (Carrefour central)</div>
                    <div style="display:flex;align-items:center;gap:10px;"><span style="width:14px;height:14px;background:#eab308;border-radius:3px;flex-shrink:0;"></span> <b>Salle des Professeurs</b> (115)</div>
                    <div style="display:flex;align-items:center;gap:10px;"><span style="width:14px;height:14px;background:#475569;border-radius:3px;flex-shrink:0;"></span> <b>Locaux techniques & Serveurs</b> (140, 142)</div>
                    <div style="display:flex;align-items:center;gap:10px;"><span style="width:14px;height:14px;background:#9ca3af;border-radius:3px;flex-shrink:0;"></span> <b>Dépôts pédagogiques</b> (124, 125, 132…)</div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">Commandes 3D</div>
                <div style="font-size:12px; color:var(--text2); line-height:1.8;">
                    <b style="color:var(--text);">Clic gauche glissé</b> — Rotation de la vue<br>
                    <b style="color:var(--text);">Clic droit glissé</b> — Déplacement (pan)<br>
                    <b style="color:var(--text);">Molette</b> — Zoom avant / arrière<br>
                    <b style="color:var(--text);">Clic sur bloc ou étiquette</b> — Sélectionner la salle
                </div>
            </div>
        </div>

    </div><!-- /sidebar -->

    <!-- ── 3D Viewport ──────────────────────────────────────────────────────── -->
    <div id="viewport">
        <canvas id="canvas-3d"></canvas>

        <!-- Top bar -->
        <div id="topbar">
            <div class="topbar-pill">
                <img src="{LOGO_B64}" style="height:30px; background:#ffffff; padding:3px 7px; border-radius:5px; display:block; object-fit:contain;" alt="ensIIE">
                <div class="topbar-divider"></div>
                <span class="floor-badge">Étage R+1</span>
                <div class="topbar-divider"></div>
                <span style="font-size:12px; color:#38bdf8; font-weight:600; display:flex; align-items:center; gap:7px;">
                    📍 GPS : Hall Principal
                </span>
            </div>

            <div id="topbar-right">
                <!-- PMR accessibility toggle -->
                <button id="btn-pmr" class="pmr-btn" title="Activer / Désactiver le guidage adapté PMR (ascenseurs, accès plain-pied)">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <circle cx="12" cy="4" r="2"/>
                        <path d="M10 9h4l1.5 5H17a1 1 0 0 1 0 2h-2l-.5-2H9.5l-.5 2H7a1 1 0 0 1 0-2h1.5L10 9z"/>
                        <path d="M8 14.5c0 2.5 2 4.5 4 5.5 2-1 4-3 4-5.5" stroke="currentColor" stroke-width="1.5" fill="none"/>
                    </svg>
                    <span>Mobilité Réduite (PMR)</span>
                </button>

                <!-- Reset cam -->
                <div class="icon-btn" id="btn-reset" title="Recentrer la vue 3D">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L12 6M12 18L12 22M2 12L6 12M18 12L22 12"/>
                        <circle cx="12" cy="12" r="4"/>
                    </svg>
                </div>
            </div>
        </div>

        <!-- Tooltip -->
        <div id="tooltip"></div>

        <!-- Legend overlay with totally distinct colors -->
        <div id="legend">
            <div class="leg-item"><div class="leg-dot" style="background:#ef4444;"></div>Amphi</div>
            <div class="leg-item"><div class="leg-dot" style="background:#06b6d4;"></div>TP</div>
            <div class="leg-item"><div class="leg-dot" style="background:#f97316;"></div>TD</div>
            <div class="leg-item"><div class="leg-dot" style="background:#10b981;"></div>Bureau</div>
            <div class="leg-item"><div class="leg-dot" style="background:#a855f7;"></div>Rotonde</div>
            <div class="leg-item"><div class="leg-dot" style="background:#eab308;"></div>Profs</div>
            <div class="leg-sep"></div>
            <div class="leg-item" style="font-size:10px; color:var(--text2);">Clic: Sélection · Molette: Zoom</div>
        </div>
    </div>

</div><!-- /app -->

<!-- Lightbox -->
<div id="lightbox" onclick="this.classList.remove('open')">
    <img id="lightbox-img" src="" alt="">
</div>

<!-- Embedded Data -->
<script>
    const SALLES = {json.dumps(salles_data, ensure_ascii=False)};
    const GRAPH  = {json.dumps(graph_data, ensure_ascii=False)};
</script>

<!-- Main App Script -->
<script>
'use strict';

// State
let activeFilter = 'all';
let selectedRoom = null;
let routeMesh = null;
let pmrMode = false;

// Three.js Elements
let scene, camera, renderer, controls, raycaster, mouse;
let hoveredMesh = null;
const roomMeshMap = new Map();
const labelSprites = [];
let gpsRing, gpsSprite;

// ── TOTALLY DISTINCT CATEGORY COLORS ─────────────────────────────────────────
const CAT_COLORS = {{
    amphi:       0xef4444, // Rouge vif (101, 102, 123)
    tp:          0x06b6d4, // Cyan / Turquoise électrique (127, 130, 131, 133)
    td:          0xf97316, // Orange vif (121, 122, 126, 135, 136, 138, 139, 141, 148, 149)
    bureau:      0x10b981, // Vert Émeraude (18 bureaux)
    rotonde:     0xa855f7, // Violet Royal (103)
    salle_profs: 0xeab308, // Jaune Or lumineux (115)
    technique:   0x475569, // Gris Foncé Ardoise (116, 129, 137, 140, 142)
    depot:       0x9ca3af, // Gris Argenté (124, 125, 128, 132, 134, 150)
    autre:       0xec4899  // Rose / Magenta
}};

const CAT_HEX = {{
    amphi:       '#ef4444',
    tp:          '#06b6d4',
    td:          '#f97316',
    bureau:      '#10b981',
    rotonde:     '#a855f7',
    salle_profs: '#eab308',
    technique:   '#475569',
    depot:       '#9ca3af',
    autre:       '#ec4899'
}};

const CAT_HEIGHT = {{
    amphi: 4.2, tp: 3.5, td: 3.0,
    bureau: 2.6, rotonde: 5.0, salle_profs: 2.8,
    technique: 2.4, depot: 2.2, autre: 2.8
}};

function initThree() {{
    const canvas = document.getElementById('canvas-3d');
    const vp = document.getElementById('viewport');

    renderer = new THREE.WebGLRenderer({{ canvas, antialias: true, alpha: true }});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    resize();

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(40, (vp.clientWidth || window.innerWidth - 360) / (vp.clientHeight || window.innerHeight), 0.1, 1000);
    camera.position.set(32, 65, 55);

    controls = new THREE.OrbitControls(camera, canvas);
    controls.target.set(32, 0, -30);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.minDistance = 15;
    controls.maxDistance = 220;
    controls.maxPolarAngle = Math.PI / 2.15;
    controls.update();

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    const ambient = new THREE.AmbientLight(0xffffff, 0.65);
    scene.add(ambient);

    const sun = new THREE.DirectionalLight(0xffffff, 0.85);
    sun.position.set(45, 90, 45);
    sun.castShadow = true;
    scene.add(sun);

    const fill = new THREE.DirectionalLight(0x93c5fd, 0.35);
    fill.position.set(-45, 30, -45);
    scene.add(fill);

    const floorGeo = new THREE.PlaneGeometry(240, 240);
    const floorMat = new THREE.MeshStandardMaterial({{
        color: 0x090d16,
        roughness: 0.95,
        metalness: 0.0
    }});
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -0.05;
    floor.receiveShadow = true;
    scene.add(floor);

    buildRoomsAndLabels();
    buildGpsMarker();

    canvas.addEventListener('mousemove', onMouseMove);
    canvas.addEventListener('click', onCanvasClick);
    window.addEventListener('resize', resize);

    animate();
}}

function resize() {{
    const vp = document.getElementById('viewport');
    if (!vp || !renderer) return;
    const w = vp.clientWidth || (window.innerWidth - 360);
    const h = vp.clientHeight || window.innerHeight;
    renderer.setSize(w, h);
    if (camera) {{
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    }}
}}

function animate() {{
    requestAnimationFrame(animate);
    controls.update();

    const t = Date.now() * 0.004;
    if (gpsRing) {{
        const s = 1.0 + 0.22 * Math.sin(t);
        gpsRing.scale.set(s, s, 1);
        gpsRing.material.opacity = 0.5 + 0.3 * Math.cos(t);
    }}
    if (gpsSprite) {{
        gpsSprite.position.y = 4.2 + 0.15 * Math.sin(t * 0.8);
    }}

    renderer.render(scene, camera);
}}

// ── Build 3D Rooms & Labels ──────────────────────────────────────────────────
function buildRoomsAndLabels() {{
    SALLES.forEach(room => {{
        const poly = room.polygon;
        if (!poly || poly.length < 3) return;

        const shape = new THREE.Shape();
        poly.forEach(([x, y], idx) => {{
            if (idx === 0) shape.moveTo(x, y);
            else shape.lineTo(x, y);
        }});
        shape.closePath();

        const h = CAT_HEIGHT[room.categorie] || 3.0;
        const geo = new THREE.ExtrudeGeometry(shape, {{
            depth: h,
            bevelEnabled: false
        }});

        const baseColor = CAT_COLORS[room.categorie] || 0xf97316;
        const mat = new THREE.MeshStandardMaterial({{
            color: baseColor,
            emissive: baseColor,
            emissiveIntensity: 0.08,
            roughness: 0.5,
            metalness: 0.12,
            transparent: true,
            opacity: 0.90
        }});

        const mesh = new THREE.Mesh(geo, mat);
        mesh.rotation.x = -Math.PI / 2;
        mesh.position.y = 0;
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        mesh.userData = {{ room, baseColor, defaultOpacity: 0.90 }};
        scene.add(mesh);
        roomMeshMap.set(room.id, mesh);

        const sprite = createRoomLabelSprite(room, h);
        if (sprite) {{
            scene.add(sprite);
            labelSprites.push(sprite);
        }}
    }});
}}

function createRoomLabelSprite(room, roomHeight) {{
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 128;
    const ctx = canvas.getContext('2d');

    const catColorHex = CAT_HEX[room.categorie] || '#f97316';
    ctx.fillStyle = 'rgba(10, 14, 26, 0.88)';
    ctx.strokeStyle = catColorHex;
    ctx.lineWidth = 4;
    drawRoundRect(ctx, 6, 6, 244, 116, 20, true, true);

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 44px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    let title = room.numero;
    let subtitle = room.categorie_nom;
    if (room.categorie === 'amphi') subtitle = 'Amphithéâtre';
    else if (room.categorie === 'tp') subtitle = 'TP Info';
    else if (room.categorie === 'td') subtitle = 'Salle TD';
    else if (room.categorie === 'bureau') subtitle = 'Bureau';
    else if (room.categorie === 'rotonde') {{ title = '103'; subtitle = 'Rotonde'; }}
    else if (room.categorie === 'salle_profs') {{ subtitle = 'Professeurs'; }}

    ctx.fillText(title, 128, 48);
    ctx.font = '600 20px Inter, sans-serif';
    ctx.fillStyle = catColorHex;
    ctx.fillText(subtitle, 128, 92);

    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter;
    const material = new THREE.SpriteMaterial({{
        map: texture,
        depthTest: false,
        transparent: true
    }});
    const sprite = new THREE.Sprite(material);
    const [cx, cy] = room.center;
    sprite.position.set(cx, roomHeight + 0.8, -cy);
    sprite.scale.set(3.4, 1.7, 1);
    sprite.userData = {{ room }};
    return sprite;
}}

function drawRoundRect(ctx, x, y, w, h, r, fill, stroke) {{
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
    if (fill) ctx.fill();
    if (stroke) ctx.stroke();
}}

// ── Build GPS Marker ("VOUS ÊTES ICI") ───────────────────────────────────────
function buildGpsMarker() {{
    const gx = 39.0;
    const gz = -18.5;

    const ringGeo = new THREE.RingGeometry(1.2, 1.6, 32);
    const ringMat = new THREE.MeshBasicMaterial({{
        color: 0x38bdf8,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.75
    }});
    gpsRing = new THREE.Mesh(ringGeo, ringMat);
    gpsRing.rotation.x = -Math.PI / 2;
    gpsRing.position.set(gx, 0.1, gz);
    scene.add(gpsRing);

    const dotGeo = new THREE.CircleGeometry(0.55, 32);
    const dotMat = new THREE.MeshBasicMaterial({{ color: 0x0284c7, side: THREE.DoubleSide }});
    const dot = new THREE.Mesh(dotGeo, dotMat);
    dot.rotation.x = -Math.PI / 2;
    dot.position.set(gx, 0.12, gz);
    scene.add(dot);

    const canvas = document.createElement('canvas');
    canvas.width = 300;
    canvas.height = 96;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#0284c7';
    drawRoundRect(ctx, 4, 4, 292, 88, 16, true, false);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 30px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('📍 VOUS ÊTES ICI', 150, 48);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMat = new THREE.SpriteMaterial({{ map: texture, depthTest: false }});
    gpsSprite = new THREE.Sprite(spriteMat);
    gpsSprite.position.set(gx, 4.2, gz);
    gpsSprite.scale.set(4.6, 1.5, 1);
    scene.add(gpsSprite);
}}

// ── Mouse & Interaction ──────────────────────────────────────────────────────
function getIntersect(event) {{
    const vp = document.getElementById('viewport');
    const rect = vp.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width)  * 2 - 1;
    mouse.y = -((event.clientY - rect.top)  / rect.height) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);

    const meshes = [...roomMeshMap.values()].filter(m => m.visible);
    const meshHits = raycaster.intersectObjects(meshes, false);
    if (meshHits.length > 0) return meshHits[0].object;

    const visibleSprites = labelSprites.filter(s => s.visible);
    const spriteHits = raycaster.intersectObjects(visibleSprites, false);
    if (spriteHits.length > 0) return spriteHits[0].object;

    return null;
}}

function onMouseMove(event) {{
    const hit = getIntersect(event);
    const tip = document.getElementById('tooltip');
    const vp  = document.getElementById('viewport');
    const rect = vp.getBoundingClientRect();

    if (hoveredMesh && hoveredMesh !== selectedRoom?.mesh) resetStyle(hoveredMesh);

    if (hit) {{
        hoveredMesh = hit;
        const room = hit.userData.room;
        if (hit.isMesh && hit !== selectedRoom?.mesh) {{
            hit.material.emissive.setHex(0xffffff);
            hit.material.emissiveIntensity = 0.25;
        }}
        tip.style.display = 'block';
        tip.style.left = (event.clientX - rect.left + 14) + 'px';
        tip.style.top  = (event.clientY - rect.top  - 32) + 'px';
        tip.textContent = room ? room.nom : '';
    }} else {{
        hoveredMesh = null;
        tip.style.display = 'none';
    }}
}}

function onCanvasClick() {{
    if (hoveredMesh && hoveredMesh.userData.room) {{
        selectRoom(hoveredMesh.userData.room);
    }}
}}

function resetStyle(mesh) {{
    if (!mesh || !mesh.isMesh) return;
    mesh.material.emissive.setHex(mesh.userData.baseColor);
    mesh.material.emissiveIntensity = 0.08;
    mesh.material.opacity = mesh.userData.defaultOpacity;
}}

// ── Room Selection ───────────────────────────────────────────────────────────
function selectRoom(room) {{
    if (selectedRoom?.mesh) resetStyle(selectedRoom.mesh);
    const mesh = roomMeshMap.get(room.id);
    selectedRoom = {{ data: room, mesh }};

    if (mesh) {{
        mesh.material.emissive.setHex(0xffffff);
        mesh.material.emissiveIntensity = 0.65;
        mesh.material.opacity = 0.98;
        const [cx, cy] = room.center;
        controls.target.set(cx, 0, -cy);
    }}

    switchTab('salles');
    updateRoomDetails(room);
    document.getElementById('select-end').value = room.id;
    highlightDirectoryRow(room.id);
}}

function deselectRoom() {{
    if (selectedRoom?.mesh) resetStyle(selectedRoom.mesh);
    selectedRoom = null;
    document.getElementById('room-details-card').style.display = 'none';
    document.getElementById('btn-close-fiche').style.display = 'none';
    highlightDirectoryRow(null);
}}

function highlightDirectoryRow(roomId) {{
    document.querySelectorAll('.room-row').forEach(row => {{
        row.classList.toggle('active', row.dataset.id === roomId);
    }});
}}

function routeToCurrentRoom() {{
    if (!selectedRoom) return;
    switchTab('itineraire');
    document.getElementById('select-end').value = selectedRoom.data.id;
    const startId = document.getElementById('select-start').value;
    calcRoute(startId, selectedRoom.data.id);
}}

function updateRoomDetails(room) {{
    const card = document.getElementById('room-details-card');
    card.style.display = 'block';
    document.getElementById('btn-close-fiche').style.display = 'inline-block';

    const photoWrap = document.getElementById('room-photo-wrap');
    const photoImg  = document.getElementById('room-photo');
    if (room.image) {{
        photoImg.src = room.image;
        photoWrap.style.display = 'block';
        photoWrap.onclick = () => {{
            document.getElementById('lightbox-img').src = room.image;
            document.getElementById('lightbox').classList.add('open');
        }};
    }} else {{
        photoWrap.style.display = 'none';
    }}

    document.getElementById('room-name').textContent = room.nom;
    document.getElementById('room-type').textContent = `${{room.categorie_nom}} · Étage R+1`;

    const badge = document.getElementById('room-status');
    const badgeTxt = document.getElementById('room-status-text');
    badge.style.display = 'inline-flex';
    if (room.actuellement_libre) {{
        badge.className = 'status-badge libre';
        badgeTxt.textContent = 'Libre';
    }} else {{
        badge.className = 'status-badge occupe';
        badgeTxt.textContent = 'Occupé';
    }}

    document.getElementById('room-surface').textContent  = room.surface ? room.surface + ' m²' : '—';
    document.getElementById('room-capacity').textContent = room.capacite || '—';

    const occ = document.getElementById('occupant-card');
    if (room.categorie === 'bureau' && room.occupant) {{
        occ.style.display = 'block';
        document.getElementById('occupant-name').textContent = room.occupant.responsable;
        document.getElementById('occupant-role').textContent = room.occupant.role;
    }} else {{
        occ.style.display = 'none';
    }}

    const sched = document.getElementById('schedule');
    sched.innerHTML = '';
    (room.planning || []).forEach(slot => {{
        const isCur  = slot.actuel;
        const isFree = ['Libre','Accès libre'].includes(slot.statut);
        const div = document.createElement('div');
        div.className = 'sched-item' + (isCur ? ' current' : '') + (isFree ? ' free' : '');
        div.innerHTML = `
            <div class="sched-row">
                <span class="sched-time">${{slot.heure}}</span>
                <span class="sched-status" style="color:${{isFree ? '#10b981' : isCur ? '#ef4444' : '#94a3b8'}}">${{slot.statut}}</span>
            </div>
            <div class="sched-desc">${{slot.titre}}</div>
        `;
        sched.appendChild(div);
    }});
}}

// ── Room Directory List ──────────────────────────────────────────────────────
function buildRoomDirectory(filteredRooms) {{
    const dir = document.getElementById('room-directory');
    dir.innerHTML = '';
    filteredRooms.forEach(room => {{
        const row = document.createElement('div');
        row.className = 'room-row' + (selectedRoom?.data?.id === room.id ? ' active' : '');
        row.dataset.id = room.id;
        const color = CAT_HEX[room.categorie] || '#f97316';
        row.innerHTML = `
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="width:8px; height:8px; border-radius:2px; background:${{color}}; flex-shrink:0;"></span>
                <span style="font-size:12px; font-weight:700; color:var(--text);">${{room.nom}}</span>
            </div>
            <span class="room-tag" style="background:${{color}}22; color:${{color}};">${{room.categorie_nom}}</span>
        `;
        row.onclick = () => selectRoom(room);
        dir.appendChild(row);
    }});
}}

// ── Tabs ─────────────────────────────────────────────────────────────────────
function switchTab(id) {{
    document.querySelectorAll('.tab').forEach(t => {{
        t.classList.toggle('active', t.dataset.tab === id);
    }});
    ['salles','itineraire','infos'].forEach(p => {{
        document.getElementById('pane-' + p).style.display = p === id ? 'flex' : 'none';
    }});
}}

document.querySelectorAll('.tab').forEach(t => {{
    t.addEventListener('click', () => switchTab(t.dataset.tab));
}});

// ── Search & Filter ──────────────────────────────────────────────────────────
document.getElementById('search').addEventListener('input', e => {{
    const q = e.target.value.toLowerCase().trim();
    if (!q) {{ applyFilter(activeFilter); return; }}

    const matches = [];
    SALLES.forEach(room => {{
        const mesh = roomMeshMap.get(room.id);
        const sprite = labelSprites.find(s => s.userData.room.id === room.id);
        if (!mesh) return;

        const match = room.nom.toLowerCase().includes(q)
            || room.numero.includes(q)
            || (room.occupant?.responsable?.toLowerCase().includes(q));

        mesh.visible = match;
        if (sprite) sprite.visible = match;
        if (match) matches.push(room);
    }});

    document.getElementById('room-count').textContent = matches.length + ' espaces trouvés';
    buildRoomDirectory(matches);
    if (matches.length > 0) selectRoom(matches[0]);
}});

document.querySelectorAll('.chip').forEach(chip => {{
    chip.addEventListener('click', () => {{
        document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        activeFilter = chip.dataset.filter;
        applyFilter(activeFilter);
    }});
}});

function applyFilter(filter) {{
    const list = [];
    SALLES.forEach(room => {{
        const mesh = roomMeshMap.get(room.id);
        const sprite = labelSprites.find(s => s.userData.room.id === room.id);
        if (!mesh) return;

        const vis = filter === 'all' ? true
            : filter === 'libre' ? room.actuellement_libre
            : room.categorie === filter;

        mesh.visible = vis;
        if (sprite) sprite.visible = vis;
        if (vis) list.push(room);
    }});
    document.getElementById('room-count').textContent = list.length + ' espaces';
    buildRoomDirectory(list);
}}

// ── PMR Accessibility Toggle ─────────────────────────────────────────────────
document.getElementById('btn-pmr').addEventListener('click', () => {{
    pmrMode = !pmrMode;
    const btn = document.getElementById('btn-pmr');
    btn.classList.toggle('active', pmrMode);

    const note = document.getElementById('pmr-note');
    if (pmrMode) {{
        note.textContent = "♿ Mode PMR actif : Trajet adapté via l'ascenseur R+1, évitement d'escaliers.";
        document.getElementById('select-start').value = 'ASCENSEUR';
    }} else {{
        note.textContent = "Mode standard : escaliers et couloirs piétons.";
        document.getElementById('select-start').value = 'VOUS_ETES_ICI';
    }}

    if (routeMesh) {{
        const s = document.getElementById('select-start').value;
        const e = document.getElementById('select-end').value;
        calcRoute(s, e);
    }}
}});

// ── Reset Cam ────────────────────────────────────────────────────────────────
document.getElementById('btn-reset').addEventListener('click', () => {{
    controls.target.set(32, 0, -30);
    camera.position.set(32, 65, 55);
}});

// ── Dropdowns ────────────────────────────────────────────────────────────────
function populateDropdowns() {{
    const s = document.getElementById('select-start');
    const e = document.getElementById('select-end');
    s.innerHTML = e.innerHTML = '';

    const entrances = [
        ['VOUS_ETES_ICI', '📍 Vous êtes ici (Hall Principal)'],
        ['ESCALIER_SUD',  '🪜 Escalier Principal (Sud)'],
        ['ASCENSEUR',     '🛗 Ascenseur R+1 (Accès PMR)'],
        ['103',           '🏛️ Rotonde 103 (Carrefour central)']
    ];
    entrances.forEach(([id, nom]) => {{
        s.innerHTML += `<option value="${{id}}">${{nom}}</option>`;
    }});

    SALLES.forEach(r => {{
        s.innerHTML += `<option value="${{r.id}}">${{r.nom}}</option>`;
        e.innerHTML += `<option value="${{r.id}}">${{r.nom}}</option>`;
    }});

    s.value = 'VOUS_ETES_ICI';
    e.value = '101';
}}

// ── Dijkstra Routing & Turn-by-Turn Engine ──────────────────────────────────
document.getElementById('btn-route').addEventListener('click', () => {{
    const startId = document.getElementById('select-start').value;
    const endId   = document.getElementById('select-end').value;
    calcRoute(startId, endId);
}});

document.getElementById('clear-route').addEventListener('click', () => {{
    if (routeMesh) {{ scene.remove(routeMesh); routeMesh.geometry.dispose(); routeMesh = null; }}
    document.getElementById('route-summary').classList.remove('visible');
    document.getElementById('route-steps-container').innerHTML = '';
    document.getElementById('clear-route').style.display = 'none';
}});

function getCorridorNode(roomId) {{
    if (roomId === 'VOUS_ETES_ICI') {{
        return pmrMode ? 'ASCENSEUR' : 'ESCALIER_SUD';
    }}
    const access = GRAPH.room_access;
    if (access && access[roomId]) return access[roomId];

    const room = SALLES.find(r => r.id === roomId);
    const coord = room ? room.center : null;
    if (!coord) return null;

    let best = null, bestD = Infinity;
    Object.entries(GRAPH.nodes).forEach(([name, nd]) => {{
        const d = Math.hypot(nd.x - coord[0], nd.y - coord[1]);
        if (d < bestD) {{ bestD = d; best = name; }}
    }});
    return best;
}}

function calcRoute(startId, endId) {{
    const startNode = getCorridorNode(startId);
    const endNode   = getCorridorNode(endId);
    if (!startNode || !endNode) return;

    const path = dijkstra(startNode, endNode);
    if (!path.length) return;

    const pts3D = path.map(n => {{
        const nd = GRAPH.nodes[n];
        return new THREE.Vector3(nd.x, 0.45, -nd.y);
    }});

    if (routeMesh) {{ scene.remove(routeMesh); routeMesh.geometry.dispose(); }}

    const curve = new THREE.CatmullRomCurve3(pts3D);
    curve.curveType = 'catmullrom';
    curve.tension = 0.15; // tighter curve to stay strictly in corridors

    const geo = new THREE.TubeGeometry(curve, pts3D.length * 8, 0.25, 8, false);
    const mat = new THREE.MeshStandardMaterial({{
        color: 0x38bdf8,
        emissive: 0x0284c7,
        emissiveIntensity: 1.1,
        roughness: 0.15,
        metalness: 0.8
    }});
    routeMesh = new THREE.Mesh(geo, mat);
    scene.add(routeMesh);

    let dist = 0;
    for (let i = 0; i < pts3D.length - 1; i++) dist += pts3D[i].distanceTo(pts3D[i+1]);
    const secs = Math.round(dist / 1.2);

    document.getElementById('route-dist').textContent = `Distance : ${{Math.round(dist)}} mètres`;
    document.getElementById('route-time').textContent  = `Temps : ~${{secs < 60 ? secs + ' sec' : Math.ceil(secs/60) + ' min à pied'}}`;
    document.getElementById('route-pmr-badge').style.display = pmrMode ? 'block' : 'none';
    document.getElementById('route-summary').classList.add('visible');
    document.getElementById('clear-route').style.display = 'block';

    // Generate Turn-by-Turn Guidance Cards
    renderTurnByTurnSteps(path, startId, endId);
}}

function dijkstra(start, target) {{
    const nodes = GRAPH.nodes;
    const dist  = {{}};
    const prev  = {{}};
    const q     = new Set(Object.keys(nodes));
    q.forEach(n => dist[n] = Infinity);
    dist[start] = 0;

    while (q.size) {{
        let u = null;
        q.forEach(n => {{ if (u === null || dist[n] < dist[u]) u = n; }});
        if (u === target || dist[u] === Infinity) break;
        q.delete(u);
        (nodes[u].voisins || []).forEach(edge => {{
            if (q.has(edge.node)) {{
                const alt = dist[u] + edge.dist;
                if (alt < dist[edge.node]) {{ dist[edge.node] = alt; prev[edge.node] = u; }}
            }}
        }});
    }}

    const path = [];
    let cur = target;
    while (cur) {{ path.unshift(cur); cur = prev[cur]; }}
    return path;
}}

// ── Turn-by-Turn Guidance Engine ─────────────────────────────────────────────
function renderTurnByTurnSteps(path, startId, endId) {{
    const container = document.getElementById('route-steps-container');
    container.innerHTML = '';

    const startRoom = SALLES.find(r => r.id === startId);
    const endRoom   = SALLES.find(r => r.id === endId);
    const startName = startId === 'VOUS_ETES_ICI' ? 'Vous êtes ici (Hall Principal)' 
                    : startId === 'ASCENSEUR' ? 'Ascenseur R+1' 
                    : startRoom ? startRoom.nom : GRAPH.nodes[path[0]].nom;
    const endName = endRoom ? endRoom.nom : GRAPH.nodes[path[path.length - 1]].nom;

    // Step 1: Start
    addStepCard(container, 'start', '📍', 'Départ', `Départ depuis : ${{startName}}`, null);

    if (path.length > 1) {{
        let prevHeading = null;
        for (let i = 0; i < path.length - 1; i++) {{
            const u = GRAPH.nodes[path[i]];
            const v = GRAPH.nodes[path[i+1]];
            const dx = v.x - u.x;
            const dy = v.y - u.y;
            const segDist = Math.max(1, Math.round(Math.hypot(dx, dy)));
            const heading = Math.atan2(dy, dx);

            if (prevHeading === null) {{
                addStepCard(container, 'straight', '⬆️', 'Continuer tout droit', `S'engager dans le couloir vers ${{v.nom}}`, segDist);
            }} else {{
                let diff = heading - prevHeading;
                while (diff > Math.PI) diff -= 2 * Math.PI;
                while (diff < -Math.PI) diff += 2 * Math.PI;
                const deg = diff * 180 / Math.PI;

                if (deg > 25 && deg <= 160) {{
                    addStepCard(container, 'left', '↰', 'Tourner à gauche', `Dans le couloir vers ${{v.nom}}`, segDist);
                }} else if (deg < -25 && deg >= -160) {{
                    addStepCard(container, 'right', '↱', 'Tourner à droite', `Dans le couloir vers ${{v.nom}}`, segDist);
                }} else {{
                    addStepCard(container, 'straight', '⬆️', 'Continuer tout droit', `Poursuivre vers ${{v.nom}}`, segDist);
                }}
            }}
            prevHeading = heading;
        }}
    }}

    // Final Step: Arrival
    addStepCard(container, 'dest', '🎯', 'Arrivée', `Vous êtes arrivé devant : ${{endName}}`, null);
}}

function addStepCard(container, type, icon, action, desc, dist) {{
    const div = document.createElement('div');
    div.className = 'step-card';
    div.innerHTML = `
        <div class="step-icon ${{type}}">${{icon}}</div>
        <div class="step-content">
            <div class="step-action">${{action}}</div>
            <div class="step-desc">${{desc}}</div>
        </div>
        ${{dist !== null ? `<div class="step-dist">${{dist}} m</div>` : ''}}
    `;
    container.appendChild(div);
}}

// ── App Initialization & Welcome Flow ────────────────────────────────────────
function enterPlan() {{
    const modal = document.getElementById('welcome-modal');
    if (modal) {{
        modal.classList.add('hidden');
        setTimeout(() => {{ modal.style.display = 'none'; }}, 600);
    }}
    setTimeout(() => {{
        if (typeof resize === 'function') resize();
    }}, 150);
}}

function initApp() {{
    try {{
        initThree();
        populateDropdowns();
        buildRoomDirectory(SALLES);
        console.log('3D scene, directory & navigation initialized successfully');
    }} catch(err) {{
        console.error('3D init error:', err);
    }}
}}

if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', initApp);
}} else {{
    initApp();
}}

const btnEnterEl = document.getElementById('btn-enter');
if (btnEnterEl) {{
    btnEnterEl.onclick = enterPlan;
}}
</script>
</body>
</html>
"""

# Write to build_app.py
with open('c:/Users/21270/OneDrive/Desktop/hackathon/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("index.html generated successfully!")
