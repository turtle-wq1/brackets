import streamlit as st
import math
import re

st.set_page_config(page_title="Bracket Maker", page_icon="🏆", layout="wide", initial_sidebar_state="collapsed")

# ═══════════════════════════ CSS ═══════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --gold:#E8B84B; --gold-dim:rgba(232,184,75,.15); --gold-glow:rgba(232,184,75,.35);
  --dark:#080C14; --surface:#0F1623; --panel:#141D2E; --panel2:#1A2540;
  --accent:#3B82F6; --accent2:#60A5FA;
  --green:#22C55E; --green-dim:rgba(34,197,94,.15);
  --purple:#A855F7; --purple-dim:rgba(168,85,247,.2);
  --red:#EF4444;
  --text:#E2E8F0; --muted:#64748B; --border:#1E2D45;
  --match-w:148px; --match-h:58px;
}

html,body,[data-testid="stAppViewContainer"]{background:var(--dark)!important;color:var(--text);font-family:'Inter',sans-serif;}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;}

/* scrollbar */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--dark)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}

/* HERO */
.hero{text-align:center;padding:2.5rem 0 1.5rem;position:relative}
.hero-title{font-family:'Oswald',sans-serif;font-size:clamp(2.8rem,6vw,5rem);font-weight:700;
  color:transparent;background:linear-gradient(135deg,#E8B84B 0%,#FDE68A 45%,#E8B84B 100%);
  -webkit-background-clip:text;background-clip:text;letter-spacing:6px;line-height:1;
  text-shadow:none;filter:drop-shadow(0 0 30px rgba(232,184,75,.4));}
.hero-sub{color:var(--muted);font-size:.75rem;letter-spacing:4px;text-transform:uppercase;margin-top:.4rem}
.hero-line{width:80px;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);
  margin:.8rem auto 0}

/* TABS */
div[data-baseweb="tab-list"]{background:var(--surface)!important;border-radius:10px!important;
  padding:3px!important;border:1px solid var(--border)!important;gap:2px!important}
div[data-baseweb="tab"]{font-family:'Oswald',sans-serif!important;font-size:1rem!important;
  letter-spacing:2px!important;color:var(--muted)!important;border-radius:7px!important;
  padding:.4rem 1.4rem!important;transition:all .2s!important}
div[aria-selected="true"][data-baseweb="tab"]{
  background:linear-gradient(135deg,#E8B84B,#F59E0B)!important;
  color:#080C14!important;font-weight:600!important}

/* BUTTONS */
.stButton>button{background:linear-gradient(135deg,#E8B84B,#F59E0B)!important;color:#080C14!important;
  font-family:'Oswald',sans-serif!important;font-size:1rem!important;letter-spacing:2px!important;
  border:none!important;border-radius:8px!important;padding:.5rem 1.8rem!important;
  transition:all .2s!important;font-weight:600!important}
.stButton>button:hover{transform:translateY(-1px)!important;
  box-shadow:0 6px 20px rgba(232,184,75,.4)!important}
.stButton>button.secondary{background:var(--panel2)!important;color:var(--muted)!important;
  border:1px solid var(--border)!important}

/* INPUTS */
.stTextInput>div>div>input,.stTextArea>div>div>textarea,
.stNumberInput>div>div>input,.stSelectbox>div>div{
  background:var(--panel)!important;border:1px solid var(--border)!important;
  color:var(--text)!important;border-radius:8px!important;font-family:'Inter',sans-serif!important}
.stTextArea>div>div>textarea{font-size:.85rem!important}
label{color:var(--muted)!important;font-size:.8rem!important;letter-spacing:.5px!important}

/* TOGGLES / RADIO */
.stRadio>div{gap:.5rem}
.stRadio>div>label{background:var(--panel)!important;border:1px solid var(--border)!important;
  border-radius:8px!important;padding:.4rem .9rem!important;font-size:.8rem!important;cursor:pointer}
[data-testid="stToggle"]>label{color:var(--text)!important;font-size:.85rem!important}

/* ══════════════ BRACKET SVG CANVAS ══════════════ */
.bracket-outer{overflow-x:auto;overflow-y:hidden;padding:1rem 0 1.5rem}
.bracket-canvas{position:relative;display:inline-block}

/* match card */
.bm{position:absolute;width:var(--match-w);cursor:default;
  border-radius:7px;overflow:hidden;border:1px solid var(--border);
  background:var(--panel);box-shadow:0 2px 12px rgba(0,0,0,.5);
  transition:border-color .2s,box-shadow .2s}
.bm:hover{border-color:var(--accent);box-shadow:0 4px 20px rgba(59,130,246,.2)}
.bm.bye-card{border-color:#1A2E1A;opacity:.65}
.bm.playin-card{border-color:var(--purple)}
.bm.final-card{border-color:var(--gold);box-shadow:0 0 24px rgba(232,184,75,.25)}

/* team row inside card */
.ts{height:29px;display:flex;align-items:center;padding:0 8px;gap:5px;
  font-size:.72rem;font-family:'Inter',sans-serif;overflow:hidden;
  border-bottom:1px solid var(--border);transition:background .15s}
.ts:last-child{border-bottom:none}
.ts.tw{background:var(--green-dim)!important;color:var(--green)!important;font-weight:600}
.ts.tt{color:var(--muted);font-style:italic}
.ts.tb{background:rgba(20,40,20,.4);color:#3A5A3A;font-style:italic}
.ts:not(.tw):not(.tt):not(.tb):hover{background:var(--gold-dim)}

/* seed pill */
.sd{min-width:18px;height:16px;background:var(--gold-dim);color:var(--gold);
  font-size:.6rem;font-weight:700;border-radius:3px;text-align:center;
  line-height:16px;flex-shrink:0;padding:0 3px}

/* round header above column */
.rh{position:absolute;font-family:'Oswald',sans-serif;font-size:.7rem;
  letter-spacing:2px;color:var(--gold);text-align:center;top:0;
  text-transform:uppercase;pointer-events:none}
.rh.playin-rh{color:var(--purple)}

/* connector lines drawn via SVG overlay */
.bracket-svg{position:absolute;top:0;left:0;pointer-events:none;overflow:visible}

/* champion card (centered, larger) */
.champ-card{margin:1.2rem auto;max-width:260px;
  background:linear-gradient(135deg,#1A1500,#0F1000);
  border:2px solid var(--gold);border-radius:14px;
  padding:1.2rem 2rem;text-align:center;
  box-shadow:0 0 50px rgba(232,184,75,.25),0 0 100px rgba(232,184,75,.1)}
.champ-card .ct{font-size:2rem}
.champ-card .cl{font-family:'Oswald',sans-serif;letter-spacing:4px;
  color:var(--gold);font-size:.85rem;margin-top:.2rem}
.champ-card .cn{font-size:1.2rem;font-weight:600;color:var(--text);margin-top:.3rem}

/* playin section */
.playin-header{font-family:'Oswald',sans-serif;font-size:.85rem;letter-spacing:3px;
  color:var(--purple);text-align:center;margin:.5rem 0}

/* section label */
.slabel{font-family:'Oswald',sans-serif;font-size:1.2rem;letter-spacing:3px;
  color:var(--text);margin:.8rem 0 .4rem}
.rbadge{font-family:'Oswald',sans-serif;font-size:1.1rem;letter-spacing:3px;
  padding-bottom:3px;border-bottom:2px solid;display:inline-block;margin-bottom:.6rem}

/* info callout */
.info-box{background:var(--gold-dim);border:1px solid rgba(232,184,75,.25);
  border-radius:7px;padding:.5rem .9rem;font-size:.78rem;color:var(--muted);margin-bottom:.7rem}

.divider{border:none;border-top:1px solid var(--border);margin:1.4rem 0}

/* NCAA 4-quadrant layout */
.ncaa-wrap{display:flex;align-items:center;justify-content:center;gap:0;overflow-x:auto;padding:1rem}
.ncaa-left,.ncaa-right{display:flex;flex-direction:row;gap:0}
.ncaa-left{flex-direction:row-reverse}
.ncaa-mid{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;min-width:180px}

/* advance button row under card (invisible until hover) */
.adv-row{display:flex;flex-direction:column;gap:2px;margin-top:2px}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════ LOGIC ═══════════════════════════

def npow2(n):
    return 1 if n <= 1 else 2 ** math.ceil(math.log2(n))

def seeded_pairs(ts):
    n, pairs = len(ts), []
    lo, hi = 0, n-1
    while lo < hi:
        pairs.append((ts[lo], ts[hi])); lo += 1; hi -= 1
    if lo == hi: pairs.append((ts[lo], None))
    return pairs

def mk(t1, t2):
    def nm(e): return "BYE" if e is None else e[1]
    def sd(e): return None if e is None else (e[0] if e[0] < 900 else None)
    m = {"team1":nm(t1),"seed1":sd(t1),"team2":nm(t2),"seed2":sd(t2),
         "winner":None,"winner_seed":None,"is_bye":False,"is_playin":False}
    if m["team2"]=="BYE": m["winner"]=m["team1"]; m["winner_seed"]=m["seed1"]; m["is_bye"]=True
    elif m["team1"]=="BYE": m["winner"]=m["team2"]; m["winner_seed"]=m["seed2"]; m["is_bye"]=True
    return m

def build_bracket(teams_seeded, use_byes, pi_count):
    """Returns (playin_rounds, main_rounds). Fixes seed-999 / TBD bug."""
    pi_rounds, pi_winners = [], []

    if pi_count > 0:
        pi_teams  = teams_seeded[-pi_count*2:] if pi_count*2 <= len(teams_seeded) else teams_seeded
        main_ts   = teams_seeded[:-len(pi_teams)]
        pi_matches = []
        for i in range(0, len(pi_teams), 2):
            t1 = pi_teams[i]
            t2 = pi_teams[i+1] if i+1 < len(pi_teams) else None
            m  = mk(t1, t2); m["is_playin"] = True
            pi_matches.append(m)
        pi_rounds.append(pi_matches)
        # TBD placeholders for play-in winners — use seed of lower-seeded team, name TBD
        for pm in pi_matches:
            s = min(x for x in [pm["seed1"],pm["seed2"]] if x is not None) if any(x is not None for x in [pm["seed1"],pm["seed2"]]) else 99
            pi_winners.append((s, "TBD"))
    else:
        main_ts = teams_seeded

    all_ts = main_ts + pi_winners
    n = len(all_ts)
    size = npow2(n)

    if use_byes:
        max_s = max((s for s,_ in all_ts), default=0)
        byes  = [(max_s+i+1, "BYE") for i in range(size-n)]
        all_ts = sorted(all_ts + byes, key=lambda x: x[0])
    else:
        # No byes: if still uneven, add play-in for remainder
        if n < size and n > size//2:
            # extra play-ins to fill odd spots — convert bottom pairs into play-ins
            extra_need = size - n  # need this many extra spots from play-ins
            extra_teams = all_ts[-(extra_need*2):]
            all_ts      = all_ts[:-extra_need*2]
            if not pi_rounds:
                pi_rounds.append([])
            for i in range(0, len(extra_teams), 2):
                t1 = extra_teams[i]
                t2 = extra_teams[i+1] if i+1 < len(extra_teams) else None
                m  = mk(t1, t2); m["is_playin"] = True
                pi_rounds[0].append(m)
                s = min(x for x in [m["seed1"],m["seed2"]] if x is not None) if any(x is not None for x in [m["seed1"],m["seed2"]]) else 99
                all_ts.append((s,"TBD"))
        all_ts = sorted(all_ts, key=lambda x: x[0])

    pairs = seeded_pairs(all_ts)
    r1 = [mk(a,b) for a,b in pairs]
    rounds = [r1]
    while len(rounds[-1]) > 1:
        prev, nr = rounds[-1], []
        for i in range(0, len(prev), 2):
            w1 = prev[i]["winner"] or "TBD"
            s1 = prev[i]["winner_seed"]
            if i+1 < len(prev):
                w2 = prev[i+1]["winner"] or "TBD"
                s2 = prev[i+1]["winner_seed"]
            else:
                w2, s2 = "TBD", None
            # Build clean entry — no 999 seeds
            e1 = (s1, w1) if (s1 is not None and w1 not in ("TBD","BYE")) else (None, w1)
            e2 = (s2, w2) if (s2 is not None and w2 not in ("TBD","BYE")) else (None, w2)
            m  = {"team1":e1[1],"seed1":e1[0],"team2":e2[1],"seed2":e2[0],
                  "winner":None,"winner_seed":None,"is_bye":False,"is_playin":False}
            nr.append(m)
        rounds.append(nr)
    return pi_rounds, rounds

def rnd_name(idx, total):
    fe = total-1-idx
    if fe==0: return "FINAL"
    if fe==1: return "SEMIS"
    if fe==2: return "QUARTERS"
    return f"R{2**(fe+1)}"

def parse_teams(raw, use_seeds):
    lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
    result = []
    for i, line in enumerate(lines, 1):
        if use_seeds:
            m = re.match(r'^(\d+)[.\s]\s*(.+)$', line)
            result.append((int(m.group(1)), m.group(2).strip()) if m else (i, line))
        else:
            result.append((i, line))
    return sorted(result, key=lambda x: x[0])

# ═══════════════════════════ SVG BRACKET RENDERER ═══════════════════════════
# We render the bracket as absolutely-positioned HTML divs on a sized canvas,
# with an SVG overlay drawing the connector lines.

CARD_W  = 150   # px
CARD_H  = 58    # px  (two 29px slots)
COL_GAP = 44    # horizontal gap between columns
ROW_HDR = 28    # top space for round label
CARD_GAP_BASE = 8   # minimum vertical gap between cards in R0

def col_x(col_idx):
    return col_idx * (CARD_W + COL_GAP)

def cards_in_col(r_idx, total_rounds, n_r0):
    return max(1, n_r0 // (2**r_idx))

def card_spacing(r_idx, n_r0):
    """Vertical distance between card tops in this round."""
    if r_idx == 0:
        return CARD_H + CARD_GAP_BASE
    return card_spacing(r_idx-1, n_r0) * 2

def card_top(r_idx, m_idx, n_r0):
    sp = card_spacing(r_idx, n_r0)
    first_offset = (sp - CARD_H) / 2   # centre card within its doubled slot
    return ROW_HDR + first_offset + m_idx * sp

def canvas_height(total_rounds, n_r0):
    sp = card_spacing(total_rounds-1, n_r0)
    return ROW_HDR + sp + 20

def canvas_width(total_rounds):
    return total_rounds * CARD_W + (total_rounds-1) * COL_GAP

def slot_html(team, seed, is_win, show_seeds, extra_cls=""):
    is_tbd = team in ("TBD",)
    is_bye = team == "BYE"
    cls = "ts"
    if is_win:   cls += " tw"
    elif is_tbd: cls += " tt"
    elif is_bye: cls += " tb"
    if extra_cls: cls += " " + extra_cls
    sd = f'<span class="sd">{seed}</span>' if show_seeds and seed is not None and not is_tbd and not is_bye else ""
    icon = "🏆 " if is_win else ""
    label = "BYE" if is_bye else ("TBD" if is_tbd else team)
    # truncate long names
    display = label[:18]+"…" if len(label) > 18 else label
    return f'<div class="{cls}" title="{label}">{sd}{icon}{display}</div>'

def render_bracket_html(bkey, pi_rounds, main_rounds, show_seeds=False, reversed_x=False):
    """
    Returns (html_string, advance_buttons_list).
    advance_buttons_list: list of dicts describing buttons to render via st.button.
    reversed_x: flip horizontal direction (for NCAA left side).
    """
    if not main_rounds: return "", []

    n_r0    = len(main_rounds[0])
    total   = len(main_rounds)
    cw      = canvas_width(total)
    ch      = canvas_height(total, n_r0)

    cards_html = []
    svg_lines  = []   # SVG path data segments
    buttons    = []   # {key, label, r_idx, m_idx, slot, team, seed}

    # ── Draw cards + collect connector info ──
    for r_idx, rnd in enumerate(main_rounds):
        xi = (total-1-r_idx) if reversed_x else r_idx
        cx = col_x(xi)
        for m_idx, match in enumerate(rnd):
            ty = card_top(r_idx, m_idx, n_r0)
            t1,s1 = match["team1"], match["seed1"]
            t2,s2 = match["team2"], match["seed2"]
            w      = match["winner"]
            is_bye = match.get("is_bye", False)
            card_cls = "bm"
            if is_bye: card_cls += " bye-card"
            if r_idx == total-1 and total > 1: card_cls += " final-card"

            h1 = slot_html(t1, s1, w==t1 and w is not None, show_seeds)
            h2 = slot_html(t2, s2, w==t2 and w is not None, show_seeds)
            cards_html.append(
                f'<div class="{card_cls}" style="left:{cx}px;top:{ty}px;width:{CARD_W}px">'
                f'{h1}{h2}</div>'
            )

            # Collect advance buttons
            if not w and not is_bye:
                for si,(team,seed) in enumerate([(t1,s1),(t2,s2)]):
                    if team not in ("TBD","BYE"):
                        buttons.append({"key":f"{bkey}_r{r_idx}_m{m_idx}_s{si}",
                                        "label":f"▶ {team[:16]}",
                                        "r_idx":r_idx,"m_idx":m_idx,"slot":si,
                                        "team":team,"seed":seed})

            # ── Connector lines ──
            if r_idx < total-1:
                nx = col_x((total-1-(r_idx+1)) if reversed_x else (r_idx+1))
                child0_y = card_top(r_idx, m_idx*2,   n_r0) + CARD_H/2
                child1_y = card_top(r_idx, m_idx*2+1, n_r0) + CARD_H/2 if m_idx*2+1 < len(main_rounds[r_idx]) else child0_y
                parent_y = ty + CARD_H/2

                if not reversed_x:
                    # right edge of child → left edge of parent
                    c_right = cx + CARD_W
                    p_left  = nx
                    mid_x   = (c_right + p_left) / 2
                    # from card right-mid to midpoint
                    svg_lines.append(f'M{c_right},{child0_y} H{mid_x}')
                    if m_idx*2+1 < len(main_rounds[r_idx]):
                        svg_lines.append(f'M{c_right},{child1_y} H{mid_x}')
                    # vertical at midpoint
                    svg_lines.append(f'M{mid_x},{child0_y} V{child1_y}')
                    # midpoint to parent left
                    svg_lines.append(f'M{mid_x},{parent_y} H{p_left}')
                else:
                    c_left  = cx
                    p_right = nx + CARD_W
                    mid_x   = (c_left + p_right) / 2
                    svg_lines.append(f'M{c_left},{child0_y} H{mid_x}')
                    if m_idx*2+1 < len(main_rounds[r_idx]):
                        svg_lines.append(f'M{c_left},{child1_y} H{mid_x}')
                    svg_lines.append(f'M{mid_x},{child0_y} V{child1_y}')
                    svg_lines.append(f'M{mid_x},{parent_y} H{p_right}')

    # ── Round headers ──
    for r_idx in range(total):
        xi = (total-1-r_idx) if reversed_x else r_idx
        cx = col_x(xi)
        label = rnd_name(r_idx, total)
        cards_html.append(
            f'<div class="rh" style="left:{cx}px;width:{CARD_W}px;top:0">{label}</div>'
        )

    svg_d = " ".join(svg_lines)
    svg   = (f'<svg class="bracket-svg" width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}">'
             f'<path d="{svg_d}" fill="none" stroke="#1E2D45" stroke-width="1.5" stroke-linecap="round"/>'
             f'</svg>')

    html = (f'<div class="bracket-outer"><div class="bracket-canvas" style="width:{cw}px;height:{ch}px">'
            + svg + "".join(cards_html) + '</div></div>')
    return html, buttons

# ═══════════════════════════ ADVANCE BUTTON HANDLER ═══════════════════════════

def render_advance_buttons(bkey, pi_rounds, main_rounds, buttons):
    """Render st.buttons for advancing teams. Returns True if a rerun was triggered."""
    if not buttons: return
    # Show in an expander to keep UI tidy
    with st.expander("⚡ Advance a team", expanded=len(buttons) <= 6):
        cols = st.columns(min(len(buttons), 4))
        for i, b in enumerate(buttons):
            with cols[i % 4]:
                if st.button(b["label"], key=b["key"]):
                    r,m,s = b["r_idx"], b["m_idx"], b["slot"]
                    mr = st.session_state[f"{bkey}_main"]
                    mr[r][m]["winner"] = b["team"]
                    mr[r][m]["winner_seed"] = b["seed"]
                    if r+1 < len(mr):
                        nmi   = m//2
                        sl    = "team1" if m%2==0 else "team2"
                        ssl   = "seed1" if m%2==0 else "seed2"
                        mr[r+1][nmi][sl]  = b["team"]
                        mr[r+1][nmi][ssl] = b["seed"]
                        mr[r+1][nmi]["winner"] = None
                        mr[r+1][nmi]["winner_seed"] = None
                    st.rerun()

def render_pi_buttons(bkey, pi_rounds):
    if not pi_rounds: return
    pr = pi_rounds[0]
    buttons = []
    for mi,match in enumerate(pr):
        if not match["winner"]:
            for si,(t,s) in enumerate([(match["team1"],match["seed1"]),(match["team2"],match["seed2"])]):
                if t not in ("TBD","BYE"):
                    buttons.append({"key":f"{bkey}_pi0_m{mi}_s{si}","label":f"▶ {t[:16]}",
                                    "mi":mi,"si":si,"team":t,"seed":s})
    if not buttons: return
    with st.expander("🎟 Play-in: advance a team", expanded=True):
        cols = st.columns(min(len(buttons),4))
        for i,b in enumerate(buttons):
            with cols[i%4]:
                if st.button(b["label"], key=b["key"]):
                    pr[b["mi"]]["winner"] = b["team"]
                    pr[b["mi"]]["winner_seed"] = b["seed"]
                    st.session_state[f"{bkey}_playin"] = pi_rounds
                    _feed_pi_winner(bkey, b["mi"], b["team"], b["seed"])
                    st.rerun()

def _feed_pi_winner(bkey, pi_mi, name, seed):
    mr = st.session_state.get(f"{bkey}_main", [])
    if not mr: return
    idx = 0
    for m in mr[0]:
        for sl,ssl in [("team1","seed1"),("team2","seed2")]:
            if m[sl] == "TBD":
                if idx == pi_mi:
                    m[sl] = name; m[ssl] = seed; return
                idx += 1

def show_bracket(bkey, show_seeds=False, reversed_x=False):
    pi = st.session_state.get(f"{bkey}_playin", [])
    mr = st.session_state.get(f"{bkey}_main",   [])
    if not mr: return

    # Play-in section
    if pi and pi[0]:
        st.markdown('<div class="playin-header">🎟 PLAY-IN GAMES</div>', unsafe_allow_html=True)
        pi_cols = st.columns(max(len(pi[0]),1))
        for mi,match in enumerate(pi[0]):
            with pi_cols[mi % len(pi[0])]:
                t1,s1 = match["team1"],match["seed1"]
                t2,s2 = match["team2"],match["seed2"]
                w      = match.get("winner")
                sd1 = f'<span class="sd">{s1}</span>' if show_seeds and s1 else ""
                sd2 = f'<span class="sd">{s2}</span>' if show_seeds and s2 else ""
                st.markdown(
                    f'<div class="bm playin-card" style="position:relative;width:100%;margin:.3rem 0">'
                    f'<div class="ts{" tw" if w==t1 else ""}">{sd1}{t1}</div>'
                    f'<div class="ts{" tw" if w==t2 else ""}">{sd2}{t2}</div>'
                    f'</div>', unsafe_allow_html=True)
        render_pi_buttons(bkey, pi)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    html, buttons = render_bracket_html(bkey, pi, mr, show_seeds, reversed_x)
    st.markdown(html, unsafe_allow_html=True)
    render_advance_buttons(bkey, pi, mr, buttons)

    # Champion
    champ = mr[-1][0].get("winner") if mr else None
    if champ and champ not in ("TBD","BYE"):
        cs = mr[-1][0].get("winner_seed")
        st.markdown(f"""<div class="champ-card">
          <div class="ct">🏆</div>
          <div class="cl">CHAMPION</div>
          <div class="cn">{champ}{f" <span style='color:var(--gold);font-size:.8rem'>#{cs}</span>" if show_seeds and cs else ""}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════ SESSION HELPERS ═══════════════════════════
def get_main(k):   return st.session_state.get(f"{k}_main")
def get_pi(k):     return st.session_state.get(f"{k}_playin",[])
def set_bk(k,pi,mr): st.session_state[f"{k}_playin"]=pi; st.session_state[f"{k}_main"]=mr
def clr(k):
    for s in ["_main","_playin"]: st.session_state.pop(f"{k}{s}",None)

# ═══════════════════════════ INPUT WIDGETS ═══════════════════════════
def team_textarea(text_key, height=160):
    return st.text_area("Teams", height=height, key=text_key,
                        placeholder="Type here, press Enter for new team",
                        label_visibility="collapsed")

def seed_toggle(key):
    return st.toggle("🔢 Assign seeds (format: `1. Team Name`)", key=key, value=False)

def options_row(prefix):
    c1,c2 = st.columns(2)
    with c1:
        bye_mode = st.radio("Uneven field handling",
            ["Auto BYEs (top seeds skip R1)","Play-ins (no free passes)"],
            key=f"{prefix}_bye", horizontal=True)
    with c2:
        pi_n = st.number_input("Extra play-in games", 0, 8, 0, key=f"{prefix}_pi",
                               help="Each adds 1 more play-in game on top of the auto ones.")
    use_byes = bye_mode.startswith("Auto")
    return use_byes, int(pi_n)

def auto_split_threshold(): return 16  # above this, auto-split into sides

# ═══════════════════════════ PAGE ═══════════════════════════
st.markdown("""<div class="hero">
  <div class="hero-title">BRACKET MAKER</div>
  <div class="hero-sub">Build · Seed · Advance</div>
  <div class="hero-line"></div>
</div>""", unsafe_allow_html=True)

tab_auto, tab_custom = st.tabs(["⚡  AUTOMATIC", "⚙️  CUSTOM"])

# ══════════════════════════════════════════
#  AUTO TAB
# ══════════════════════════════════════════
with tab_auto:
    st.markdown('<div class="slabel">Teams / Players</div>', unsafe_allow_html=True)
    raw_a = team_textarea("auto_names", height=170)
    use_seeds_a = seed_toggle("auto_seeds")

    st.markdown('<div class="slabel">Options</div>', unsafe_allow_html=True)
    use_byes_a, pi_a = options_row("auto")

    st.markdown(f'<div class="info-box">💡 If you enter more than {auto_split_threshold()} teams, the bracket will automatically split into Left / Right sides.</div>',
                unsafe_allow_html=True)

    c1,c2 = st.columns([3,1])
    with c1: gen_a = st.button("🏆  GENERATE BRACKET", key="gen_auto")
    with c2:
        if st.button("↺  Reset", key="rst_auto"):
            for k in ["auto","auto_left","auto_right","auto_final"]: clr(k)
            st.rerun()

    if gen_a:
        teams_a = parse_teams(raw_a, use_seeds_a)
        if len(teams_a) < 2:
            st.error("Enter at least 2 teams.")
        else:
            if len(teams_a) > auto_split_threshold():
                # split into two halves
                mid = len(teams_a)//2
                left_ts  = teams_a[:mid]
                right_ts = teams_a[mid:]
                pi_l,ml = build_bracket(left_ts,  use_byes_a, pi_a)
                pi_r,mr = build_bracket(right_ts, use_byes_a, pi_a)
                set_bk("auto_left",  pi_l, ml)
                set_bk("auto_right", pi_r, mr)
                blank = [{"team1":"TBD","team2":"TBD","winner":None,"winner_seed":None,
                          "seed1":None,"seed2":None,"is_bye":False,"is_playin":False}]
                set_bk("auto_final", [], [blank])
                st.session_state["auto_split"] = True
            else:
                pi_a_r, mr_a = build_bracket(teams_a, use_byes_a, pi_a)
                set_bk("auto", pi_a_r, mr_a)
                st.session_state["auto_split"] = False
            st.rerun()

    if st.session_state.get("auto_split") and get_main("auto_left"):
        show_s = st.session_state.get("auto_seeds", False)
        c1,c2 = st.columns(2)
        with c1:
            st.markdown('<span class="rbadge" style="color:#E8B84B;border-color:#E8B84B">LEFT</span>', unsafe_allow_html=True)
            show_bracket("auto_left", show_seeds=show_s)
        with c2:
            st.markdown('<span class="rbadge" style="color:#3B82F6;border-color:#3B82F6">RIGHT</span>', unsafe_allow_html=True)
            show_bracket("auto_right", show_seeds=show_s)

        lc = get_main("auto_left")[-1][0]
        rc = get_main("auto_right")[-1][0]
        fin = get_main("auto_final")
        if lc["winner"] and lc["winner"] not in ("TBD","BYE"):
            fin[0][0]["team1"]=lc["winner"]; fin[0][0]["seed1"]=lc.get("winner_seed")
        if rc["winner"] and rc["winner"] not in ("TBD","BYE"):
            fin[0][0]["team2"]=rc["winner"]; fin[0][0]["seed2"]=rc.get("winner_seed")
        st.markdown('<div style="text-align:center;font-family:Oswald,sans-serif;font-size:1rem;letter-spacing:3px;color:var(--gold);margin:.8rem 0">⚡ THE FINAL ⚡</div>', unsafe_allow_html=True)
        show_bracket("auto_final", show_seeds=show_s)

    elif not st.session_state.get("auto_split") and get_main("auto") is not None:
        show_bracket("auto", show_seeds=st.session_state.get("auto_seeds", False))

# ══════════════════════════════════════════
#  CUSTOM TAB
# ══════════════════════════════════════════
with tab_custom:
    st.markdown('<div class="slabel">Bracket Structure</div>', unsafe_allow_html=True)
    structure = st.selectbox("Structure", ["Simple","Two Sides (Left / Right)","Regions (4 — NCAA style)"],
                             key="c_struct", label_visibility="collapsed")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ─────────────── SIMPLE ───────────────
    if structure == "Simple":
        raw_s = team_textarea("c_s_teams")
        use_seeds_s = seed_toggle("c_s_seeds")
        st.markdown('<div class="slabel">Options</div>', unsafe_allow_html=True)
        ub_s, pi_s = options_row("c_s")
        c1,c2 = st.columns([3,1])
        with c1:
            if st.button("🏆  BUILD BRACKET", key="c_s_gen"):
                ts = parse_teams(raw_s, use_seeds_s)
                if len(ts)<2: st.error("Need ≥2 teams.")
                else:
                    pi,mr = build_bracket(ts,ub_s,pi_s)
                    set_bk("c_s",pi,mr); st.rerun()
        with c2:
            if st.button("↺  Reset", key="c_s_rst"): clr("c_s"); st.rerun()
        if get_main("c_s") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            show_bracket("c_s", show_seeds=st.session_state.get("c_s_seeds",False))

    # ─────────────── TWO SIDES ───────────────
    elif structure == "Two Sides (Left / Right)":
        ln = st.text_input("Left name", value="LEFT",  key="ln")
        rn = st.text_input("Right name",value="RIGHT", key="rn")
        c1,c2 = st.columns(2)
        with c1:
            st.markdown(f'<span class="rbadge" style="color:#E8B84B;border-color:#E8B84B">{ln.upper()}</span>',unsafe_allow_html=True)
            raw_tl = team_textarea("c_tl_teams", 130)
            use_seeds_tl = seed_toggle("c_tl_seeds")
            ub_tl, pi_tl = options_row("c_tl")
        with c2:
            st.markdown(f'<span class="rbadge" style="color:#3B82F6;border-color:#3B82F6">{rn.upper()}</span>',unsafe_allow_html=True)
            raw_tr = team_textarea("c_tr_teams", 130)
            use_seeds_tr = seed_toggle("c_tr_seeds")
            ub_tr, pi_tr = options_row("c_tr")

        cb1,cb2 = st.columns([3,1])
        with cb1: build_sides = st.button("🏆  BUILD BRACKET", key="c_tl_gen")
        with cb2:
            if st.button("↺  Reset", key="c_tl_rst"):
                for k in ["c_tl","c_tr","c_tf"]: clr(k); st.rerun()

        if build_sides:
            lt = parse_teams(raw_tl,use_seeds_tl); rt = parse_teams(raw_tr,use_seeds_tr)
            if len(lt)<2 or len(rt)<2: st.error("Each side needs ≥2 teams.")
            else:
                pi_l,ml = build_bracket(lt,ub_tl,pi_tl)
                pi_r,mr = build_bracket(rt,ub_tr,pi_tr)
                set_bk("c_tl",pi_l,ml); set_bk("c_tr",pi_r,mr)
                blank=[{"team1":"TBD","team2":"TBD","winner":None,"winner_seed":None,
                        "seed1":None,"seed2":None,"is_bye":False,"is_playin":False}]
                set_bk("c_tf",[],[blank]); st.rerun()

        if get_main("c_tl") is not None:
            st.markdown('<hr class="divider">',unsafe_allow_html=True)
            co1,co2 = st.columns(2)
            with co1:
                st.markdown(f'<span class="rbadge" style="color:#E8B84B;border-color:#E8B84B">{st.session_state.get("ln","LEFT").upper()}</span>',unsafe_allow_html=True)
                show_bracket("c_tl", show_seeds=st.session_state.get("c_tl_seeds",False))
            with co2:
                st.markdown(f'<span class="rbadge" style="color:#3B82F6;border-color:#3B82F6">{st.session_state.get("rn","RIGHT").upper()}</span>',unsafe_allow_html=True)
                show_bracket("c_tr", show_seeds=st.session_state.get("c_tr_seeds",False))
            lc=get_main("c_tl")[-1][0]; rc=get_main("c_tr")[-1][0]
            fin=get_main("c_tf")
            if lc["winner"] and lc["winner"] not in("TBD","BYE"):
                fin[0][0]["team1"]=lc["winner"]; fin[0][0]["seed1"]=lc.get("winner_seed")
            if rc["winner"] and rc["winner"] not in("TBD","BYE"):
                fin[0][0]["team2"]=rc["winner"]; fin[0][0]["seed2"]=rc.get("winner_seed")
            st.markdown('<div style="text-align:center;font-family:Oswald,sans-serif;font-size:1rem;letter-spacing:3px;color:var(--gold);margin:.8rem 0">⚡ THE FINAL ⚡</div>',unsafe_allow_html=True)
            show_bracket("c_tf", show_seeds=True)

    # ─────────────── 4 REGIONS / NCAA ───────────────
    elif structure == "Regions (4 — NCAA style)":
        R_DEF   = ["EAST","WEST","NORTH","SOUTH"]
        R_COLS  = ["#E8B84B","#3B82F6","#22C55E","#EF4444"]
        # Layout: EAST(0) and WEST(1) on left side, NORTH(2) and SOUTH(3) on right side
        # EAST bracket reads left→right, WEST reads left→right but flipped
        # We'll collect input first, then render

        region_data = {}  # i → {raw, use_seeds, ub, pi}
        input_cols = st.columns(2)
        for i in range(4):
            with input_cols[i%2]:
                rn_i = st.text_input(f"Region {i+1} name", value=R_DEF[i], key=f"rn_{i}")
                st.markdown(f'<span class="rbadge" style="color:{R_COLS[i]};border-color:{R_COLS[i]}">{rn_i.upper()}</span>',unsafe_allow_html=True)
                raw_i = team_textarea(f"rt_{i}", 100)
                us_i  = seed_toggle(f"rs_{i}")
                ub_i, pi_i = options_row(f"crg{i}")
                region_data[i] = {"raw":raw_i,"us":us_i,"ub":ub_i,"pi":pi_i}

        cb1,cb2 = st.columns([3,1])
        with cb1: build_nc = st.button("🏆  BUILD BRACKET", key="nc_gen")
        with cb2:
            if st.button("↺  Reset", key="nc_rst"):
                for i in range(4): clr(f"nc{i}")
                for k in ["nc_f1","nc_f2","nc_champ"]: clr(k)
                st.rerun()

        if build_nc:
            ok=True
            for i in range(4):
                d=region_data[i]; ts=parse_teams(d["raw"],d["us"])
                rn_i=st.session_state.get(f"rn_{i}",R_DEF[i])
                if len(ts)<2: st.error(f"Region '{rn_i}' needs ≥2 teams."); ok=False; break
                pi_i2,mr_i=build_bracket(ts,d["ub"],d["pi"])
                set_bk(f"nc{i}",pi_i2,mr_i)
            if ok:
                blank=lambda:[{"team1":"TBD","team2":"TBD","winner":None,"winner_seed":None,
                               "seed1":None,"seed2":None,"is_bye":False,"is_playin":False}]
                set_bk("nc_f1",[],[blank()]); set_bk("nc_f2",[],[blank()])
                set_bk("nc_champ",[],[blank()]); st.rerun()

        if get_main("nc0") is not None:
            st.markdown('<hr class="divider">',unsafe_allow_html=True)

            # NCAA Layout: columns are [R0-left, R1-left, ... Final-left | Champ | Final-right, ..., R0-right]
            # Regions 0,1 go on left side (0=top-left, 1=bottom-left)
            # Regions 2,3 go on right side (2=top-right, 3=bottom-right)
            # Each region bracket on left reads L→R toward center
            # Each region bracket on right reads R→L toward center (reversed)

            show_seeds_list = [st.session_state.get(f"rs_{i}",False) for i in range(4)]

            # ── Generate HTML + buttons for each region ──
            region_htmls = {}
            region_buttons = {}
            for i in range(4):
                pi_i = st.session_state.get(f"nc{i}_playin",[])
                mr_i = st.session_state.get(f"nc{i}_main",[])
                rev  = i in (1,3)  # bottom regions don't reverse; right-side regions (2,3) do
                # Actually NCAA: left side (0,1) reads left-to-right toward center
                # right side (2,3) reads right-to-left toward center
                rev = i in (2,3)
                h,b = render_bracket_html(f"nc{i}", pi_i, mr_i, show_seeds_list[i], reversed_x=rev)
                region_htmls[i] = h
                region_buttons[i] = b

            # Feed region winners into finals
            for i,slot,fkey in [(0,"team1","nc_f1"),(1,"team1","nc_f2"),
                                 (2,"team2","nc_f1"),(3,"team2","nc_f2")]:
                mr_i = get_main(f"nc{i}")
                if mr_i:
                    c = mr_i[-1][0]
                    fin = get_main(fkey)
                    if fin and c["winner"] and c["winner"] not in("TBD","BYE"):
                        fin[0][0][slot] = c["winner"]
                        fin[0][0]["seed1" if slot=="team1" else "seed2"] = c.get("winner_seed")

            # Generate final htmls
            f1_html,f1_btns = render_bracket_html("nc_f1",[],get_main("nc_f1") or [],True,False)
            f2_html,f2_btns = render_bracket_html("nc_f2",[],get_main("nc_f2") or [],True,False)

            # Feed final winners into championship
            for fk,slot in [("nc_f1","team1"),("nc_f2","team2")]:
                fm = get_main(fk)
                if fm:
                    c = fm[-1][0]
                    chm = get_main("nc_champ")
                    if chm and c["winner"] and c["winner"] not in("TBD","BYE"):
                        chm[0][0][slot] = c["winner"]
                        chm[0][0]["seed1" if slot=="team1" else "seed2"] = c.get("winner_seed")

            champ_html,champ_btns = render_bracket_html("nc_champ",[],get_main("nc_champ") or [],True,False)

            # ── NCAA visual layout ──
            # Top row: Region 0 (left) | Final1 | Region 2 (right)
            # Bottom row: Region 1 (left) | Final2 | Region 3 (right)
            # Center: Championship

            r0n = st.session_state.get("rn_0",R_DEF[0])
            r1n = st.session_state.get("rn_1",R_DEF[1])
            r2n = st.session_state.get("rn_2",R_DEF[2])
            r3n = st.session_state.get("rn_3",R_DEF[3])

            def region_header(name, color):
                return f'<div style="font-family:Oswald,sans-serif;font-size:.9rem;letter-spacing:3px;color:{color};text-align:center;margin-bottom:.4rem">{name.upper()}</div>'

            # Row 1: Region0 | spacer | Region2
            st.markdown("**Top Bracket**")
            col_r0, col_mid_top, col_r2 = st.columns([5,2,5])
            with col_r0:
                st.markdown(region_header(r0n, R_COLS[0]), unsafe_allow_html=True)
                if get_pi("nc0") and get_pi("nc0")[0]:
                    show_bracket("nc0", show_seeds=show_seeds_list[0])
                else:
                    st.markdown(region_htmls[0], unsafe_allow_html=True)
                    render_advance_buttons("nc0", get_pi("nc0"), get_main("nc0"), region_buttons[0])
            with col_r2:
                st.markdown(region_header(r2n, R_COLS[2]), unsafe_allow_html=True)
                if get_pi("nc2") and get_pi("nc2")[0]:
                    show_bracket("nc2", show_seeds=show_seeds_list[2])
                else:
                    st.markdown(region_htmls[2], unsafe_allow_html=True)
                    render_advance_buttons("nc2", get_pi("nc2"), get_main("nc2"), region_buttons[2])

            # Row 2: Region1 | spacer | Region3
            st.markdown("**Bottom Bracket**")
            col_r1, col_mid_bot, col_r3 = st.columns([5,2,5])
            with col_r1:
                st.markdown(region_header(r1n, R_COLS[1]), unsafe_allow_html=True)
                if get_pi("nc1") and get_pi("nc1")[0]:
                    show_bracket("nc1", show_seeds=show_seeds_list[1])
                else:
                    st.markdown(region_htmls[1], unsafe_allow_html=True)
                    render_advance_buttons("nc1", get_pi("nc1"), get_main("nc1"), region_buttons[1])
            with col_r3:
                st.markdown(region_header(r3n, R_COLS[3]), unsafe_allow_html=True)
                if get_pi("nc3") and get_pi("nc3")[0]:
                    show_bracket("nc3", show_seeds=show_seeds_list[3])
                else:
                    st.markdown(region_htmls[3], unsafe_allow_html=True)
                    render_advance_buttons("nc3", get_pi("nc3"), get_main("nc3"), region_buttons[3])

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center;font-family:Oswald,sans-serif;font-size:1rem;letter-spacing:3px;color:var(--gold);margin:.8rem 0">⚡ FINAL FOUR ⚡</div>',unsafe_allow_html=True)
            fc1,fc2 = st.columns(2)
            with fc1:
                st.markdown(f'<div style="text-align:center;color:var(--muted);font-size:.75rem;letter-spacing:2px">{r0n.upper()} vs {r2n.upper()}</div>',unsafe_allow_html=True)
                st.markdown(f1_html,unsafe_allow_html=True)
                render_advance_buttons("nc_f1",[],get_main("nc_f1"),f1_btns)
            with fc2:
                st.markdown(f'<div style="text-align:center;color:var(--muted);font-size:.75rem;letter-spacing:2px">{r1n.upper()} vs {r3n.upper()}</div>',unsafe_allow_html=True)
                st.markdown(f2_html,unsafe_allow_html=True)
                render_advance_buttons("nc_f2",[],get_main("nc_f2"),f2_btns)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center;font-family:Oswald,sans-serif;font-size:1.4rem;letter-spacing:4px;color:var(--gold)">🏆 CHAMPIONSHIP 🏆</div>',unsafe_allow_html=True)
            _,cc = st.columns([1,3]); __,cc2 = st.columns([3,1])
            col_champ = st.columns([1,2,1])[1]
            with col_champ:
                st.markdown(champ_html,unsafe_allow_html=True)
                render_advance_buttons("nc_champ",[],get_main("nc_champ"),champ_btns)
            champ_m = get_main("nc_champ")
            if champ_m:
                c=champ_m[-1][0]
                if c["winner"] and c["winner"] not in("TBD","BYE"):
                    cs=c.get("winner_seed")
                    st.markdown(f"""<div class="champ-card">
                      <div class="ct">🏆</div><div class="cl">CHAMPION</div>
                      <div class="cn">{c["winner"]}{f" <span style='color:var(--gold);font-size:.8rem'>#{cs}</span>" if cs else ""}</div>
                    </div>""",unsafe_allow_html=True)

st.markdown('<hr class="divider">',unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:var(--muted);font-size:.7rem;letter-spacing:2px">BRACKET MAKER · BUILT WITH STREAMLIT</p>',unsafe_allow_html=True)
