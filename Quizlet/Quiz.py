#####################
#   Project No.1    #
#       Quiz        #
#   By: ExWaltz     #
#####################
import os
import json
import random


class PythonQuiz:
    def QuizBook(self, bookname, question=None, choices=[], answer=0, mode=0, qrandom=False, recordTime=True):
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
            fixed_bookname = self._checkBookName(bookname)
            fixed_answer = json.dumps(answer)
            fixed_random = json.dumps(qrandom)
            fixed_recordTime = json.dumps(recordTime)
            fixed_choices = json.dumps(choices)

            if mode == 0:
                choices = [True, False]
            elif mode == 1:
                fixed_answer = json.dumps(choices[int(answer)])

            if qbStaus:
                jsnFile = open(str(fixed_bookname), 'w', encoding="utf-8")
                self.AddQuizToList(os.path.realpath(jsnFile.name))
                if question is None:
                    data = f'{{"{bookname}":[{{"random": {fixed_random}, "recordTime": {fixed_recordTime}}}]}}'
                else:
                    data = f'{{"{bookname}": [{{"{question}": [{{"choices": {fixed_choices}, "answer": {fixed_answer}, "mode": {mode}, "time": null}}], "random": {fixed_random}, "recordTime": {fixed_recordTime}}}]}}'
                jsnLoad = json.loads(data)
                json.dump(jsnLoad, jsnFile, indent=2)
                jsnFile.close()
            elif question is not None:
                self.UpdateQuizBook(bookname, question,
                                    choices, answer, mode)

            # Quizlet options
            def AddQuizlet(qquestion, qchoice=[], qanswer=0, qmode=0):
                if qmode == 0:
                    qchoice = [True, False]
                self.UpdateQuizBook(bookname, qquestion,
                                    qchoice, qanswer, qmode)

            def RemoveQuizlet(qquestion):
                self.DeleteQuizlet(bookname, qquestion)

            def GetQuizInfo(qquestion):
                return self.getQuizletInfo(bookname, qquestion)

            def GetAllQuizInfo():
                return self.getAllQuizletInfo(bookname)

            def GetQuestions():
                return self.getQuestions(bookname)

            self.QuizBook.__dict__["Add"] = AddQuizlet
            self.QuizBook.__dict__["Remove"] = RemoveQuizlet
            self.QuizBook.__dict__["GetQuizInfo"] = GetQuizInfo
            self.QuizBook.__dict__["GetAllQuizInfo"] = GetAllQuizInfo
            self.QuizBook.__dict__["GetQuestions"] = GetQuestions

            return self.QuizBook
        except Exception as e:
            raise e("TypeError: Invalid Type")

    def QuizBookOptions(self, bookname, qrandom=False, recordTime=True):
        fixed_bookname = self._checkBookName(bookname)
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        data[bookname][0]["random"] = qrandom
        data[bookname][0]["recordTime"] = recordTime
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    def UpdateQuizBook(self, ubookname, uquestion, uchoices=[], uanswer=0, umode=1):
        fixed_ubookname = self._checkBookName(ubookname)
        fixed_answer = uanswer
        if umode == 1:
            fixed_answer = uchoices[int(uanswer)]
        jsnFile = open(str(fixed_ubookname), 'r+', encoding="utf-8")
        self.AddQuizToList(os.path.realpath(jsnFile.name))
        data = json.loads(jsnFile.read())
        uquestionData = {"choices": uchoices,
                         "answer": fixed_answer, "mode": umode, "time": None}
        if data[str(ubookname)][0].get(str(uquestion)) is None:
            data[str(ubookname)][0][str(uquestion)] = [uquestionData]
        data[str(ubookname)][0][str(uquestion)][0] = uquestionData
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    def DeleteQuizlet(self, bookname, qquestion):
        if self._verifyQuizlet(bookname, qquestion):
            fixed_bookname = self._checkBookName(bookname)
            jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
            data = json.loads(jsnFile.read())
            del data[bookname][0][qquestion]
            jsnFile.seek(0)
            json.dump(data, jsnFile, indent=2)
            jsnFile.truncate()
            jsnFile.close()
        else:
            raise Exception("Question does not exist")

    def AddQuizToList(self, bookname):
        bookpath = str(bookname).replace("\\", "/")
        if not os.path.exists("quizList.json"):
            savequizList = open("quizList.json", "w", encoding="utf-8")
            data = f'{{"QuizList": ["{str(bookpath)}"]}}'
            jsnLoad = json.loads(data)
            jsnData = json.dumps(jsnLoad, indent=2)
            savequizList.write(jsnData)
            savequizList.close()
        else:
            savequizList = open("quizList.json", "r+", encoding="utf-8")
            data = json.loads(savequizList.read())
            quizList = data["QuizList"]
            quizList.append(bookpath)
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
                * 1: Multiple Choice quizlet
                * 2: Input quizlet
        '''
        self.QuizBook(quizname, question, choices, answer, mode)

    def ResetQuiz(self, qbookname, qquestion):
        fixed_qbookname = self._checkBookName(qbookname)
        jsnFile = open(str(fixed_qbookname), 'r+', encoding="utf-8")
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
        fixed_bookname = self._checkBookName(bookname)
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        quizBookData = data.get(bookname)[0]
        quizQuestions = list(dict.fromkeys(quizBookData))
        quizQuestions.remove("random")
        quizQuestions.remove("recordTime")
        if len(quizQuestions) == 0:
            return []
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
        fixed_bookname = self._checkBookName(bookname)
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        if data.get(bookname)[0].get(quizletname):
            quizQuestion = quizletname
            quizChoices = data[bookname][0][quizletname][0]["choices"]
            quizAnswer = data[bookname][0][quizletname][0]["answer"]
            quizTime = data[bookname][0][quizletname][0]["time"]
            compileInfo = [quizQuestion, quizChoices, quizAnswer, quizTime]
            return compileInfo

    def getQuestions(self, bookname):
        fixed_bookname = self._checkBookName(bookname)
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
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

    def _checkQuizBook(self, quizbookname):
        f_quizbookname = self._checkBookName(quizbookname)
        if os.path.exists(str(f_quizbookname)):
            if self._verifyQuizBook(quizbookname):
                return False
        return True

    def _verifyQuizBook(self, bookname):
        try:
            fixed_bookname = self._checkBookName(bookname)
            jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
            data = json.loads(jsnFile.read())
            data[bookname][0]["random"]
            data[bookname][0]["recordTime"]
            return True
        except Exception:
            return False

    def _verifyQuizlet(self, bookname, quizletname):
        try:
            fixed_bookname = self._checkBookName(bookname)
            jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
            data = json.loads(jsnFile.read())
            data[bookname][0][quizletname][0]["choices"][0]
            data[bookname][0][quizletname][0]["answer"]
            data[bookname][0][quizletname][0]["mode"]
            data[bookname][0][quizletname][0]["time"]
            return True
        except Exception:
            return False


quiz = PythonQuiz()
# quiz.QuizBookOptions(bookname="Test", qrandom=True)
test = quiz.QuizBook("Cool")
test.Add("Wata")
print(quiz.getAllQuizletInfo("Test"))
