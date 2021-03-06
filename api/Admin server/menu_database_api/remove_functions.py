from flask import render_template
import mysql.connector

from exceptions import *

remove_queries = {
    # Delete a course by c_id
    "remove_course": ["DELETE FROM course_ingredient WHERE c_id = {c_id}", "DELETE FROM course_selection WHERE c_id = {c_id}", "DELETE FROM course WHERE c_id = {c_id}"],

    # THIS FUNCTION NEEDS TO WORK PROPERLY
    # Delete an ingredient by i_id
    "remove_ingredient": ["DELETE FROM course_selection WHERE (SELECT s_id FROM (SELECT s_id, i_id FROM course_selection AS cs INNER JOIN selection AS s ON s.s_id=cs.s_id) WHERE i_id = {i_id})", "DELETE FROM selection WHERE i_id = {i_id}", "DELETE FROM ingredient_allergene WHERE i_id = {i_id}", "DELETE FROM course_ingredient WHERE i_id = {i_id}", "DELETE FROM ingredient WHERE i_id = {i_id}"],

    # Delete an allergene by a_id
    "remove_allergene": ["DELETE FROM ingredient_allergene WHERE a_id = {a_id}", "DELETE FROM allergene WHERE a_id = {a_id}"],

    # Delete an ingredient for a course by c_id and i_id
    "remove_course_ingredient": ["DELETE FROM course_ingredient WHERE c_id = {c_id} AND i_id = {i_id}"],

    # Delete a selection for a course by c_id and s_id
    "remove_course_selection": ["DELETE FROM course_selection WHERE c_id = {c_id} AND s_id = {s_id}"],

    # Delete an allergene for an ingredient by i_id and a_id
    "remove_ingredient_allergene": ["DELETE FROM ingredient_allergene WHERE i_id = {i_id} AND a_id = {a_id}"],

    # Delete a category by ca_id
    "remove_category": ["DELETE FROM category WHERE ca_id = {ca_id}"],

    # Delete a selection by s_id
    "remove_selection": ["DELETE FROM course_selection WHERE s_id = {s_id}", "DELETE FROM selection WHERE s_id = {s_id}"],

    # Delete a selection by s_id
    "remove_selection_category": ["DELETE FROM selection_category WHERE sc_id = {sc_id}"]

    # Fixing:
        # Fix delete ingredient by i_id
}


def remove_course(db, c_id):
    for q in remove_queries["remove_course"]:
        q = q.replace("{c_id}", str(c_id))
        execute_query(q, db)


def remove_ingredient(db, i_id):
    for q in remove_queries["remove_ingredient"]:
        q = q.replace("{i_id}", str(i_id))
        execute_query(q, db)


def remove_allergene(db, a_id):
    for q in remove_queries["remove_allergene"]:
        q = q.replace("{a_id}", str(a_id))
        execute_query(q, db)


def remove_course_ingredient(db, c_id, i_id):
    for q in remove_queries["remove_course_ingredient"]:
        q = q.replace("{c_id}", str(c_id)).replace("{i_id}", str(i_id))
        execute_query(q, db)


def remove_course_selection(db, c_id, s_id):
    for q in remove_queries["remove_course_selection"]:
        q = q.replace("{c_id}", str(c_id)).replace("{s_id}", str(s_id))
        execute_query(q, db)


def remove_ingredient_allergene(db, i_id, a_id):
    for q in remove_queries["remove_ingredient_allergene"]:
        q = q.replace("{i_id}", str(i_id)).replace("{a_id}", str(a_id))
        execute_query(q, db)


def remove_category(db, ca_id):
    for q in remove_queries["remove_category"]:
        q = q.replace("{ca_id}", str(ca_id))
        execute_query(q, db)


def remove_selection(db, s_id):
    for q in remove_queries["remove_selection"]:
        q = q.replace("{s_id}", str(s_id))
        execute_query(q, db)


def remove_selection_category(db, sc_id):
    for q in remove_queries["remove_selection_category"]:
        q = q.replace("{sc_id}", str(sc_id))
        execute_query(q, db)


def execute_query(query, db):
    cur = db.cursor()

    try:
        cur.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print(err)
        return render_template("error.html", msg=err)
    finally:
        cur.close()

