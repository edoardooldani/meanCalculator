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


def calculate(examsList, inputType):

  totalMean = round(meanCalculate(examsList),3)

  examToCut, higherMean = meanClearer(examsList, totalMean)

  meanString = "Mean: " + str(totalMean)
  meanCutString = "The most penalizing exam is " + examToCut + " with a mean without it: " + str(higherMean)

  sg.theme('DarkAmber')
  layout2 = [[sg.Text(meanString)],
             [sg.Text(meanCutString)],
             [sg.Button('Back')]]
                
  titleString = 'Mean calculator: ' +  inputType + ' input'
  windowResult = sg.Window(titleString, layout2)

  while True:
    event, values = windowResult.read()

    if event == sg.WIN_CLOSED or event == 'Back': # if user closes window or clicks exit
        break

  windowResult.close()


def meanCalculator():
  sg.theme('DarkAmber')
  layout = [[sg.Text('Which input type do you choose?')],
            [sg.Button('File'), sg.Button('Directory'), sg.Button('Back')] ]

  window = sg.Window("Mean calculator", layout, size=(400,300))

  while True:
      event, values = window.read()

      if event == sg.WIN_CLOSED or event == 'Back': # if user closes window or clicks exit
          break

      elif event == 'File':
        examsList = open("grades.txt", "r").read().split('\n')
        calculate(examsList, 'file')

      elif event == 'Directory':
        examsList = os.listdir(".") 
        calculate(examsList, 'directory')
        
  window.close()



# Main 
sg.theme('DarkAmber')
mainLayout = [[sg.Text('Mean Calculator', font=15, justification='center')],
              [sg.Text('Choose what u want to do')],
              [],
              [sg.Button('Mean calculate'), sg.Button('Rating to be taken'), sg.Button('Exit')]]

mainWindow = sg.Window("Mean Calculator", mainLayout, size=(400,300), grab_anywhere=True)

while True:
  event, values = mainWindow.read()

  if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
    break

  elif event == 'Mean calculate':
    meanCalculator()

  elif event == 'Rating to be taken':
    meanCalculator()

mainWindow.close()

