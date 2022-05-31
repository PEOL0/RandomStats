from ast import arg
from alive_progress import alive_it, alive_bar
import secrets
from matplotlib.pyplot import title
from pyfiglet import Figlet
import os
import multiprocessing
import random
import csv


def stdRand(size):
    result = []
    for each in range(size):
        result.append(random.randint(0, 100))
    return result


def secretRand(size):
    result = []
    for each in range(size):
        result.append(secrets.randbelow(100))
    return result


def exportStdRand(data):
    with open("StdRand.csv", "w") as csvfile:
        my_writer = csv.writer(csvfile, dialect="excel", delimiter="\n")
        my_writer.writerow(data)


def exportSecretRand(data):
    with open("SecretRand.csv", "w") as csvfile:
        my_writer = csv.writer(csvfile, dialect="excel", delimiter="\n")
        my_writer.writerow(data)


def main():
    terminal = os.get_terminal_size()
    welcome_fig = Figlet(
        font="kban", justify="left", width=getattr(terminal, "columns")
    )
    print()
    print(welcome_fig.renderText("RandStats"))
    print("By: PEOL0", end="\n\n")

    sampleSize = int(input("Sample size: "))
    processCount = os.cpu_count()

    processSize = []
    for each in alive_it(range(processCount)):
        if each < processCount - 1:
            processSize.append(int(sampleSize / processCount))
    if each == processCount - 1:
        processSize.append(int(sampleSize - sum(processSize)))


    pool = multiprocessing.Pool()
    stdResults = pool.map(stdRand, processSize)
    secretResults = pool.map(secretRand, processSize)
    pool.close()


    combinedStdResults = []
    for each in alive_it(stdResults):
        for items in each:
            combinedStdResults.append(items)

    combinedSecretResults = []
    for each in alive_it(secretResults):
        for items in each:
            combinedSecretResults.append(items)

    listCombinedStdResults = [combinedStdResults]
    listCombinedSecretResults = [combinedSecretResults]


    saveToFile = input("Save to file? (Y/n): ").casefold
    if (
        saveToFile == "".casefold
        or saveToFile == "Y".casefold
        or saveToFile == "Yes".casefold
    ):
        
        with alive_bar(2, title="Exporting to file") as bar:

            e1 = multiprocessing.Process(
                target=exportStdRand, args=(listCombinedStdResults)
            )
            e2 = multiprocessing.Process(
                target=exportSecretRand, args=(listCombinedSecretResults)
            )
            e1.start()
            print("E1 started")
            e2.start()
            print("E2 started")
            bar()
            e1.join()
            print("E1 finished")
            e2.join()
            print("E2 finished")
            bar()

    print("Script finished")


if __name__ == "__main__":
    main()
