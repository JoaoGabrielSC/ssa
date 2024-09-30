import matplotlib.pyplot as plt
import csv
import argparse

def plot_index_from_log(log_filepath):
    times = []
    indices = []

    # Lendo o arquivo de log CSV
    with open(log_filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            times.append(float(row['Time(s)']))
            indices.append(float(row['Index']))

    # Plotando o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(times, indices, marker='o', linestyle='-', color='b')
    plt.title('Index em Função do Tempo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-log', type=str, required=True, help="caminho para o log")
    args = parser.parse_args()
    log_filepath = args.log
    plot_index_from_log(log_filepath)
