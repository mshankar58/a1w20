from typing import List

import course
import survey
import criterion
import grouper
import pytest


class TestStudent:

    answer = survey.Answer(True)
    wrong = survey.Answer("rockrock")
    question = survey.YesNoQuestion(4, "Are you a rock?")
    question2 = survey.YesNoQuestion(5, "Are you a sock?")
    question3 = survey.YesNoQuestion(6, "Are you a smock?")

    def test_student_properties(self) -> None:
        student = course.Student(1, "Hermione")
        assert student.id == 1
        assert student.name == 'Hermione'
        assert str(student) == student.name

    def test_set_answer(self) -> None:
        student = course.Student(1, "Hermione")
        # set answer
        student.set_answer(self.question, self.answer)
        student.set_answer(self.question2, self.wrong)

    def test_get_answer(self) -> None:
        student = course.Student(1, "Hermione")
        # set answer
        student.set_answer(self.question, self.answer)
        student.set_answer(self.question2, self.wrong)
        # get answer
        assert student.get_answer(self.question) == self.answer
        assert student.get_answer(self.question2) == self.wrong
        assert student.get_answer(self.question3) is None

    def test_has_answer(self) -> None:
        student = course.Student(1, "Hermione")
        # set answer
        student.set_answer(self.question, self.answer)
        student.set_answer(self.question2, self.wrong)
        # has answer
        assert student.has_answer(self.question)
        assert not student.has_answer(self.question2)
        assert not student.has_answer(self.question3)


class TestCourse:

    def test_course_enroll(self) -> None:
        c = course.Course("underwater basket weaving")
        assert c.name == 'underwater basket weaving'
        assert c.students == []
        students = [course.Student(1, "ay"), course.Student(3, "bee"),
                    course.Student(2, "sea")]
        c.enroll_students(students)
        assert len(c.students) == len(students)
        for s in students:
            assert s in c.students

    def test_course_get_students(self) -> None:
        c = course.Course("mental health")
        students = [course.Student(1, "ay"), course.Student(3, "bee"),
                    course.Student(2, "sea")]
        c.enroll_students(students)
        assert c.get_students()[1].name == 'sea'


def test_sort_students() -> None:
    s1 = course.Student(1, "gad")
    s2 = course.Student(53, "floof")
    s3 = course.Student(9, "gad")
    s4 = course.Student(15, "blep")
    s5 = course.Student(4, "meep")
    ppl = [s1, s2, s3, s4, s5]
    assert course.sort_students(ppl, 'id') == [s1, s5, s3, s4, s2]
    assert course.sort_students(ppl, 'name') == [s4, s2, s1, s3, s5]


def test_slice_list() -> None:
    assert grouper.slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    assert grouper.slice_list(['a', 1, 6.0, False], 3) \
        == [['a', 1, 6.0], [False]]


def test_windows() -> None:
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

    def test_group_properties(self) -> None:
        g = grouper.Group(self.members)
        assert len(g) == 4
        assert self.s4 in g
        assert self.s5 not in g
        assert str(g) == 'gad, floof, gad, blep.'

    def test_get_members(self) -> None:
        g = grouper.Group(self.members)
        assert g.get_members()[2].id == 9
        assert len(g.get_members()) == len(g)


class TestGrouping:

    def test_grouping_properties(self) -> None:
        gping = grouper.Grouping()
        assert len(gping) == 0

    def test_add_group(self) -> None:
        gping = grouper.Grouping()
        assert gping.add_group(grouper.Group(TestGroup.members))
        assert not gping.add_group(grouper.Group(TestGroup.members[:2]))
        assert gping.add_group(grouper.Group([TestGroup.s5]))
        assert len(gping) == 2

    def test_get_groups(self) -> None:
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
    def test_question_properties(self) -> None:
        q = survey.Question(44, "question?")
        assert q.id == 44
        assert q.text == 'question?'

    def test_answer_properties(self) -> None:
        a = survey.Answer("yeet")
        assert a.content == 'yeet'


class TestMCQuestion:
    """
    mcq
    """
    def test_mcq_properties(self) -> None:
        q = survey.MultipleChoiceQuestion(1, "species?",
                                          ["human", 'bug', 'owl'])
        assert q.id == 1
        assert q.text == 'species?'

    def test_string(self) -> None:
        q = survey.MultipleChoiceQuestion(1, "species?",
                                          ["human", 'bug', 'owl'])
        s = str(q)
        assert q.text in s
        assert "human" in s
        assert "owl" in s

    def test_validate_answer(self) -> None:
        q = survey.MultipleChoiceQuestion(1, "species?",
                                          ["human", 'bug', 'owl'])
        a1 = survey.Answer("human")
        a2 = survey.Answer("bug")
        a3 = survey.Answer("rip")
        assert q.validate_answer(a1) == a1.is_valid(q)
        assert q.validate_answer(a1)
        assert q.validate_answer(a2)
        assert not q.validate_answer(a3)

    def test_similarity(self) -> None:
        q = survey.MultipleChoiceQuestion(1, "species?",
                                          ["human", 'bug', 'owl'])
        a1 = survey.Answer("human")
        a2 = survey.Answer("human")
        a3 = survey.Answer("owl")
        assert q.get_similarity(a1, a2) == 1.0
        assert q.get_similarity(a2, a3) == 0.0
        assert q.get_similarity(a1, a3) == 0.0


class TestNumQuestion:
    """
    numeric
    """
    def test_num_properties(self) -> None:
        q = survey.NumericQuestion(4, "number of legs?", 1, 8)
        assert q.id == 4
        assert q.text == 'number of legs?'

    def test_string(self) -> None:
        q = survey.NumericQuestion(4, "number of legs?", 1, 8)
        s = str(q)
        assert q.text in s
        assert "1" in s
        assert "8" in s

    def test_validate_answer(self) -> None:
        q = survey.NumericQuestion(4, "number of legs?", 1, 8)
        a1 = survey.Answer(1)
        a2 = survey.Answer(8)
        a3 = survey.Answer(11)
        assert q.validate_answer(a1)
        assert q.validate_answer(a2)
        assert not q.validate_answer(a3)

    def test_similarity(self) -> None:
        q = survey.NumericQuestion(4, "number of legs?", 1, 9)
        a1 = survey.Answer(1)
        a2 = survey.Answer(9)
        a3 = survey.Answer(3)
        assert q.get_similarity(a1, a2) == 0.0
        assert q.get_similarity(a2, a3) == 0.25
        assert q.get_similarity(a1, a3) == 0.75


class TestYNQuestion:
    """
    yes/no
    """
    def test_yesno_properties(self) -> None:
        q = survey.YesNoQuestion(44, "are you human?")
        assert q.id == 44
        assert q.text == 'are you human?'

    def test_string(self) -> None:
        q = survey.YesNoQuestion(44, "are you human?")
        s = str(q)
        assert q.text in s

    def test_validate_answer(self) -> None:
        q = survey.YesNoQuestion(44, "are you human?")
        a1 = survey.Answer(True)
        a2 = survey.Answer(False)
        a3 = survey.Answer("yep")
        assert q.validate_answer(a1)
        assert q.validate_answer(a2)
        assert not q.validate_answer(a3)

    def test_get_similarity(self) -> None:
        q = survey.YesNoQuestion(44, "are you human?")
        a1 = survey.Answer(True)
        a2 = survey.Answer(False)
        a3 = survey.Answer(False)
        assert q.get_similarity(a1, a2) == 0.0
        assert q.get_similarity(a2, a3) == 1.0
        assert q.get_similarity(a1, a3) == 0.0


class TestCheckboxQuestion:
    """
    mcq
    """
    def test_checkbox_properties(self) -> None:
        q = survey.CheckboxQuestion(44, "type?", ["chaotic", "evil", "neutral"])
        assert q.id == 44
        assert q.text == 'type?'

    def test_string(self) -> None:
        q = survey.CheckboxQuestion(44, "type?", ["chaotic", "evil", "neutral"])
        s = str(q)
        assert q.text in s

    def test_validate_answer(self) -> None:
        q = survey.CheckboxQuestion(44, "type?", ["chaotic", "evil", "neutral"])
        a1 = survey.Answer(["chaotic", "evil"])
        a2 = survey.Answer(["evil", "neutral"])
        a3 = survey.Answer(["neutral", "good"])
        assert q.validate_answer(a1)
        assert q.validate_answer(a2)
        assert not q.validate_answer(a3)

    def test_similarity(self) -> None:
        q = survey.CheckboxQuestion(44, "type?", ["chaotic", "evil", "neutral"])
        a1 = survey.Answer(["chaotic", "evil"])
        a2 = survey.Answer(["evil", "neutral"])
        a3 = survey.Answer(["neutral"])
        assert q.get_similarity(a1, a2) == 0.3333333333333333
        assert q.get_similarity(a2, a3) == 0.5
        assert q.get_similarity(a1, a3) == 0.0


class TestCriterion:
    question1 = survey.CheckboxQuestion(1, "species?", ["human", 'bug', 'owl'])
    a11 = survey.Answer(["human", "bug"])
    a12 = survey.Answer(["human"])
    a13 = survey.Answer(["owl"])
    answers1 = [a11, a12, a13]
    question2 = survey.NumericQuestion(4, "number of legs?", 1, 8)
    a21 = survey.Answer(1)
    a22 = survey.Answer(4)
    a23 = survey.Answer(8)
    answers2 = [a21, a22, a23]
    answers3 = [a21, a21, a21]

    def test_homogeneous(self) -> None:
        hom = criterion.HomogeneousCriterion()
        assert hom.score_answers(self.question1, self.answers1) \
            == 0.16666666666666666
        assert hom.score_answers(self.question2, self.answers2) \
            == 0.3333333333333333

    def test_heterogeneous(self) -> None:
        het = criterion.HeterogeneousCriterion()
        assert het.score_answers(self.question1, self.answers1) \
            == 0.8333333333333334
        assert het.score_answers(self.question2, self.answers2) \
            == 0.6666666666666667

    def test_lonely(self) -> None:
        sad = criterion.LonelyMemberCriterion()
        assert sad.score_answers(self.question2, self.answers2) == 0.0
        assert sad.score_answers(self.question2, self.answers3) == 1.0


class TestGrouper:

    q1 = survey.MultipleChoiceQuestion(1, "species?", ["human", 'bug', 'owl'])
    q2 = survey.YesNoQuestion(2, "are you human?")
    q3 = survey.CheckboxQuestion(3, "type?", ["chaotic", "evil", "neutral"])
    q4 = survey.NumericQuestion(4, "number of legs?", 1, 8)
    s = survey.Survey([q1, q2, q3, q4])
    c = course.Course("Learning 101")

    def answer_questions(self) -> List[course.Student]:
        # students
        s1 = course.Student(2, "First")
        s1.set_answer(self.q1, survey.Answer("owl"))
        s1.set_answer(self.q2, survey.Answer(False))
        s1.set_answer(self.q3, survey.Answer(["chaotic", "evil"]))
        s1.set_answer(self.q4, survey.Answer(1))
        s2 = course.Student(25, "Second")
        s2.set_answer(self.q1, survey.Answer("bug"))
        s2.set_answer(self.q2, survey.Answer(False))
        s2.set_answer(self.q3, survey.Answer(["chaotic", "evil", "neutral"]))
        s2.set_answer(self.q4, survey.Answer(8))
        s3 = course.Student(34, "Third")
        s3.set_answer(self.q1, survey.Answer("human"))
        s3.set_answer(self.q2, survey.Answer(True))
        s3.set_answer(self.q3, survey.Answer(["chaotic", "neutral"]))
        s3.set_answer(self.q4, survey.Answer(5))
        s4 = course.Student(9, "Fourth")
        s4.set_answer(self.q1, survey.Answer("owl"))
        s4.set_answer(self.q2, survey.Answer(False))
        s4.set_answer(self.q3, survey.Answer(["neutral"]))
        s4.set_answer(self.q4, survey.Answer(2))
        s5 = course.Student(89, "Last")
        s5.set_answer(self.q1, survey.Answer("human"))
        s5.set_answer(self.q2, survey.Answer(True))
        s5.set_answer(self.q3, survey.Answer(["evil"]))
        s5.set_answer(self.q4, survey.Answer(7))
        s = [s1, s2, s3, s4, s5]
        return s

    def test_course_all_answered(self) -> None:
        self.c.enroll_students(self.answer_questions())
        assert self.c.all_answered(self.s)

    def test_score_students(self) -> None:
        self.c.enroll_students(self.answer_questions())
        assert self.s.score_students(self.answer_questions()) \
               == 0.34761904761904766
        assert self.s.score_students(self.answer_questions()[:3]) \
               == 0.3055555555555555
        assert self.s.score_students(self.answer_questions()[2:4]) \
               == 0.26785714285714285

    def test_alpha_grouper(self) -> None:
        self.c.enroll_students(self.answer_questions())
        g = grouper.AlphaGrouper(3)
        gps = g.make_grouping(self.c, self.s).get_groups()
        assert len(gps) == 2
        assert gps[1].get_members()[1].id == 34
        assert len(gps[1].get_members()) == 2
        g = grouper.AlphaGrouper(2)
        gps = g.make_grouping(self.c, self.s).get_groups()
        assert gps[1].get_members()[1].id == 25  # number incorrect
        assert len(gps) == 3
        h = []
        for group in gps:
            h.extend(group.get_members())
        for student in self.c.students:
            assert student in h

    def test_score_grouping(self) -> None:
        self.c.enroll_students(self.answer_questions())
        g = grouper.AlphaGrouper(3)
        gps = g.make_grouping(self.c, self.s)
        assert self.s.score_grouping(gps) == 0.3125
        self.c.enroll_students(self.answer_questions())
        g2 = grouper.GreedyGrouper(3)
        gps2 = g2.make_grouping(self.c, self.s)
        assert self.s.score_grouping(gps2) == 0.5892857142857143

    def test_random_grouper(self) -> None:
        self.c.enroll_students(self.answer_questions())
        g = grouper.RandomGrouper(3)
        gps = g.make_grouping(self.c, self.s).get_groups()
        assert len(gps) == 2
        assert len(gps[1].get_members()) == 2
        g = grouper.RandomGrouper(2)
        gps = g.make_grouping(self.c, self.s).get_groups()
        assert len(gps) == 3
        h = []
        for group in gps:
            h.extend(group.get_members())
        for student in self.c.students:
            assert student in h

    def test_greedy_grouper(self) -> None:
        self.c.enroll_students(self.answer_questions())
        g = grouper.GreedyGrouper(3)
        gps = g.make_grouping(self.c, self.s).get_groups()
        assert len(gps) == 2
        assert gps[1].get_members()[1].id == 89
        assert len(gps[1].get_members()) == 2
        g = grouper.GreedyGrouper(2)
        gps = g.make_grouping(self.c, self.s).get_groups()
        assert len(gps) == 3
        assert gps[1].get_members()[1].id == 34
        h = []
        for group in gps:
            h.extend(group.get_members())
        for student in self.c.students:
            assert student in h

    def test_window_grouper(self) -> None:
        self.c.enroll_students(self.answer_questions())
        g = grouper.WindowGrouper(3)
        gps = g.make_grouping(self.c, self.s).get_groups()
        assert len(gps) == 2
        assert gps[0].get_members()[1] == 9  # number incorrect
        assert len(gps[1].get_members()) == 2
        h = []
        for group in gps:
            h.extend(group.get_members())
        for student in self.c.students:
            assert student in h

class TestSurvey:

    q1 = survey.MultipleChoiceQuestion(1, "species?", ["human"])
    q5 = survey.YesNoQuestion(5, "are you human?")
    q3 = survey.CheckboxQuestion(3, "type?", ["fae"])
    q4 = survey.NumericQuestion(4, "number of legs?", 1, 5)
    q2 = survey.Question(2, "are you human?")
    qs = [q1, q4, q3, q2, q3, q5]  # list of questions
    questions = [q1, q4, q3, q5]

    def test_survey_properties(self) -> None:
        s = survey.Survey(self.qs)
        assert len(s) == 5
        for q in self.qs:
            assert q in s

    def test_get_questions(self) -> None:
        s = survey.Survey(self.questions)
        descr = s.get_questions()
        assert self.q1 in descr
        assert self.q2 not in descr
        assert self.q3 in descr
        assert self.q4 in descr
        assert self.q5 in descr

    def test_set_weight(self) -> None:
        s = survey.Survey(self.questions)
        assert s.set_weight(2, self.q1)
        assert s.set_weight(5, self.q5)
        assert s.set_weight(-1, self.q3)
        assert not s.set_weight(2, self.q2)

    def test_set_criterion(self) -> None:
        s = survey.Survey(self.questions)
        assert s.set_criterion(criterion.LonelyMemberCriterion(), self.q1)
        assert s.set_criterion(criterion.HeterogeneousCriterion(), self.q5)
        assert not s.set_criterion(criterion.HomogeneousCriterion(), self.q2)


if __name__ == '__main__':
    pytest.main(['tests.py'])
