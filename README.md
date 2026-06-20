# 📈 Smart Stock Market Dashboard v0.1.0

**SNEHA Dashboard** is an interactive and lightweight stock market dashboard that enables users to visualize stock price movements, explore trends, and filter historical stock data for any publicly traded company. Built using Python's data stack and deployed on Hugging Face Spaces, it delivers a simple, fast, and intuitive interface for both technical and non-technical users.


---
 
## 🚀 Features

- 🔍 **Search Any Stock**: Enter any publicly listed company name or ticker symbol.
- 📅 **Date Filtering**: Filter stock data by month range or custom date intervals.
- 📊 **Dynamic Visualizations**: Line charts and trend plots powered by Matplotlib.
- 💡 **Real-Time Data**: Automatically fetches latest data using `yfinance`.
- 🖥️ **Deployed on HF Spaces**: Seamless and free deployment on Hugging Face.

---

## 🛠️ Tech Stack

| Component         | Library         | Purpose                                |
|------------------|------------------|----------------------------------------|
| Data Fetching     | [`yfinance`](https://pypi.org/project/yfinance/)  | Retrieve historical market data         |
| Data Processing   | [`pandas`](https://pandas.pydata.org/)           | Time series manipulation and analysis   |
| Visualization     | [`matplotlib`](https://matplotlib.org/)          | Plotting and charting                   |
| Frontend Interface| [`gradio`](https://www.gradio.app/)              | Interactive user interface              |
| Deployment        | [Hugging Face Spaces](https://huggingface.co/spaces) | Web hosting for ML apps             |

---

## 📦 Installation

To run SMART STOCK MARKET Dashboard locally:

```bash
git https://github.com/snehabhusari/Smart-Stock-Market-Dashboard
cd Stock-Market-Dashboard
pip install -r requirements.txt
python app.py
```

💻 Usage
- Run the app locally with python app.py or open the HF Spaces App.

- Enter a company name or ticker symbol (e.g., AAPL, TSLA, GOOGL).

- Select a date range or number of months.

- View the generated line charts and stock trends.

🌐 Demo

You can try out the live version hosted on Hugging Face:


```bash
cd Smart-Stock-Market-Dashboard
├── app.py                  # Main Gradio app
├── helper_funcs.py         # Helper functions for fetching and cleaning data
├── viz.py                  # Matplotlib charting functions
├── data_preprocess.py      # Data preprocessing functions
├── ticker.py               # To fetch the ticker symbol
├── generate_analysis.py    # Generates the final output
├── main.py                 # Interface logic
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to suggest improvements or bug fixes.

🧠 Author

Sneha Bhusari

- [LinkedIn]https://www.linkedin.com/in/sneha-bhusari-9aa3412b5/
- [Github]https://github.com/snehabhusari


🌟 Show Your Support

If you like this project, don’t forget to ⭐ the repo and share it with others!
