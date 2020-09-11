#####################
#   Project No.1    #
#       Quiz        #
#   By: ExWaltz     #
#####################
import os
import json
import random


class PythonQuiz:
    def QuizBook(self, bookname, question=None, choices=[], answer=0, mode=1, qrandom=False, recordTime=True):
        ''' bookname:   # Required
                * Enter existing or new Quiz Book name
            question:   # Optional
                * Question of Quizlet
            choices:    # Optional
                * Answers to question
            answer:     # Optional
                * Choice Index
            mode:       # Optional
                * 0: True or False quizlet
                * 1: Multiple Choice quizlet
                * 2: Input quizlet
            qrandom:     # Optional
                * Randomized Quizlet order every load and Reset
            recordTime: # Optional
                * True: Record time to answer in each Quizlet
                * False: Record time off
        '''
        try:
            qbStaus = self._checkQuizBook(bookname)
            f_bookname = self._checkBookName(bookname)
            f_answer = json.dumps(answer)

            if mode == 0:
                choices = [True, False]
            elif mode == 1:
                f_answer = json.dumps(choices[int(answer)])

            if qbStaus:
                jsnFile = open(str(f_bookname), 'w', encoding="utf-8")
                self.AddQuizToList(os.path.realpath(jsnFile.name))
                if question is None:
                    data = f'{{"{bookname}":[{{"random": {random}, "recordTime": {recordTime}}}]}}'
                else:
                    data = f'{{"{bookname}": [{{"{question}": [{{"choices": {json.dumps(choices)}, "answer": {f_answer}, "mode": {mode}, "time": null}}], "random": {json.dumps(qrandom)}, "recordTime": {json.dumps(recordTime)}}}]}}'
                jsnLoad = json.loads(data)
                json.dump(jsnLoad, jsnFile, indent=2)
                jsnFile.close()
            elif question is not None:
                self.UpdateQuizBook(bookname, question,
                                    choices, answer, mode)
        except Exception as e:
            raise e("TypeError: Invalid Type")

    def QuizBookOptions(self, bookname, qrandom=False, recordTime=True):
        f_bookname = self._checkBookName(bookname)
        jsnFile = open(str(f_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        data[bookname][0]["random"] = qrandom
        data[bookname][0]["recordTime"] = recordTime
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    def UpdateQuizBook(self, ubookname, uquestion, uchoices=[], uanswer=0, umode=1):
        f_ubookname = self._checkBookName(ubookname)
        f_answer = uanswer
        if umode == 1:
            f_answer = uchoices[int(uanswer)]
        print(f_answer)
        jsnFile = open(str(f_ubookname), 'r+', encoding="utf-8")
        self.AddQuizToList(os.path.realpath(jsnFile.name))
        data = json.loads(jsnFile.read())
        uquestionData = {"choices": uchoices,
                         "answer": f_answer, "mode": umode, "time": None}
        if data[str(ubookname)][0].get(str(uquestion)) is None:
            data[str(ubookname)][0][str(uquestion)] = [uquestionData]
        data[str(ubookname)][0][str(uquestion)][0] = uquestionData
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

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

    def CreateQuizlet(self, quizname, question, choices=[], answer=0, mode=1):
        ''' quizname:   # Required
                * Enter existing or new Quiz Book name
            question:   # Required
                * Question of Quizlet
            choices:    # Required if mode=False
                * Answers to question
            mode:       # Optional
                * 0: True or False quizlet
                * 1: Multiple Choice quizlet # Default
                * 2: Input quizlet
                * mode > 2: Multiple Choice quizlet
        '''
        self.QuizBook(quizname, question, choices, answer, mode)

    def ResetQuiz(self, qbookname, qquestion):
        f_qbookname = self._checkBookName(qbookname)
        jsnFile = open(str(f_qbookname), 'r+', encoding="utf-8")
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

    def getAllQuizletInfo(self, bookname):
        f_bookname = self._checkBookName(bookname)
        jsnFile = open(str(f_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        quizBookData = data.get(bookname)[0]
        quizQuestions = list(dict.fromkeys(quizBookData))
        quizQuestions.remove("random")
        quizQuestions.remove("recordTime")
        isRand = quizBookData.get("random")
        if isRand:
            random.shuffle(quizQuestions)
        quizInfo = []
        for eachQuestion in quizQuestions:
            choices = data[bookname][0][eachQuestion][0]["choices"]
            answer = data[bookname][0][eachQuestion][0]["answer"]
            time = data[bookname][0][eachQuestion][0]["time"]
            compileInfo = [eachQuestion, choices, answer, time]
            quizInfo.append(compileInfo)
        return quizInfo

    def getQuizletInfo(self, bookname, quizletname):
        f_bookname = self._checkBookName(bookname)
        jsnFile = open(str(f_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        if data.get(bookname)[0].get(quizletname):
            quizQuestion = quizletname
            quizChoices = data[bookname][0][quizletname][0]["choices"]
            quizAnswer = data[bookname][0][quizletname][0]["answer"]
            quizTime = data[bookname][0][quizletname][0]["time"]
            compileInfo = [quizQuestion, quizChoices, quizAnswer, quizTime]
            return compileInfo

    def getQuestions(self, bookname):
        f_bookname = self._checkBookName(bookname)
        jsnFile = open(str(f_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        quizBookData = data.get(bookname)[0]
        quizQuestions = list(dict.fromkeys(quizBookData))
        quizQuestions.remove("random")
        quizQuestions.remove("recordTime")
        isRand = quizBookData.get("random")
        if isRand:
            random.shuffle(quizQuestions)
        return quizQuestions

    def _checkBookName(self, bookname):
        if str(bookname).find(".quiz") == -1:
            return str(bookname) + ".quiz"
        return str(bookname)

    def _verifyQuizBook(self, bookname):
        try:
            f_bookname = self._checkBookName(bookname)
            jsnFile = open(str(f_bookname), 'r+', encoding="utf-8")
            data = json.loads(jsnFile.read())
            data[bookname][0]["random"]
            data[bookname][0]["recordTime"]
            return True
        except Exception:
            return False

    def _checkQuizBook(self, quizbookname):
        f_quizbookname = self._checkBookName(quizbookname)
        if os.path.exists(str(f_quizbookname)):
            if self._verifyQuizBook(quizbookname):
                return False
        return True


quiz = PythonQuiz()
# quiz.QuizBookOptions(bookname="Test", qrandom=True)
quiz.CreateQuizlet("Test", "Watame ch", answer=False, mode=0)
print(quiz.getAllQuizletInfo("Test"))
