import json

def load_data_from_json(path):
    with open(path, "r") as file:
        return json.load(file)

def collect_grouped_data_to_list(grouped):
    x_cords = list()
    y_cords = dict()

    for key, value in grouped.items():
        x_cords.append(key)
        for param, v in value.items():
            if y_cords.get(param) is not None:
                y_cords[param].append(v)
            else:
                y_cords[param] = [v]


    return {
        "x": x_cords,
        "y": y_cords
    }

def group_data_by(arr, field_key, field_val):
    statistic = dict()

    for item in arr:
        key = item[field_key]
        value = item[field_val]
        if statistic.get(key):
            statistic[key]["total"] += value
            statistic[key]["count"] += 1
            statistic[key]["max"] = max(statistic[key]["max"], value)
            statistic[key]["min"] = min(statistic[key]["min"], value)
        else:
            statistic[key] = dict()
            statistic[key]["total"] = value
            statistic[key]["count"] = 1
            statistic[key]["max"] = value
            statistic[key]["min"] = value

    for key, value in statistic.items():
        statistic[key]["avg"] = value["total"] / value["count"]
        statistic[key].pop("count")
        statistic[key].pop("total")

    return statistic