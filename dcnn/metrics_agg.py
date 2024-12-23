import os

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix


def create_bar_with_baseline(baseline, fusions, col, path="metrics",
               dcnn_color="#eba834", fusion_color="#55d3fa"):
    cat = []
    val = []
    c = []
    for model, metrics in baseline.items():
        m = metrics[col]
        cat.append(model)
        val.append(m)
        c.append(dcnn_color)
    n_baseline = len(val)
    max_val = max(val)
    avg_val = sum(val) / n_baseline
    c.append(dcnn_color)
    cat.append(" ")
    val.append(0)

    for model, metrics in fusions.items():
        m = metrics[col]
        cat.append(model)
        val.append(m)
        c.append(fusion_color)
    plt.bar(cat, val, color=c)
    plt.axhline(y=max_val, xmin=(n_baseline + .5) / len(val),
                 color="b", linestyle="--", label=f"dcnn maximum {col}: {max_val:.2f}")

    plt.axhline(y=avg_val, xmin=(n_baseline + .5) / len(val),
                 color="r", linestyle="--", label=f"dcnn average {col}: {avg_val:.2f}")
    plt.legend(loc=3)

    plt.axvline(x=n_baseline, color="k")
    plt.xticks(rotation=23)
    plt.xlabel('Models')
    plt.ylabel(f"{col}")
    plt.title(f"{col} Bar graph")
    plt.savefig(f"{path}/{col}_bar_graph")
    plt.clf()


def save_conf_mat(y_true, y_pred, name):
    cm = confusion_matrix(y_true, y_pred)

    # Create a heatmap using Seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix: {name}')
    plt.xlabel('Predicted')

    plt.ylabel('Actual')

    # Save the image
    plt.savefig(f'{name}_confusion_matrix.png')
    plt.clf()



def create_bar(metrics, col):
    cat = []
    val = []
    
    for model, metrics in metrics.items():
        m = metrics[col]
        cat.append(model.split("_")[0])
        val.append(m)
    plt.bar(cat, val,)

    plt.xticks(rotation=90, va="bottom")
    plt.xlabel('Models')
    plt.ylabel(f"{col}")
    plt.title(f"{col} Bar graph")
    plt.savefig(f"{path}/{col}_bar_graph")
    plt.clf()





def parse_metrics(path):

    files = os.listdir(path)
    metrics = {}


    for file_name in files:
        if not  file_name.endswith(".txt"):
            continue	


        with open(f"{path}/{file_name}", "r") as f:
            met = {"precision": 0,
                 "recall": 0,
                 "f1-score": 0,
                  "accuracy": 0}
            f.readline()
            f.readline()
            for _ in range(11):
                line = f.readline()
                m = line.split()[1:4]
                met["precision"]+= float(m[0])/11
                met["recall"]   += float(m[1])/11
                met["f1-score"] += float(m[2])/11
            f.readline()
            met["accuracy"] = float(f.readline().split()[1])
            metrics[file_name]= met
            print(file_name.split("_")[0], met)
    return metrics


if __name__=="__main__":
    path = "./metrics/CRE"

    models = parse_metrics(path)

    create_bar(models, "accuracy")
    create_bar(models, "f1-score")
    create_bar(models, "precision")
    create_bar(models, "recall")


    
