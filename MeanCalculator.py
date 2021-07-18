import os
import re
import PySimpleGUI as sg


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


def meanClearer(examsList, totalMean):

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


  #print("The most penalizing exam is", examToCut, "with a mean without it:", round(higherMean,3))

  return examToCut, round(higherMean,3)


def calculate(examsList, type):

  totalMean = round(meanCalculate(examsList),3)

  examToCut, higherMean = meanClearer(examsList, totalMean)

  meanString = "Mean: " + str(totalMean)
  meanCutString = "The most penalizing exam is " + examToCut + " with a mean without it: " + str(higherMean)

  layout2 = [[sg.Text(meanString)],
             [sg.Text(meanCutString)],
             [sg.Button('Exit')]]
                
  windowResult = sg.Window('Mean calculator: {type} input', layout2)

  while True:
    event, values = windowResult.read()

    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
        break

  windowResult.close()

# Main 

layout = [[sg.Text('Which input type do you choose?')],
          [sg.Button('File'), sg.Button('Directory'), sg.Button('Exit')] ]

window = sg.Window("Mean calculator", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
        break

    elif event == 'File':
      examsList = open("grades.txt", "r").read().split('\n')
      calculate(examsList, 'file')

    elif event == 'Directory':
      examsList = os.listdir(".") 
      calculate(examsList, 'directory')
      
window.close()

