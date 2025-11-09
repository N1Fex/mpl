import SheetsManager
from Lab1v2.ChartManager import draw_several_charts, show_chart_window, draw_chart
from Lab1v2.DataManager import filter_by_period, prepare_prices_data, prepare_avg_price_monthly, filter_by_year

spreadsheet_id = '1YZyYAMdcsVIuI-fkTxZjf8ohuDqp_PPy7XjtVW_-dxA'
range_name = 'История котировок!A2:F154002'

ticker = "MGNT"
date_from = '24.01.2025'
date_to = '20.02.2025'

def main():
    service = SheetsManager.build_service()

    data = SheetsManager.read_data(service, spreadsheet_id, range_name)
    filtered = filter_by_period(data, date_from, date_to, ticker)
    prepared = prepare_prices_data(filtered)

    colors = {
        "max": "red",
        "open": "blue",
        "close": "purple",
        "min": "green"
    }
    legend = {
        "max": "Максимальная цена",
        "open": "Цена открытия",
        "close": "Цена закрытия",
        "min": "Минимальная цена"
    }

    draw_several_charts("Динамика акции " + ticker, prepared["x"], prepared["y"],
                        colors, legend, xlabel="Даты", ylabel="Цена", x_rot=30)
    year:int = 2024
    monthly = prepare_avg_price_monthly(filter_by_year(data, 'MGNT', year))

    draw_chart(f"Средняя цена по месяцам акции {ticker} на {year}" , monthly["x"], monthly["y"],
               "green", legend=["Ср. Цена"], xlabel="Месяца", ylabel="Цена", x_rot=15, xlabel_fontsize=10)

    show_chart_window()


if __name__=="__main__":
    main()