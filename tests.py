import course
import survey
import criterion
import grouper
import pytest
from typing import List


def test_student_properties():
    student = course.Student(1, "Hermione")
    assert student.id == 1
    assert student.name == 'Hermione'
    student2 = course.Student(1, "Hannah")
    assert student == student2
    assert str(student) == student.name

# test set answer in Student
# test get answer in Student
# test has answer in Student


def test_course_enroll():
    c = course.Course("underwater basket weaving")
    assert c.name == 'underwater basket weaving'
    assert c.students == []
    students = [course.Student(1, "ay"), course.Student(3, "bee"),
                course.Student(2, "sea")]
    c.enroll_students(students)
    assert len(c.students) == len(students)
    for s in students:
        assert s in c.students


def test_course_get_students():
    c = course.Course("mental health")
    students = [course.Student(1, "wun"), course.Student(3, "too"),
                course.Student(2, "for")]
    c.enroll_students(students)
    assert c.get_students()[1].name == 'for'

# test all answered in Course


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
    pass


class TestGrouping:
    pass


class TestQuestion:
    """
    mcq/"/
    numeric
    yesno
    checkbox
    """
    pass


class TestAnswer:
    pass


class TestCriterion:
    """
    homo
    hetero
    lonely
    """
    pass


class TestSurvey:
    pass


class TestGrouper:
    """
    alpha
    random
    greedy
    window
    """
    pass
if __name__ == '__main__':
    pytest.main(['tests.py'])
