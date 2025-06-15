import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# === TRANSLATIONS ===

TRANSLATIONS = {
    "en": {
        "page_title": "Retention Model",
        "main_title": "Recruitment Planning for 90,000 Retained International Workers by 2030",
        "select_scenario": "Select retention scenario:",
        "single": "single",
        "partnered": "partnered with another worker",
        "national_average": "national average",
        "fix_recruitment": "Fix recruitment for 2029",
        "year": "Year",
        "recruits": "Recruits",
        "retention_rate": "Retention Rate",
        "retained_2030": "Retained in 2030",
        "summary_text": "📌 <strong>To retain 90,000 workers by 2030</strong> in the <strong>{scenario}</strong> scenario, we would need to recruit <strong>{total}</strong> people in total, assuming <strong>{r2029}</strong> are hired in 2029.",
        "chart_title": "Annual Recruitment vs. Retention",
        "chart_ylabel": "Number of People",
        "retention_curve_title": "{scenario} Retention Curve",
        "retention_curve_xlabel": "Years After Arrival",
        "retention_curve_ylabel": "Retention Rate",
        "caption_1": "Retention rates are applied cohort by cohort: 2025 gets Year 5 retention, 2029 gets Year 1 retention.",
        "caption_2": "Rates from Copenhagen Kommune's Nøgletalsanalyser",
        "language": "Language",
        "error": "Error",
        "cost_analysis_title": "Financial Impact Analysis",
        "cost_mix_international": "100% international recruitment",
        "cost_mix_mixed": "50% domestic + 50% international recruitment",
        "cost_mix_average": "70% international + 30% domestic recruitment",
        "total_recruitment_cost": "Total Recruitment Cost",
        "avg_per_hire": "Avg per hire",
        "savings_vs_single": "Savings vs Single Scenario",
        "lower": "lower",
        "baseline_scenario": "Baseline Scenario",
        "baseline_text": "Reference point",
        "cost_assumptions": "Cost Assumptions",
        "domestic_cost": "Domestic recruitment",
        "international_cost": "International recruitment", 
        "scenario_mix": "This scenario"
    },
    "da": {
        "page_title": "Fastholdelsesmodel",
        "main_title": "Rekrutteringsplanlægning for 90.000 fastholdte internationale arbejdere inden 2030",
        "select_scenario": "Vælg fastholdelsesscenarie:",
        "single": "enlig",
        "partnered": "i parforhold med en anden arbejder",
        "national_average": "landsdækkende gennemsnit",
        "fix_recruitment": "Fastlæg rekruttering for 2029",
        "year": "År",
        "recruits": "Rekrutterede",
        "retention_rate": "Fastholdelsesgrad",
        "retained_2030": "Fastholdt i 2030",
        "summary_text": "📌 <strong>For at fastholde 90.000 arbejdere inden 2030</strong> i <strong>{scenario}</strong>-scenariet, skal vi rekruttere <strong>{total}</strong> personer i alt, forudsat at <strong>{r2029}</strong> ansættes i 2029.",
        "chart_title": "Årlig rekruttering vs. fastholdelse",
        "chart_ylabel": "Antal personer",
        "retention_curve_title": "{scenario} fastholdelseskurve",
        "retention_curve_xlabel": "År efter ankomst",
        "retention_curve_ylabel": "Fastholdelsesgrad",
        "caption_1": "Fastholdelsesgrader anvendes kohorte for kohorte: 2025 får år 5 fastholdelse, 2029 får år 1 fastholdelse.",
        "caption_2": "Satser fra København Kommunes Nøgletalsanalyser",
        "language": "Sprog",
        "error": "Fejl",
        "cost_analysis_title": "Økonomisk konsekvensanalyse",
        "cost_mix_international": "100% international rekruttering",
        "cost_mix_mixed": "50% indenlandsk + 50% international rekruttering",
        "cost_mix_average": "70% international + 30% indenlandsk rekruttering",
        "total_recruitment_cost": "Samlet rekrutteringsomkostning",
        "avg_per_hire": "Gns. pr. ansættelse",
        "savings_vs_single": "Besparelser vs. enlig-scenario",
        "lower": "lavere",
        "baseline_scenario": "Reference-scenario",
        "baseline_text": "Referencepunkt",
        "cost_assumptions": "Omkostningsforudsætninger",
        "domestic_cost": "Indenlandsk rekruttering",
        "international_cost": "International rekruttering",
        "scenario_mix": "Dette scenario"
    }
}

# === BRAND STYLING ===

TEAL = "#69C4C0"
BLUE = "#43AEFF"
ORANGE = "#E08800"
BG_WHITE = "#F8FAFB"
GRAY = "#CCCCCC"
GRAY_LIGHT = "#EEEEEE"
TEXT = "#333333"
COLOR_CYCLE = [TEAL, BLUE, ORANGE, "#419693", "#1C87D6", "#A7DEDA", "#9AD2FF", "#FFBC66"]

def setup_hardcoded_styling():
    font_family = 'Georgia'
    available_fonts = set(f.name for f in mpl.font_manager.fontManager.ttflist)
    if font_family not in available_fonts:
        font_family = 'serif'

    mpl.rcParams.update({
        'font.family': font_family,
        'font.size': 13,
        'figure.figsize': (10, 6),
        'figure.facecolor': BG_WHITE,
        'axes.facecolor': BG_WHITE,
        'axes.edgecolor': GRAY,
        'axes.linewidth': 1.0,
        'axes.grid': True,
        'axes.prop_cycle': plt.cycler('color', COLOR_CYCLE),
        'axes.titlesize': 16,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'grid.color': GRAY_LIGHT,
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
        'xtick.color': TEXT,
        'ytick.color': TEXT,
        'xtick.major.size': 3.5,
        'ytick.major.size': 3.5,
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.edgecolor': GRAY_LIGHT,
        'legend.facecolor': BG_WHITE,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.facecolor': BG_WHITE,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.axisbelow': True
    })

def apply_chart_style(ax, title=None, xlabel=None, ylabel=None):
    if title: ax.set_title(title, fontsize=16, pad=15)
    if xlabel: ax.set_xlabel(xlabel, fontsize=12)
    if ylabel: ax.set_ylabel(ylabel, fontsize=12)
    if ax.get_legend():
        ax.legend(loc='best', frameon=True, facecolor=BG_WHITE, edgecolor=GRAY_LIGHT)
    ax.set_axisbelow(True)
    ax.grid(True, linestyle='--', alpha=0.7, color=GRAY_LIGHT)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['left'].set_color(GRAY)
    ax.spines['bottom'].set_color(GRAY)
    plt.tight_layout()

def get_text(key, lang="en"):
    return TRANSLATIONS[lang].get(key, key)

def get_scenario_options(lang="en"):
    return {
        get_text("single", lang): "single",
        get_text("partnered", lang): "partnered with another worker", 
        get_text("national_average", lang): "national average"
    }

# === MODEL LOGIC ===

retention_rates = {
    "single": [0.70, 0.55, 0.50, 0.47, 0.41],
    "partnered with another worker": [0.91, 0.80, 0.75, 0.65, 0.61],
    "national average": [0.75, 0.65, 0.53, 0.49, 0.47]
}

def solve_recruitment_hardcode(ret, target, r2029_fixed):
    weights = np.array([ret[4], ret[3], ret[2], ret[1]])
    r1 = ret[0]
    retained_from_2029 = r2029_fixed * r1
    remaining_target = target - retained_from_2029

    if remaining_target <= 0:
        raise ValueError("Fixed R2029 too high — total retained exceeds target.")

    inv_weights = 1 / weights
    proportions = inv_weights / inv_weights.sum()
    r_2025_to_2028 = (proportions * remaining_target / weights).round()

    recruits = np.append(r_2025_to_2028, r2029_fixed)
    retention_weights = np.append(weights, r1)
    return recruits, retention_weights

# === STREAMLIT UI ===

# Must be first Streamlit command
st.set_page_config(page_title="Retention Model", layout="centered", page_icon="🎯" )

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Language toggle in sidebar
with st.sidebar:
    st.selectbox(
        "🌐 Language / Sprog",
        options=['en', 'da'],
        format_func=lambda x: 'English' if x == 'en' else 'Dansk',
        key='language'
    )

lang = st.session_state.language
setup_hardcoded_styling()
st.title(get_text("main_title", lang))

# Get scenario options in current language
scenario_options = get_scenario_options(lang)
selected_scenario_display = st.selectbox(
    get_text("select_scenario", lang), 
    options=list(scenario_options.keys())
)
scenario = scenario_options[selected_scenario_display]

ret = retention_rates[scenario]
target = 90000
years = [2025, 2026, 2027, 2028, 2029]

r2029_fixed = st.slider(
    get_text("fix_recruitment", lang), 
    min_value=2000, 
    max_value=30000, 
    value=15000, 
    step=1000
)

try:
    recruits, weights = solve_recruitment_hardcode(ret, target, r2029_fixed)
    retained = recruits * weights

    df = pd.DataFrame({
        get_text("year", lang): years,
        get_text("recruits", lang): recruits.astype(int),
        get_text("retention_rate", lang): weights.round(3),
        get_text("retained_2030", lang): retained.astype(int)
    })
    st.dataframe(df)

    total_recruited = int(recruits.sum())
    r2029_val = int(r2029_fixed)

    total_recruited_str = f"{total_recruited:,}"
    r2029_val_str = f"{r2029_val:,}"

    st.markdown(
        f"""
        <div style="
            background-color:#FFF3CD;
            border-left: 8px solid #E08800;
            padding: 1.2em;
            margin-top: 1em;
            margin-bottom: 1.5em;
            font-size: 1.3em;
            font-family: Georgia, serif;
        ">
        {get_text("summary_text", lang).format(
            scenario=selected_scenario_display,
            total=total_recruited_str,
            r2029=r2029_val_str
        )}
        </div>
        """,
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots()
    ax.bar(df[get_text("year", lang)], df[get_text("recruits", lang)], label=get_text("recruits", lang))
    ax.plot(df[get_text("year", lang)], df[get_text("retained_2030", lang)], marker="o", color=ORANGE, label=get_text("retained_2030", lang))
    apply_chart_style(ax, title=get_text("chart_title", lang), ylabel=get_text("chart_ylabel", lang))
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    ax2.plot([1, 2, 3, 4, 5], ret, marker='o')
    ax2.set_ylim(0, 1)
    apply_chart_style(ax2, 
                      title=get_text("retention_curve_title", lang).format(scenario=selected_scenario_display),
                      xlabel=get_text("retention_curve_xlabel", lang), 
                      ylabel=get_text("retention_curve_ylabel", lang))
    st.pyplot(fig2)

    st.caption(get_text("caption_1", lang))
    st.caption(get_text("caption_2", lang))

    # === COST ANALYSIS SECTION ===
    st.markdown("---")
    st.subheader(get_text("cost_analysis_title", lang))
    
    # Cost constants (DKK)
    domestic_cost_min = 26636
    domestic_cost_max = 88386
    international_cost_min = 40496
    international_cost_max = 155746
    
    # Calculate cost mix based on scenario
    if scenario == "single":
        # 100% international
        cost_per_hire_min = international_cost_min
        cost_per_hire_max = international_cost_max
        cost_mix_text = get_text("cost_mix_international", lang)
    elif scenario == "partnered with another worker":
        # 50% domestic + 50% international
        cost_per_hire_min = (domestic_cost_min + international_cost_min) / 2
        cost_per_hire_max = (domestic_cost_max + international_cost_max) / 2
        cost_mix_text = get_text("cost_mix_mixed", lang)
    else:
        # National average - assume 70% international, 30% domestic
        cost_per_hire_min = (0.7 * international_cost_min) + (0.3 * domestic_cost_min)
        cost_per_hire_max = (0.7 * international_cost_max) + (0.3 * domestic_cost_max)
        cost_mix_text = get_text("cost_mix_average", lang)
    
    # Calculate total costs
    total_cost_min = total_recruited * cost_per_hire_min
    total_cost_max = total_recruited * cost_per_hire_max
    
    # Calculate savings vs single scenario for comparison
    single_cost_min = total_recruited * international_cost_min
    single_cost_max = total_recruited * international_cost_max
    
    savings_min = single_cost_min - total_cost_min
    savings_max = single_cost_max - total_cost_max
    
    # Display cost analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label=get_text("total_recruitment_cost", lang),
            value=f"DKK {total_cost_min/1000000:.0f}M - {total_cost_max/1000000:.0f}M",
            delta=f"{get_text('avg_per_hire', lang)}: {cost_per_hire_min/1000:.0f}K - {cost_per_hire_max/1000:.0f}K"
        )
    
    with col2:
        if scenario != "single":
            savings_pct_min = (savings_min / single_cost_min) * 100
            savings_pct_max = (savings_max / single_cost_max) * 100
            st.metric(
                label=get_text("savings_vs_single", lang),
                value=f"DKK {savings_min/1000000:.0f}M - {savings_max/1000000:.0f}M",
                delta=f"{savings_pct_min:.0f}% - {savings_pct_max:.0f}% {get_text('lower', lang)}"
            )
        else:
            st.metric(
                label=get_text("baseline_scenario", lang),
                value=get_text("baseline_text", lang)
            )
    
    # Cost breakdown explanation
    st.markdown(
        f"""
        <div style="
            background-color: #F0F8F7;
            border-left: 8px solid {TEAL};
            padding: 1em;
            margin-top: 1em;
            font-size: 1.1em;
            font-family: Georgia, serif;
        ">
        💰 <strong>{get_text('cost_assumptions', lang)}</strong><br>
        • {get_text('domestic_cost', lang)}: DKK 27K - 88K<br>
        • {get_text('international_cost', lang)}: DKK 40K - 156K<br>
        • {get_text('scenario_mix', lang)}: {cost_mix_text}
        </div>
        """,
        unsafe_allow_html=True
    )

except Exception as e:
    st.error(f"{get_text('error', lang)}: {e}")