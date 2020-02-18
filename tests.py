import course
import survey
import criterion
import grouper
import pytest
from typing import List


class TestStudent:

    answer = survey.Answer(True)
    wrong = survey.Answer("yes")
    question = survey.YesNoQuestion(4, "Are you a rock?")

    def test_student_properties(self):
        student = course.Student(1, "Hermione")
        assert student.id == 1
        assert student.name == 'Hermione'
        assert str(student) == student.name

    def test_set_answer(self):
        student = course.Student(1, "Hermione")
        student.set_answer(self.question, self.answer)

    def test_get_answer(self):
        # TODO
        pass

    def test_has_answer(self):
        # TODO
        pass


class TestCourse:

    """
    have preloaded students (TestStudent.s, etc.)
    that include answers to survey question.
    add them into a course here (TestCourse.course)
    """

    students = [course.Student(1, "wun"), course.Student(3, "too"),
                course.Student(2, "for")]
    course = None

    def test_course_enroll(self):
        c = course.Course("underwater basket weaving")
        assert c.name == 'underwater basket weaving'
        assert c.students == []
        students = [course.Student(1, "ay"), course.Student(3, "bee"),
                    course.Student(2, "sea")]
        c.enroll_students(students)
        assert len(c.students) == len(students)
        for s in students:
            assert s in c.students

    def test_course_get_students(self):
        c = course.Course("mental health")
        c.enroll_students(self.students)
        self.course = c
        assert c.get_students()[1].name == 'for'

    def test_all_answered(self):
        pass
        # TODO: fniishit his


def test_sort_students():
    s1 = course.Student(1, "gad")
    s2 = course.Student(53, "floof")
    s3 = course.Student(9, "gad")
    s4 = course.Student(15, "blep")
    s5 = course.Student(4, "meep")
    ppl = [s1, s2, s3, s4, s5]
    assert course.sort_students(ppl, 'id') == [s1, s5, s3, s4, s2]
    assert course.sort_students(ppl, 'name') == [s4, s2, s1, s3, s5]


def test_slice_list():
    assert grouper.slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    assert grouper.slice_list(['a', 1, 6.0, False], 3) \
        == [['a', 1, 6.0], [False]]


def test_windows():
    assert grouper.windows([3, 4, 6, 2, 3], 2) == \
           [[3, 4], [4, 6], [6, 2], [2, 3]]
    assert grouper.windows(['a', 1, 6.0, False], 3) == \
        [['a', 1, 6.0], [1, 6.0, False]]


class TestGroup:

    s1 = course.Student(1, "gad")
    s2 = course.Student(53, "floof")
    s3 = course.Student(9, "gad")
    s4 = course.Student(15, "blep")
    s5 = course.Student(4, "meep")
    members = [s1, s2, s3, s4]

    def test_group_properties(self):
        g = grouper.Group(self.members)
        assert len(g) == 4
        assert self.s4 in g
        assert self.s5 not in g
        assert str(g) == 'gad, floof, gad, blep.'

    def test_get_members(self):
        g = grouper.Group(self.members)
        assert g.get_members()[2].id == 9
        assert len(g.get_members()) == len(g)


class TestGrouping:

    def test_grouping_properties(self):
        gping = grouper.Grouping()
        assert len(gping) == 0

    def test_add_group(self):
        gping = grouper.Grouping()
        assert gping.add_group(grouper.Group(TestGroup.members))
        assert not gping.add_group(grouper.Group(TestGroup.members[:2]))
        assert gping.add_group(grouper.Group([TestGroup.s5]))
        assert len(gping) == 2

    def test_get_groups(self):
        gping = grouper.Grouping()
        assert gping.get_groups() == []
        gping.add_group(grouper.Group(TestGroup.members))
        gping.add_group(grouper.Group([TestGroup.s5]))
        assert gping.get_groups()[1].get_members()[0] == TestGroup.s5
        assert gping.get_groups()[0].get_members()[1] == TestGroup.s2


class TestQuestionAnswer:
    """
    regular Question, no implemented methods
    """
    # TODO: answer.is_valid and all Question subclasses
    def test_question_properties(self):
        q = survey.Question(44, "question?")
        assert q.id == 44
        assert q.text == 'question?'

    def test_answer_properties(self):
        a = survey.Answer("yeet")
        assert a.content == 'yeet'


class TestMCQuestion:
    """
    mcq
    """
    # TODO: finish this class
    def test_question_properties(self):
        q = survey.Question(44, "question?")
        assert q.id == 44
        assert q.text == 'question?'


class TestNumQuestion:
    """
    numeric
    """
    # TODO: finish this class

    def test_question_properties(self):
        q = survey.Question(44, "question?")
        assert q.id == 44
        assert q.text == 'question?'


class TestYNQuestion:
    """
    yes/no
    """
    # TODO: finish this class

    def test_question_properties(self):
        q = survey.Question(44, "question?")
        assert q.id == 44
        assert q.text == 'question?'


class TestCheckboxQuestion:
    """
    mcq
    """
    # TODO: finish this class

    def test_question_properties(self):
        q = survey.Question(44, "question?")
        assert q.id == 44
        assert q.text == 'question?'


class TestCriterion:
    """
    homo
    hetero
    lonely
    """
    # TODO: finish this class as one class.
    # TODO: needs one question and a list of answers
    pass


class TestSurvey:
    # TODO: finish this class

    questions = []  # list of questions
    survey = survey.Survey(questions)


class TestGrouper:
    """
    alpha
    random
    greedy
    window
    """
    # TODO: finish this class as four classes
    pass


if __name__ == '__main__':
    pytest.main(['tests.py'])
