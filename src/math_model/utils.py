def parse_pre_config(pre_config): 
    characteristics = []
    subcharacteristics = []
    measures = []
    metrics = []

    for characteristic in pre_config["data"]["characteristics"]: 
        characteristics.append({"key": characteristic["key"]})
        for subcharacteristic in characteristic["subcharacteristics"]: 
            subcharacteristics.append({"key": subcharacteristic["key"]})
            for measure in subcharacteristic["measures"]: 
                measures.append({"key": measure["key"]})
                metrics+=measure["metrics"]


    return characteristics, subcharacteristics, measures, metrics




