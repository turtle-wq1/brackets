import streamlit as st
import math
import re
import json
import os

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
  --match-w:152px; --match-h:58px;
}

html,body,[data-testid="stAppViewContainer"]{background:var(--dark)!important;color:var(--text);font-family:'Inter',sans-serif;}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;}

::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--dark)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}

.hero{text-align:center;padding:2.5rem 0 1.5rem;position:relative}
.hero-title{font-family:'Oswald',sans-serif;font-size:clamp(2.8rem,6vw,5rem);font-weight:700;
  color:transparent;background:linear-gradient(135deg,#E8B84B 0%,#FDE68A 45%,#E8B84B 100%);
  -webkit-background-clip:text;background-clip:text;letter-spacing:6px;line-height:1;
  filter:drop-shadow(0 0 30px rgba(232,184,75,.4));}
.hero-sub{color:var(--muted);font-size:.75rem;letter-spacing:4px;text-transform:uppercase;margin-top:.4rem}
.hero-line{width:80px;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:.8rem auto 0}

div[data-baseweb="tab-list"]{background:var(--surface)!important;border-radius:10px!important;
  padding:3px!important;border:1px solid var(--border)!important;gap:2px!important}
div[data-baseweb="tab"]{font-family:'Oswald',sans-serif!important;font-size:1rem!important;
  letter-spacing:2px!important;color:var(--muted)!important;border-radius:7px!important;
  padding:.4rem 1.4rem!important;transition:all .2s!important}
div[aria-selected="true"][data-baseweb="tab"]{
  background:linear-gradient(135deg,#E8B84B,#F59E0B)!important;
  color:#080C14!important;font-weight:600!important}

.stButton>button{background:linear-gradient(135deg,#E8B84B,#F59E0B)!important;color:#080C14!important;
  font-family:'Oswald',sans-serif!important;font-size:1rem!important;letter-spacing:2px!important;
  border:none!important;border-radius:8px!important;padding:.5rem 1.8rem!important;
  transition:all .2s!important;font-weight:600!important}
.stButton>button:hover{transform:translateY(-1px)!important;
  box-shadow:0 6px 20px rgba(232,184,75,.4)!important}

.stTextInput>div>div>input,.stTextArea>div>div>textarea,
.stNumberInput>div>div>input,.stSelectbox>div>div{
  background:var(--panel)!important;border:1px solid var(--border)!important;
  color:var(--text)!important;border-radius:8px!important;font-family:'Inter',sans-serif!important}
.stTextArea>div>div>textarea{font-size:.85rem!important}
label{color:var(--muted)!important;font-size:.8rem!important;letter-spacing:.5px!important}

.stRadio>div{gap:.5rem}
.stRadio>div>label{background:var(--panel)!important;border:1px solid var(--border)!important;
  border-radius:8px!important;padding:.4rem .9rem!important;font-size:.8rem!important;cursor:pointer}
[data-testid="stToggle"]>label{color:var(--text)!important;font-size:.85rem!important}

/* BRACKET */
.bracket-outer{overflow-x:auto;overflow-y:hidden;padding:1rem 0 1.5rem}
.bracket-canvas{position:relative;display:inline-block}

.bm{position:absolute;width:var(--match-w);cursor:default;
  border-radius:7px;overflow:hidden;border:1px solid var(--border);
  background:var(--panel);box-shadow:0 2px 12px rgba(0,0,0,.5);
  transition:border-color .2s,box-shadow .2s}
.bm:hover{border-color:var(--accent);box-shadow:0 4px 20px rgba(59,130,246,.2)}
.bm.bye-card{border-color:#1A2E1A;opacity:.65}
.bm.playin-card{border-color:var(--purple)}
.bm.final-card{border-color:var(--gold);box-shadow:0 0 24px rgba(232,184,75,.25)}

/* Clickable team slot */
.ts{height:29px;display:flex;align-items:center;padding:0 8px;gap:5px;
  font-size:.72rem;font-family:'Inter',sans-serif;overflow:hidden;
  border-bottom:1px solid var(--border);transition:background .15s,color .15s}
.ts:last-child{border-bottom:none}
.ts.tw{background:var(--green-dim)!important;color:var(--green)!important;font-weight:600}
.ts.tt{color:var(--muted);font-style:italic}
.ts.tb{background:rgba(20,40,20,.4);color:#3A5A3A;font-style:italic}
/* Clickable (advanceable) slot */
.ts.clickable{cursor:pointer}
.ts.clickable:hover{background:var(--gold-dim)!important;color:var(--gold)!important}
.ts.clickable:hover .adv-hint{opacity:1}
.adv-hint{opacity:0;font-size:.6rem;color:var(--gold);margin-left:auto;transition:opacity .15s;flex-shrink:0}

.sd{min-width:18px;height:16px;background:var(--gold-dim);color:var(--gold);
  font-size:.6rem;font-weight:700;border-radius:3px;text-align:center;
  line-height:16px;flex-shrink:0;padding:0 3px}

.rh{position:absolute;font-family:'Oswald',sans-serif;font-size:.7rem;
  letter-spacing:2px;color:var(--gold);text-align:center;top:0;
  text-transform:uppercase;pointer-events:none}
.rh.playin-rh{color:var(--purple)}

.bracket-svg{position:absolute;top:0;left:0;pointer-events:none;overflow:visible}

.champ-card{margin:1.2rem auto;max-width:260px;
  background:linear-gradient(135deg,#1A1500,#0F1000);
  border:2px solid var(--gold);border-radius:14px;
  padding:1.2rem 2rem;text-align:center;
  box-shadow:0 0 50px rgba(232,184,75,.25),0 0 100px rgba(232,184,75,.1)}
.champ-card .ct{font-size:2rem}
.champ-card .cl{font-family:'Oswald',sans-serif;letter-spacing:4px;
  color:var(--gold);font-size:.85rem;margin-top:.2rem}
.champ-card .cn{font-size:1.2rem;font-weight:600;color:var(--text);margin-top:.3rem}

.playin-header{font-family:'Oswald',sans-serif;font-size:.85rem;letter-spacing:3px;
  color:var(--purple);text-align:center;margin:.5rem 0}

.slabel{font-family:'Oswald',sans-serif;font-size:1.2rem;letter-spacing:3px;
  color:var(--text);margin:.8rem 0 .4rem}
.rbadge{font-family:'Oswald',sans-serif;font-size:1.1rem;letter-spacing:3px;
  padding-bottom:3px;border-bottom:2px solid;display:inline-block;margin-bottom:.6rem}

.info-box{background:var(--gold-dim);border:1px solid rgba(232,184,75,.25);
  border-radius:7px;padding:.5rem .9rem;font-size:.78rem;color:var(--muted);margin-bottom:.7rem}

.divider{border:none;border-top:1px solid var(--border);margin:1.4rem 0}

/* Bracket name banner */
.bracket-name-banner{
  font-family:'Oswald',sans-serif;font-size:1.6rem;letter-spacing:5px;
  color:var(--gold);text-align:center;margin:.5rem 0 1rem;
  text-transform:uppercase;
}

/* Saved brackets list */
.saved-item{background:var(--panel);border:1px solid var(--border);border-radius:8px;
  padding:.6rem 1rem;margin:.3rem 0;display:flex;align-items:center;justify-content:space-between;
  font-size:.85rem;color:var(--text);cursor:pointer;transition:border-color .2s}
.saved-item:hover{border-color:var(--gold)}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════ PERSISTENCE ═══════════════════════════

SAVE_DIR = os.path.join(os.path.dirname(__file__), "brackets_saved")
os.makedirs(SAVE_DIR, exist_ok=True)

def save_path(name):
    safe = re.sub(r'[^\w\-_\. ]', '_', name).strip()
    return os.path.join(SAVE_DIR, f"{safe}.json")

def list_saved():
    try:
        files = [f[:-5] for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
        return sorted(files)
    except Exception:
        return []

def save_bracket(name, data):
    try:
        with open(save_path(name), "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        st.error(f"Save failed: {e}")
        return False

def load_bracket(name):
    try:
        with open(save_path(name)) as f:
            return json.load(f)
    except Exception:
        return None

def delete_bracket(name):
    try:
        os.remove(save_path(name))
    except Exception:
        pass

def get_saveable_state():
    """Collect all bracket session keys into a dict for saving."""
    keys_to_save = {}
    for k, v in st.session_state.items():
        if any(k.endswith(s) for s in ["_main","_playin","_split"]) or \
           k.startswith("rn_") or k in ("ln","rn","c_struct","auto_split",
                                         "bracket_name","bracket_mode"):
            try:
                json.dumps(v)  # Only save JSON-serializable values
                keys_to_save[k] = v
            except Exception:
                pass
    return keys_to_save

def restore_state(data):
    for k, v in data.items():
        st.session_state[k] = v

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
    """Returns (playin_rounds, main_rounds).
    
    Improved logic:
    - pi_count = number of explicit extra play-in games requested
    - use_byes: whether to fill uneven slots with BYEs or auto-generate play-ins
    - Auto play-ins: if n is not a power of 2 and use_byes=False, pair up the
      bottom teams to play in, producing the right number of winners to fill bracket
    """
    pi_rounds, pi_winners = [], []

    # Step 1: Handle explicitly-requested play-in games
    if pi_count > 0:
        pi_count_clamped = min(pi_count, len(teams_seeded) // 2)
        pi_teams  = teams_seeded[-(pi_count_clamped*2):]
        main_ts   = teams_seeded[:-len(pi_teams)]
        pi_matches = []
        for i in range(0, len(pi_teams), 2):
            t1 = pi_teams[i]
            t2 = pi_teams[i+1] if i+1 < len(pi_teams) else None
            m  = mk(t1, t2); m["is_playin"] = True
            pi_matches.append(m)
        pi_rounds.append(pi_matches)
        for pm in pi_matches:
            s = min((x for x in [pm["seed1"],pm["seed2"]] if x is not None), default=99)
            pi_winners.append((s, "TBD"))
    else:
        main_ts = teams_seeded

    all_ts = main_ts + pi_winners
    n = len(all_ts)
    size = npow2(n)

    if use_byes:
        # Fill to next power of 2 with BYEs — top seeds get byes
        if n < size:
            max_s = max((s for s,_ in all_ts), default=0)
            byes  = [(max_s+i+1, "BYE") for i in range(size-n)]
            all_ts = sorted(all_ts + byes, key=lambda x: x[0])
    else:
        # No byes: auto play-ins for leftover teams
        # How many play-in games do we need? We have n teams, nearest power of 2 is size.
        # We need (size - n) play-in winners to fill the bracket.
        # That requires (size - n) play-in games using (size - n)*2 of the bottom teams.
        extra_needed = size - n
        if extra_needed > 0:
            # Take 2*extra_needed bottom teams as play-in participants
            pi_team_count = extra_needed * 2
            if pi_team_count <= len(all_ts):
                extra_teams = all_ts[-pi_team_count:]
                all_ts = all_ts[:-pi_team_count]
                extra_matches = []
                for i in range(0, len(extra_teams), 2):
                    t1 = extra_teams[i]
                    t2 = extra_teams[i+1] if i+1 < len(extra_teams) else None
                    m  = mk(t1, t2); m["is_playin"] = True
                    extra_matches.append(m)
                    s = min((x for x in [m["seed1"],m["seed2"]] if x is not None), default=99)
                    all_ts.append((s,"TBD"))
                if pi_rounds:
                    pi_rounds[0].extend(extra_matches)
                else:
                    pi_rounds.append(extra_matches)
            # else: shouldn't happen, but fall through
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

CARD_W  = 152
CARD_H  = 58
COL_GAP = 44
ROW_HDR = 28
CARD_GAP_BASE = 8

def col_x(col_idx):
    return col_idx * (CARD_W + COL_GAP)

def card_spacing(r_idx, n_r0):
    if r_idx == 0:
        return CARD_H + CARD_GAP_BASE
    return card_spacing(r_idx-1, n_r0) * 2

def card_top(r_idx, m_idx, n_r0):
    sp = card_spacing(r_idx, n_r0)
    first_offset = (sp - CARD_H) / 2
    return ROW_HDR + first_offset + m_idx * sp

def canvas_height(total_rounds, n_r0):
    sp = card_spacing(total_rounds-1, n_r0)
    return ROW_HDR + sp + 20

def canvas_width(total_rounds):
    return total_rounds * CARD_W + (total_rounds-1) * COL_GAP

def slot_html(team, seed, is_win, show_seeds, clickable=False, click_key=""):
    is_tbd = team in ("TBD",)
    is_bye = team == "BYE"
    cls = "ts"
    if is_win:   cls += " tw"
    elif is_tbd: cls += " tt"
    elif is_bye: cls += " tb"
    elif clickable: cls += " clickable"

    sd = f'<span class="sd">{seed}</span>' if show_seeds and seed is not None and not is_tbd and not is_bye else ""
    icon = "🏆 " if is_win else ""
    label = "BYE" if is_bye else ("TBD" if is_tbd else team)
    display = label[:18]+"…" if len(label) > 18 else label
    hint = '<span class="adv-hint">▶ advance</span>' if clickable else ""

    if clickable and click_key:
        return (f'<div class="{cls}" title="Click to advance {label}" '
                f'onclick="window.advanceTeam(\'{click_key}\')" style="cursor:pointer">'
                f'{sd}{icon}{display}{hint}</div>')
    return f'<div class="{cls}" title="{label}">{sd}{icon}{display}</div>'

def render_bracket_html(bkey, pi_rounds, main_rounds, show_seeds=False, reversed_x=False):
    """
    Returns (html_string, advance_info_list).
    advance_info_list: list of dicts {key, r_idx, m_idx, slot, team, seed}
    Click-to-advance: we embed data-* keys on slots and use JS + query params.
    """
    if not main_rounds: return "", []

    n_r0    = len(main_rounds[0])
    total   = len(main_rounds)
    cw      = canvas_width(total)
    ch      = canvas_height(total, n_r0)

    cards_html = []
    svg_lines  = []
    advance_info = []   # {key, r_idx, m_idx, slot, team, seed}

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

            # Determine if slots are clickable (no winner yet, team is real)
            can_click = not w and not is_bye
            def make_akey(si): return f"{bkey}||{r_idx}||{m_idx}||{si}"

            t1_click = can_click and t1 not in ("TBD","BYE")
            t2_click = can_click and t2 not in ("TBD","BYE")

            if t1_click: advance_info.append({"key":make_akey(0),"r_idx":r_idx,"m_idx":m_idx,"slot":0,"team":t1,"seed":s1})
            if t2_click: advance_info.append({"key":make_akey(1),"r_idx":r_idx,"m_idx":m_idx,"slot":1,"team":t2,"seed":s2})

            h1 = slot_html(t1, s1, w==t1 and w is not None, show_seeds,
                           clickable=t1_click, click_key=make_akey(0))
            h2 = slot_html(t2, s2, w==t2 and w is not None, show_seeds,
                           clickable=t2_click, click_key=make_akey(1))
            cards_html.append(
                f'<div class="{card_cls}" style="left:{cx}px;top:{ty}px;width:{CARD_W}px">'
                f'{h1}{h2}</div>'
            )

            # Connector lines
            if r_idx < total-1:
                nx = col_x((total-1-(r_idx+1)) if reversed_x else (r_idx+1))
                child0_y = card_top(r_idx, m_idx*2,   n_r0) + CARD_H/2
                child1_y = card_top(r_idx, m_idx*2+1, n_r0) + CARD_H/2 if m_idx*2+1 < len(main_rounds[r_idx]) else child0_y
                parent_y = ty + CARD_H/2
                if not reversed_x:
                    c_right = cx + CARD_W; p_left = nx
                    mid_x = (c_right + p_left) / 2
                    svg_lines.append(f'M{c_right},{child0_y} H{mid_x}')
                    if m_idx*2+1 < len(main_rounds[r_idx]):
                        svg_lines.append(f'M{c_right},{child1_y} H{mid_x}')
                    svg_lines.append(f'M{mid_x},{child0_y} V{child1_y}')
                    svg_lines.append(f'M{mid_x},{parent_y} H{p_left}')
                else:
                    c_left = cx; p_right = nx + CARD_W
                    mid_x = (c_left + p_right) / 2
                    svg_lines.append(f'M{c_left},{child0_y} H{mid_x}')
                    if m_idx*2+1 < len(main_rounds[r_idx]):
                        svg_lines.append(f'M{c_left},{child1_y} H{mid_x}')
                    svg_lines.append(f'M{mid_x},{child0_y} V{child1_y}')
                    svg_lines.append(f'M{mid_x},{parent_y} H{p_right}')

    for r_idx in range(total):
        xi = (total-1-r_idx) if reversed_x else r_idx
        cx = col_x(xi)
        label = rnd_name(r_idx, total)
        cards_html.append(f'<div class="rh" style="left:{cx}px;width:{CARD_W}px;top:0">{label}</div>')

    svg_d = " ".join(svg_lines)
    svg   = (f'<svg class="bracket-svg" width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}">'
             f'<path d="{svg_d}" fill="none" stroke="#1E2D45" stroke-width="1.5" stroke-linecap="round"/>'
             f'</svg>')
    html = (f'<div class="bracket-outer"><div class="bracket-canvas" style="width:{cw}px;height:{ch}px">'
            + svg + "".join(cards_html) + '</div></div>')
    return html, advance_info

# ═══════════════════════════ CLICK-TO-ADVANCE JS BRIDGE ═══════════════════════════

def inject_advance_js():
    """Inject JS that captures click-to-advance events via URL query params."""
    st.markdown("""
    <script>
    window.advanceTeam = function(key) {
        const url = new URL(window.location.href);
        url.searchParams.set('advance_key', key);
        window.location.href = url.toString();
    };
    window.advancePi = function(key) {
        const url = new URL(window.location.href);
        url.searchParams.set('pi_advance_key', key);
        window.location.href = url.toString();
    };
    </script>
    """, unsafe_allow_html=True)

def process_advance_click():
    """Check query params for pending advance action and process it."""
    try:
        params = st.query_params
        akey = params.get("advance_key", None)
        if akey:
            # Clear param immediately
            st.query_params.clear()
            parts = akey.split("||")
            if len(parts) == 4:
                bkey, r_idx, m_idx, slot = parts[0], int(parts[1]), int(parts[2]), int(parts[3])
                mr_key = f"{bkey}_main"
                mr = st.session_state.get(mr_key)
                if mr:
                    match = mr[r_idx][m_idx]
                    if not match.get("winner"):
                        team = match["team1"] if slot == 0 else match["team2"]
                        seed = match["seed1"] if slot == 0 else match["seed2"]
                        if team not in ("TBD", "BYE"):
                            mr[r_idx][m_idx]["winner"] = team
                            mr[r_idx][m_idx]["winner_seed"] = seed
                            # Propagate to next round
                            if r_idx + 1 < len(mr):
                                nmi = m_idx // 2
                                sl  = "team1" if m_idx % 2 == 0 else "team2"
                                ssl = "seed1"  if m_idx % 2 == 0 else "seed2"
                                mr[r_idx+1][nmi][sl]  = team
                                mr[r_idx+1][nmi][ssl] = seed
                                mr[r_idx+1][nmi]["winner"] = None
                                mr[r_idx+1][nmi]["winner_seed"] = None
                            st.session_state[mr_key] = mr
                            # Auto-save if bracket has a name
                            bname = st.session_state.get("bracket_name","").strip()
                            if bname:
                                save_bracket(bname, get_saveable_state())
                            st.rerun()
    except Exception:
        pass

def process_pi_advance_click():
    """Check query params for play-in advance. Key format: bkey||mi||si"""
    try:
        params = st.query_params
        akey = params.get("pi_advance_key", None)
        if akey:
            st.query_params.clear()
            parts = akey.split("||")
            if len(parts) == 3:
                bkey, mi, si = parts[0], int(parts[1]), int(parts[2])
                pi_key = f"{bkey}_playin"
                pi = st.session_state.get(pi_key, [])
                if pi and pi[0] and mi < len(pi[0]):
                    match = pi[0][mi]
                    if not match.get("winner"):
                        team = match["team1"] if si == 0 else match["team2"]
                        seed = match["seed1"] if si == 0 else match["seed2"]
                        if team not in ("TBD","BYE"):
                            pi[0][mi]["winner"] = team
                            pi[0][mi]["winner_seed"] = seed
                            st.session_state[pi_key] = pi
                            _feed_pi_winner(bkey, mi, team, seed)
                            bname = st.session_state.get("bracket_name","").strip()
                            if bname:
                                save_bracket(bname, get_saveable_state())
                            st.rerun()
    except Exception:
        pass

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

# ═══════════════════════════ SHOW BRACKET ═══════════════════════════

def show_bracket_mini(bkey):
    """Show a compact clickable match card for finals/champ in center column."""
    mr = st.session_state.get(f"{bkey}_main", [])
    if not mr: return
    match = mr[0][0]
    t1, s1, t2, s2, w = match["team1"],match["seed1"],match["team2"],match["seed2"],match.get("winner")
    can_click = not w
    def mslot(team, seed, is_w, clickable, slot_idx):
        if not team: team = "TBD"
        cls = "ts" + (" tw" if is_w else (" clickable" if clickable else " tt"))
        sd = f'<span class="sd">{seed}</span>' if seed else ""
        hint = '<span class="adv-hint">▶</span>' if clickable else ""
        akey = f"{bkey}||0||0||{slot_idx}"
        cb = f'onclick="window.advanceTeam(\'{akey}\')" style="cursor:pointer"' if clickable else ""
        display = (team[:16]+"…") if len(team) > 16 else team
        return f'<div class="{cls}" {cb}>{sd}{display}{hint}</div>'
    t1_c = can_click and t1 not in ("TBD","BYE")
    t2_c = can_click and t2 not in ("TBD","BYE")
    card_cls = "bm" + (" final-card" if "champ" in bkey else "")
    st.markdown(
        f'<div class="{card_cls}" style="position:relative;width:100%;margin:.3rem 0">'
        f'{mslot(t1,s1,w==t1 and w is not None,t1_c,0)}'
        f'{mslot(t2,s2,w==t2 and w is not None,t2_c,1)}'
        f'</div>', unsafe_allow_html=True)


def show_bracket(bkey, show_seeds=False, reversed_x=False):
    pi = st.session_state.get(f"{bkey}_playin", [])
    mr = st.session_state.get(f"{bkey}_main",   [])
    if not mr: return

    # Play-in section
    if pi and pi[0]:
        st.markdown('<div class="playin-header">🎟 PLAY-IN GAMES — Click a team to advance</div>', unsafe_allow_html=True)
        pi_cols = st.columns(max(len(pi[0]),1))
        for mi, match in enumerate(pi[0]):
            with pi_cols[mi % len(pi[0])]:
                t1,s1 = match["team1"],match["seed1"]
                t2,s2 = match["team2"],match["seed2"]
                w      = match.get("winner")
                sd1 = f'<span class="sd">{s1}</span>' if show_seeds and s1 else ""
                sd2 = f'<span class="sd">{s2}</span>' if show_seeds and s2 else ""

                pi_key_t1 = f"{bkey}||{mi}||0"
                pi_key_t2 = f"{bkey}||{mi}||1"
                t1_click = not w and t1 not in ("TBD","BYE")
                t2_click = not w and t2 not in ("TBD","BYE")

                def pi_slot(team, sd_html, is_winner, clickable, pi_k):
                    cls = "ts"
                    if is_winner: cls += " tw"
                    elif clickable: cls += " clickable"
                    hint = '<span class="adv-hint">▶ advance</span>' if clickable else ""
                    cb = f'onclick="window.advancePi(\'{pi_k}\')" style="cursor:pointer"' if clickable else ""
                    return f'<div class="{cls}" {cb}>{sd_html}{team}{hint}</div>'

                st.markdown(
                    f'<div class="bm playin-card" style="position:relative;width:100%;margin:.3rem 0">'
                    f'{pi_slot(t1, sd1, w==t1, t1_click, pi_key_t1)}'
                    f'{pi_slot(t2, sd2, w==t2, t2_click, pi_key_t2)}'
                    f'</div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    html, _ = render_bracket_html(bkey, pi, mr, show_seeds, reversed_x)
    st.markdown(html, unsafe_allow_html=True)

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

def auto_split_threshold(): return 16

# ═══════════════════════════ PROCESS CLICK EVENTS ═══════════════════════════
inject_advance_js()
process_advance_click()
process_pi_advance_click()

# ═══════════════════════════ PAGE HEADER ═══════════════════════════
st.markdown("""<div class="hero">
  <div class="hero-title">BRACKET MAKER</div>
  <div class="hero-sub">Build · Seed · Advance</div>
  <div class="hero-line"></div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════ BRACKET NAME & SAVE/LOAD ═══════════════════════════
with st.expander("💾  Bracket Name & Save / Load", expanded=True):
    nc1, nc2, nc3 = st.columns([3, 1, 1])
    with nc1:
        bname = st.text_input("Bracket name", key="bracket_name",
                              placeholder="Enter a unique name to save & reload later…",
                              label_visibility="collapsed")
    with nc2:
        if st.button("💾 Save", key="do_save"):
            n = st.session_state.get("bracket_name","").strip()
            if not n:
                st.warning("Enter a bracket name first.")
            else:
                if save_bracket(n, get_saveable_state()):
                    st.success(f"Saved: {n}")
    with nc3:
        if st.button("🗑 Delete", key="do_del"):
            n = st.session_state.get("bracket_name","").strip()
            if n:
                delete_bracket(n)
                st.success(f"Deleted: {n}")
                st.rerun()

    saved = list_saved()
    if saved:
        st.markdown('<div style="color:var(--muted);font-size:.78rem;letter-spacing:1px;margin-top:.5rem">SAVED BRACKETS</div>', unsafe_allow_html=True)
        load_cols = st.columns(min(len(saved), 4))
        for i, sname in enumerate(saved):
            with load_cols[i % 4]:
                if st.button(f"📂 {sname}", key=f"load_{sname}"):
                    data = load_bracket(sname)
                    if data:
                        restore_state(data)
                        st.session_state["bracket_name"] = sname
                        st.success(f"Loaded: {sname}")
                        st.rerun()
    else:
        st.markdown('<div style="color:var(--muted);font-size:.75rem;font-style:italic">No saved brackets yet.</div>', unsafe_allow_html=True)

# Show banner if bracket has a name
bname_val = st.session_state.get("bracket_name","").strip()
if bname_val:
    st.markdown(f'<div class="bracket-name-banner">🏆 {bname_val} 🏆</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ═══════════════════════════ TABS ═══════════════════════════
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

    st.markdown(f'<div class="info-box">💡 If you enter more than {auto_split_threshold()} teams, the bracket will automatically split into Left / Right sides facing each other in a Final.</div>',
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

    # ── Split display: Left | Final (center) | Right ──
    if st.session_state.get("auto_split") and get_main("auto_left"):
        show_s = st.session_state.get("auto_seeds", False)

        # Update final with winners
        lc = get_main("auto_left")[-1][0]
        rc = get_main("auto_right")[-1][0]
        fin = get_main("auto_final")
        if fin:
            if lc["winner"] and lc["winner"] not in ("TBD","BYE"):
                fin[0][0]["team1"]=lc["winner"]; fin[0][0]["seed1"]=lc.get("winner_seed")
            if rc["winner"] and rc["winner"] not in ("TBD","BYE"):
                fin[0][0]["team2"]=rc["winner"]; fin[0][0]["seed2"]=rc.get("winner_seed")

        # Center layout: LEFT bracket | THE FINAL | RIGHT bracket (reversed)
        col_l, col_mid, col_r = st.columns([5, 2, 5])
        with col_l:
            st.markdown('<span class="rbadge" style="color:#E8B84B;border-color:#E8B84B">LEFT</span>', unsafe_allow_html=True)
            show_bracket("auto_left", show_seeds=show_s, reversed_x=False)
        with col_mid:
            st.markdown('<div style="text-align:center;font-family:Oswald,sans-serif;font-size:1rem;letter-spacing:3px;color:var(--gold);margin:2rem 0 .5rem">⚡ THE FINAL ⚡</div>', unsafe_allow_html=True)
            show_bracket("auto_final", show_seeds=show_s)
        with col_r:
            st.markdown('<span class="rbadge" style="color:#3B82F6;border-color:#3B82F6">RIGHT</span>', unsafe_allow_html=True)
            show_bracket("auto_right", show_seeds=show_s, reversed_x=True)

    elif not st.session_state.get("auto_split") and get_main("auto") is not None:
        # Single bracket — final card at the right
        show_bracket("auto", show_seeds=st.session_state.get("auto_seeds", False))

# ══════════════════════════════════════════
#  CUSTOM TAB
# ══════════════════════════════════════════
with tab_custom:
    st.markdown('<div class="slabel">Bracket Structure</div>', unsafe_allow_html=True)
    structure = st.selectbox("Structure", ["Simple","Two Regions","Four Regions (NCAA style)"],
                             key="c_struct", label_visibility="collapsed")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    R_DEF   = ["EAST","WEST","NORTH","SOUTH"]
    R_COLS  = ["#E8B84B","#3B82F6","#22C55E","#EF4444"]

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
            # Single region — final is at the right (normal left→right)
            show_bracket("c_s", show_seeds=st.session_state.get("c_s_seeds",False))

    # ─────────────── TWO REGIONS ───────────────
    elif structure == "Two Regions":
        ln = st.text_input("Left region name", value=R_DEF[0],  key="ln")
        rn_inp = st.text_input("Right region name",value=R_DEF[1], key="rn")
        c1,c2 = st.columns(2)
        with c1:
            st.markdown(f'<span class="rbadge" style="color:{R_COLS[0]};border-color:{R_COLS[0]}">{ln.upper()}</span>',unsafe_allow_html=True)
            raw_tl = team_textarea("c_tl_teams", 130)
            use_seeds_tl = seed_toggle("c_tl_seeds")
            ub_tl, pi_tl = options_row("c_tl")
        with c2:
            st.markdown(f'<span class="rbadge" style="color:{R_COLS[1]};border-color:{R_COLS[1]}">{rn_inp.upper()}</span>',unsafe_allow_html=True)
            raw_tr = team_textarea("c_tr_teams", 130)
            use_seeds_tr = seed_toggle("c_tr_seeds")
            ub_tr, pi_tr = options_row("c_tr")

        cb1,cb2 = st.columns([3,1])
        with cb1: build_sides = st.button("🏆  BUILD BRACKET", key="c_tl_gen")
        with cb2:
            if st.button("↺  Reset", key="c_tl_rst"):
                for k in ["c_tl","c_tr","c_tf"]: clr(k)
                st.rerun()

        if build_sides:
            lt = parse_teams(raw_tl,use_seeds_tl); rt = parse_teams(raw_tr,use_seeds_tr)
            if len(lt)<2 or len(rt)<2: st.error("Each region needs ≥2 teams.")
            else:
                pi_l,ml = build_bracket(lt,ub_tl,pi_tl)
                pi_r,mr = build_bracket(rt,ub_tr,pi_tr)
                set_bk("c_tl",pi_l,ml); set_bk("c_tr",pi_r,mr)
                blank=[{"team1":"TBD","team2":"TBD","winner":None,"winner_seed":None,
                        "seed1":None,"seed2":None,"is_bye":False,"is_playin":False}]
                set_bk("c_tf",[],[blank]); st.rerun()

        if get_main("c_tl") is not None:
            st.markdown('<hr class="divider">',unsafe_allow_html=True)

            ln_disp = st.session_state.get("ln", R_DEF[0]).upper()
            rn_disp = st.session_state.get("rn", R_DEF[1]).upper()

            # Update final
            lc=get_main("c_tl")[-1][0]; rc=get_main("c_tr")[-1][0]
            fin=get_main("c_tf")
            if fin:
                if lc["winner"] and lc["winner"] not in("TBD","BYE"):
                    fin[0][0]["team1"]=lc["winner"]; fin[0][0]["seed1"]=lc.get("winner_seed")
                if rc["winner"] and rc["winner"] not in("TBD","BYE"):
                    fin[0][0]["team2"]=rc["winner"]; fin[0][0]["seed2"]=rc.get("winner_seed")

            # Layout: Left region | THE FINAL (center) | Right region (reversed)
            col_l, col_mid, col_r = st.columns([5, 2, 5])
            with col_l:
                st.markdown(f'<span class="rbadge" style="color:{R_COLS[0]};border-color:{R_COLS[0]}">{ln_disp}</span>',unsafe_allow_html=True)
                show_bracket("c_tl", show_seeds=st.session_state.get("c_tl_seeds",False), reversed_x=False)
            with col_mid:
                st.markdown(f'<div style="text-align:center;font-family:Oswald,sans-serif;font-size:1rem;letter-spacing:3px;color:var(--gold);margin:2rem 0 .5rem">⚡ THE FINAL ⚡</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center;color:var(--muted);font-size:.7rem;letter-spacing:2px;margin-bottom:.8rem">{ln_disp} vs {rn_disp}</div>', unsafe_allow_html=True)
                show_bracket("c_tf", show_seeds=True)
            with col_r:
                st.markdown(f'<span class="rbadge" style="color:{R_COLS[1]};border-color:{R_COLS[1]}">{rn_disp}</span>',unsafe_allow_html=True)
                show_bracket("c_tr", show_seeds=st.session_state.get("c_tr_seeds",False), reversed_x=True)

    # ─────────────── 4 REGIONS / NCAA ───────────────
    elif structure == "Four Regions (NCAA style)":
        region_data = {}
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

            show_seeds_list = [st.session_state.get(f"rs_{i}",False) for i in range(4)]

            r0n = st.session_state.get("rn_0",R_DEF[0])
            r1n = st.session_state.get("rn_1",R_DEF[1])
            r2n = st.session_state.get("rn_2",R_DEF[2])
            r3n = st.session_state.get("rn_3",R_DEF[3])

            # Feed region winners into semifinals
            # Region 0 (top-left) vs Region 2 (top-right) → Final 1
            # Region 1 (bottom-left) vs Region 3 (bottom-right) → Final 2
            for i,slot,fkey in [(0,"team1","nc_f1"),(2,"team2","nc_f1"),
                                 (1,"team1","nc_f2"),(3,"team2","nc_f2")]:
                mr_i = get_main(f"nc{i}")
                if mr_i:
                    c = mr_i[-1][0]
                    fin = get_main(fkey)
                    if fin and c["winner"] and c["winner"] not in("TBD","BYE"):
                        fin[0][0][slot] = c["winner"]
                        fin[0][0]["seed1" if slot=="team1" else "seed2"] = c.get("winner_seed")

            # Feed final winners into championship
            for fk,slot in [("nc_f1","team1"),("nc_f2","team2")]:
                fm = get_main(fk)
                if fm:
                    c = fm[-1][0]
                    chm = get_main("nc_champ")
                    if chm and c["winner"] and c["winner"] not in("TBD","BYE"):
                        chm[0][0][slot] = c["winner"]
                        chm[0][0]["seed1" if slot=="team1" else "seed2"] = c.get("winner_seed")

            def region_header(name, color):
                return f'<div style="font-family:Oswald,sans-serif;font-size:.9rem;letter-spacing:3px;color:{color};text-align:center;margin-bottom:.4rem">{name.upper()}</div>'

            # ── NCAA Layout: Left(0,1) | Center(Finals+Champ) | Right(2,3) ──
            # Left side: Region 0 on top, Region 1 on bottom (both read L→R toward center)
            # Right side: Region 2 on top, Region 3 on bottom (both reversed, read R→L toward center)
            # Center: Final Four + Championship

            # Render all bracket HTMLs
            def nc_bracket_col(bkey_i, show_s, rev):
                pi_i = st.session_state.get(f"nc{bkey_i}_playin",[])
                mr_i = st.session_state.get(f"nc{bkey_i}_main",[])
                if not mr_i: return
                # Play-in
                if pi_i and pi_i[0]:
                    st.markdown('<div class="playin-header">🎟 PLAY-IN</div>', unsafe_allow_html=True)
                    pi_cols = st.columns(max(len(pi_i[0]),1))
                    for mi, match in enumerate(pi_i[0]):
                        with pi_cols[mi % len(pi_i[0])]:
                            t1,s1 = match["team1"],match["seed1"]
                            t2,s2 = match["team2"],match["seed2"]
                            w = match.get("winner")
                            sd1 = f'<span class="sd">{s1}</span>' if show_s and s1 else ""
                            sd2 = f'<span class="sd">{s2}</span>' if show_s and s2 else ""
                            pi_k1 = f"nc{bkey_i}||{mi}||0"
                            pi_k2 = f"nc{bkey_i}||{mi}||1"
                            c1_click = not w and t1 not in ("TBD","BYE")
                            c2_click = not w and t2 not in ("TBD","BYE")
                            def pslot(team, sdh, is_w, clickable, pk):
                                cls = "ts" + (" tw" if is_w else (" clickable" if clickable else ""))
                                hint = '<span class="adv-hint">▶</span>' if clickable else ""
                                cb = f'onclick="window.advancePi(\'{pk}\')" style="cursor:pointer"' if clickable else ""
                                return f'<div class="{cls}" {cb}>{sdh}{team}{hint}</div>'
                            st.markdown(
                                f'<div class="bm playin-card" style="position:relative;width:100%;margin:.3rem 0">'
                                f'{pslot(t1,sd1,w==t1,c1_click,pi_k1)}'
                                f'{pslot(t2,sd2,w==t2,c2_click,pi_k2)}'
                                f'</div>', unsafe_allow_html=True)

                html, _ = render_bracket_html(f"nc{bkey_i}", pi_i, mr_i, show_s, rev)
                st.markdown(html, unsafe_allow_html=True)
                champ = mr_i[-1][0].get("winner") if mr_i else None
                if champ and champ not in ("TBD","BYE"):
                    cs = mr_i[-1][0].get("winner_seed")
                    st.markdown(f'<div style="text-align:center;font-size:.8rem;color:var(--green);margin:.3rem 0">🏆 {champ}{f" #{cs}" if cs else ""} advances</div>', unsafe_allow_html=True)

            # ── Actual layout: col_left | col_center | col_right ──
            col_left, col_center, col_right = st.columns([5, 3, 5])

            with col_left:
                st.markdown(region_header(r0n, R_COLS[0]), unsafe_allow_html=True)
                nc_bracket_col(0, show_seeds_list[0], reversed_x=False)
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown(region_header(r1n, R_COLS[1]), unsafe_allow_html=True)
                nc_bracket_col(1, show_seeds_list[1], reversed_x=False)

            with col_center:
                st.markdown('<div style="text-align:center;font-family:Oswald,sans-serif;font-size:1rem;letter-spacing:3px;color:var(--gold);margin:1rem 0 .5rem">⚡ FINAL FOUR ⚡</div>',unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center;color:var(--muted);font-size:.7rem;letter-spacing:2px;margin-bottom:.4rem">{r0n.upper()} vs {r2n.upper()}</div>',unsafe_allow_html=True)
                show_bracket_mini("nc_f1")
                st.markdown(f'<div style="text-align:center;color:var(--muted);font-size:.7rem;letter-spacing:2px;margin:.8rem 0 .4rem">{r1n.upper()} vs {r3n.upper()}</div>',unsafe_allow_html=True)
                show_bracket_mini("nc_f2")

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown('<div style="text-align:center;font-family:Oswald,sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--gold);margin:.5rem 0">🏆 CHAMPIONSHIP 🏆</div>',unsafe_allow_html=True)
                show_bracket_mini("nc_champ")

                champ_m = get_main("nc_champ")
                if champ_m:
                    c=champ_m[-1][0]
                    if c["winner"] and c["winner"] not in("TBD","BYE"):
                        cs=c.get("winner_seed")
                        st.markdown(f"""<div class="champ-card">
                          <div class="ct">🏆</div><div class="cl">CHAMPION</div>
                          <div class="cn">{c["winner"]}{f" <span style='color:var(--gold);font-size:.8rem'>#{cs}</span>" if cs else ""}</div>
                        </div>""",unsafe_allow_html=True)

            with col_right:
                st.markdown(region_header(r2n, R_COLS[2]), unsafe_allow_html=True)
                nc_bracket_col(2, show_seeds_list[2], reversed_x=True)
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown(region_header(r3n, R_COLS[3]), unsafe_allow_html=True)
                nc_bracket_col(3, show_seeds_list[3], reversed_x=True)

st.markdown('<hr class="divider">',unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:var(--muted);font-size:.7rem;letter-spacing:2px">BRACKET MAKER · BUILT WITH STREAMLIT</p>',unsafe_allow_html=True)
