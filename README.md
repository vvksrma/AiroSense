# 🌏 AiroSense

**AiroSense** is a real-time air quality monitoring and forecasting platform that combines satellite observations, ground-based measurements, and AI/ML models to track pollution levels across Indian cities. The project aims to educate, visualize, and predict air pollution data with transparency and interactivity.

---

## 🚀 Features

- ✅ Real-time NO₂, PM2.5, PM10, SO₂, and O₃ pollutant tracking  
- 🛰️ Data sourced from Google Earth Engine & OpenAQ  
- 📊 Interactive heatmaps and graphs for Indian cities  
- 📅 Forecasting using AI/ML (upcoming)  
- 📚 Educational hub for pollution awareness (upcoming)

---

## 🗂️ Project Structure

```
airosense/
├── app/
│   └── routes.py
├── templates/
│   └── index.html
├── static/
│   └── css/style.css
├── data/
│   ├── raw/
│   └── processed/
├── utils/
│   ├── fetch_no2.py
│   ├── fetch_pm25.py
│   └── data_handler.py
├── run.py
└── README.md
```

---

## 📦 Requirements

Install required packages:

```bash
pip install -r requirements.txt
```

If you're using Google Earth Engine:

```bash
earthengine authenticate
```

---

## ⚙️ How to Run

```bash
git clone https://github.com/yourusername/airosense.git
cd airosense
python run.py
```

Open in browser:  
`http://127.0.0.1:5000/`

---

## 📥 Data Sources

| Pollutant | Source             | Script           | Format |
|-----------|--------------------|------------------|--------|
| NO₂       | Google Earth Engine| fetch_no2.py     | CSV    |
| PM2.5     | OpenAQ API         | fetch_pm25.py    | CSV    |
| PM10      | OpenAQ API         | fetch_pm10.py    | CSV    |
| SO₂       | OpenAQ API         | fetch_so2.py     | CSV    |
| O₃        | OpenAQ API         | fetch_o3.py      | CSV    |

Run `data_handler.py` to combine all into:  
📁 `data/processed/combined_pollution_data.csv`

---

## 🗺️ Dashboard

- 🗺️ Map shows pollution as color-coded heatmap  
- ✅ Filters by pollutant  
- 📍 Hover for city-wise data  
- 🔁 Updated manually or via cron

---

## 📚 Learning Resources

- [Google Earth Engine Docs](https://developers.google.com/earth-engine)
- [OpenAQ API v3 Docs](https://docs.openaq.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Leaflet.js for Maps](https://leafletjs.com/)

---

## 🛠️ Future Plans

- [ ] AI/ML Forecasting  
- [ ] Education hub for pollution  
- [ ] User alerts system  
- [ ] Mobile app integration

---

## 🙋 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
