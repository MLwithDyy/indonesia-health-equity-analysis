import pandas as pd, plotly.express as px, plotly.graph_objects as go, streamlit as st

st.set_page_config(page_title="Life expectancy by province, Indonesia 2024", layout="wide")
D = "data/processed/"
df = pd.read_csv(D + "province_health_2024.csv")
corr = pd.read_csv(D + "corr.csv")
model = pd.read_csv(D + "model.csv")

FACTORS = {"pov": "Poverty rate (%, mean of March and September)", "sanitasi": "Households with decent sanitation (%)",
           "aps_16_18": "School participation, ages 16-18 (%)", "lgdp": "log GRDP per capita (current prices)"}
MEASURES = {"ahh": "Mean of male and female", "ahh_l": "Male", "ahh_p": "Female"}

st.title("Life expectancy across Indonesian provinces, 2024")
st.caption("Source: Statistics Indonesia (BPS), province tables, 2024. Province-level correlations, not cause and effect. "
           "Life expectancy here is the mean of male and female values, not the official BPS total.")
t1, t2, t3, t4 = st.tabs(["Gap", "Factors", "Model", "Notes"])

with t1:
    m = st.radio("Life expectancy", list(MEASURES), format_func=MEASURES.get, horizontal=True)
    d = df.sort_values(m)
    c1, c2, c3 = st.columns(3)
    c1.metric("Highest", f"{d[m].max():.2f}", d.loc[d[m].idxmax(), "prov"].title(), delta_color="off")
    c2.metric("Lowest", f"{d[m].min():.2f}", d.loc[d[m].idxmin(), "prov"].title(), delta_color="off")
    c3.metric("Gap (years)", f"{d[m].max() - d[m].min():.2f}")
    fig = px.bar(d, x=m, y="prov", color="wilayah", orientation="h", height=800,
                 labels={m: "Life expectancy (years)", "prov": "", "wilayah": "Region"})
    fig.update_xaxes(range=[d[m].min() - 2, d[m].max() + 1])
    st.plotly_chart(fig, use_container_width=True)
    st.caption("The female minus male difference varies only between "
               f"{df.ahh_gap.min():.2f} and {df.ahh_gap.max():.2f} years across provinces, so male and female rankings are almost identical.")

with t2:
    f = st.selectbox("Factor", list(FACTORS), format_func=FACTORS.get)
    hide = st.checkbox("Hide the six Papua provinces", value=False)
    d = df[~df.papua] if hide else df
    fig = px.scatter(d, x=f, y="ahh", color="wilayah", hover_name="prov",
                     labels={f: FACTORS[f], "ahh": "Life expectancy (years)", "wilayah": "Region"}, height=550)
    st.plotly_chart(fig, use_container_width=True)
    sc = "Without Papua (n=32)" if hide else "All provinces (n=38)"
    r = corr[(corr.factor == f) & corr.scenario.str.startswith(sc[:7])].iloc[0]
    st.markdown(f"**Spearman rho = {r.rho:.2f}** (95% bootstrap interval {r.lo95:.2f} to {r.hi95:.2f}), {r.scenario}.")
    st.dataframe(corr.pivot(index="factor", columns="scenario", values="rho").round(2).rename(index=FACTORS), use_container_width=True)

with t3:
    sc = st.radio("Scenario", model.scenario.unique().tolist(), horizontal=True)
    mm = model[(model.scenario == sc) & (model.term != "const")]
    fig = go.Figure(go.Scatter(x=mm.coef, y=mm.term.map(lambda t: FACTORS.get(t, t)), mode="markers",
                               error_x=dict(type="data", symmetric=False, array=mm.hi95 - mm.coef, arrayminus=mm.coef - mm.lo95)))
    fig.add_vline(x=0, line_dash="dash")
    fig.update_layout(height=350, xaxis_title="Change in life expectancy (years) per 1 SD of the factor, 95% bootstrap interval")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"R2 = {model[model.scenario == sc].r2.iloc[0]:.2f}, adjusted R2 = {model[model.scenario == sc].r2_adj.iloc[0]:.2f}. "
               "In-sample fit only, not predictive accuracy. Intervals that include 0 mean the data cannot separate that factor's association from zero.")
    st.markdown("**Largest residuals of the main model** (life expectancy minus model prediction, years)")
    res = df.sort_values("resid")
    a, b = st.columns(2)
    a.write("Below prediction"); a.dataframe(res.head(5)[["prov", "wilayah", "ahh", "resid"]].round(2), hide_index=True)
    b.write("Above prediction"); b.dataframe(res.tail(5).iloc[::-1][["prov", "wilayah", "ahh", "resid"]].round(2), hide_index=True)
    st.caption("With 38 provinces, individual residuals are noisy. Several Java provinces sit above prediction, "
               "which suggests something the model does not measure (for example health services); that is a guess, not a finding.")

with t4:
    st.markdown("""
**Questions** (fixed before the analysis, see `QUESTIONS.md`): size of the gap between provinces; which factors correlate with
life expectancy; which still relate to it when considered together; which provinces are far above or below prediction;
whether the female minus male difference varies.

**Limitations**
- Province-level correlations, not cause and effect; a province average does not describe the people in it.
- 38 provinces and one year, so intervals are wide. The six Papua provinces sit at the extreme of most variables and affect results.
- GRDP per capita is distorted by mining. Poverty is the simple mean of two survey rounds.
- A quick look at correlations happened before the analysis choices were fixed, so the model selection is exploratory.
- Health facility and health worker data were not available in recent years and are not included.

**Data:** BPS statistical tables, accessed on the date listed in `data_sources.md`.
""")
    st.download_button("Download the processed table (CSV)", df.to_csv(index=False), "province_health_2024.csv", "text/csv")
