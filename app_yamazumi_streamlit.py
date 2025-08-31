
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Yamazumi App", layout="wide")
st.title("Simulador Yamazumi (Upload de Excel)")

st.markdown(
    "Carregue uma planilha **.xlsx** com **três colunas**:"
    " **Estacao**, **Tempo** e **Categoria**."
    " O tempo pode estar em segundos ou minutos (você escolhe abaixo)."
)

with st.sidebar:
    st.header("Configurações")
    unit = st.radio("Unidade do tempo na planilha", ["segundos", "minutos"], index=0)
    takt_min = st.number_input("Takt time (min)", min_value=0.0, value=3.5, step=0.1)
    show_table = st.checkbox("Mostrar resumo por estação", value=True)

uploaded = st.file_uploader("Planilha Excel (.xlsx)", type=["xlsx"])
gerar = st.button("Gerar gráfico")

def validate_and_normalize(df: pd.DataFrame) -> pd.DataFrame:
    # normaliza nomes de coluna (case-insensitive e trims)
    norm_cols = {c.lower().strip(): c for c in df.columns}
    required = ["estacao", "tempo", "categoria"]
    missing = [c for c in required if c not in norm_cols]
    if missing:
        raise ValueError(f"Colunas ausentes: {missing}. A planilha deve ter Estacao, Tempo e Categoria.")
    col_e = norm_cols["estacao"]
    col_t = norm_cols["tempo"]
    col_c = norm_cols["categoria"]

    out = pd.DataFrame({
        "Estacao": df[col_e],
        "Tempo": pd.to_numeric(df[col_t], errors="coerce"),
        "Categoria": df[col_c].astype(str).str.upper().str.strip()
    }).dropna(subset=["Tempo"])
    if unit == "minutos":
        out["Tempo"] = out["Tempo"] * 60.0  # converte para segundos
    out.rename(columns={"Tempo": "Tempo_s"}, inplace=True)
    return out

def plot_yamazumi(df_norm: pd.DataFrame, takt_s: float):
    # agrega por estação e categoria
    pivot = df_norm.groupby(["Estacao", "Categoria"])["Tempo_s"].sum().unstack(fill_value=0)
    totals = pivot.sum(axis=1)
    # ordena por estação como string natural
    try:
        order = sorted(pivot.index, key=lambda x: int(str(x).split()[-1]))
        pivot = pivot.loc[order]
        totals = totals.loc[order]
    except Exception:
        pass

    fig, ax = plt.subplots(figsize=(12, 6))
    pivot.plot(kind="bar", stacked=True, ax=ax)
    if takt_s > 0:
        ax.axhline(takt_s, linestyle="--", linewidth=2, label=f"Takt: {takt_s:.0f}s")
    ax.set_xlabel("Estação")
    ax.set_ylabel("Tempo (s)")
    ax.set_title("Gráfico Yamazumi (Tempo por Estação)")
    ax.legend(loc="upper right")
    # marca gargalo
    try:
        idx_max = totals.idxmax()
        x_pos = list(pivot.index).index(idx_max)
        ax.annotate(
            "Gargalo",
            xy=(x_pos, totals.max()),
            xytext=(x_pos, totals.max() * 1.05),
            ha="center",
            arrowprops=dict(arrowstyle="->")
        )
    except Exception:
        pass
    fig.tight_layout()
    return fig, pivot, totals

if gerar:
    if not uploaded:
        st.error("Envie um arquivo .xlsx.")
    else:
        try:
            raw = pd.read_excel(uploaded)
            df = validate_and_normalize(raw)
            fig, pivot, totals = plot_yamazumi(df, takt_min * 60.0)
            st.pyplot(fig)

            if show_table:
                st.subheader("Resumo por estação (segundos)")
                resumo = totals.to_frame("Total_s")
                if takt_min > 0:
                    resumo["Δ_vs_Takt_s"] = (resumo["Total_s"] - takt_min * 60.0)
                st.dataframe(resumo.round(1))

            # botão para baixar PNG do gráfico
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
            st.download_button(
                "Baixar gráfico (PNG)",
                data=buf.getvalue(),
                file_name="yamazumi.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Erro ao processar: {e}")
