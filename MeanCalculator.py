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

    if examSplit[1] == "30L":
      examSplit[1] = "33"

    credictSum += int(pattern.findall(examSplit[2])[0])

    examsDict[examSplit[0]] = int(pattern.findall(examSplit[1])[0]) * int(pattern.findall(examSplit[2])[0])

  
  return sum(examsDict.values()) / credictSum, credictSum


# MEAN CLEAR

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

    meanCleared, totalCredits = meanCalculate(examsList, item)

    if meanCleared > higherMean:
      examToCut = item
      higherMean = meanCleared


  return examToCut, round(higherMean,3)


def calculateMean(examsList, inputType):

  totalMean, totalCredits = meanCalculate(examsList)

  totalMean = round(totalMean,3)

  examToCut, higherMean = meanClearer(examsList, totalMean)

  meanString = "Mean: " + str(totalMean) + " equivalent to " + str(round(totalMean*110/30,3)) + "/110"
  meanCutString = "The most penalizing exam is " + examToCut + " with a mean without it: " + str(higherMean)  + " equivalent to " + str(round(higherMean*110/30,3)) + "/110"

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

  return higherMean, totalCredits


def meanMenuInputType():
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
        totalMean, totalCredits = calculateMean(examsList, 'file')
        break

      elif event == 'Directory':
        examsList = os.listdir(".") 
        totalMean, totalCredits = calculateMean(examsList, 'directory')
        break
        
  window.close()
  return totalMean, totalCredits

# RATING TO TAKE

def ratingToTake(examsNumber, creditsNumber, finalMean, actualMean, totalCredits):
  meanXcredits = actualMean*totalCredits
  creditsSum = totalCredits + creditsNumber

  result = (((creditsSum) * finalMean) - (meanXcredits))


  resultOnCredits = round(result/creditsNumber,3)

  meanXcredits += result
  
  #if result < 33 and result > 18:
  meanString = "Grade to take: " + str(resultOnCredits) + " with a final mean of " + str(finalMean) + " equivalent to: " + str(round((meanXcredits/creditsSum)*110/30,3)) + "/110" 
  #else:
   # meanString = "You will never have a mean of" + str(finalMean) + ", I'm sorry bro"

  sg.theme('DarkAmber')
  layout = [[sg.Text(meanString)],
             [sg.Button('Back')]]
                
  titleString = 'Rating to be taken'
  windowResult = sg.Window(titleString, layout)

  while True:
    event, values = windowResult.read()

    if event == sg.WIN_CLOSED or event == 'Back':
        break

  windowResult.close()


def ratingToTakeCalculator():

  sg.theme('DarkAmber')
  layout = [[sg.Text('how many exams are you missing?\n (example: 3)')],
            [sg.InputText()],
            [sg.Text('How many credits these exams have?\n (n° total credits example: 30)')],
            [sg.InputText()],
            [sg.Text('Do you want to calculate your actual mean? \n (recommended choise if you don\'t know mean and credits)', key='-MEAN-')],
            [sg.Button('Calculate', key='-CALCULATE-'), sg.Button('Manual', key='-MANUAL-')],
            [sg.Text('what grades mean would you like to have?\n (final mean)')],
            [sg.InputText()],
            [sg.Button('Submit'), sg.Button('Back')] ]

  ratingWindow = sg.Window("Rating to take calculator", layout, size=(400,400))

  actualMean = 0
  totalCredits = 0
  while True:
      event, values = ratingWindow.read()     
      
      if event == sg.WIN_CLOSED or event == 'Back': # if user closes window or clicks exit
        break
      
      if event == '-CALCULATE-':
        actualMean, totalCredits = meanMenuInputType()

      if event == '-MANUAL-':
        eventPopUp, valuesPopUp = sg.Window('Manual choice', [[sg.Text('Your actual mean?\n (if you don\'t know check the other page)')],[sg.InputText()], [sg.Text('Your total credits?')],[sg.InputText()], [sg.OK()] ]).read(close=True)
        
        if valuesPopUp[0] == '' or valuesPopUp[1] == '':
          break
        
        actualMean = float(valuesPopUp[0])
        totalCredits = int(valuesPopUp[1])


      stringMean = "Mean: " + str(actualMean) +  " equivalent to " + str(round(actualMean*110/30,3)) + "/110" + " Credits: " + str(totalCredits)
      ratingWindow['-MEAN-'].update(stringMean)
      ratingWindow['-CALCULATE-'].update(visible=False)
      ratingWindow['-MANUAL-'].update(visible=False)

      if event == 'Submit':
        break
        

  if values[0] == '' or values[1] == '' or values[2] == '':
    sg.popup('One or more field empty')
    
  else:
    examsNumber = int(values[0])
    creditsNumber = int(values[1])
    finalMean = float(values[2])

    
    if finalMean > 31:
      finalMean=31

    ratingToTake(examsNumber, creditsNumber, finalMean, actualMean, totalCredits)

  ratingWindow.close()



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
    meanMenuInputType()

  elif event == 'Rating to be taken':
    ratingToTakeCalculator()

mainWindow.close()

