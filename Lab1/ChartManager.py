import matplotlib.pyplot as plt

def show_chart_window():
    plt.show()

def draw_chart(title, x_arr, y_arr, color='red', alpha=1, legend="Параметр1",
               xlabel="Переменная X", ylabel="Переменная Y", x_rot = 0, xlabel_fontsize = 12):
    plt.figure(title +"("+ xlabel+")")
    plt.scatter(x_arr, y_arr, color=color, alpha=alpha)

    plt.legend(legend)
    plt.xlabel(xlabel)
    plt.xticks(fontsize=xlabel_fontsize)
    plt.gca().tick_params(axis="x", labelrotation=x_rot)

    plt.ylabel(ylabel)
    plt.title(title)

def draw_several_charts(title, x_arr, y_dict, colors, legend, alpha=1,
                        xlabel="Переменная X", ylabel="Переменная Y", x_rot = 0, xlabel_fontsize = 12):
    plt.figure(title +"("+ xlabel+")")
    leg_labels = []
    for k, v in legend.items():
        leg_labels.append(v)
        plt.scatter(x_arr, y_dict[k], color=colors[k], alpha=alpha)

    plt.legend(leg_labels)
    plt.xlabel(xlabel)
    plt.xticks(fontsize=xlabel_fontsize)
    plt.gca().tick_params(axis="x", labelrotation=x_rot)

    plt.ylabel(ylabel)
    plt.title(title)