#####################
#   Project No.1    #
#       Quiz        #
#   By: ExWaltz     #
#####################
import os
import json
import random


class PythonQuiz:
    def QuizBook(self, bookname, question=None, choices=[], answer=0, mode=2, qrandom=False, recordTime=True):
        """ bookname:   # Required
                * Enter existing or new Quiz Book name
            question:   # Optional
                * Question of Quizlet
            choices:    # Optional
                * Answers to question
            answer:     # Optional
                * Choice Index
            mode:       # Optional
                * 1: True or False quizlet
                * 2: Multiple Choice quizlet
                * 3: Input quizlet
            qrandom:     # Optional
                * Randomized Quizlet order every load and Reset
            recordTime: # Optional
                * True: Record time to answer in each Quizlet
                * False: Record time off
        """
        try:
            qbStaus = self._checkQuizBook(bookname)
            if mode == 1:
                choices = [True, False]
            if qbStaus:
                jsnFile = open(f"{bookname}.quiz", 'w', encoding="utf-8")
                self.AddQuizToList(os.path.realpath(jsnFile.name))
                if question is None:
                    data = f'{{"{bookname}":[{{"random": {random}, "recordTime": {recordTime}}}]}}'
                else:
                    data = f'{{"{bookname}": [{{"{question}": [{{"choices": {json.dumps(choices)}, "answer": {json.dumps(choices[answer])}, "mode": {mode}, "time": null}}], "random": {json.dumps(qrandom)}, "recordTime": {json.dumps(recordTime)}}}]}}'
                print(data)
                jsnLoad = json.loads(data)
                json.dump(jsnLoad, jsnFile, indent=2)
                jsnFile.close()
            elif question is not None:
                self._updateQuizBook(bookname, question,
                                     choices, answer, mode)
        except Exception as e:
            raise e("TypeError: Invalid Type")

    def QuizBookOptions(self, bookname, qrandom=False, recordTime=True):
        jsnFile = open(f"{bookname}.quiz", 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        data[bookname][0]["random"] = qrandom
        data[bookname][0]["recordTime"] = recordTime
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    def _updateQuizBook(self, ubookname, uquestion, uchoices=[], uanswer=0, umode=2):
        jsnFile = open(f"{ubookname}.quiz", 'r+', encoding="utf-8")
        self.AddQuizToList(os.path.realpath(jsnFile.name))
        data = json.loads(jsnFile.read())
        uquestionData = {"choices": uchoices,
                         "answer": uchoices[uanswer], "mode": umode, "time": None}
        if data[str(ubookname)][0].get(str(uquestion)) is None:
            data[str(ubookname)][0][str(uquestion)] = [uquestionData]
        data[str(ubookname)][0][str(uquestion)][0] = uquestionData
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    def _checkQuizBook(self, quizbookname):
        # Get QuizBook_list
        # if quizbookname is in QuizBook_list
        #   retrun True
        # else:
        #   return False
        if os.path.exists(f"{quizbookname}.quiz"):
            return False
        return True

    def AddQuizToList(self, bookname):
        fixbookname = str(bookname).replace("\\", "/")
        if not os.path.exists("quizList.json"):
            savequizList = open("quizList.json", "w", encoding="utf-8")
            data = f'{{"QuizList": ["{str(fixbookname)}"]}}'
            jsnLoad = json.loads(data)
            jsnData = json.dumps(jsnLoad, indent=2)
            savequizList.write(jsnData)
            savequizList.close()
        else:
            savequizList = open("quizList.json", "r+", encoding="utf-8")
            data = json.loads(savequizList.read())
            quizList = data["QuizList"]
            quizList.append(fixbookname)
            cleanQuizList = list(dict.fromkeys(quizList))
            data["QuizList"] = cleanQuizList
            savequizList.seek(0)
            json.dump(data, savequizList, indent=2)
            savequizList.truncate()
            savequizList.close()

    def CreateQuizlet(self, quizname, question, choices=[], answer=0, mode=2):
        ''' quizname:   # Required
                * Enter existing or new Quiz Book name
            question:   # Required
                * Question of Quizlet
            choices:    # Required if mode=False
                * Answers to question
            mode:       # Optional
                * 1: True or False quizlet
                * 2: Multiple Choice quizlet # Default
                * 3: Input quizlet
                * mode > 3: Multiple Choice quizlet
        '''
        self.QuizBook(quizname, question, choices, answer, mode)

    def ResetQuiz(self, qbookname):
        # Save score
        # if recordTime=True
        #   Reset Time
        # if random=True
        #   Randomized choices position
        #   Randomized quiz position

        jsnFile = open(f"{qbookname}.quiz", 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        quizBookData = data.get(str(qbookname))[0]
        isRand = quizBookData.get("random")
        isTime = quizBookData.get("recordTime")
        if isRand:
            ansList = quizBookData[0][0]["choices"]
            random.shuffle(ansList)
            quizBookData[0][0]["choices"] = ansList
        if isTime:
            quizBookData[0][0]["time"] = "null"
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    def getQuestions(self, bookname):
        # Get Quiz Book info
        # if recordTime=True
        #   Record Time
        # if random=True
        #   Randomized choices position
        #   Randomized quiz position
        jsnFile = open(f"{bookname}.quiz", 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        quizBookData = data.get(bookname)[0]
        quizQuestions = list(dict.fromkeys(quizBookData))
        quizQuestions.remove("random")
        quizQuestions.remove("recordTime")
        isRand = quizBookData.get("random")
        if isRand:
            random.shuffle(quizQuestions)
        return quizQuestions


quiz = PythonQuiz()
# quiz.QuizBookOptions(bookname="Test", qrandom=True)
quiz.CreateQuizlet("Test", "Rushia ch", [42, "sfs", 12, 510], 2)
print(quiz.getQuestions("Test"))
