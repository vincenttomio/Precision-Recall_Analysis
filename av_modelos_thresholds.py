import sys

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
    
    total_precision = 0
    total_recall = 0
    total_f1_score = 0

    # Calculando métricas para cada conjunto de valores e exibindo
    for threshold, TP, FP, FN in zip(thresholds, TP_values, FP_values, FN_values):
        precision, recall, f1_score = calculate_metrics(TP, FP, FN)
        total_precision += precision
        total_recall += recall
        total_f1_score += f1_score
        print(f"Threshold: {threshold:.2f} | Precision: {precision:.2f} | Recall: {recall:.2f} | F1-Score: {f1_score:.2f}")

    num_thresholds = len(thresholds)
    avg_precision = total_precision / num_thresholds
    avg_recall = total_recall / num_thresholds
    avg_f1_score = total_f1_score / num_thresholds

    # Exibindo métricas médias
    print("\nAverage Metrics:")
    print(f"Avg Precision: {avg_precision:.2f} | Avg Recall: {avg_recall:.2f} | Avg F1-Score: {avg_f1_score:.2f}\n\n\n\n")

if __name__ == "__main__":
    # Lendo os nomes de arquivo da linha de comando
    entry = sys.argv
    for file in entry[1:]:
        print(file)
        process_file(file)
