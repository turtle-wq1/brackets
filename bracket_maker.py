import streamlit as st
import math

st.set_page_config(
    page_title="Bracket Maker",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold:   #F5C842;
    --dark:   #0D0D0D;
    --panel:  #16213E;
    --accent: #E94560;
    --text:   #E8E8F0;
    --muted:  #8888AA;
    --win:    #2ECC71;
    --playin: #9B59B6;
    --border: #2A2A4A;
    --bye:    #2A3A2A;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark) !important;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
h1,h2,h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; }

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 6rem);
    color: var(--gold);
    text-align: center;
    letter-spacing: 6px;
    line-height: 1;
    text-shadow: 0 0 40px rgba(245,200,66,.35);
    margin: 0;
}
.hero-sub {
    text-align: center; color: var(--muted);
    font-size: .9rem; letter-spacing: 3px;
    text-transform: uppercase; margin-bottom: 2rem;
}

div[data-baseweb="tab-list"] {
    background: var(--panel) !important;
    border-radius: 12px !important; padding: 4px !important;
    border: 1px solid var(--border) !important;
}
div[data-baseweb="tab"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important; letter-spacing: 2px !important;
    color: var(--muted) !important;
}
div[aria-selected="true"][data-baseweb="tab"] {
    background: var(--gold) !important; color: var(--dark) !important;
    border-radius: 8px !important;
}

.stButton > button {
    background: var(--gold) !important; color: var(--dark) !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important; letter-spacing: 2px !important;
    border: none !important; border-radius: 8px !important;
    padding: .55rem 2rem !important; transition: all .2s !important;
}
.stButton > button:hover {
    background: #ffd85a !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(245,200,66,.3) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: var(--panel) !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* match card */
.match-wrapper {
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 10px; overflow: hidden;
    margin: 4px 0; box-shadow: 0 4px 16px rgba(0,0,0,.4);
}
.match-wrapper.playin-card { border-color: var(--playin); }
.match-wrapper.bye-card    { border-color: var(--bye); opacity: .7; }

.team-slot {
    padding: 7px 10px; font-size: .8rem;
    font-family: 'DM Sans', sans-serif;
    white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis;
    border-bottom: 1px solid var(--border); color: var(--text);
    display: flex; align-items: center; gap: 6px;
}
.team-slot:last-child { border-bottom: none; }
.team-slot.winner  { background: rgba(46,204,113,.15) !important; color: #2ECC71 !important; font-weight: 600; }
.team-slot.tbd     { color: var(--muted); font-style: italic; }
.team-slot.bye-slot{ background: var(--bye); color: var(--muted); font-style: italic; }

.seed-badge {
    display: inline-block; min-width: 20px; height: 20px;
    background: rgba(245,200,66,.18); color: var(--gold);
    font-size: .65rem; font-weight: 700; border-radius: 4px;
    text-align: center; line-height: 20px; flex-shrink: 0;
}
.playin-badge {
    display: inline-block; font-size: .6rem; font-weight: 700;
    background: rgba(155,89,182,.25); color: var(--playin);
    border-radius: 4px; padding: 1px 5px; flex-shrink: 0;
}

.round-label {
    font-family: 'Bebas Neue', sans-serif; font-size: .95rem;
    letter-spacing: 2px; color: var(--gold);
    text-align: center; margin-bottom: 8px;
}
.playin-label {
    font-family: 'Bebas Neue', sans-serif; font-size: .95rem;
    letter-spacing: 2px; color: var(--playin);
    text-align: center; margin-bottom: 8px;
}
.region-badge {
    font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem;
    letter-spacing: 3px; color: var(--accent);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 4px; margin-bottom: 1rem; display: inline-block;
}
.champion-box {
    background: linear-gradient(135deg, #2a2500, #1a1500);
    border: 2px solid var(--gold); border-radius: 14px;
    padding: 1.5rem 2.5rem; text-align: center;
    margin: 1rem auto; max-width: 300px;
    box-shadow: 0 0 40px rgba(245,200,66,.2);
}
.champion-box .trophy { font-size: 2.5rem; }
.champion-box .label {
    font-family: 'Bebas Neue', sans-serif; letter-spacing: 4px;
    color: var(--gold); font-size: 1.1rem;
}
.champion-box .name { font-size: 1.4rem; font-weight: 600; color: var(--text); margin-top: 4px; }

.divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }
.section-header {
    font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem;
    letter-spacing: 3px; color: var(--text); margin: 1rem 0 .5rem;
}
.info-box {
    background: rgba(245,200,66,.07); border: 1px solid rgba(245,200,66,.2);
    border-radius: 8px; padding: .6rem 1rem; font-size: .82rem; color: var(--muted);
    margin-bottom: .8rem;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
#  CORE LOGIC
# ═══════════════════════════════════════════════════

def next_power_of_two(n):
    return 1 if n <= 1 else 2 ** math.ceil(math.log2(n))


def seeded_matchups(teams_seeded):
    """
    teams_seeded: list of (seed, name) sorted by seed asc.
    Returns matchup pairs using standard seeding (1v last, 2v second-last …)
    """
    n = len(teams_seeded)
    pairs = []
    lo, hi = 0, n - 1
    while lo < hi:
        pairs.append((teams_seeded[lo], teams_seeded[hi]))
        lo += 1; hi -= 1
    if lo == hi:
        pairs.append((teams_seeded[lo], None))   # odd one gets a BYE
    return pairs


def make_match(t1_entry, t2_entry):
    """t_entry: (seed, name) or None for BYE"""
    def entry_name(e):
        if e is None: return "BYE"
        seed, name = e
        return name

    def entry_seed(e):
        if e is None: return None
        return e[0]

    m = {
        "team1": entry_name(t1_entry), "seed1": entry_seed(t1_entry),
        "team2": entry_name(t2_entry), "seed2": entry_seed(t2_entry),
        "winner": None, "winner_seed": None,
        "is_playin": False, "is_bye": False,
    }
    # auto-advance BYE
    if m["team2"] == "BYE":
        m["winner"] = m["team1"]; m["winner_seed"] = m["seed1"]; m["is_bye"] = True
    elif m["team1"] == "BYE":
        m["winner"] = m["team2"]; m["winner_seed"] = m["seed2"]; m["is_bye"] = True
    return m


def build_bracket_full(teams_seeded, use_byes: bool, playin_count: int):
    """
    teams_seeded: list of (seed, name)
    use_byes:     if False, pad to power-of-2 with BYE slots AND mark them
    playin_count: number of play-in games (each produces 1 slot winner)
    Returns (playin_rounds, main_rounds)
    """
    # --- PLAY-INS ---
    playin_rounds = []
    playin_winners = []   # (seed, name) placeholders fed into main bracket

    if playin_count > 0:
        # Take the bottom `playin_count*2` teams for play-ins
        # They compete for `playin_count` spots
        playin_teams = teams_seeded[-playin_count * 2:]
        main_teams   = teams_seeded[:-playin_count * 2]

        pi_matches = []
        for i in range(0, len(playin_teams), 2):
            t1 = playin_teams[i]
            t2 = playin_teams[i+1] if i+1 < len(playin_teams) else None
            m  = make_match(t1, t2)
            m["is_playin"] = True
            pi_matches.append(m)
        playin_rounds.append(pi_matches)

        # Create TBD winners for these play-in spots
        for i, m in enumerate(pi_matches):
            seed_placeholder = playin_teams[i*2][0]  # use lower seed number
            playin_winners.append((seed_placeholder, "TBD"))
    else:
        main_teams = teams_seeded

    # --- MAIN BRACKET ---
    n = len(main_teams) + len(playin_winners)
    size = next_power_of_two(n) if not use_byes else next_power_of_two(n)

    all_teams = main_teams + playin_winners

    if use_byes:
        # Pad with BYE to power-of-2
        bye_count = size - len(all_teams)
        # Assign BYE pseudo-seeds higher than any real seed
        max_s = max((s for s, _ in all_teams), default=0)
        byes = [(max_s + i + 1, "BYE") for i in range(bye_count)]
        all_teams = all_teams + byes

    # Sort by seed for proper seeding matchups
    all_teams_sorted = sorted(all_teams, key=lambda x: x[0])

    pairs = seeded_matchups(all_teams_sorted)
    r1 = [make_match(a, b) for a, b in pairs]

    rounds = [r1]
    while len(rounds[-1]) > 1:
        prev = rounds[-1]
        new_round = []
        for i in range(0, len(prev), 2):
            w1 = prev[i]["winner"] or "TBD"
            s1 = prev[i]["winner_seed"]
            w2_entry = prev[i+1] if i+1 < len(prev) else None
            w2 = w2_entry["winner"] if w2_entry else "TBD"
            s2 = w2_entry["winner_seed"] if w2_entry else None
            m  = make_match((s1, w1) if s1 is not None else (999, w1),
                             (s2, w2) if s2 is not None else (999, w2))
            new_round.append(m)
        rounds.append(new_round)

    return playin_rounds, rounds


def round_name(round_idx, total_rounds):
    from_end = total_rounds - 1 - round_idx
    if from_end == 0: return "FINAL"
    if from_end == 1: return "SEMI-FINALS"
    if from_end == 2: return "QUARTER-FINALS"
    return f"ROUND OF {2 ** (from_end + 1)}"


# ═══════════════════════════════════════════════════
#  RENDERING
# ═══════════════════════════════════════════════════

def _slot_html(team, seed, is_winner, is_tbd, is_bye_slot, show_seeds):
    cls = "team-slot"
    if is_winner:   cls += " winner"
    elif is_tbd:    cls += " tbd"
    elif is_bye_slot: cls += " bye-slot"

    seed_html = ""
    if show_seeds and seed is not None and team not in ("TBD","BYE"):
        seed_html = f'<span class="seed-badge">{seed}</span>'

    icon = "🏆 " if is_winner else ""
    display = "BYE" if team == "BYE" else ("TBD" if is_tbd else team)
    return f'<div class="{cls}">{seed_html}{icon}{display}</div>'


def render_bracket(bracket_key, playin_rounds, main_rounds, show_seeds=True, show_title=""):
    if show_title:
        st.markdown(f'<span class="region-badge">{show_title}</span>', unsafe_allow_html=True)

    total_main = len(main_rounds)

    # ── Play-in phase ──
    if playin_rounds:
        for pi_r_idx, pi_round in enumerate(playin_rounds):
            st.markdown('<div class="playin-label">🎟 PLAY-IN GAMES</div>', unsafe_allow_html=True)
            pi_cols = st.columns(max(len(pi_round), 1))
            for mi, match in enumerate(pi_round):
                with pi_cols[mi % len(pi_cols)]:
                    card_cls = "match-wrapper playin-card"
                    t1,t2,w = match["team1"], match["team2"], match["winner"]
                    s1,s2   = match["seed1"], match["seed2"]
                    st.markdown(
                        f'<div class="{card_cls}">'
                        f'{_slot_html(t1,s1,w==t1,t1=="TBD",t1=="BYE",show_seeds)}'
                        f'{_slot_html(t2,s2,w==t2,t2=="TBD",t2=="BYE",show_seeds)}'
                        f'</div>', unsafe_allow_html=True)

                    if not w:
                        for si, (team, seed) in enumerate([(t1,s1),(t2,s2)]):
                            if team not in ("TBD","BYE"):
                                bk = f"{bracket_key}_pi{pi_r_idx}_m{mi}_s{si}"
                                if st.button(f"▶ {team}", key=bk, help=f"Advance {team}"):
                                    st.session_state[f"{bracket_key}_playin"][pi_r_idx][mi]["winner"] = team
                                    st.session_state[f"{bracket_key}_playin"][pi_r_idx][mi]["winner_seed"] = seed
                                    # Feed winner into main bracket R0 matching TBD slot
                                    _feed_playin_winner(bracket_key, mi, team, seed)
                                    st.rerun()
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Main bracket ──
    cols = st.columns(total_main)
    for r_idx, (col, rnd) in enumerate(zip(cols, main_rounds)):
        with col:
            lbl = round_name(r_idx, total_main)
            st.markdown(f'<div class="round-label">{lbl}</div>', unsafe_allow_html=True)
            for m_idx, match in enumerate(rnd):
                t1,t2,w = match["team1"], match["team2"], match["winner"]
                s1,s2   = match["seed1"], match["seed2"]
                is_bye  = match.get("is_bye", False)
                card_cls = "match-wrapper bye-card" if is_bye else "match-wrapper"

                st.markdown(
                    f'<div class="{card_cls}">'
                    f'{_slot_html(t1,s1,w==t1 and w is not None,t1=="TBD",t1=="BYE",show_seeds)}'
                    f'{_slot_html(t2,s2,w==t2 and w is not None,t2=="TBD",t2=="BYE",show_seeds)}'
                    f'</div>', unsafe_allow_html=True)

                if not w and not is_bye:
                    for si, (team, seed) in enumerate([(t1,s1),(t2,s2)]):
                        if team not in ("TBD","BYE"):
                            bk = f"{bracket_key}_r{r_idx}_m{m_idx}_s{si}"
                            if st.button(f"▶ {team}", key=bk, help=f"Advance {team}"):
                                mr = st.session_state[f"{bracket_key}_main"]
                                mr[r_idx][m_idx]["winner"] = team
                                mr[r_idx][m_idx]["winner_seed"] = seed
                                if r_idx + 1 < total_main:
                                    nmi  = m_idx // 2
                                    slot = "team1" if m_idx % 2 == 0 else "team2"
                                    sslt = "seed1" if m_idx % 2 == 0 else "seed2"
                                    mr[r_idx+1][nmi][slot] = team
                                    mr[r_idx+1][nmi][sslt] = seed
                                    mr[r_idx+1][nmi]["winner"] = None
                                    mr[r_idx+1][nmi]["winner_seed"] = None
                                st.rerun()

    # ── Champion ──
    champ = main_rounds[-1][0]["winner"] if main_rounds else None
    if champ and champ not in ("TBD","BYE"):
        seed_txt = f" (#{main_rounds[-1][0]['winner_seed']})" if show_seeds and main_rounds[-1][0].get("winner_seed") else ""
        st.markdown(f"""
        <div class="champion-box">
            <div class="trophy">🏆</div>
            <div class="label">CHAMPION</div>
            <div class="name">{champ}{seed_txt}</div>
        </div>""", unsafe_allow_html=True)


def _feed_playin_winner(bracket_key, pi_match_idx, winner_name, winner_seed):
    """Find the TBD slot in main R0 that corresponds to this play-in match and fill it."""
    main = st.session_state.get(f"{bracket_key}_main", [])
    if not main: return
    tbd_count = 0
    for m in main[0]:
        for slot in [("team1","seed1"),("team2","seed2")]:
            if m[slot[0]] == "TBD":
                if tbd_count == pi_match_idx:
                    m[slot[0]] = winner_name
                    m[slot[1]] = winner_seed
                    return
                tbd_count += 1


# ═══════════════════════════════════════════════════
#  SESSION STATE HELPERS
# ═══════════════════════════════════════════════════

def get_main(key):    return st.session_state.get(f"{key}_main")
def get_playin(key):  return st.session_state.get(f"{key}_playin", [])

def set_bracket(key, playin_rounds, main_rounds):
    st.session_state[f"{key}_main"]   = main_rounds
    st.session_state[f"{key}_playin"] = playin_rounds

def clear_bracket(key):
    for k in [f"{key}_main", f"{key}_playin"]:
        st.session_state.pop(k, None)


# ═══════════════════════════════════════════════════
#  TEAM INPUT WIDGET  (returns list of (seed, name))
# ═══════════════════════════════════════════════════

def team_input_widget(text_key, show_seeds_key, height=180,
                      placeholder="Team Alpha\nTeam Beta\nTeam Gamma"):
    use_seeds = st.toggle("🔢 Assign seeds", key=show_seeds_key)

    if use_seeds:
        st.markdown('<div class="info-box">Enter one team per line as <code>seed. Name</code> — e.g. <code>1. Lakers</code>. If you skip the number, seeds are auto-assigned.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">One team per line. Seeds auto-assigned by order.</div>', unsafe_allow_html=True)

    raw = st.text_area("Teams", height=height, key=text_key,
                       placeholder=placeholder, label_visibility="collapsed")
    return raw, use_seeds


def parse_teams(raw, use_seeds) -> list:
    """Returns list of (seed, name) sorted by seed."""
    lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
    result = []
    for i, line in enumerate(lines, 1):
        if use_seeds:
            # Try "N. Name" or "N Name"
            import re
            m = re.match(r'^(\d+)[.\s]\s*(.+)$', line)
            if m:
                result.append((int(m.group(1)), m.group(2).strip()))
            else:
                result.append((i, line))
        else:
            result.append((i, line))
    result.sort(key=lambda x: x[0])
    return result


def bye_playin_options(key_prefix):
    c1, c2 = st.columns(2)
    with c1:
        bye_mode = st.radio(
            "How to handle uneven team counts?",
            ["Auto BYEs (top seeds get bye)", "No BYEs (play-in games instead)"],
            key=f"{key_prefix}_bye_mode",
        )
    with c2:
        pi_count = st.number_input(
            "Extra play-in games (optional)",
            min_value=0, max_value=8, value=0, step=1,
            key=f"{key_prefix}_pi_count",
            help="Each play-in game produces 1 winner who enters the main bracket.",
        )
    use_byes = bye_mode.startswith("Auto BYEs")
    return use_byes, int(pi_count)


# ═══════════════════════════════════════════════════
#  PAGE
# ═══════════════════════════════════════════════════

st.markdown('<h1 class="hero-title">BRACKET MAKER</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Tournament · Playoffs · Showdowns</p>', unsafe_allow_html=True)

tab_auto, tab_custom = st.tabs(["⚡  AUTOMATIC", "⚙️  CUSTOM"])


# ══════════════ AUTO TAB ══════════════
with tab_auto:
    st.markdown('<div class="section-header">Teams / Players</div>', unsafe_allow_html=True)
    raw_auto, use_seeds_auto = team_input_widget("auto_names", "auto_use_seeds")

    st.markdown('<div class="section-header">Options</div>', unsafe_allow_html=True)
    use_byes_auto, pi_count_auto = bye_playin_options("auto")

    c1, c2 = st.columns([2, 1])
    with c1:
        gen = st.button("🏆  GENERATE BRACKET", key="gen_auto")
    with c2:
        if st.button("↺  RESET", key="reset_auto"):
            clear_bracket("auto"); st.rerun()

    if gen:
        teams = parse_teams(raw_auto, use_seeds_auto)
        if len(teams) < 2:
            st.error("Please enter at least 2 names.")
        else:
            pi, main = build_bracket_full(teams, use_byes_auto, pi_count_auto)
            set_bracket("auto", pi, main)
            st.rerun()

    if get_main("auto") is not None:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        show_s = st.session_state.get("auto_use_seeds", False)
        render_bracket("auto", get_playin("auto"), get_main("auto"), show_seeds=show_s)


# ══════════════ CUSTOM TAB ══════════════
with tab_custom:
    st.markdown('<div class="section-header">Bracket Structure</div>', unsafe_allow_html=True)

    structure = st.selectbox(
        "Structure type",
        ["Simple (no divisions)", "Two Sides (Left / Right)", "Regions (4 regions like NCAA)"],
        key="custom_structure",
    )
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ────────────────── SIMPLE ──────────────────
    if structure == "Simple (no divisions)":
        raw_s, use_seeds_s = team_input_widget("c_simple_teams", "c_simple_seeds")
        st.markdown('<div class="section-header">Options</div>', unsafe_allow_html=True)
        use_byes_s, pi_s = bye_playin_options("c_simple")
        c1, c2 = st.columns([2, 1])
        with c1:
            if st.button("🏆  BUILD BRACKET", key="c_simple_gen"):
                teams = parse_teams(raw_s, use_seeds_s)
                if len(teams) < 2:
                    st.error("Need at least 2 teams.")
                else:
                    pi, main = build_bracket_full(teams, use_byes_s, pi_s)
                    set_bracket("c_simple", pi, main)
                    st.rerun()
        with c2:
            if st.button("↺  RESET", key="c_simple_reset"):
                clear_bracket("c_simple"); st.rerun()

        if get_main("c_simple") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            render_bracket("c_simple", get_playin("c_simple"), get_main("c_simple"),
                           show_seeds=st.session_state.get("c_simple_seeds", False))

    # ────────────────── TWO SIDES ──────────────────
    elif structure == "Two Sides (Left / Right)":
        left_name  = st.text_input("Left side name",  value="LEFT",  key="left_name")
        right_name = st.text_input("Right side name", value="RIGHT", key="right_name")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<span class="region-badge" style="color:#F5C842;border-color:#F5C842">{left_name.upper()}</span>', unsafe_allow_html=True)
            raw_l, use_seeds_l = team_input_widget("c_left_teams", "c_left_seeds", height=130)
            st.markdown("**Options**")
            use_byes_l, pi_l = bye_playin_options("c_left")
        with c2:
            st.markdown(f'<span class="region-badge" style="color:#E94560;border-color:#E94560">{right_name.upper()}</span>', unsafe_allow_html=True)
            raw_r, use_seeds_r = team_input_widget("c_right_teams", "c_right_seeds", height=130)
            st.markdown("**Options**")
            use_byes_r, pi_r = bye_playin_options("c_right")

        cb1, cb2 = st.columns([2, 1])
        with cb1:
            build_sides = st.button("🏆  BUILD BRACKET", key="c_sides_gen")
        with cb2:
            if st.button("↺  RESET", key="c_sides_reset"):
                for k in ["c_left","c_right","c_sides_final"]:
                    clear_bracket(k)
                st.rerun()

        if build_sides:
            l_teams = parse_teams(raw_l, use_seeds_l)
            r_teams = parse_teams(raw_r, use_seeds_r)
            if len(l_teams) < 2 or len(r_teams) < 2:
                st.error("Each side needs at least 2 teams.")
            else:
                pi_l_r, main_l = build_bracket_full(l_teams, use_byes_l, pi_l)
                pi_r_r, main_r = build_bracket_full(r_teams, use_byes_r, pi_r)
                set_bracket("c_left",  pi_l_r, main_l)
                set_bracket("c_right", pi_r_r, main_r)
                set_bracket("c_sides_final", [],
                            [[{"team1":"TBD","team2":"TBD","winner":None,
                               "winner_seed":None,"seed1":None,"seed2":None,
                               "is_playin":False,"is_bye":False}]])
                st.rerun()

        if get_main("c_left") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            co1, co2 = st.columns(2)
            with co1:
                render_bracket("c_left", get_playin("c_left"), get_main("c_left"),
                               show_seeds=st.session_state.get("c_left_seeds", False),
                               show_title=st.session_state.get("left_name","LEFT").upper())
            with co2:
                render_bracket("c_right", get_playin("c_right"), get_main("c_right"),
                               show_seeds=st.session_state.get("c_right_seeds", False),
                               show_title=st.session_state.get("right_name","RIGHT").upper())

            l_champ = get_main("c_left")[-1][0]["winner"]
            r_champ = get_main("c_right")[-1][0]["winner"]
            l_seed  = get_main("c_left")[-1][0].get("winner_seed")
            r_seed  = get_main("c_right")[-1][0].get("winner_seed")
            final   = get_main("c_sides_final")
            if l_champ and l_champ not in ("TBD","BYE"):
                final[0][0]["team1"] = l_champ; final[0][0]["seed1"] = l_seed
            if r_champ and r_champ not in ("TBD","BYE"):
                final[0][0]["team2"] = r_champ; final[0][0]["seed2"] = r_seed

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-header" style="text-align:center;color:var(--gold)">⚡ THE FINAL ⚡</div>', unsafe_allow_html=True)
            render_bracket("c_sides_final", [], final, show_seeds=True)

    # ────────────────── 4 REGIONS ──────────────────
    elif structure == "Regions (4 regions like NCAA)":
        region_defaults = ["EAST", "WEST", "NORTH", "SOUTH"]
        region_colors   = ["#F5C842", "#E94560", "#00B4D8", "#2ECC71"]

        st.markdown("Name your 4 regions and add teams to each:")
        rcols = st.columns(2)
        region_raws, region_seeds_flags, region_byes, region_pis = [], [], [], []

        for i in range(4):
            with rcols[i % 2]:
                rn = st.text_input(f"Region {i+1} name", value=region_defaults[i], key=f"rname_{i}")
                st.markdown(f'<span class="region-badge" style="color:{region_colors[i]};border-color:{region_colors[i]}">{rn.upper()}</span>', unsafe_allow_html=True)
                raw_ri, use_seeds_ri = team_input_widget(f"rteams_{i}", f"rseeds_{i}", height=110)
                use_byes_ri, pi_ri = bye_playin_options(f"creg{i}")
                region_raws.append(raw_ri)
                region_seeds_flags.append(use_seeds_ri)
                region_byes.append(use_byes_ri)
                region_pis.append(pi_ri)

        cb1, cb2 = st.columns([2, 1])
        with cb1:
            build_regs = st.button("🏆  BUILD BRACKET", key="c_regions_gen")
        with cb2:
            if st.button("↺  RESET", key="c_regions_reset"):
                for i in range(4): clear_bracket(f"c_reg{i}")
                for k in ["c_rsemi1","c_rsemi2","c_rfinal"]: clear_bracket(k)
                st.rerun()

        if build_regs:
            ok = True
            for i in range(4):
                teams_i = parse_teams(region_raws[i], region_seeds_flags[i])
                rn = st.session_state.get(f"rname_{i}", region_defaults[i])
                if len(teams_i) < 2:
                    st.error(f"Region '{rn}' needs at least 2 teams."); ok = False; break
                pi_i, main_i = build_bracket_full(teams_i, region_byes[i], region_pis[i])
                set_bracket(f"c_reg{i}", pi_i, main_i)
            if ok:
                blank = lambda: [[{"team1":"TBD","team2":"TBD","winner":None,
                                   "winner_seed":None,"seed1":None,"seed2":None,
                                   "is_playin":False,"is_bye":False}]]
                set_bracket("c_rsemi1", [], blank())
                set_bracket("c_rsemi2", [], blank())
                set_bracket("c_rfinal", [], blank())
                st.rerun()

        if get_main("c_reg0") is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            for pair_idx, (ia, ib) in enumerate([(0,1),(2,3)]):
                rn_a = st.session_state.get(f"rname_{ia}", region_defaults[ia])
                rn_b = st.session_state.get(f"rname_{ib}", region_defaults[ib])
                co1, co2 = st.columns(2)
                with co1:
                    render_bracket(f"c_reg{ia}", get_playin(f"c_reg{ia}"), get_main(f"c_reg{ia}"),
                                   show_seeds=st.session_state.get(f"rseeds_{ia}", False),
                                   show_title=rn_a.upper())
                with co2:
                    render_bracket(f"c_reg{ib}", get_playin(f"c_reg{ib}"), get_main(f"c_reg{ib}"),
                                   show_seeds=st.session_state.get(f"rseeds_{ib}", False),
                                   show_title=rn_b.upper())

                semi_key = f"c_rsemi{pair_idx+1}"
                semi = get_main(semi_key)
                for reg_idx, slot in [(ia,"team1"),(ib,"team2")]:
                    champ = get_main(f"c_reg{reg_idx}")[-1][0]["winner"]
                    seed  = get_main(f"c_reg{reg_idx}")[-1][0].get("winner_seed")
                    if champ and champ not in ("TBD","BYE"):
                        semi[0][0][slot] = champ
                        semi[0][0]["seed1" if slot=="team1" else "seed2"] = seed

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                label = ["SEMI-FINAL 1","SEMI-FINAL 2"][pair_idx]
                st.markdown(f'<div class="section-header" style="text-align:center">⚡ {label}</div>', unsafe_allow_html=True)
                render_bracket(semi_key, [], semi, show_seeds=True)

            s1w = get_main("c_rsemi1")[-1][0]["winner"]
            s2w = get_main("c_rsemi2")[-1][0]["winner"]
            s1s = get_main("c_rsemi1")[-1][0].get("winner_seed")
            s2s = get_main("c_rsemi2")[-1][0].get("winner_seed")
            final = get_main("c_rfinal")
            if s1w and s1w not in ("TBD","BYE"):
                final[0][0]["team1"] = s1w; final[0][0]["seed1"] = s1s
            if s2w and s2w not in ("TBD","BYE"):
                final[0][0]["team2"] = s2w; final[0][0]["seed2"] = s2s

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-header" style="text-align:center;color:var(--gold);font-size:2rem">🏆 CHAMPIONSHIP 🏆</div>', unsafe_allow_html=True)
            render_bracket("c_rfinal", [], final, show_seeds=True)


st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:var(--muted);font-size:.75rem;letter-spacing:2px">BRACKET MAKER · BUILT WITH STREAMLIT</p>', unsafe_allow_html=True)
