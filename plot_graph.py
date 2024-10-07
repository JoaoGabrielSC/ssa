import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np


def plot_index_with_logarithmic_regression(log_filepath):
    times = []
    indices = []

    # Lendo o arquivo de log CSV
    with open(log_filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            times.append(float(row['Time(s)']))
            indices.append(float(row['Index']))

    # Garantir que todos os valores de tempo são positivos para aplicar log
    times = np.array(times)
    indices = np.array(indices)

    # Realizando a regressão logarítmica
    log_times = np.log(times)
    coeffs = np.polyfit(log_times, indices, 1)

    # Gerar a linha de regressão logarítmica
    regression_line = coeffs[0] * log_times + coeffs[1]

    # Plotando os dados e a regressão logarítmica
    plt.figure(figsize=(10, 6))
    plt.plot(times, indices, linestyle='-', color='b', label='Dados')
    plt.plot(times, regression_line, color='r', label=f'Regressão Logarítmica: y = {coeffs[0]:.2f}log(x) + {coeffs[1]:.2f}')
    plt.title('Index em Função do Tempo com Regressão Logarítmica')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-log', type=str, required=True, help="caminho para o log")
    args = parser.parse_args()
    log_filepath = args.log
    plot_index_with_logarithmic_regression(log_filepath)

