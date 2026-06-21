import gradio as gr 
from generate_analysis import run_analysis, run_analysis_multi
import os

def make_company_cards(summary_df): 
    if summary_df is None or summary_df.empty:
        return "<p>No data available.</p>"
    cards_html = "<div class='cards-container'>" 
    for _, row in summary_df.iterrows():
        cards_html += f"""
        <div class='company-card'>
            <h4>{row['Company']}</h4>
            <p>Close: {row['Close']:.2f}</p>
            <p>RSI: {row['RSI_10']:.2f}</p>
            <p>MA: {row['MA_10']:.2f}</p>
        </div>
        """
    cards_html += "</div>"
    return cards_html

def launch_ui():
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo"), title="📈 Sneha's Stock Dashboard") as demo:

        gr.HTML("""
        <style>
        .company-card {
          background: linear-gradient(90deg, #FFD700, #4f46e5, #9333ea);
          color: #f9fafb;
          padding: 12px;
          border-radius: 10px;
          width: 180px;
          transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .company-card h4 {
          margin: 0;
          color: #fbbf24;
        }
        .company-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        }
        .cards-container {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
        } 
        .marquee-container {
          overflow: hidden;
          white-space: nowrap;
          box-sizing: border-box;
        }
    .marquee-text {
  display: inline-block;
  padding-left: 100%;
  animation: marquee 12s linear infinite, gradientFlow 6s ease infinite;
  font-size: 22px;
  font-weight: bold;
  background: linear-gradient(90deg, #FFD700, #4f46e5, #9333ea);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

@keyframes marquee {
  0%   { transform: translate(0, 0); }
  100% { transform: translate(-100%, 0); }
}

@keyframes gradientFlow {
  0% { background-position: 0% center; }
  50% { background-position: 100% center; }
  100% { background-position: 0% center; }
}

        </style>
        """)

        gr.HTML("""
        <div class="marquee-container">
            <div class="marquee-text">
                📊 SNEHA: SMART STOCK PORTFOLIO DASHBOARD | SINGLE + MULTI COMPANY ANALYSIS | RSI + MA 📈
            </div>
        </div>
        """)

        with gr.Tabs():
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

            with gr.TabItem("ℹ️ About"):
                gr.HTML("""
                <div style="padding:20px; color:#f1f5f9;">
                    <h3 style="color:#fbbf24;">Welcome to Sneha's Financial Intelligence Hub ✨</h3>
                    <p>This dashboard supports both single stock and multi-company portfolio analysis with RSI + Moving Averages.</p>
                </div>
                """)

        def toggle(mode):
            return gr.update(visible=(mode == "Relative Period")), gr.update(visible=(mode == "Custom Date Range"))
        date_mode.change(toggle, inputs=[date_mode], outputs=[period_group, date_group])

        def toggle_multi(mode):
            return gr.update(visible=(mode == "Relative Period")), gr.update(visible=(mode == "Custom Date Range"))
        date_mode_multi.change(toggle_multi, inputs=[date_mode_multi], outputs=[period_group_multi, date_group_multi])

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
