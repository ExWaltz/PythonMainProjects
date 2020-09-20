#####################
#   Project No.1    #
#       Quiz        #
#   By: ExWaltz     #
#####################
# TODO
# - [x] Add Quality of life
# - [ ] Make GUI
import os
import json
import random
from pathlib import Path


class PythonQuiz:
    """
        Decript Check Quiz.py for updated version
        # Future Improvements
            * Make the code more readable
            * Add more documentation
    """

    def QuizBook(self, bookname, question=None, choices=[], answer=0, mode=True, qrandom=False, recordTime=True):
        ''' bookname:   # Required
                * Enter existing or new Quiz Book name
            question:   # Optional
                * Question of Quizlet
            choices:    # Optional
                * Answers to question
            answer:     # Optional
                * Choice Index
            mode:       # Optional
                * True: True or False quizlet
                * False: Multiple Choice quizlet
            qrandom:     # Optional
                * Randomized Quizlet order every load and Reset
            recordTime: # Optional
                * True: Record time to answer in each Quizlet
                * False: Record time off
        '''
        try:
            qbStaus = self._checkQuizBook(bookname)     # Check if does not bookname exist
            # Convert values into json
            fixed_bookname = self._checkBookName(bookname)
            fixed_question = str(question).lower()
            bookname = str(bookname).upper()
            fixed_answer = json.dumps(answer)
            fixed_random = json.dumps(qrandom)
            fixed_recordTime = json.dumps(recordTime)
            fixed_choices = json.dumps(choices)
            fixed_mode = json.dumps(mode)

            # Check mode
            if mode:
                choices = [False, True]
            else:
                fixed_answer = json.dumps(choices[int(answer)])

            # Book does not exist
            if qbStaus:
                jsnFile = open(str(fixed_bookname), 'w', encoding="utf-8")
                self.AddQuizToList(os.path.realpath(jsnFile.name))
                # If no question is given
                if question is None:
                    data = f'''{{"{bookname}": [{{
                                 "random": {fixed_random},
                                 "recordTime": {fixed_recordTime},
                                 "bestTime": null
                                 }}]}}'''
                else:
                    data = f'''{{"{bookname}": [{{
                                 "{fixed_question}": [{{
                                 "choices": {fixed_choices},
                                 "answer": {fixed_answer},
                                 "mode": {fixed_mode},
                                 "original": "{question}",
                                 "time": null}}],
                                 "random": {fixed_random},
                                 "recordTime": {fixed_recordTime},
                                 "bestTime": null
                                 }}]}}'''
                # Save json file
                jsnLoad = json.loads(data)
                json.dump(jsnLoad, jsnFile, indent=2)
                jsnFile.close()

            elif question is not None:
                # if QuizBook exist and question is Inputed
                self.UpdateQuizBook(bookname, question, choices, answer, mode)

            # Quizlet options
            def QuizletOpt():
                def AddQuizlet(question, choice=[], answer=0, mode=True):
                    if mode:
                        choice = [False, True]
                    self.UpdateQuizBook(bookname, question, choice, answer, mode)

                def RemoveQuizlet(question):
                    self.DeleteQuizlet(bookname, question)

                def GetQuizInfo(question):
                    return self.getQuizletInfo(bookname, question)

                QuizletOpt.__dict__["add"] = AddQuizlet
                QuizletOpt.__dict__["remove"] = RemoveQuizlet
                QuizletOpt.__dict__["quiz"] = GetQuizInfo
                QuizletOpt.__dict__["allquiz"] = self.getAllQuizletInfo(bookname)
                QuizletOpt.__dict__["info"] = self.getBookInfo(bookname)
                QuizletOpt.__dict__["path"] = os.path.realpath(fixed_bookname)
                QuizletOpt.__dict__["name"] = bookname

                # QuizletOpt.__dict__["allquestions"] = self.getQuestions(bookname)
            QuizletOpt()
            return QuizletOpt

        except Exception as e:
            raise e("TypeError: Invalid Type")

    def QuizBookOptions(self, bookname, qrandom=False, recordTime=True):
        """qrandom: Everytime QuizBook is called or reset the order
            of questions is randomized.
            recordTime: Record time from start of the quizlet to the end of the quizlet"""
        fixed_bookname = self._checkBookName(bookname)
        bookname = str(bookname).upper()
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())

        data[bookname][0]["random"] = qrandom
        data[bookname][0]["recordTime"] = recordTime

        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    def UpdateQuizBook(self, ubookname, uquestion, uchoices=[], uanswer=0, umode=True):
        """Add or Update quizlet in QuizBook"""
        fixed_ubookname = self._checkBookName(ubookname)
        ubookname = str(ubookname).upper()
        fixed_question = str(uquestion).lower()
        fixed_answer = uchoices[int(uanswer)]
        jsnFile = open(str(fixed_ubookname), 'r+', encoding="utf-8")
        self.AddQuizToList(os.path.realpath(jsnFile.name))
        data = json.loads(jsnFile.read())

        uquestionData = {"choices": uchoices,
                         "answer": fixed_answer,
                         "mode": umode,
                         "original": uquestion,
                         "time": None}

        if data[str(ubookname)][0].get(fixed_question) is None:
            data[str(ubookname)][0][fixed_question] = [uquestionData]

        data[str(ubookname)][0][fixed_question][0] = uquestionData

        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    def DeleteQuizBook(self, bookname):
        path = os.path.realpath(bookname)
        os.remove(path)

    def DeleteQuizlet(self, bookname, qquestion):
        if self._verifyQuizlet(bookname, qquestion):
            fixed_bookname = self._checkBookName(bookname)
            bookname = str(bookname).upper()
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
        """Save QuizBook in quizList.json"""
        bookpath = str(bookname).replace("\\", "/")
        bookpath = bookpath.upper()
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

    def quizTime(self, bookname, quizname, time_="null"):
        fixed_bookname = self._checkBookName(bookname)
        quizname = str(quizname).lower()
        bookname = str(bookname).upper()
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        data[bookname][0][quizname][0]["time"] = time_
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()

    @property
    def AllQuizBook(self):
        """Get all QuizBook from quizList.json"""
        if os.path.exists("quizList.json"):
            savequizList = open("quizList.json", "r+", encoding="utf-8")
            data = json.loads(savequizList.read())
            quizList = data["QuizList"]
            returnList = []
            for quiz in quizList:
                if os.path.exists(quiz):
                    filename = Path(quiz).stem
                    qb = self.QuizBook(filename)
                    returnList.append(qb)
                else:
                    data["QuizList"].remove(quiz)
                    savequizList.seek(0)
                    json.dump(data, savequizList, indent=2)
                    savequizList.truncate()
            savequizList.close()
            return returnList
        else:
            return None

    def AvgTime(self, bookname):
        fixed_bookname = self._checkBookName(bookname)
        quizzes = self.getAllQuizletInfo(bookname)
        bookname = str(bookname).upper()
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        allQuizTime = [eq[-1] for eq in quizzes]
        bestTime = 0
        for eqt in allQuizTime:
            feq = float(eqt)
            bestTime += feq
        bestTime /= len(allQuizTime)
        bestTime = float("%.2f" % bestTime)
        initBestTime = data[bookname][0]["bestTime"]
        if bestTime <= initBestTime:
            data[bookname][0]["bestTime"] = bestTime
        jsnFile.seek(0)
        json.dump(data, jsnFile, indent=2)
        jsnFile.truncate()
        jsnFile.close()
        return bestTime

    def CreateQuizlet(self, quizname, question, choices=[], answer=0, mode=True):
        """ Make a Quizbook and add a quizlet. If quizname already exist then
            Update or Add question to QuizBook"""
        self.QuizBook(quizname, question, choices, answer, mode)

    def getBookInfo(self, bookname):
        fixed_bookname = self._checkBookName(bookname)
        bookname = str(bookname).upper()
        jsnFile = open(str(fixed_bookname), 'r', encoding="utf-8")
        data = json.loads(jsnFile.read())
        quizBookData = data.get(bookname)[0]
        rand = quizBookData["random"]
        recTime = quizBookData["recordTime"]
        bTime = quizBookData["bestTime"]
        compInfo = [bookname, rand, recTime, bTime]
        jsnFile.close()
        return compInfo

    def getAllQuizletInfo(self, bookname):
        """ Get all quizlet info from QuizBook
            All questions, choices, answers and record time
            will be returned as a list"""
        fixed_bookname = self._checkBookName(bookname)
        bookname = str(bookname).upper()
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        quizBookData = data.get(bookname)[0]
        quizQuestions = list(dict.fromkeys(quizBookData))
        quizQuestions.remove("random")
        quizQuestions.remove("recordTime")
        quizQuestions.remove("bestTime")
        if len(quizQuestions) == 0:
            return []
        isRand = quizBookData.get("random")
        if isRand:
            random.shuffle(quizQuestions)
        quizInfo = []
        for eachQuestion in quizQuestions:
            compileInfo = self.filterInfo(data, bookname, eachQuestion)
            quizInfo.append(compileInfo)
        jsnFile.close()
        return quizInfo

    def filterInfo(self, data, bookname, question):
        qquestion = data[bookname][0][question][0]["original"]
        qchoices = data[bookname][0][question][0]["choices"]
        qanswer = data[bookname][0][question][0]["answer"]
        qtime = data[bookname][0][question][0]["time"]
        compileInfo = [qquestion, qchoices, qanswer, qtime]
        return compileInfo

    def getQuizletInfo(self, bookname, quizletname):
        """ Get a specific quizlet info from a Quizbook.
            return a the question, choices, answer and record time in a list"""
        fixed_bookname = self._checkBookName(bookname)
        bookname = str(bookname).upper()
        quizletname = str(quizletname).lower()
        jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
        data = json.loads(jsnFile.read())
        if data.get(bookname)[0].get(quizletname):
            compileInfo = self.filterInfo(data, bookname, quizletname)
            jsnFile.close()
            return compileInfo

    def _checkBookName(self, bookname):
        """Check if file input has .quiz extension"""
        if str(bookname).find(".quiz") == -1:
            return str(bookname) + ".quiz"
        return str(bookname)

    def _checkQuizBook(self, quizbookname):
        """Check if QuizBook exist"""
        f_quizbookname = self._checkBookName(quizbookname)
        if os.path.exists(str(f_quizbookname)):
            if self._verifyQuizBook(quizbookname):
                return False
        return True

    def _verifyQuizBook(self, bookname):
        """Verify if file is on QuizBook format"""
        try:
            fixed_bookname = self._checkBookName(bookname)
            bookname = str(bookname).upper()
            jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
            data = json.loads(jsnFile.read())
            data[bookname][0]["random"]
            data[bookname][0]["recordTime"]
            data[bookname][0]["bestTime"]
            jsnFile.close()
            return True
        except Exception:
            return False

    def _verifyQuizlet(self, bookname, quizletname):
        """Verify if the QuizBook has questions"""
        try:
            fixed_bookname = self._checkBookName(bookname)
            quizletname = str(quizletname).lower()
            bookname = str(bookname).upper()
            jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
            data = json.loads(jsnFile.read())
            data[bookname][0][quizletname][0]["choices"][0]
            data[bookname][0][quizletname][0]["answer"]
            data[bookname][0][quizletname][0]["mode"]
            data[bookname][0][quizletname][0]["time"]
            jsnFile.close()
            return True
        except Exception:
            return False

    # Things are I think are overshadowed by other functions
    # In other words useless stuff
    # U can use them if you want

    # I have trouble implementing this one
    # I decided to add this feature to the GUI instead of the package
    #
    # def ResetQuiz(self, bookname, question):
    #     """Reset Everything inside the QuizBook. (All Recorded Time will be erased)"""
    #     fixed_bookname = self._checkBookName(bookname)
    #     bookname = str(bookname).upper()
    #     jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
    #     data = json.loads(jsnFile.read())
    #     quizBookData = data.get(str(bookname))[0]
    #     isRand = quizBookData.get("random")
    #     isTime = quizBookData.get("recordTime")
    #     if isRand:
    #         ansList = quizBookData[0][0]["choices"]
    #         random.shuffle(ansList)
    #         quizBookData[0][0]["choices"] = ansList
    #     if isTime:
    #         quizBookData[0][0]["time"] = "null"
    #     jsnFile.seek(0)
    #     json.dump(data, jsnFile, indent=2)
    #     jsnFile.truncate()
    #     jsnFile.close()

    # Overshadowed by literaly everything
    # Why did I make this again?
    #
    # def getQuestions(self, bookname):
    #     """ Get all the questions from a QuizBook
    #         will return a list of questions"""
    #     fixed_bookname = self._checkBookName(bookname)
    #     jsnFile = open(str(fixed_bookname), 'r+', encoding="utf-8")
    #     data = json.loads(jsnFile.read())
    #     quizBookData = data.get(bookname)[0]
    #     quizQuestions = list(dict.fromkeys(quizBookData))
    #     quizQuestions.remove("random")
    #     quizQuestions.remove("recordTime")
    #     isRand = quizBookData.get("random")
    #     if isRand:
    #         random.shuffle(quizQuestions)
    #     return quizQuestions
