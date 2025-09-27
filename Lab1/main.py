from Lab1.ChartManager import draw_chart, draw_several_charts, show_chart_window
from Lab1.DataManager import load_data_from_json, group_data_by, collect_grouped_data_to_list

if __name__ == "__main__":

    data = load_data_from_json("res/data.json")
    grouped_by_year = group_data_by(data, "year", "price")
    grouped_by_ticker = group_data_by(data, "ticker", "price")

    collected_by_year = collect_grouped_data_to_list(grouped_by_year)
    collected_by_ticker = collect_grouped_data_to_list(grouped_by_ticker)

    colors = {
        "max": "red",
        "avg": "blue",
        "min": "green"
    }

    legend = {
        "max": "Максимальное",
        "avg": "Среднее",
        "min": "Минимальное"
    }

    draw_several_charts("Статистика цен криптовалют", collected_by_year["x"], collected_by_year["y"], colors, legend, xlabel="Год", ylabel="Цена")
    draw_chart("Статистика цен криптовалют", collected_by_ticker["x"], collected_by_ticker["y"]["avg"], "green", legend=["Цена"], xlabel="Тикер", ylabel="Цена", x_rot=45, xlabel_fontsize=8)

    #draw_chart("График", collected["x"], collected["y"]["min"], "black", 1.0)

    show_chart_window()