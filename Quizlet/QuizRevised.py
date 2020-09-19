import json
import random
import os
from pathlib import Path


class QuizBook:
    # __slots__ = ["title", "disableRandom", "disableRecordTime"]

    def __init__(self, title, disableRandom=True, path=None):
        self.title = str(title).upper()
        self.disableRandom = disableRandom
        self.path = path
        self.saveQuizBook()

    def saveQuizBook(self):
        fileName = self.AddExtention(self.path)
        if not self.path:
            fileName = self.AddExtention(self.title)
        isExist = self.fileExists(fileName)
        jsnDisableRandom = json.dumps(self.disableRandom)
        if not isExist:
            quizBookFile = open(fileName, "w", encoding="utf-8")

            jsnTitle = json.dumps(self.title)
            quizBookData = f'{{"Title": {jsnTitle}, "disableRandom": {jsnDisableRandom}}}'

            jsnQuizBookData = json.loads(quizBookData)
            json.dump(jsnQuizBookData, quizBookFile, indent=2)
        else:
            quizBookFile = open(fileName, "r+", encoding="utf-8")
            jsnQuizBookData = json.load(quizBookFile)
            jsnQuizBookData["Title"] = self.title
            jsnQuizBookData["disableRandom"] = jsnDisableRandom
            quizBookFile.seek(0)
            json.dump(jsnQuizBookData, quizBookFile, indent=2)
            quizBookFile.truncate()
        return [jsnQuizBookData, fileName]

    def AddExtention(self, path):
        if str(path).endswith(".quiz"):
            return Path(path).name
        return f"{path}.quiz"

    def fileExists(self, path):
        if os.path.exists(path):
            return True
        return False

    def AllQuestions(self):
        fileName = self.AddExtention(self.path)
        if not self.path:
            fileName = self.AddExtention(self.title)
        quizBookFile = open(fileName, "r", encoding="utf-8")
        jsnQuizBookData = json.load(quizBookFile)
        try:
            questions = jsnQuizBookData["Questions"][0]
            if not self.disableRandom:
                keys = list(questions.keys())
                random.shuffle(keys)
                randomizedQuestions = {}
                for key in keys:
                    randomizedQuestions.update({key: questions[key]})
                questions = randomizedQuestions
            return questions
        except Exception:
            return {}

    def __len__(self):
        fileName = self.AddExtention(self.path)
        if not self.path:
            fileName = self.AddExtention(self.title)
        quizBookFile = open(fileName, "r", encoding="utf-8")
        jsnQuizBookData = json.load(quizBookFile)
        try:
            questions = jsnQuizBookData["Questions"][0]
            return len(questions)
        except Exception:
            return 0

    def remove(self):
        fileName = self.AddExtention(self.path)
        if not self.path:
            fileName = self.AddExtention(self.title)
        filePath = os.path.realpath(fileName)
        os.remove(filePath)


class QuizQuestion(QuizBook):
    def __init__(self, title, question, choices=None, answer=0, disableRandom=True, path=None):
        super(QuizQuestion, self).__init__(title, disableRandom, path)
        self.question = str(question).upper()
        self.choices = choices
        self.answer = answer
        self.path = path

        if choices is None:
            self.choices = []
        self.saveQuestion()

    def saveQuestion(self):
        jsnData, fileName = self.saveQuizBook()
        quizBookFile = open(fileName, "r+", encoding="utf-8")
        jsnQuestion = json.dumps(self.question)
        jsnChoices = json.dumps(self.choices)
        questionData = f'{{{jsnQuestion}: [{{"choices": {jsnChoices}, "answerIndex": {self.answer}}}]}}'
        jsnQuestionData = json.loads(questionData)
        if jsnData.get("Questions"):
            jsnData["Questions"][0][self.question] = jsnQuestionData[self.question]
        else:
            jsnData["Questions"] = [jsnQuestionData]

        quizBookFile.seek(0)
        json.dump(jsnData, quizBookFile, indent=2)
        quizBookFile.truncate()
        quizBookFile.close()

    def remove(self):
        jsnData, fileName = self.saveQuizBook()
        quizBookFile = open(fileName, "r+", encoding="utf-8")
        del jsnData["Questions"][0][self.question]

        quizBookFile.seek(0)
        json.dump(jsnData, quizBookFile, indent=2)
        quizBookFile.truncate()
        quizBookFile.close()


QuizQuestion("CoverGroup", "Kusdda", ["Kusd1a", "Subarash4i", "Kus5o"], 0)
QuizQuestion("CoverGroup", "peko", ["opek", "eokp", "kope"], 0)
print(QuizBook("CoverGroup", False).AllQuestions())
