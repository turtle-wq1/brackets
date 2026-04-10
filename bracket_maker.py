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
  --gold:#E8B84B; --gold-dim:rgba(232,184,75,.15);
  --dark:#080C14; --surface:#0F1623; --panel:#141D2E; --panel2:#1A2540;
  --accent:#3B82F6; --green:#22C55E; --green-dim:rgba(34,197,94,.15);
  --purple:#A855F7; --red:#EF4444;
  --text:#E2E8F0; --muted:#64748B; --border:#1E2D45;
}
html,body,[data-testid="stAppViewContainer"]{background:var(--dark)!important;color:var(--text);font-family:'Inter',sans-serif;}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--dark)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.hero{text-align:center;padding:2.5rem 0 1.5rem}
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
  background:linear-gradient(135deg,#E8B84B,#F59E0B)!important;color:#080C14!important;font-weight:600!important}
.stButton>button{background:linear-gradient(135deg,#E8B84B,#F59E0B)!important;color:#080C14!important;
  font-family:'Oswald',sans-serif!important;font-size:1rem!important;letter-spacing:2px!important;
  border:none!important;border-radius:8px!important;padding:.5rem 1.8rem!important;transition:all .2s!important;font-weight:600!important}
.stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 6px 20px rgba(232,184,75,.4)!important}
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stNumberInput>div>div>input{
  background:var(--panel)!important;border:1px solid var(--border)!important;
  color:var(--text)!important;border-radius:8px!important;font-family:'Inter',sans-serif!important}
.stTextArea>div>div>textarea{font-size:.85rem!important}
label{color:var(--muted)!important;font-size:.8rem!important;letter-spacing:.5px!important}
.stRadio>div{gap:.5rem}
.stRadio>div>label{background:var(--panel)!important;border:1px solid var(--border)!important;
  border-radius:8px!important;padding:.4rem .9rem!important;font-size:.8rem!important;cursor:pointer}
[data-testid="stToggle"]>label{color:var(--text)!important;font-size:.85rem!important}
.bracket-outer{overflow-x:auto;overflow-y:hidden;padding:.5rem 0 1rem}
.bracket-canvas{position:relative;display:inline-block}
.bm{position:absolute;border-radius:7px;overflow:hidden;border:1px solid var(--border);
  background:var(--panel);box-shadow:0 2px 12px rgba(0,0,0,.5);}
.bm.bye-card{border-color:#1A2E1A;opacity:.65}
.bm.playin-card{border-color:var(--purple)}
.bm.final-card{border-color:var(--gold);box-shadow:0 0 24px rgba(232,184,75,.25)}
.ts{height:29px;display:flex;align-items:center;padding:0 8px;gap:5px;
  font-size:.72rem;font-family:'Inter',sans-serif;overflow:hidden;border-bottom:1px solid var(--border);}
.ts:last-child{border-bottom:none}
.ts.tw{background:var(--green-dim)!important;color:var(--green)!important;font-weight:600}
.ts.tt{color:var(--muted);font-style:italic}
.ts.tb{background:rgba(20,40,20,.4);color:#3A5A3A;font-style:italic}
.sd{min-width:18px;height:16px;background:var(--gold-dim);color:var(--gold);
  font-size:.6rem;font-weight:700;border-radius:3px;text-align:center;line-height:16px;flex-shrink:0;padding:0 3px}
.rh{position:absolute;font-family:'Oswald',sans-serif;font-size:.7rem;letter-spacing:2px;
  color:var(--gold);text-align:center;top:0;text-transform:uppercase;pointer-events:none}
.bracket-svg{position:absolute;top:0;left:0;pointer-events:none;overflow:visible}
.champ-card{margin:1rem auto;max-width:260px;background:linear-gradient(135deg,#1A1500,#0F1000);
  border:2px solid var(--gold);border-radius:14px;padding:1.2rem 2rem;text-align:center;
  box-shadow:0 0 50px rgba(232,184,75,.25)}
.champ-card .ct{font-size:2rem}
.champ-card .cl{font-family:'Oswald',sans-serif;letter-spacing:4px;color:var(--gold);font-size:.85rem;margin-top:.2rem}
.champ-card .cn{font-size:1.2rem;font-weight:600;color:var(--text);margin-top:.3rem}
.playin-header{font-family:'Oswald',sans-serif;font-size:.85rem;letter-spacing:3px;color:var(--purple);text-align:center;margin:.5rem 0}
.slabel{font-family:'Oswald',sans-serif;font-size:1.2rem;letter-spacing:3px;color:var(--text);margin:.8rem 0 .4rem}
.rbadge{font-family:'Oswald',sans-serif;font-size:1.1rem;letter-spacing:3px;padding-bottom:3px;border-bottom:2px solid;display:inline-block;margin-bottom:.6rem}
.info-box{background:var(--gold-dim);border:1px solid rgba(232,184,75,.25);border-radius:7px;padding:.5rem .9rem;font-size:.78rem;color:var(--muted);margin-bottom:.7rem}
.divider{border:none;border-top:1px solid var(--border);margin:1.4rem 0}
.section-hdr{font-family:'Oswald',sans-serif;font-size:.9rem;letter-spacing:3px;text-align:center;margin:.8rem 0 .4rem}
.bracket-name-banner{font-family:'Oswald',sans-serif;font-size:1.8rem;letter-spacing:5px;color:var(--gold);text-align:center;margin:.5rem 0 1rem;text-transform:uppercase;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════ SAVE / LOAD ═══════════════════════════

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brackets_saved")
os.makedirs(SAVE_DIR, exist_ok=True)

def _safe_name(name):
    return re.sub(r'[^\w\-_\. ]', '_', name).strip()

def save_path(name):
    return os.path.join(SAVE_DIR, f"{_safe_name(name)}.json")

def list_saved():
    try:
        return sorted(f[:-5] for f in os.listdir(SAVE_DIR) if f.endswith(".json"))
    except Exception:
        return []

def _serializable(v):
    try:
        json.dumps(v)
        return True
    except Exception:
        return False

def get_saveable_state():
    keep = {}
    for k, v in st.session_state.items():
        if any(k.endswith(s) for s in ("_main", "_playin", "_split")) or \
           k.startswith("rn_") or k in ("ln", "rn_inp", "c_struct", "auto_split", "bracket_name"):
            if _serializable(v):
                keep[k] = v
    return keep

def do_save():
    name = st.session_state.get("bracket_name", "").strip()
    if not name:
        st.warning("Enter a bracket name first.")
        return
    try:
        with open(save_path(name), "w") as f:
            json.dump(get_saveable_state(), f)
        st.success(f"Saved: {name}")
    except Exception as e:
        st.error(f"Save failed: {e}")

def do_load(name):
    try:
        with open(save_path(name)) as f:
            data = json.load(f)
        for k, v in data.items():
            st.session_state[k] = v
        st.session_state["bracket_name"] = name
        st.rerun()
    except Exception as e:
        st.error(f"Load failed: {e}")

def do_delete(name):
    try:
        os.remove(save_path(name))
    except Exception:
        pass

def _autosave():
    name = st.session_state.get("bracket_name", "").strip()
    if name:
        try:
            with open(save_path(name), "w") as f:
                json.dump(get_saveable_state(), f)
        except Exception:
            pass

# ═══════════════════════════ BRACKET LOGIC ═══════════════════════════

def npow2(n):
    return 1 if n <= 1 else 2 ** math.ceil(math.log2(n))

def seeded_pairs(ts):
    pairs, lo, hi = [], 0, len(ts) - 1
    while lo < hi:
        pairs.append((ts[lo], ts[hi]))
        lo += 1; hi -= 1
    if lo == hi:
        pairs.append((ts[lo], None))
    return pairs

def mk(t1, t2):
    nm = lambda e: "BYE" if e is None else e[1]
    sd = lambda e: None if e is None else (e[0] if e[0] < 900 else None)
    m = {"team1": nm(t1), "seed1": sd(t1), "team2": nm(t2), "seed2": sd(t2),
         "winner": None, "winner_seed": None, "is_bye": False, "is_playin": False}
    if m["team2"] == "BYE":
        m["winner"] = m["team1"]; m["winner_seed"] = m["seed1"]; m["is_bye"] = True
    elif m["team1"] == "BYE":
        m["winner"] = m["team2"]; m["winner_seed"] = m["seed2"]; m["is_bye"] = True
    return m

def build_bracket(teams_seeded, use_byes, pi_count):
    pi_rounds, pi_winners = [], []

    if pi_count > 0:
        pc = min(pi_count, len(teams_seeded) // 2)
        pi_teams = teams_seeded[-(pc * 2):]
        main_ts = teams_seeded[:-len(pi_teams)]
        pims = []
        for i in range(0, len(pi_teams), 2):
            m = mk(pi_teams[i], pi_teams[i + 1] if i + 1 < len(pi_teams) else None)
            m["is_playin"] = True
            pims.append(m)
        pi_rounds.append(pims)
        for pm in pims:
            s = min((x for x in [pm["seed1"], pm["seed2"]] if x is not None), default=99)
            pi_winners.append((s, "TBD"))
    else:
        main_ts = teams_seeded

    all_ts = main_ts + pi_winners
    n = len(all_ts)
    size = npow2(n)

    if use_byes:
        if n < size:
            ms = max((s for s, _ in all_ts), default=0)
            byes = [(ms + i + 1, "BYE") for i in range(size - n)]
            all_ts = sorted(all_ts + byes, key=lambda x: x[0])
    else:
        extra_needed = size - n
        if extra_needed > 0:
            pic = extra_needed * 2
            if pic <= len(all_ts):
                extra = all_ts[-pic:]
                all_ts = all_ts[:-pic]
                ems = []
                for i in range(0, len(extra), 2):
                    m = mk(extra[i], extra[i + 1] if i + 1 < len(extra) else None)
                    m["is_playin"] = True
                    ems.append(m)
                    s = min((x for x in [m["seed1"], m["seed2"]] if x is not None), default=99)
                    all_ts.append((s, "TBD"))
                if pi_rounds:
                    pi_rounds[0].extend(ems)
                else:
                    pi_rounds.append(ems)
        all_ts = sorted(all_ts, key=lambda x: x[0])

    pairs = seeded_pairs(all_ts)
    r1 = [mk(a, b) for a, b in pairs]
    rounds = [r1]
    while len(rounds[-1]) > 1:
        prev, nr = rounds[-1], []
        for i in range(0, len(prev), 2):
            w1 = prev[i]["winner"] or "TBD"
            s1 = prev[i]["winner_seed"]
            if i + 1 < len(prev):
                w2 = prev[i + 1]["winner"] or "TBD"
                s2 = prev[i + 1]["winner_seed"]
            else:
                w2, s2 = "TBD", None
            e1 = (s1, w1) if s1 is not None and w1 not in ("TBD", "BYE") else (None, w1)
            e2 = (s2, w2) if s2 is not None and w2 not in ("TBD", "BYE") else (None, w2)
            nr.append({"team1": e1[1], "seed1": e1[0], "team2": e2[1], "seed2": e2[0],
                       "winner": None, "winner_seed": None, "is_bye": False, "is_playin": False})
        rounds.append(nr)
    return pi_rounds, rounds

def rnd_name(idx, total):
    fe = total - 1 - idx
    if fe == 0: return "FINAL"
    if fe == 1: return "SEMIS"
    if fe == 2: return "QUARTERS"
    return f"R{2 ** (fe + 1)}"

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

CARD_W = 150
CARD_H = 58
COL_GAP = 44
ROW_HDR = 28
CARD_GAP = 8


def col_x(ci):
    return ci * (CARD_W + COL_GAP)


def card_sp(ri, n0):
    if ri == 0:
        return CARD_H + CARD_GAP
    return card_sp(ri - 1, n0) * 2


def card_top(ri, mi, n0):
    sp = card_sp(ri, n0)
    return ROW_HDR + (sp - CARD_H) / 2 + mi * sp


def canvas_h(total, n0):
    return ROW_HDR + card_sp(total - 1, n0) + 20


def canvas_w(total):
    return total * CARD_W + (total - 1) * COL_GAP


def slot_h(team, seed, win, show_seeds):
    tbd = team == "TBD"
    bye = team == "BYE"
    cls = "ts" + (" tw" if win else " tt" if tbd else " tb" if bye else "")
    sd_html = f'<span class="sd">{seed}</span>' if show_seeds and seed and not tbd and not bye else ""
    label = "BYE" if bye else ("TBD" if tbd else team)
    disp = (label[:18] + "…") if len(label) > 18 else label
    icon = "🏆 " if win else ""
    return f'<div class="{cls}" title="{label}">{sd_html}{icon}{disp}</div>'


def render_bracket_html(main_rounds, show_seeds=False, reversed_x=False):
    if not main_rounds:
        return ""
    n0 = len(main_rounds[0])
    total = len(main_rounds)
    cw = canvas_w(total)
    ch = canvas_h(total, n0)
    cards = []
    svgl = []

    for ri, rnd in enumerate(main_rounds):
        xi = (total - 1 - ri) if reversed_x else ri
        cx = col_x(xi)
        for mi, match in enumerate(rnd):
            ty = card_top(ri, mi, n0)
            t1, s1 = match["team1"], match["seed1"]
            t2, s2 = match["team2"], match["seed2"]
            w = match["winner"]
            bye = match.get("is_bye", False)
            cls = "bm" + (" bye-card" if bye else "") + (
                " final-card" if ri == total - 1 and total > 1 else "")
            cards.append(
                f'<div class="{cls}" style="left:{cx}px;top:{ty}px;width:{CARD_W}px">'
                f'{slot_h(t1, s1, w == t1 and w is not None, show_seeds)}'
                f'{slot_h(t2, s2, w == t2 and w is not None, show_seeds)}'
                f'</div>')
            if ri < total - 1:
                nx = col_x((total - 1 - (ri + 1)) if reversed_x else ri + 1)
                cy0 = card_top(ri, mi * 2, n0) + CARD_H / 2
                has_pair = mi * 2 + 1 < len(main_rounds[ri])
                cy1 = card_top(ri, mi * 2 + 1, n0) + CARD_H / 2 if has_pair else cy0
                py = ty + CARD_H / 2
                if not reversed_x:
                    cr2 = cx + CARD_W
                    pl = nx
                    mx2 = (cr2 + pl) / 2
                    svgl.append(f'M{cr2},{cy0} H{mx2}')
                    if has_pair:
                        svgl.append(f'M{cr2},{cy1} H{mx2}')
                    svgl.append(f'M{mx2},{cy0} V{cy1}')
                    svgl.append(f'M{mx2},{py} H{pl}')
                else:
                    cl2 = cx
                    pr = nx + CARD_W
                    mx2 = (cl2 + pr) / 2
                    svgl.append(f'M{cl2},{cy0} H{mx2}')
                    if has_pair:
                        svgl.append(f'M{cl2},{cy1} H{mx2}')
                    svgl.append(f'M{mx2},{cy0} V{cy1}')
                    svgl.append(f'M{mx2},{py} H{pr}')

    for ri in range(total):
        xi = (total - 1 - ri) if reversed_x else ri
        cards.append(
            f'<div class="rh" style="left:{col_x(xi)}px;width:{CARD_W}px;top:0">'
            f'{rnd_name(ri, total)}</div>')

    svg_d = " ".join(svgl)
    svg = (f'<svg class="bracket-svg" width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}">'
           f'<path d="{svg_d}" fill="none" stroke="#1E2D45" stroke-width="1.5" stroke-linecap="round"/></svg>')
    return (f'<div class="bracket-outer"><div class="bracket-canvas" style="width:{cw}px;height:{ch}px">'
            + svg + "".join(cards) + '</div></div>')


# ═══════════════════════════ ADVANCE LOGIC ═══════════════════════════

def advance_team(bkey, ri, mi, slot):
    mr = st.session_state.get(f"{bkey}_main", [])
    if not mr:
        return
    match = mr[ri][mi]
    team = match["team1"] if slot == 0 else match["team2"]
    seed = match["seed1"] if slot == 0 else match["seed2"]
    if team in ("TBD", "BYE"):
        return
    mr[ri][mi]["winner"] = team
    mr[ri][mi]["winner_seed"] = seed
    if ri + 1 < len(mr):
        nmi = mi // 2
        sl = "team1" if mi % 2 == 0 else "team2"
        ssl = "seed1" if mi % 2 == 0 else "seed2"
        mr[ri + 1][nmi][sl] = team
        mr[ri + 1][nmi][ssl] = seed
        mr[ri + 1][nmi]["winner"] = None
        mr[ri + 1][nmi]["winner_seed"] = None
    st.session_state[f"{bkey}_main"] = mr
    _autosave()


def advance_pi(bkey, mi, slot):
    pi = st.session_state.get(f"{bkey}_playin", [])
    if not pi or not pi[0] or mi >= len(pi[0]):
        return
    match = pi[0][mi]
    team = match["team1"] if slot == 0 else match["team2"]
    seed = match["seed1"] if slot == 0 else match["seed2"]
    if team in ("TBD", "BYE"):
        return
    pi[0][mi]["winner"] = team
    pi[0][mi]["winner_seed"] = seed
    st.session_state[f"{bkey}_playin"] = pi
    mr = st.session_state.get(f"{bkey}_main", [])
    if mr:
        idx = 0
        for m in mr[0]:
            for sl, ssl in [("team1", "seed1"), ("team2", "seed2")]:
                if m[sl] == "TBD":
                    if idx == mi:
                        m[sl] = team
                        m[ssl] = seed
                        st.session_state[f"{bkey}_main"] = mr
                        _autosave()
                        return
                    idx += 1


# ═══════════════════════════ DISPLAY FUNCTIONS ═══════════════════════════

def show_bracket(bkey, show_seeds=False, reversed_x=False):
    """Full bracket: SVG canvas + per-round advance buttons below it."""
    pi = st.session_state.get(f"{bkey}_playin", [])
    mr = st.session_state.get(f"{bkey}_main", [])
    if not mr:
        return

    # Play-in games
    if pi and pi[0]:
        st.markdown('<div class="playin-header">🎟 PLAY-IN GAMES</div>', unsafe_allow_html=True)
        n_pi = max(len(pi[0]), 1)
        pi_cols = st.columns(n_pi)
        for mi, match in enumerate(pi[0]):
            with pi_cols[mi % n_pi]:
                t1, s1 = match["team1"], match["seed1"]
                t2, s2 = match["team2"], match["seed2"]
                w = match.get("winner")
                sd1 = f'<span class="sd">{s1}</span>' if show_seeds and s1 else ""
                sd2 = f'<span class="sd">{s2}</span>' if show_seeds and s2 else ""
                w1c = " tw" if w == t1 else ""
                w2c = " tw" if w == t2 else ""
                st.markdown(
                    f'<div class="bm playin-card" style="position:relative;width:100%;margin:.3rem 0">'
                    f'<div class="ts{w1c}">{sd1}{t1}</div>'
                    f'<div class="ts{w2c}">{sd2}{t2}</div></div>',
                    unsafe_allow_html=True)
                if not w:
                    ba, bb = st.columns(2)
                    with ba:
                        if t1 not in ("TBD", "BYE"):
                            if st.button(f"▶ {t1[:14]}", key=f"{bkey}_pi_{mi}_0",
                                         use_container_width=True):
                                advance_pi(bkey, mi, 0)
                                st.rerun()
                    with bb:
                        if t2 not in ("TBD", "BYE"):
                            if st.button(f"▶ {t2[:14]}", key=f"{bkey}_pi_{mi}_1",
                                         use_container_width=True):
                                advance_pi(bkey, mi, 1)
                                st.rerun()
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # SVG bracket
    st.markdown(render_bracket_html(mr, show_seeds, reversed_x), unsafe_allow_html=True)

    # Advance buttons — one row per round that has undecided matches
    for ri, rnd in enumerate(mr):
        pending = [
            (mi, m) for mi, m in enumerate(rnd)
            if not m["winner"] and not m.get("is_bye")
            and not (m["team1"] in ("TBD", "BYE") and m["team2"] in ("TBD", "BYE"))
        ]
        if not pending:
            continue
        rname = rnd_name(ri, len(mr))
        st.markdown(
            f'<div style="color:var(--muted);font-size:.7rem;letter-spacing:2px;'
            f'margin:.5rem 0 .2rem">{rname} — click a team to advance</div>',
            unsafe_allow_html=True)
        for mi, match in pending:
            t1, t2 = match["team1"], match["team2"]
            c1, c2, _ = st.columns([2, 2, 0.3])
            with c1:
                if t1 not in ("TBD", "BYE"):
                    if st.button(f"▶ {t1[:22]}", key=f"{bkey}_adv_{ri}_{mi}_0",
                                 use_container_width=True):
                        advance_team(bkey, ri, mi, 0)
                        st.rerun()
            with c2:
                if t2 not in ("TBD", "BYE"):
                    if st.button(f"▶ {t2[:22]}", key=f"{bkey}_adv_{ri}_{mi}_1",
                                 use_container_width=True):
                        advance_team(bkey, ri, mi, 1)
                        st.rerun()

    # Champion banner
    if mr and mr[-1][0].get("winner") and mr[-1][0]["winner"] not in ("TBD", "BYE"):
        w = mr[-1][0]["winner"]
        cs = mr[-1][0].get("winner_seed")
        st.markdown(f"""<div class="champ-card">
          <div class="ct">🏆</div><div class="cl">CHAMPION</div>
          <div class="cn">{w}{f' <span style="color:var(--gold);font-size:.8rem">#{cs}</span>'
                            if show_seeds and cs else ""}</div>
        </div>""", unsafe_allow_html=True)


def show_final_card(bkey):
    """A single clickable match card used for Finals / Championship in the center column."""
    mr = st.session_state.get(f"{bkey}_main", [])
    if not mr:
        return
    match = mr[0][0]
    t1, s1 = match["team1"], match["seed1"]
    t2, s2 = match["team2"], match["seed2"]
    w = match.get("winner")
    w1c = " tw" if w == t1 else ""
    w2c = " tw" if w == t2 else ""
    sd1 = f'<span class="sd">{s1}</span>' if s1 else ""
    sd2 = f'<span class="sd">{s2}</span>' if s2 else ""
    d1 = (t1[:20] + "…") if len(t1) > 20 else t1
    d2 = (t2[:20] + "…") if len(t2) > 20 else t2
    icon1 = "🏆 " if w == t1 and w else ""
    icon2 = "🏆 " if w == t2 and w else ""
    st.markdown(
        f'<div class="bm final-card" style="position:relative;width:100%;margin:.4rem 0">'
        f'<div class="ts{w1c}">{sd1}{icon1}{d1}</div>'
        f'<div class="ts{w2c}">{sd2}{icon2}{d2}</div></div>',
        unsafe_allow_html=True)
    if not w:
        c1, c2 = st.columns(2)
        with c1:
            if t1 not in ("TBD", "BYE"):
                if st.button(f"▶ {t1[:16]}", key=f"{bkey}_fin_0", use_container_width=True):
                    advance_team(bkey, 0, 0, 0)
                    st.rerun()
        with c2:
            if t2 not in ("TBD", "BYE"):
                if st.button(f"▶ {t2[:16]}", key=f"{bkey}_fin_1", use_container_width=True):
                    advance_team(bkey, 0, 0, 1)
                    st.rerun()
    if w and w not in ("TBD", "BYE"):
        cs = match.get("winner_seed")
        st.markdown(f"""<div class="champ-card">
          <div class="ct">🏆</div><div class="cl">CHAMPION</div>
          <div class="cn">{w}{f' <span style="color:var(--gold);font-size:.8rem">#{cs}</span>'
                            if cs else ""}</div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════ SESSION HELPERS ═══════════════════════════

def get_main(k):
    return st.session_state.get(f"{k}_main")


def set_bk(k, pi, mr):
    st.session_state[f"{k}_playin"] = pi
    st.session_state[f"{k}_main"] = mr


def clr(k):
    st.session_state.pop(f"{k}_main", None)
    st.session_state.pop(f"{k}_playin", None)


def blank_match():
    return {"team1": "TBD", "team2": "TBD", "winner": None, "winner_seed": None,
            "seed1": None, "seed2": None, "is_bye": False, "is_playin": False}


def feed_winner_into(src_bkey, slot, dst_bkey):
    """Copy winner from last round of src into the given slot of dst[0][0]."""
    src = get_main(src_bkey)
    dst = get_main(dst_bkey)
    if src and dst:
        c = src[-1][0]
        if c["winner"] and c["winner"] not in ("TBD", "BYE"):
            dst[0][0][slot] = c["winner"]
            dst[0][0]["seed1" if slot == "team1" else "seed2"] = c.get("winner_seed")


# ═══════════════════════════ INPUT HELPERS ═══════════════════════════

def team_textarea(key, height=160):
    return st.text_area("Teams", height=height, key=key,
                        placeholder="One team per line", label_visibility="collapsed")


def seed_toggle(key):
    return st.toggle("🔢 Seeds (format: `1. Team Name`)", key=key, value=False)


def options_row(prefix):
    c1, c2 = st.columns(2)
    with c1:
        bm = st.radio("Uneven field",
                      ["Auto BYEs (top seeds skip R1)", "Play-ins (no free passes)"],
                      key=f"{prefix}_bye", horizontal=True)
    with c2:
        pi_n = st.number_input("Extra play-in games", 0, 8, 0, key=f"{prefix}_pi")
    return bm.startswith("Auto"), int(pi_n)


# ═══════════════════════════ PAGE ═══════════════════════════

st.markdown("""<div class="hero">
  <div class="hero-title">BRACKET MAKER</div>
  <div class="hero-sub">Build · Seed · Advance</div>
  <div class="hero-line"></div>
</div>""", unsafe_allow_html=True)

# ── Save / Load panel ──
with st.expander("💾  Bracket Name & Save / Load", expanded=True):
    na, nb, nc_col = st.columns([3, 1, 1])
    with na:
        st.text_input("Bracket name", key="bracket_name",
                      placeholder="Give your bracket a unique name to save & reload…",
                      label_visibility="collapsed")
    with nb:
        if st.button("💾 Save"):
            do_save()
    with nc_col:
        del_name = st.session_state.get("bracket_name", "").strip()
        if del_name and st.button("🗑 Delete"):
            do_delete(del_name)
            st.rerun()

    saved = list_saved()
    if saved:
        st.markdown(
            '<div style="color:var(--muted);font-size:.75rem;letter-spacing:1px;margin:.4rem 0 .2rem">'
            'SAVED BRACKETS</div>', unsafe_allow_html=True)
        load_cols = st.columns(min(len(saved), 5))
        for i, sname in enumerate(saved):
            with load_cols[i % 5]:
                if st.button(f"📂 {sname}", key=f"_load_{sname}"):
                    do_load(sname)
    else:
        st.caption("No saved brackets yet.")

bname = st.session_state.get("bracket_name", "").strip()
if bname:
    st.markdown(f'<div class="bracket-name-banner">🏆 {bname} 🏆</div>', unsafe_allow_html=True)

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
    st.markdown(
        '<div class="info-box">💡 More than 16 teams auto-splits into Left / Right sides '
        'with a Final in the center.</div>', unsafe_allow_html=True)

    gc, rc = st.columns([3, 1])
    with gc:
        if st.button("🏆  GENERATE BRACKET", key="gen_auto"):
            teams_a = parse_teams(raw_a, use_seeds_a)
            if len(teams_a) < 2:
                st.error("Enter at least 2 teams.")
            elif len(teams_a) > 16:
                mid = len(teams_a) // 2
                pi_l, ml = build_bracket(teams_a[:mid], use_byes_a, pi_a)
                pi_r, mr = build_bracket(teams_a[mid:], use_byes_a, pi_a)
                set_bk("auto_left", pi_l, ml)
                set_bk("auto_right", pi_r, mr)
                set_bk("auto_final", [], [[blank_match()]])
                st.session_state["auto_split"] = True
                st.rerun()
            else:
                pi_r2, mr_a = build_bracket(teams_a, use_byes_a, pi_a)
                set_bk("auto", pi_r2, mr_a)
                st.session_state["auto_split"] = False
                st.rerun()
    with rc:
        if st.button("↺  Reset", key="rst_auto"):
            for k in ["auto", "auto_left", "auto_right", "auto_final"]:
                clr(k)
            st.session_state.pop("auto_split", None)
            st.rerun()

    if st.session_state.get("auto_split") and get_main("auto_left"):
        show_s = st.session_state.get("auto_seeds", False)
        feed_winner_into("auto_left", "team1", "auto_final")
        feed_winner_into("auto_right", "team2", "auto_final")

        cl, cm, cr = st.columns([5, 2, 5])
        with cl:
            st.markdown(
                '<span class="rbadge" style="color:#E8B84B;border-color:#E8B84B">LEFT</span>',
                unsafe_allow_html=True)
            show_bracket("auto_left", show_seeds=show_s, reversed_x=False)
        with cm:
            st.markdown(
                '<div class="section-hdr" style="color:var(--gold)">⚡ THE FINAL ⚡</div>',
                unsafe_allow_html=True)
            show_final_card("auto_final")
        with cr:
            st.markdown(
                '<span class="rbadge" style="color:#3B82F6;border-color:#3B82F6">RIGHT</span>',
                unsafe_allow_html=True)
            show_bracket("auto_right", show_seeds=show_s, reversed_x=True)

    elif not st.session_state.get("auto_split") and get_main("auto") is not None:
        show_bracket("auto", show_seeds=st.session_state.get("auto_seeds", False))

# ══════════════════════════════════════════
#  CUSTOM TAB
# ══════════════════════════════════════════
with tab_custom:
    st.markdown('<div class="slabel">Bracket Structure</div>', unsafe_allow_html=True)
    structure = st.selectbox(
        "Structure",
        ["Simple (1 region)", "Two Regions", "Four Regions (NCAA style)"],
        key="c_struct", label_visibility="collapsed")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    R_DEF = ["EAST", "WEST", "NORTH", "SOUTH"]
    R_COLS = ["#E8B84B", "#3B82F6", "#22C55E", "#EF4444"]

    # ─────────────── SIMPLE ───────────────
    if structure == "Simple (1 region)":
        raw_s = team_textarea("c_s_teams")
        use_seeds_s = seed_toggle("c_s_seeds")
        st.markdown('<div class="slabel">Options</div>', unsafe_allow_html=True)
        ub_s, pi_s = options_row("c_s")
        gc2, rc2 = st.columns([3, 1])
        with gc2:
            if st.button("🏆  BUILD BRACKET", key="c_s_gen"):
                ts = parse_teams(raw_s, use_seeds_s)
                if len(ts) < 2:
                    st.error("Need ≥2 teams.")
                else:
                    pi2, mr2 = build_bracket(ts, ub_s, pi_s)
                    set_bk("c_s", pi2, mr2)
                    st.rerun()
        with rc2:
            if st.button("↺  Reset", key="c_s_rst"):
                clr("c_s")
                st.rerun()
        if get_main("c_s") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            show_bracket("c_s", show_seeds=st.session_state.get("c_s_seeds", False))

    # ─────────────── TWO REGIONS ───────────────
    elif structure == "Two Regions":
        lname = st.text_input("Left region name", value=R_DEF[0], key="ln")
        rname = st.text_input("Right region name", value=R_DEF[1], key="rn_inp")
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown(
                f'<span class="rbadge" style="color:{R_COLS[0]};border-color:{R_COLS[0]}">'
                f'{lname.upper()}</span>', unsafe_allow_html=True)
            raw_tl = team_textarea("c_tl_teams", 130)
            us_tl = seed_toggle("c_tl_seeds")
            ub_tl, pi_tl = options_row("c_tl")
        with tc2:
            st.markdown(
                f'<span class="rbadge" style="color:{R_COLS[1]};border-color:{R_COLS[1]}">'
                f'{rname.upper()}</span>', unsafe_allow_html=True)
            raw_tr = team_textarea("c_tr_teams", 130)
            us_tr = seed_toggle("c_tr_seeds")
            ub_tr, pi_tr = options_row("c_tr")

        gc3, rc3 = st.columns([3, 1])
        with gc3:
            if st.button("🏆  BUILD BRACKET", key="c_tl_gen"):
                lt = parse_teams(raw_tl, us_tl)
                rt = parse_teams(raw_tr, us_tr)
                if len(lt) < 2 or len(rt) < 2:
                    st.error("Each region needs ≥2 teams.")
                else:
                    pi_l2, ml2 = build_bracket(lt, ub_tl, pi_tl)
                    pi_r2, mr2 = build_bracket(rt, ub_tr, pi_tr)
                    set_bk("c_tl", pi_l2, ml2)
                    set_bk("c_tr", pi_r2, mr2)
                    set_bk("c_tf", [], [[blank_match()]])
                    st.rerun()
        with rc3:
            if st.button("↺  Reset", key="c_tl_rst"):
                for k in ["c_tl", "c_tr", "c_tf"]:
                    clr(k)
                st.rerun()

        if get_main("c_tl") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            ln_d = st.session_state.get("ln", R_DEF[0]).upper()
            rn_d = st.session_state.get("rn_inp", R_DEF[1]).upper()
            feed_winner_into("c_tl", "team1", "c_tf")
            feed_winner_into("c_tr", "team2", "c_tf")

            cl2, cm2, cr2 = st.columns([5, 2, 5])
            with cl2:
                st.markdown(
                    f'<span class="rbadge" style="color:{R_COLS[0]};border-color:{R_COLS[0]}">'
                    f'{ln_d}</span>', unsafe_allow_html=True)
                show_bracket("c_tl",
                             show_seeds=st.session_state.get("c_tl_seeds", False),
                             reversed_x=False)
            with cm2:
                st.markdown(
                    '<div class="section-hdr" style="color:var(--gold)">⚡ THE FINAL ⚡</div>',
                    unsafe_allow_html=True)
                st.markdown(
                    f'<div style="text-align:center;color:var(--muted);font-size:.7rem;'
                    f'letter-spacing:2px;margin-bottom:.4rem">{ln_d} vs {rn_d}</div>',
                    unsafe_allow_html=True)
                show_final_card("c_tf")
            with cr2:
                st.markdown(
                    f'<span class="rbadge" style="color:{R_COLS[1]};border-color:{R_COLS[1]}">'
                    f'{rn_d}</span>', unsafe_allow_html=True)
                show_bracket("c_tr",
                             show_seeds=st.session_state.get("c_tr_seeds", False),
                             reversed_x=True)

    # ─────────────── FOUR REGIONS ───────────────
    elif structure == "Four Regions (NCAA style)":
        region_data = {}
        ic = st.columns(2)
        for i in range(4):
            with ic[i % 2]:
                rn_i = st.text_input(f"Region {i + 1} name", value=R_DEF[i], key=f"rn_{i}")
                st.markdown(
                    f'<span class="rbadge" style="color:{R_COLS[i]};border-color:{R_COLS[i]}">'
                    f'{rn_i.upper()}</span>', unsafe_allow_html=True)
                raw_i = team_textarea(f"rt_{i}", 100)
                us_i = seed_toggle(f"rs_{i}")
                ub_i, pi_i = options_row(f"crg{i}")
                region_data[i] = {"raw": raw_i, "us": us_i, "ub": ub_i, "pi": pi_i}

        gc4, rc4 = st.columns([3, 1])
        with gc4:
            if st.button("🏆  BUILD BRACKET", key="nc_gen"):
                ok = True
                for i in range(4):
                    d = region_data[i]
                    ts = parse_teams(d["raw"], d["us"])
                    label = st.session_state.get(f"rn_{i}", R_DEF[i])
                    if len(ts) < 2:
                        st.error(f"Region '{label}' needs ≥2 teams.")
                        ok = False
                        break
                    pi2, mr2 = build_bracket(ts, d["ub"], d["pi"])
                    set_bk(f"nc{i}", pi2, mr2)
                if ok:
                    set_bk("nc_f1", [], [[blank_match()]])
                    set_bk("nc_f2", [], [[blank_match()]])
                    set_bk("nc_champ", [], [[blank_match()]])
                    st.rerun()
        with rc4:
            if st.button("↺  Reset", key="nc_rst"):
                for i in range(4):
                    clr(f"nc{i}")
                for k in ["nc_f1", "nc_f2", "nc_champ"]:
                    clr(k)
                st.rerun()

        if get_main("nc0") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            r_names = [st.session_state.get(f"rn_{i}", R_DEF[i]) for i in range(4)]
            show_seeds_list = [st.session_state.get(f"rs_{i}", False) for i in range(4)]

            # Feed region winners into Final Four semis
            feed_winner_into("nc0", "team1", "nc_f1")
            feed_winner_into("nc2", "team2", "nc_f1")
            feed_winner_into("nc1", "team1", "nc_f2")
            feed_winner_into("nc3", "team2", "nc_f2")
            # Feed semi winners into Championship
            feed_winner_into("nc_f1", "team1", "nc_champ")
            feed_winner_into("nc_f2", "team2", "nc_champ")

            def rh(name, color):
                return (f'<div style="font-family:Oswald,sans-serif;font-size:.9rem;'
                        f'letter-spacing:3px;color:{color};text-align:center;'
                        f'margin-bottom:.4rem">{name.upper()}</div>')

            col_l, col_c, col_r = st.columns([5, 3, 5])

            with col_l:
                st.markdown(rh(r_names[0], R_COLS[0]), unsafe_allow_html=True)
                show_bracket("nc0", show_seeds=show_seeds_list[0], reversed_x=False)
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown(rh(r_names[1], R_COLS[1]), unsafe_allow_html=True)
                show_bracket("nc1", show_seeds=show_seeds_list[1], reversed_x=False)

            with col_c:
                st.markdown(
                    '<div class="section-hdr" style="color:var(--gold);font-size:1rem">'
                    '⚡ FINAL FOUR ⚡</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div style="text-align:center;color:var(--muted);font-size:.7rem;'
                    f'letter-spacing:2px;margin-bottom:.3rem">'
                    f'{r_names[0].upper()} vs {r_names[2].upper()}</div>',
                    unsafe_allow_html=True)
                show_final_card("nc_f1")
                st.markdown(
                    f'<div style="text-align:center;color:var(--muted);font-size:.7rem;'
                    f'letter-spacing:2px;margin:.8rem 0 .3rem">'
                    f'{r_names[1].upper()} vs {r_names[3].upper()}</div>',
                    unsafe_allow_html=True)
                show_final_card("nc_f2")
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-hdr" style="color:var(--gold);font-size:1.1rem">'
                    '🏆 CHAMPIONSHIP 🏆</div>', unsafe_allow_html=True)
                show_final_card("nc_champ")

            with col_r:
                st.markdown(rh(r_names[2], R_COLS[2]), unsafe_allow_html=True)
                show_bracket("nc2", show_seeds=show_seeds_list[2], reversed_x=True)
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown(rh(r_names[3], R_COLS[3]), unsafe_allow_html=True)
                show_bracket("nc3", show_seeds=show_seeds_list[3], reversed_x=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:var(--muted);font-size:.7rem;letter-spacing:2px">'
    'BRACKET MAKER · BUILT WITH STREAMLIT</p>',
    unsafe_allow_html=True)
