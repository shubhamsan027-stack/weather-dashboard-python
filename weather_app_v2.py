import sys
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QMessageBox
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


# ============================================================
# WEATHER API SETTINGS
# ============================================================

API_KEY = "94074ee65fe84b4bbe351427262809"

BASE_URL = "https://api.weatherapi.com/v1/forecast.json"


# ============================================================
# MAIN WEATHER APPLICATION
# ============================================================

class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()

        self.current_weather = None
        self.forecast_data = None
        self.is_celsius = True

        self.setup_ui()


    # ========================================================
    # USER INTERFACE
    # ========================================================

    def setup_ui(self):

        self.setWindowTitle("Weather Dashboard")
        self.setGeometry(300, 100, 950, 850)

        self.setMinimumSize(850, 750)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b1117;
                color: white;
                font-family: Arial;
            }

            QLineEdit {
                background-color: #18232d;
                border: 2px solid #00aaff;
                border-radius: 12px;
                padding: 12px;
                color: white;
                font-size: 17px;
            }

            QPushButton {
                background-color: #00aaff;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 22px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #0088cc;
            }

            QPushButton:pressed {
                background-color: #006699;
            }

            QFrame {
                background-color: #18232d;
                border-radius: 15px;
            }
        """)


        # ====================================================
        # MAIN LAYOUT
        # ====================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(15)


        # ====================================================
        # TITLE
        # ====================================================

        title = QLabel("WEATHER DASHBOARD")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            QLabel {
                background-color: #18232d;
                color: #00aaff;
                border-radius: 15px;
                padding: 12px;
                font-size: 30px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(title)


        # ====================================================
        # SUBTITLE
        # ====================================================

        subtitle = QLabel("Real-time weather information")

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""
            QLabel {
                color: #9aa7b2;
                font-size: 16px;
                padding: 5px;
            }
        """)

        main_layout.addWidget(subtitle)


        # ====================================================
        # SEARCH AREA
        # ====================================================

        search_layout = QHBoxLayout()

        self.city_input = QLineEdit()

        self.city_input.setPlaceholderText("Enter city name...")

        self.city_input.setText("Silchar")

        search_layout.addWidget(self.city_input)


        self.search_button = QPushButton("Search")

        self.search_button.clicked.connect(self.get_weather)

        search_layout.addWidget(self.search_button)


        self.unit_button = QPushButton("°C / °F")

        self.unit_button.clicked.connect(self.toggle_temperature)

        search_layout.addWidget(self.unit_button)


        main_layout.addLayout(search_layout)


        # ====================================================
        # CURRENT WEATHER CARD
        # ====================================================

        self.weather_card = QFrame()

        self.weather_card.setMinimumHeight(190)

        weather_layout = QVBoxLayout()

        weather_layout.setContentsMargins(20, 15, 20, 15)

        weather_layout.setSpacing(3)


        # CITY

        self.city_label = QLabel("Weather Information")

        self.city_label.setAlignment(Qt.AlignCenter)

        self.city_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 26px;
                font-weight: bold;
            }
        """)

        weather_layout.addWidget(self.city_label)


        # TEMPERATURE

        self.temperature_label = QLabel("-- °C")

        self.temperature_label.setAlignment(Qt.AlignCenter)

        self.temperature_label.setMinimumHeight(70)

        self.temperature_label.setStyleSheet("""
            QLabel {
                color: #00ff66;
                font-size: 48px;
                font-weight: bold;
                padding: 2px;
                margin: 0px;
            }
        """)

        weather_layout.addWidget(self.temperature_label)


        # WEATHER EMOJI

        self.condition_icon = QLabel("☀️")

        self.condition_icon.setAlignment(Qt.AlignCenter)

        self.condition_icon.setStyleSheet("""
            QLabel {
                font-size: 38px;
                padding: 0px;
            }
        """)

        weather_layout.addWidget(self.condition_icon)


        # CONDITION

        self.condition_label = QLabel("Search for a city")

        self.condition_label.setAlignment(Qt.AlignCenter)

        self.condition_label.setStyleSheet("""
            QLabel {
                color: #dddddd;
                font-size: 19px;
                padding: 2px;
            }
        """)

        weather_layout.addWidget(self.condition_label)


        self.weather_card.setLayout(weather_layout)

        main_layout.addWidget(self.weather_card)


        # ====================================================
        # DETAILS GRID
        # ====================================================

        details_layout = QGridLayout()

        details_layout.setSpacing(12)


        self.feels_label = self.create_info_card(
            "Feels Like",
            "--"
        )

        self.humidity_label = self.create_info_card(
            "Humidity",
            "--"
        )

        self.wind_label = self.create_info_card(
            "Wind",
            "--"
        )

        self.pressure_label = self.create_info_card(
            "Pressure",
            "--"
        )

        self.visibility_label = self.create_info_card(
            "Visibility",
            "--"
        )

        self.cloud_label = self.create_info_card(
            "Cloud Cover",
            "--"
        )


        details_layout.addWidget(self.feels_label, 0, 0)

        details_layout.addWidget(self.humidity_label, 0, 1)

        details_layout.addWidget(self.wind_label, 0, 2)

        details_layout.addWidget(self.pressure_label, 1, 0)

        details_layout.addWidget(self.visibility_label, 1, 1)

        details_layout.addWidget(self.cloud_label, 1, 2)


        main_layout.addLayout(details_layout)


        # ====================================================
        # FORECAST TITLE
        # ====================================================

        forecast_title = QLabel("5-DAY FORECAST")

        forecast_title.setAlignment(Qt.AlignCenter)

        forecast_title.setStyleSheet("""
            QLabel {
                color: #00aaff;
                background-color: #18232d;
                font-size: 21px;
                font-weight: bold;
                padding: 8px;
                border-radius: 8px;
            }
        """)

        main_layout.addWidget(forecast_title)


        # ====================================================
        # FORECAST AREA
        # ====================================================

        self.forecast_layout = QHBoxLayout()

        self.forecast_layout.setSpacing(10)

        main_layout.addLayout(self.forecast_layout)


        # ====================================================
        # STATUS
        # ====================================================

        self.status_label = QLabel(
            "Enter a city and click Search"
        )

        self.status_label.setAlignment(Qt.AlignCenter)

        self.status_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 13px;
                padding: 5px;
            }
        """)

        main_layout.addWidget(self.status_label)


        self.setLayout(main_layout)


    # ========================================================
    # INFORMATION CARD
    # ========================================================

    def create_info_card(self, title, value):

        card = QFrame()

        card.setMinimumHeight(75)

        layout = QVBoxLayout()

        layout.setContentsMargins(10, 8, 10, 8)

        title_label = QLabel(title)

        title_label.setAlignment(Qt.AlignCenter)

        title_label.setStyleSheet("""
            QLabel {
                color: #8d9aa5;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        value_label = QLabel(value)

        value_label.setAlignment(Qt.AlignCenter)

        value_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
        """)

        layout.addWidget(title_label)

        layout.addWidget(value_label)

        card.setLayout(layout)

        return card


    # ========================================================
    # GET WEATHER
    # ========================================================

    def get_weather(self):

        city = self.city_input.text().strip()


        if not city:

            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter a city name."
            )

            return


        if API_KEY == "YOUR_API_KEY_HERE":

            QMessageBox.warning(
                self,
                "API Key Missing",
                "Please add your WeatherAPI API key in the code."
            )

            return


        self.status_label.setText(
            f"Getting weather information for {city}..."
        )


        try:

            params = {
                "key": API_KEY,
                "q": city,
                "days": 5,
                "aqi": "no",
                "alerts": "no"
            }


            response = requests.get(
                BASE_URL,
                params=params,
                timeout=10
            )


            if response.status_code != 200:

                try:

                    error_message = response.json()["error"]["message"]

                except Exception:

                    error_message = "Unable to get weather data."


                QMessageBox.warning(
                    self,
                    "Weather Error",
                    error_message
                )

                self.status_label.setText(
                    "Could not retrieve weather data."
                )

                return


            data = response.json()


            self.current_weather = data["current"]

            self.forecast_data = data["forecast"]["forecastday"]


            self.update_current_weather(data)

            self.update_forecast()


            self.status_label.setText(
                f"Weather updated successfully for {city}"
            )


        except requests.exceptions.Timeout:

            QMessageBox.warning(
                self,
                "Connection Error",
                "The weather server took too long to respond."
            )


        except requests.exceptions.ConnectionError:

            QMessageBox.warning(
                self,
                "Internet Error",
                "Please check your internet connection."
            )


        except Exception as error:

            QMessageBox.warning(
                self,
                "Error",
                f"Something went wrong:\n{error}"
            )


    # ========================================================
    # UPDATE CURRENT WEATHER
    # ========================================================

    def update_current_weather(self, data):

        location = data["location"]

        current = data["current"]


        city = location["name"]

        region = location["region"]

        country = location["country"]


        self.city_label.setText(
            f"{city}, {region}"
            if region
            else f"{city}, {country}"
        )


        condition = current["condition"]["text"]


        self.condition_label.setText(condition)


        # Temperature

        self.update_temperature_display()


        # Weather icon

        self.condition_icon.setText(
            self.get_weather_emoji(condition)
        )


        # Feels like

        self.update_info_card(
            self.feels_label,
            "Feels Like",
            self.get_temperature(
                current["feelslike_c"],
                current["feelslike_f"]
            )
        )


        # Humidity

        self.update_info_card(
            self.humidity_label,
            "Humidity",
            f"{current['humidity']} %"
        )


        # Wind

        if self.is_celsius:

            wind_text = f"{current['wind_kph']} km/h"

        else:

            wind_text = f"{current['wind_mph']} mph"


        self.update_info_card(
            self.wind_label,
            "Wind",
            wind_text
        )


        # Pressure

        self.update_info_card(
            self.pressure_label,
            "Pressure",
            f"{current['pressure_mb']} hPa"
        )


        # Visibility

        if self.is_celsius:

            visibility_text = (
                f"{current['vis_km']} km"
            )

        else:

            visibility_text = (
                f"{current['vis_miles']} miles"
            )


        self.update_info_card(
            self.visibility_label,
            "Visibility",
            visibility_text
        )


        # Cloud cover

        self.update_info_card(
            self.cloud_label,
            "Cloud Cover",
            f"{current['cloud']} %"
        )


    # ========================================================
    # UPDATE TEMPERATURE
    # ========================================================

    def update_temperature_display(self):

        if not self.current_weather:

            return


        temp_c = self.current_weather["temp_c"]

        temp_f = self.current_weather["temp_f"]


        if self.is_celsius:

            temperature = f"{temp_c:.1f} °C"

        else:

            temperature = f"{temp_f:.1f} °F"


        self.temperature_label.setText(
            temperature
        )


    # ========================================================
    # TEMPERATURE UNIT
    # ========================================================

    def toggle_temperature(self):

        self.is_celsius = not self.is_celsius


        if self.current_weather:

            self.update_temperature_display()

            current = self.current_weather


            self.update_info_card(
                self.feels_label,
                "Feels Like",
                self.get_temperature(
                    current["feelslike_c"],
                    current["feelslike_f"]
                )
            )


            if self.is_celsius:

                wind_text = (
                    f"{current['wind_kph']} km/h"
                )

                visibility_text = (
                    f"{current['vis_km']} km"
                )

            else:

                wind_text = (
                    f"{current['wind_mph']} mph"
                )

                visibility_text = (
                    f"{current['vis_miles']} miles"
                )


            self.update_info_card(
                self.wind_label,
                "Wind",
                wind_text
            )


            self.update_info_card(
                self.visibility_label,
                "Visibility",
                visibility_text
            )


        self.update_forecast()


    # ========================================================
    # GET TEMPERATURE
    # ========================================================

    def get_temperature(self, celsius, fahrenheit):

        if self.is_celsius:

            return f"{celsius:.1f} °C"

        return f"{fahrenheit:.1f} °F"


    # ========================================================
    # UPDATE INFO CARD
    # ========================================================

    def update_info_card(self, card, title, value):

        layout = card.layout()

        if layout is None:

            return


        title_label = layout.itemAt(0).widget()

        value_label = layout.itemAt(1).widget()


        title_label.setText(title)

        value_label.setText(value)


    # ========================================================
    # UPDATE 5-DAY FORECAST
    # ========================================================

    def update_forecast(self):

        # Remove old forecast cards

        while self.forecast_layout.count():

            item = self.forecast_layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()


        if not self.forecast_data:

            return


        for day in self.forecast_data:

            card = self.create_forecast_card(day)

            self.forecast_layout.addWidget(card)


    # ========================================================
    # CREATE FORECAST CARD
    # ========================================================

    def create_forecast_card(self, day):

        card = QFrame()

        card.setMinimumHeight(140)

        card.setStyleSheet("""
            QFrame {
                background-color: #18232d;
                border-radius: 14px;
            }
        """)


        layout = QVBoxLayout()

        layout.setContentsMargins(8, 8, 8, 8)

        layout.setSpacing(4)


        # Date

        date = day["date"]

        date_text = date[5:]

        date_label = QLabel(date_text)

        date_label.setAlignment(Qt.AlignCenter)

        date_label.setStyleSheet("""
            QLabel {
                color: #00aaff;
                font-size: 15px;
                font-weight: bold;
            }
        """)

        layout.addWidget(date_label)


        # Emoji

        condition = day["day"]["condition"]["text"]

        emoji_label = QLabel(
            self.get_weather_emoji(condition)
        )

        emoji_label.setAlignment(Qt.AlignCenter)

        emoji_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
            }
        """)

        layout.addWidget(emoji_label)


        # Temperature

        max_c = day["day"]["maxtemp_c"]

        min_c = day["day"]["mintemp_c"]

        max_f = day["day"]["maxtemp_f"]

        min_f = day["day"]["mintemp_f"]


        if self.is_celsius:

            temp_text = (
                f"{max_c:.1f}° / {min_c:.1f}°"
            )

        else:

            temp_text = (
                f"{max_f:.1f}° / {min_f:.1f}°"
            )


        temp_label = QLabel(temp_text)

        temp_label.setAlignment(Qt.AlignCenter)

        temp_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        layout.addWidget(temp_label)


        # Condition

        condition_label = QLabel(condition)

        condition_label.setAlignment(Qt.AlignCenter)

        condition_label.setWordWrap(True)

        condition_label.setStyleSheet("""
            QLabel {
                color: #b8c3cc;
                font-size: 12px;
            }
        """)

        layout.addWidget(condition_label)


        card.setLayout(layout)

        return card


    # ========================================================
    # WEATHER EMOJI
    # ========================================================

    def get_weather_emoji(self, condition):

        condition = condition.lower()


        if "thunder" in condition:

            return "⛈️"


        if "rain" in condition:

            return "🌧️"


        if "drizzle" in condition:

            return "🌦️"


        if "snow" in condition:

            return "❄️"


        if "mist" in condition:

            return "🌫️"


        if "fog" in condition:

            return "🌫️"


        if "cloud" in condition:

            if "partly" in condition:

                return "⛅"

            return "☁️"


        if "overcast" in condition:

            return "☁️"


        if "sunny" in condition:

            return "☀️"


        if "clear" in condition:

            return "🌙"


        return "🌤️"


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = WeatherApp()

    window.show()

    sys.exit(app.exec_())