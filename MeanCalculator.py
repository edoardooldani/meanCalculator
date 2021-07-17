import os
import re
import PySimpleGUI as sg


examsList = os.listdir(".")
pattern = re.compile(r"\((\d+)\)")

def meanCalculate(examsList, ignoredExam = ""):

  credictSum = 0
  examsDict= {}

  if len(examsList) == 0:
    return 0

  for exam in examsList:
    examSplit = exam.split(" ")

    if len(examSplit) < 3:
      continue

    if ignoredExam != "":
      if exam == ignoredExam:
        continue

    credictSum += int(pattern.findall(examSplit[2])[0])

    examsDict[examSplit[0]] = int(pattern.findall(examSplit[1])[0]) * int(pattern.findall(examSplit[2])[0])

  
  return sum(examsDict.values()) / credictSum


totalMean = meanCalculate(examsList)


def meanClearer(examsList):

  filteredList = []
  for exam in examsList:
    examSplit = exam.split(" ")

    if len(examSplit) < 3:
      continue

    if int(pattern.findall(examSplit[1])[0]) < totalMean:
      filteredList.append(exam)


  higherMean = totalMean
  examToCut = ""

  for item in filteredList:

    meanCleared = meanCalculate(examsList, item)

    if meanCleared > higherMean:
      examToCut = item
      higherMean = meanCleared


  print("The most penalizing exam is", examToCut, "with a mean without it:", round(higherMean,3))

  return examToCut, higherMean


print("Mean: ", round(totalMean,3))

examToCut, higherMean = meanClearer(examsList)

meanString = "Mean: " + str(round(totalMean, 3))
meanCutString = "The most penalizing exam is " + examToCut + " with a mean without it: " + str(round(higherMean,3))

layout = [[sg.Text(meanString)],
          [sg.Text(meanCutString)]]

# Create the window
window = sg.Window("Mean calculator", layout).read()
