from alive_progress import alive_it
import secrets
from pyfiglet import Figlet
import os
import multiprocessing
import random


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


if __name__ == "__main__":
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

    combinedStdReslults = []
    for each in alive_it(stdResults):
        for items in each:
            combinedStdReslults.append(items)

    combinedSecretResults = []
    for each in alive_it(secretResults):
        for items in each:
            combinedSecretResults.append(items)

    print(combinedStdReslults)
    print()
    print(combinedSecretResults)
