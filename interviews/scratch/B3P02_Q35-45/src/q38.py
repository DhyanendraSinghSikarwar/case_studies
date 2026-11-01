# Q38: many-to-many: no enrolment, enrolled in every course (division), pairs sharing a course
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE courses(course_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE enrollments(student_id INTEGER, course_id INTEGER);   -- no primary key, so duplicates are possible
INSERT INTO students VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO courses VALUES (10,'SQL'),(20,'Stats'),(30,'ML');
INSERT INTO enrollments VALUES
 (1,10),(1,20),(1,30),
 (2,10),(2,10),(2,20),
 (3,10),(3,20),(3,30),
 (5,30);
"""
SQL_NONE = """
SELECT s.name FROM students s
WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.student_id)
ORDER BY s.student_id
"""
SQL_ALL = """
SELECT s.name
FROM students s
JOIN enrollments e ON e.student_id = s.student_id
JOIN courses c ON c.course_id = e.course_id
GROUP BY s.student_id, s.name
HAVING COUNT(DISTINCT e.course_id) = (SELECT COUNT(*) FROM courses)
ORDER BY s.student_id
"""
SQL_ALL_WRONG = """
SELECT s.name FROM students s JOIN enrollments e ON e.student_id = s.student_id
GROUP BY s.student_id, s.name
HAVING COUNT(e.course_id) = (SELECT COUNT(*) FROM courses)
ORDER BY s.student_id
"""
SQL_PAIRS = """
SELECT a.student_id AS s1, b.student_id AS s2, COUNT(*) AS shared_courses
FROM (SELECT DISTINCT student_id, course_id FROM enrollments) a
JOIN (SELECT DISTINCT student_id, course_id FROM enrollments) b ON a.course_id = b.course_id AND a.student_id < b.student_id
GROUP BY a.student_id, b.student_id
ORDER BY s1, s2
"""
SQL_PAIRS_NAIVE = SQL_PAIRS.replace("(SELECT DISTINCT student_id, course_id FROM enrollments)",
                                    "enrollments")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
col = lambda q: [r[0] for r in con.execute(q).fetchall()]
print("no enrolment:", col(SQL_NONE))
print("every course:", col(SQL_ALL))
print("every course, COUNT(e.course_id) instead of DISTINCT (wrong):", col(SQL_ALL_WRONG))
pairs = pd.read_sql_query(SQL_PAIRS, con)
print("\npairs sharing a course (deduplicated):")
print(pairs.to_string(index=False))
print("\npairs with duplicate rows not removed (shared_courses inflated):")
print(pd.read_sql_query(SQL_PAIRS_NAIVE, con).to_string(index=False))

# pandas
students = pd.read_sql_query("SELECT * FROM students", con)
courses = pd.read_sql_query("SELECT * FROM courses", con)
enr = pd.read_sql_query("SELECT * FROM enrollments", con)
none_p = students.loc[~students["student_id"].isin(enr["student_id"]), "name"].tolist()
valid = enr.drop_duplicates().merge(courses[["course_id"]], on="course_id")           # drop dups, keep real courses
n_courses = valid.groupby("student_id")["course_id"].nunique()
all_ids = n_courses[n_courses == len(courses)].index
all_p = students.loc[students["student_id"].isin(all_ids)].sort_values("student_id")["name"].tolist()
d = enr.drop_duplicates()
pp = d.merge(d, on="course_id", suffixes=("_1", "_2"))
pp = pp[pp["student_id_1"] < pp["student_id_2"]]
pairs_p = (pp.groupby(["student_id_1", "student_id_2"], as_index=False).size()
           .rename(columns={"student_id_1": "s1", "student_id_2": "s2", "size": "shared_courses"})
           .sort_values(["s1", "s2"]).reset_index(drop=True))
assert none_p == col(SQL_NONE) == ["Dev"]
assert all_p == col(SQL_ALL) == ["Asha", "Chitra"]
pd.testing.assert_frame_equal(pairs, pairs_p, check_dtype=False)
print("\npandas: no enrolment", none_p, "| every course", all_p)
print("asserts passed (pairs compared sorted by s1, s2)")

# edge: no courses at all
con.execute("DELETE FROM courses")
print("with an empty courses table, 'every course' returns:", col(SQL_ALL))
con.close()
