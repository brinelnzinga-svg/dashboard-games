import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

##################### CONFIG PAGE
st.set_page_config(
    page_title="Game Sales Command Center",
    page_icon="🎮",
    layout="wide",
)

##################### CONSTANTES
REGIONS = {
    "Monde": "Global_Sales",
    "Amérique du Nord": "NA_Sales",
    "Europe": "EU_Sales",
    "Japon": "JP_Sales",
    "Autres régions": "Other_Sales",
}
REG_COLS = {
    "NA_Sales": "Amérique du Nord",
    "EU_Sales": "Europe",
    "JP_Sales": "Japon",
    "Other_Sales": "Autres régions",
}
REG_COLOR = {
    "Amérique du Nord": "#00BBF9",
    "Europe": "#FF2E97",
    "Japon": "#FEE440",
    "Autres régions": "#9B5DE5",
}
NEON_SCALE = ["#2B1055", "#9B5DE5", "#00F5D4"]
YEAR_MAX = 2016  # 2017+ : quasi aucune donnée (base incomplète)


##################### CHARGEMENT DES DONNÉES
@st.cache_data
def load_data(path="vgsales.csv"):
    d = pd.read_csv(path)
    d["Publisher"] = d["Publisher"].fillna("Inconnu")
    d = d.dropna(subset=["Year"])
    d["Year"] = d["Year"].astype(int)
    d = d[d["Year"] <= YEAR_MAX]
    return d


df = load_data()


##################### THÈME ARCADE (CSS + ANIMATIONS)
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Orbitron:wght@500;700;900&display=swap');

.stApp {
    background: radial-gradient(circle at 15% 10%, #1b1040 0%, #0b0720 45%, #05030f 100%);
    color: #E8E8FF;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14093a 0%, #0a0620 100%);
    border-right: 2px solid #9B5DE5;
}
.stApp p, .stApp label, .stApp li, .stApp span { color: #E8E8FF; }
h1, h2, h3 { font-family: 'Press Start 2P', monospace !important; color: #00F5D4 !important; }
h3 { font-size: 1.0rem !important; line-height: 1.6 !important; }

/* ---------- HERO ---------- */
.hero { text-align:center; padding: 8px 0 0 0; }
.hero-title {
    font-family:'Press Start 2P', monospace; font-size: 2.0rem; color:#FEE440;
    text-shadow: 0 0 8px #FF2E97, 0 0 22px #FF2E97, 4px 4px 0 #9B5DE5;
    animation: flicker 3s infinite;
}
.hero-sub { font-family:'Press Start 2P', monospace; font-size:.65rem; color:#00F5D4; margin-top:14px;
    animation: blink 1.2s steps(2,start) infinite; }
@keyframes blink { to { visibility:hidden; } }
@keyframes flicker { 0%,19%,21%,60%,62%,100%{opacity:1;} 20%,61%{opacity:.75;} }

/* ---------- PERSONNAGES QUI SAUTENT ---------- */
.chars { display:flex; justify-content:center; gap:34px; font-size:2.4rem; margin: 18px 0 4px 0; }
.chars span { display:inline-block; animation: bounce 1.1s ease-in-out infinite; filter: drop-shadow(0 0 8px #9B5DE5); }
.chars span:nth-child(2){ animation-delay:.15s; } .chars span:nth-child(3){ animation-delay:.3s; }
.chars span:nth-child(4){ animation-delay:.45s; } .chars span:nth-child(5){ animation-delay:.6s; }
.chars span:nth-child(6){ animation-delay:.75s; } .chars span:nth-child(7){ animation-delay:.9s; }
@keyframes bounce { 0%,100%{ transform:translateY(0) rotate(-6deg);} 50%{ transform:translateY(-22px) rotate(6deg);} }

/* ---------- PAC-MAN QUI POURSUIT LES FANTÔMES ---------- */
.pac-track { position:relative; height:56px; overflow:hidden; margin: 6px 0 14px 0;
    background-image: radial-gradient(circle, #FEE440 4px, transparent 5px);
    background-size: 40px 56px; background-position: 0 center; opacity:.95;
    border-top: 2px dashed #3a2a7a; border-bottom: 2px dashed #3a2a7a; }
.pac { position:absolute; top:8px; left:-120px; width:0; height:0; border-style:solid; border-width:20px;
    border-color:#FFD400 transparent #FFD400 #FFD400; border-radius:50%;
    animation: chomp .25s linear infinite, run 9s linear infinite; }
@keyframes chomp { 0%,100%{ border-right-color:#FFD400; } 50%{ border-right-color:transparent; } }
.ghost { position:absolute; top:8px; left:-120px; font-size:32px; animation: run 9s linear infinite; }
.g1{ animation-delay:-1.2s; } .g2{ animation-delay:-2.0s; } .g3{ animation-delay:-2.8s; }
@keyframes run { from{ left:-120px; } to{ left:100%; } }

/* ---------- CARTES KPI ---------- */
.kpi { background: linear-gradient(145deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
    border: 2px solid var(--c); border-radius: 14px; padding: 14px 12px; text-align:center;
    box-shadow: 0 0 14px var(--c), inset 0 0 12px rgba(0,0,0,.4); height: 100%;
    transition: transform .2s; }
.kpi:hover { transform: translateY(-5px) scale(1.03); }
.kpi-icon { font-size: 1.8rem; animation: bounce 2s ease-in-out infinite; }
.kpi-label { font-family:'Press Start 2P', monospace; font-size:.5rem; color:#b8b8e0; margin-top:6px; line-height:1.5; }
.kpi-value { font-family:'Orbitron', sans-serif; font-weight:900; font-size:1.55rem; color:var(--c); margin-top:6px;
    text-shadow: 0 0 10px var(--c); }
.kpi-sub { font-family:'Orbitron', sans-serif; font-size:.72rem; color:#cfcff5; margin-top:2px; }

/* ---------- CARTES INSIGHT / DÉCISION ---------- */
.insight { background: rgba(155,93,229,.12); border-left: 5px solid var(--c); border-radius: 10px;
    padding: 12px 14px; height:100%; }
.insight b { color: var(--c); font-family:'Orbitron', sans-serif; }
.insight .t { font-family:'Press Start 2P', monospace; font-size:.55rem; color:var(--c); line-height:1.6; }
.decision { background: linear-gradient(90deg, rgba(0,245,212,.15), rgba(255,46,151,.15));
    border: 2px solid #00F5D4; border-radius: 14px; padding: 14px 20px; margin-top: 10px; }
.section { font-family:'Press Start 2P', monospace; color:#FEE440; font-size:.85rem; margin: 26px 0 8px 0;
    text-shadow: 0 0 8px #FF9F1C; }
</style>
""",
    unsafe_allow_html=True,
)


##################### FONCTIONS UTILES
def show(fig):
    """Affiche un graphique plotly (compatible anciennes et nouvelles versions de Streamlit)."""
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def style(fig, height=380, title=None):
    """Applique le thème néon à un graphique."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="Orbitron, sans-serif", color="#E8E8FF", size=12),
        height=height,
        margin=dict(l=10, r=10, t=55 if title else 20, b=10),
        title=dict(text=title, font=dict(family="Press Start 2P, monospace", size=12, color="#FEE440")) if title else None,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, x=0),
    )
    return fig


def kpi(icon, label, value, sub, color):
    return (
        f'<div class="kpi" style="--c:{color}"><div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div></div>'
    )


def insight(title, body, color):
    return f'<div class="insight" style="--c:{color}"><div class="t">{title}</div><p style="margin-top:8px">{body}</p></div>'


def hero(subtitle):
    st.markdown(
        f"""
<div class="hero">
<div class="hero-title">🎮 GAME SALES COMMAND CENTER</div>
<div class="hero-sub">{subtitle}</div>
</div>
<div class="chars"><span>🍄</span><span>👾</span><span>🐢</span><span>🕹️</span><span>⭐</span><span>🦔</span><span>👻</span></div>
<div class="pac-track"><div class="pac"></div><span class="ghost g1">👻</span><span class="ghost g2">👻</span><span class="ghost g3">👻</span></div>
""",
        unsafe_allow_html=True,
    )


def section(txt):
    st.markdown(f'<div class="section">{txt}</div>', unsafe_allow_html=True)


##################### BARRE LATÉRALE & NAVIGATION
st.sidebar.title("🕹️ MENU")
pages = ["Description du projet", "Résultats principaux", "Tableau de bord"]
page = st.sidebar.radio("Aller à la page :", pages)


##################### PAGE 0 : DESCRIPTION
if page == pages[0]:
    hero("INSERT COIN TO START")

    st.write("## Contexte & mission")
    st.write(
        "Vous êtes l'équipe data de la **Direction des ventes** d'un éditeur de jeux vidéo. "
        "La direction doit décider **quels genres, quelles plateformes et quels marchés prioriser**. "
        "À partir de la base `vgsales` (ventes mondiales de jeux, en millions d'unités), "
        "nous construisons un tableau de bord lisible **en un coup d'œil**."
    )

    c1, c2, c3 = st.columns(3)
    c1.markdown(insight("🎯 QUESTION 1", "Quels <b>genres</b> génèrent le plus de ventes… et lesquels sont les plus <b>rentables par jeu</b> ?", "#00F5D4"), unsafe_allow_html=True)
    c2.markdown(insight("🌍 QUESTION 2", "Les <b>préférences régionales</b> diffèrent-elles (Amérique du Nord, Europe, Japon) ?", "#FF2E97"), unsafe_allow_html=True)
    c3.markdown(insight("📈 QUESTION 3", "Où va le marché : quelles <b>plateformes</b> et quels <b>éditeurs</b> dominent, et quelle est la tendance ?", "#FEE440"), unsafe_allow_html=True)

    st.write("")
    if st.checkbox("Afficher le dataframe"):
        st.dataframe(df)
    if st.checkbox("Afficher les noms des variables"):
        st.write(list(df.columns))
    if st.checkbox("Afficher les statistiques descriptives"):
        st.dataframe(df.describe())

    st.caption(
        f"Base nettoyée : {len(df):,} jeux, de {df['Year'].min()} à {df['Year'].max()}. "
        "Les lignes sans année (≈1,6 %) et les années > 2016 (données quasi vides) sont exclues."
    )


##################### PAGE 1 : RÉSULTATS PRINCIPAUX
elif page == pages[1]:
    hero("PLAYER 1 : ANALYSES CLÉS")

    # ---------- Analyse 1 : genres
    section("1 · LES GENRES : VOLUME vs RENTABILITÉ")
    g = df.groupby("Genre")["Global_Sales"].agg(total="sum", jeux="count", moyenne="mean").sort_values("total", ascending=False)
    top3 = g.head(3)
    part_top3 = top3["total"].sum() / g["total"].sum() * 100
    best_avg = g[g["jeux"] >= 100]["moyenne"].idxmax()

    col1, col2 = st.columns([0.55, 0.45])
    with col1:
        fig = px.bar(
            g.reset_index().sort_values("total"),
            x="total", y="Genre", orientation="h", text_auto=".0f",
            color="moyenne", color_continuous_scale=NEON_SCALE,
            labels={"total": "Ventes mondiales (M)", "moyenne": "Moy. / jeu (M)"},
        )
        show(style(fig, 420, "VENTES TOTALES (couleur = vente moyenne/jeu)"))
    with col2:
        st.markdown(
            f"**Analyse** : {', '.join(top3.index)} pèsent **{part_top3:.0f} %** des ventes mondiales.  \n\n"
            f"**Interprétation** : le volume vient surtout du nombre de sorties. "
            f"Rapporté au nombre de jeux, **{best_avg}** est le plus rentable "
            f"({g.loc[best_avg, 'moyenne']:.2f} M/jeu contre {g['moyenne'].mean():.2f} M en moyenne).  \n\n"
            f"**Recommandation** : sécuriser un portefeuille sur les genres volume, mais concentrer les gros budgets "
            f"sur les genres à forte vente moyenne par titre."
        )

    # ---------- Analyse 2 : régions
    section("2 · PRÉFÉRENCES RÉGIONALES")
    reg = df.groupby("Genre")[list(REG_COLS)].sum().rename(columns=REG_COLS)
    reg_pct = (reg / reg.sum() * 100).round(1)
    jp_rpg = reg_pct.loc["Role-Playing", "Japon"]
    na_rpg = reg_pct.loc["Role-Playing", "Amérique du Nord"]
    na_shoot = reg_pct.loc["Shooter", "Amérique du Nord"]
    jp_shoot = reg_pct.loc["Shooter", "Japon"]
    st.markdown(
        f"**Analyse** : le Role-Playing représente **{jp_rpg:.0f} %** des ventes au Japon contre **{na_rpg:.0f} %** en Amérique du Nord, "
        f"alors que le Shooter pèse **{na_shoot:.0f} %** en Amérique du Nord contre **{jp_shoot:.0f} %** au Japon.  \n\n"
        "**Interprétation** : les marchés n'ont pas les mêmes goûts, un lancement mondial uniforme est sous-optimal.  \n\n"
        "**Recommandation** : adapter le plan de lancement par région (RPG en priorité au Japon, Shooter/Sport en Amérique du Nord)."
    )
    scale = ["#4a0d3a", "#FF2E97", "#FEE440"]

    def _rgb(h):
        return [int(h[i:i + 2], 16) for i in (1, 3, 5)]

    def _color(v, vmin, vmax):
        t = 0 if vmax == vmin else (v - vmin) / (vmax - vmin)
        pos = t * (len(scale) - 1)
        i = min(int(pos), len(scale) - 2)
        a, b = _rgb(scale[i]), _rgb(scale[i + 1])
        rgb = [round(a[k] + (b[k] - a[k]) * (pos - i)) for k in range(3)]
        lum = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        txt = "#111111" if lum > 150 else "#FFFFFF"
        return f"background-color: rgb({rgb[0]},{rgb[1]},{rgb[2]}); color: {txt}; font-weight: 600;"

    vmin, vmax = reg_pct.min().min(), reg_pct.max().max()
    styled = reg_pct.style.apply(
    lambda d: d.map(lambda v: _color(v, vmin, vmax)), axis=None).format("{:.1f} %")
    st.dataframe(styled, height=(len(reg_pct) + 1) * 35 + 3)

    # ---------- Analyse 3 : éditeurs & plateformes
    section("3 · QUI DOMINE ? ÉDITEURS & PLATEFORMES")
    pub = df.groupby("Publisher")["Global_Sales"].sum().sort_values(ascending=False)
    plat = df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(pub.head(8).sort_values().reset_index(), x="Global_Sales", y="Publisher", orientation="h",
                     text_auto=".0f", color_discrete_sequence=["#FF2E97"], labels={"Global_Sales": "Ventes (M)"})
        show(style(fig, 360, "TOP 8 ÉDITEURS"))
    with col2:
        fig = px.bar(plat.head(8).sort_values().reset_index(), x="Global_Sales", y="Platform", orientation="h",
                     text_auto=".0f", color_discrete_sequence=["#00BBF9"], labels={"Global_Sales": "Ventes (M)"})
        show(style(fig, 360, "TOP 8 PLATEFORMES"))
    st.markdown(
        f"**Analyse** : **{pub.index[0]}** réalise **{pub.iloc[0] / pub.sum() * 100:.0f} %** des ventes mondiales, "
        f"et **{plat.index[0]}** est la plateforme la plus vendeuse.  \n\n"
        "**Recommandation** : face à un leader aussi installé, privilégier les genres/régions où la concurrence est moins forte "
        "(voir la carte « Où investir ? » du tableau de bord)."
    )


##################### PAGE 2 : TABLEAU DE BORD
elif page == pages[2]:
    hero("DASHBOARD : DÉCIDEZ EN UN COUP D'ŒIL")

    ######## CONTENEUR 1 : FILTRES
    st.sidebar.header("🎛️ Filtres")
    marche = st.sidebar.selectbox("Marché analysé", list(REGIONS), index=0)
    col = REGIONS[marche]
    annees = st.sidebar.slider("Période", int(df["Year"].min()), int(df["Year"].max()), (1990, int(df["Year"].max())))
    genres_sel = st.sidebar.multiselect("Genres (vide = tous)", sorted(df["Genre"].unique()))
    plat_sel = st.sidebar.multiselect("Plateformes (vide = toutes)", sorted(df["Platform"].unique()))
    top_pub = df.groupby("Publisher")["Global_Sales"].sum().sort_values(ascending=False).head(50).index.tolist()
    pub_sel = st.sidebar.multiselect("Éditeurs (top 50, vide = tous)", top_pub)

    f = df[df["Year"].between(*annees)]
    if genres_sel:
        f = f[f["Genre"].isin(genres_sel)]
    if plat_sel:
        f = f[f["Platform"].isin(plat_sel)]
    if pub_sel:
        f = f[f["Publisher"].isin(pub_sel)]

    if f.empty or f[col].sum() == 0:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
        st.stop()

    ######## Calculs communs
    g = f.groupby("Genre")[col].agg(total="sum", jeux="count", moyenne="mean")
    gp = f.groupby("Platform")[col].sum().sort_values(ascending=False)
    pb = f.groupby("Publisher")[col].sum().sort_values(ascending=False)
    reg_tot = f[list(REG_COLS)].sum().rename(REG_COLS)
    yearly = f.groupby("Year")[col].sum()

    total = f[col].sum()
    top_genre = g["total"].idxmax()
    top_genre_share = g["total"].max() / total * 100

    ######## CONTENEUR 2 : KPI
    section(f"📊 KPI : MARCHÉ « {marche.upper()} »")
    k = st.columns(6)
    cards = [
        kpi("💰", "VENTES TOTALES", f"{total:,.0f} M", f"{annees[0]}–{annees[1]}", "#00F5D4"),
        kpi("🎮", "JEUX SORTIS", f"{len(f):,}", f"{f['Name'].nunique():,} titres uniques", "#FF2E97"),
        kpi("⚖️", "VENTE MOY. / JEU", f"{total / len(f):.2f} M", "par référence", "#FEE440"),
        kpi("🏆", "GENRE N°1", top_genre, f"{top_genre_share:.0f} % des ventes", "#9B5DE5"),
        kpi("🕹️", "PLATEFORME N°1", gp.index[0], f"{gp.iloc[0] / total * 100:.0f} % des ventes", "#00BBF9"),
        kpi("🏢", "ÉDITEUR N°1", pb.index[0][:16], f"{pb.iloc[0] / total * 100:.0f} % des ventes", "#FF9F1C"),
    ]
    for c, html in zip(k, cards):
        c.markdown(html, unsafe_allow_html=True)

    ######## CONTENEUR 3 : VERDICT AUTOMATIQUE (insights)
    section("🧠 LE VERDICT EN 10 SECONDES")
    g_ok = g[g["jeux"] >= 20] if (g["jeux"] >= 20).any() else g
    best_avg = g_ok["moyenne"].idxmax()
    leader_region = reg_tot.idxmax()
    leader_share = reg_tot.max() / reg_tot.sum() * 100

    # Tendance : 5 dernières années vs 5 précédentes (dans la sélection)
    last = int(yearly.index.max())
    recent = yearly[yearly.index.isin(range(last - 4, last + 1))].sum()
    prev = yearly[yearly.index.isin(range(last - 9, last - 4))].sum()
    if prev > 0:
        growth = (recent / prev - 1) * 100
        trend_icon, trend_color = ("📈", "#00F5D4") if growth >= 0 else ("📉", "#FF2E97")
        trend_txt = f"Sur {last - 4}-{last}, les ventes sont <b>{growth:+.0f} %</b> vs les 5 années précédentes."
    else:
        trend_icon, trend_color, trend_txt = "➖", "#FEE440", "Période trop courte pour mesurer une tendance."
    peak = int(yearly.idxmax())

    i1, i2, i3, i4 = st.columns(4)
    i1.markdown(insight("🏆 VALEUR SÛRE", f"<b>{top_genre}</b> = {top_genre_share:.0f} % des ventes. Le plus gros réservoir de volume.", "#00F5D4"), unsafe_allow_html=True)
    i2.markdown(insight("💎 PLUS RENTABLE", f"<b>{best_avg}</b> : {g_ok.loc[best_avg, 'moyenne']:.2f} M par jeu (moy. {total / len(f):.2f} M).", "#FEE440"), unsafe_allow_html=True)
    i3.markdown(insight("🌍 MARCHÉ DOMINANT", f"<b>{leader_region}</b> : {leader_share:.0f} % des ventes de la sélection.", "#00BBF9"), unsafe_allow_html=True)
    i4.markdown(insight(f"{trend_icon} TENDANCE", f"{trend_txt} Pic en <b>{peak}</b>.", trend_color), unsafe_allow_html=True)

    st.markdown(
        f'<div class="decision">🎯 <b>DÉCISION SUGGÉRÉE</b> : maintenir le portefeuille sur <b>{top_genre}</b> (volume), '
        f'réserver les budgets premium à <b>{best_avg}</b> (rentabilité par titre) et piloter les lancements en priorité '
        f'sur <b>{leader_region}</b>. Voir « Où investir ? » ci-dessous pour affiner.</div>',
        unsafe_allow_html=True,
    )

    ######## CONTENEUR 4 : ÉVOLUTION + RÉGIONS
    section("📈 DYNAMIQUE DU MARCHÉ")
    c1, c2 = st.columns([0.62, 0.38])
    with c1:
        ev = f.groupby("Year")[list(REG_COLS)].sum().reset_index().melt("Year", var_name="Région", value_name="Ventes (M)")
        ev["Région"] = ev["Région"].map(REG_COLS)
        fig = px.area(ev, x="Year", y="Ventes (M)", color="Région", color_discrete_map=REG_COLOR)
        show(style(fig, 380, "VENTES PAR ANNÉE ET PAR RÉGION (M)"))
    with c2:
        fig = px.pie(values=reg_tot.values, names=reg_tot.index, hole=0.55,
                     color=reg_tot.index, color_discrete_map=REG_COLOR)
        fig.update_traces(textinfo="percent+label", textfont_size=12)
        fig.update_layout(showlegend=False)
        show(style(fig, 380, "RÉPARTITION DES VENTES"))

    ######## CONTENEUR 5 : GENRES + OÙ INVESTIR
    section("🎯 QUELS GENRES ? OÙ INVESTIR ?")
    c1, c2 = st.columns(2)
    with c1:
        gg = g.reset_index().sort_values("total")
        fig = px.bar(gg, x="total", y="Genre", orientation="h", text_auto=".0f",
                     color="total", color_continuous_scale=NEON_SCALE, labels={"total": "Ventes (M)"})
        fig.update_layout(coloraxis_showscale=False)
        show(style(fig, 460, f"VENTES PAR GENRE : {marche.upper()} (M)"))
    with c2:
        gb = g.reset_index()
        fig = px.scatter(gb, x="jeux", y="moyenne", size="total", color="Genre", text="Genre", size_max=55,
                         color_discrete_sequence=px.colors.qualitative.Bold,
                         labels={"jeux": "Nombre de jeux sortis", "moyenne": "Vente moyenne / jeu (M)"})
        fig.update_traces(textposition="top center", textfont_size=10)
        fig.add_hline(y=gb["moyenne"].median(), line_dash="dot", line_color="#888")
        fig.add_vline(x=gb["jeux"].median(), line_dash="dot", line_color="#888")
        for txt, x, y in [("💎 NICHE RENTABLE", 0.02, 0.98), ("⭐ VALEURS SÛRES", 0.98, 0.98),
                          ("🔍 À SURVEILLER", 0.02, 0.02), ("⚠️ MARCHÉ SATURÉ", 0.98, 0.02)]:
            fig.add_annotation(text=txt, xref="paper", yref="paper", x=x, y=y, showarrow=False,
                               xanchor="left" if x < 0.5 else "right", yanchor="top" if y > 0.5 else "bottom",
                               font=dict(size=10, color="#FEE440"))
        fig.update_layout(showlegend=False)
        show(style(fig, 460, "OÙ INVESTIR ? (taille = ventes totales)"))
    st.caption("Lecture : haut = chaque jeu se vend bien ; droite = beaucoup de titres (forte concurrence). "
               "Haut-gauche = genres rentables avec peu de sorties : opportunités.")

    ######## CONTENEUR 6 : HEATMAP + PLATEFORMES
    section("🌍 QUI AIME QUOI ? PLATEFORMES & MARCHÉS")
    c1, c2 = st.columns([0.55, 0.45])
    with c1:
        hm = f.groupby("Genre")[list(REG_COLS)].sum().rename(columns=REG_COLS)
        hm = (hm / hm.sum() * 100).round(0)
        hm = hm.loc[hm.sum(axis=1).sort_values(ascending=False).index]
        fig = px.imshow(hm, text_auto=".0f", aspect="auto", color_continuous_scale=["#0b0720", "#9B5DE5", "#00F5D4"],
                        labels=dict(color="% ventes"))
        fig.update_layout(coloraxis_showscale=False)
        show(style(fig, 420, "PART DE CHAQUE GENRE DANS CHAQUE RÉGION (%)"))
    with c2:
        pl = gp.head(10).sort_values().reset_index()
        fig = px.bar(pl, x=col, y="Platform", orientation="h", text_auto=".0f",
                     color=col, color_continuous_scale=["#2B1055", "#00BBF9", "#00F5D4"], labels={col: "Ventes (M)"})
        fig.update_layout(coloraxis_showscale=False)
        show(style(fig, 420, "TOP 10 PLATEFORMES (M)"))

    ######## CONTENEUR 7 : ÉDITEURS + JEUX
    section("🏅 LES LÉGENDES : ÉDITEURS & JEUX")
    c1, c2 = st.columns(2)
    with c1:
        pbt = pb.head(10).sort_values().reset_index()
        fig = px.bar(pbt, x=col, y="Publisher", orientation="h", text_auto=".0f",
                     color=col, color_continuous_scale=["#4a0d3a", "#FF2E97", "#FEE440"], labels={col: "Ventes (M)"})
        fig.update_layout(coloraxis_showscale=False)
        show(style(fig, 420, "TOP 10 ÉDITEURS (M)"))
    with c2:
        tg = f.sort_values(col, ascending=False).head(10).copy()
        tg["Titre"] = tg["Name"].str.slice(0, 28) + " (" + tg["Platform"] + ")"
        fig = px.bar(tg, x=col, y="Titre", orientation="h", text_auto=".1f",
                     color="Genre", color_discrete_sequence=px.colors.qualitative.Bold, labels={col: "Ventes (M)"})
        fig.update_yaxes(categoryorder="total ascending")
        fig = style(fig, 460, "TOP 10 JEUX (M)")
        fig.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.22, x=0, title_text=""),
            margin=dict(l=10, r=10, t=55, b=10),
        )
        show(fig)

    st.caption("Source : vgsales (ventes en millions d'unités). Les années 2017+ et les jeux sans année sont exclus.")
