import gradio as gr
from generate_analysis import run_analysis, run_analysis_multi
import os

# --- helper to convert summary dataframe into HTML cards ---
def make_company_cards(summary_df):
    if summary_df is None or summary_df.empty:
        return "<p>No data available.</p>"
    cards_html = "<div style='display:flex;flex-wrap:wrap;gap:10px;'>"
    for _, row in summary_df.iterrows():
        cards_html += f"""
        <div style='background:#1f2937;color:#f9fafb;padding:10px;border-radius:8px;width:180px;'>
            <h4 style='margin:0;color:#fbbf24;'>{row['Company']}</h4>
            <p>Close: {row['Close']:.2f}</p>
            <p>RSI: {row['RSI_10']:.2f}</p>
            <p>MA: {row['MA_10']:.2f}</p>
        </div>
        """
    cards_html += "</div>"
    return cards_html

def launch_ui():
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo"), title="📈 Sneha's Stock Dashboard") as demo:

        # Animated Header
        gr.HTML("""
        <div class="marquee-container">
            <div class="marquee-text">
                📊 SNEHA: SMART STOCK PORTFOLIO DASHBOARD | SINGLE + MULTI COMPANY ANALYSIS | RSI + MA 📈
            </div>
        </div>
        """)

        with gr.Tabs():
            # --- Single Company Analysis Tab ---
            with gr.TabItem("💹 Single Stock Analysis"):
                with gr.Row():
                    with gr.Column(scale=1):
                        ticker = gr.Textbox(label="Stock Symbol", value="RVNL", placeholder="e.g. RELIANCE.NS")
                        date_mode = gr.Radio(["Relative Period", "Custom Date Range"], value="Relative Period", label="Select Mode")

                        with gr.Group() as period_group:
                            months = gr.Slider(1, 24, value=6, label="Period (Months)")

                        with gr.Group(visible=False) as date_group:
                            start_date = gr.Textbox(label="Start Date (YYYY-MM-DD)", value="2023-01-01")
                            end_date = gr.Textbox(label="End Date (YYYY-MM-DD)", value="2023-12-31")

                        plot_type = gr.Dropdown(
                            ["Price Only", "Price + MA", "RSI Only", "Price + MA + RSI"],
                            value="Price + MA + RSI",
                            label="Analysis Type"
                        )
                        run_btn_single = gr.Button("🚀 Analyze Single Stock")

                    with gr.Column(scale=2):
                        output_plot_single = gr.Plot(label="Stock Chart")
                        output_df_single = gr.Dataframe(label="Stock Data Preview")

            # --- Multi Company Portfolio Tab ---
            with gr.TabItem("📈 Portfolio Analysis"):
                with gr.Row():
                    with gr.Column(scale=1):
                        companies = gr.Dropdown(
                            ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ITC.NS"],
                            label="Select Companies",
                            multiselect=True,
                            value=["RELIANCE.NS","INFY.NS"]
                        )
                        date_mode_multi = gr.Radio(["Relative Period", "Custom Date Range"], value="Relative Period", label="Select Mode")

                        with gr.Group() as period_group_multi:
                            months_multi = gr.Slider(1, 24, value=6, label="Period (Months)")

                        with gr.Group(visible=False) as date_group_multi:
                            start_date_multi = gr.Textbox(label="Start Date (YYYY-MM-DD)", value="2023-01-01")
                            end_date_multi = gr.Textbox(label="End Date (YYYY-MM-DD)", value="2023-12-31")

                        plot_type_multi = gr.Dropdown(
                            ["Price Only", "Price + MA", "RSI Only", "Price + MA + RSI"],
                            value="Price + MA + RSI",
                            label="Analysis Type"
                        )
                        run_btn_multi = gr.Button("🚀 Analyze Portfolio")

                    with gr.Column(scale=2):
                        output_plot_multi = gr.Plot(label="Portfolio Chart")
                        output_df_multi = gr.Dataframe(label="Portfolio Data Preview")
                        company_cards = gr.HTML(label="Company Summaries")

            # --- About Tab ---
            with gr.TabItem("ℹ️ About"):
                gr.HTML("""
                <div style="padding:20px; color:#f1f5f9;">
                    <h3 style="color:#fbbf24;">Welcome to Sneha's Financial Intelligence Hub ✨</h3>
                    <p>This dashboard supports both single stock and multi-company portfolio analysis with RSI + Moving Averages.</p>
                </div>
                """)

        # Toggle logic for single tab
        def toggle(mode):
            return gr.update(visible=(mode == "Relative Period")), gr.update(visible=(mode == "Custom Date Range"))
        date_mode.change(toggle, inputs=[date_mode], outputs=[period_group, date_group])

        # Toggle logic for multi tab
        def toggle_multi(mode):
            return gr.update(visible=(mode == "Relative Period")), gr.update(visible=(mode == "Custom Date Range"))
        date_mode_multi.change(toggle_multi, inputs=[date_mode_multi], outputs=[period_group_multi, date_group_multi])

        # Bindings
        run_btn_single.click(
            fn=run_analysis,
            inputs=[ticker, date_mode, months, start_date, end_date, plot_type],
            outputs=[output_plot_single, output_df_single]
        )

        def run_multi_and_cards(companies, date_mode_multi, months_multi, start_date_multi, end_date_multi, plot_type_multi):
            fig, summary = run_analysis_multi(companies, date_mode_multi, months_multi, start_date_multi, end_date_multi, plot_type_multi)
            cards_html = make_company_cards(summary)
            return fig, summary, cards_html

        run_btn_multi.click(
            fn=run_multi_and_cards,
            inputs=[companies, date_mode_multi, months_multi, start_date_multi, end_date_multi, plot_type_multi],
            outputs=[output_plot_multi, output_df_multi, company_cards]
        )

    return demo

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    launch_ui().launch(server_name="0.0.0.0", server_port=port)
