import sys
import matplotlib.pyplot as plt

# Função para calcular métricas a partir dos valores de True Positives (TP), False Positives (FP) e False Negatives (FN).
def calculate_metrics(TP, FP, FN):
    precision = TP / (TP + FP)  # Cálculo da precisão
    recall = TP / (TP + FN)     # Cálculo da taxa de recall
    f1_score = 2 * (precision * recall) / (precision + recall)  # Cálculo do F1-Score
    return precision, recall, f1_score

# Função para processar um arquivo com resultados.
def process_file(file_path):
    thresholds = []
    TP_values = []
    FP_values = []
    FN_values = []

    # Lendo o arquivo de resultados
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if "for conf_thresh =" in line and "average IoU" in line:
                parts = line.split(',')
                for part in parts:
                    if "for conf_thresh =" in part:
                        threshold = float(part.split('=')[1].strip())
                        thresholds.append(threshold)
                    elif "TP =" in part:
                        TP = int(part.split('=')[1].strip())
                        TP_values.append(TP)
                    elif "FP =" in part:
                        FP = int(part.split('=')[1].strip())
                        FP_values.append(FP)
                    elif "FN =" in part:
                        FN = int(part.split('=')[1].strip())
                        FN_values.append(FN)
    
    precision_values = []
    recall_values = []

    # Calculando as métricas para cada conjunto de valores
    for threshold, TP, FP, FN in zip(thresholds, TP_values, FP_values, FN_values):
        precision, recall, _ = calculate_metrics(TP, FP, FN)
        precision_values.append(precision)
        recall_values.append(recall)
    
    f1_scores = []

    # Calculando os F1-Scores para cada conjunto de valores
    for TP, FP, FN in zip(TP_values, FP_values, FN_values):
        _, _, f1_score = calculate_metrics(TP, FP, FN)
        f1_scores.append(f1_score)
    
    best_threshold_index = f1_scores.index(max(f1_scores))
    best_threshold = thresholds[best_threshold_index]
    best_f1_score = max(f1_scores)
    
    return best_threshold, best_f1_score, recall_values, precision_values

if __name__ == "__main__":
    entry = sys.argv
    files = entry[1:]
    
    best_file = None
    best_f1_score = 0
    best_recall = []
    best_precision = []
    
    plt.figure(figsize=(10, 6))
    
    print()
    for file in files:
        best_threshold, f1_score, recall_values, precision_values = process_file(file)
        if f1_score > best_f1_score:
            best_f1_score = f1_score
            best_file = file
            best_recall = recall_values
            best_precision = precision_values
        
        plt.plot(recall_values, precision_values, label=file)
        
        print(f"Arquivo: {file}")
        print(f"Melhor Threshold: {best_threshold:.2f}")
        print(f"Precision: {best_precision[-1]:.2f}")
        print(f"Recall: {best_recall[-1]:.2f}")
        print(f"F1-Score: {f1_score:.2f}")
        print()
    
    # Criando e mostrando o gráfico da curva Precision-Recall
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Melhor arquivo: {best_file}")
    print(f"Melhor F1-Score: {best_f1_score:.2f}")
    
    # Criando e mostrando o gráfico da melhor curva Precision-Recall
    plt.figure(figsize=(10, 6))
    plt.plot(best_recall, best_precision, label=best_file)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Best Precision-Recall Curve')
    plt.legend()
    plt.grid(True)
    plt.show()
