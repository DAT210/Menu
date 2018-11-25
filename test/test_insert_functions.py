import unittest
import update_functions
import get_functions
import test_database
import mysql.connector
from exceptions import *
from insert_functions import *
from mysql.connector import errorcode, IntegrityError, DataError, Error

# Magnus Steinstø

def get_db():
    return mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='test_menu')


class TestInsertFunctions(unittest.TestCase):

    def setUp(self):
        # Called before each test
        test_database.create_test_db()


    def tearDown(self):
        # Called after every test
        test_database.drop_test_db()


    def test_insert_course(self):
        db = get_db()
        # Valid input
        insert_course(db, "insert course", 3.67)
        cur = db.cursor()
        try:
            cur.execute("SELECT c_name, price FROM course WHERE c_id = (SELECT MAX(c_id) FROM course)")
            values = cur.fetchone()
            name = values[0]
            price = values[1]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(name, "insert course")
        self.assertEqual(str(price), str(3.67))

        # Insert invalid name
        self.assertEqual(insert_course(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4.56),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert invalid price
        self.assertEqual(insert_course(db, "course with valid name", "a"),
                         INVALID_DECIMAL_VALUE)

        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_course(db, "course alpha", 2.13),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_course(db, None, 5.78),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty price
        self.assertEqual(insert_course(db, "course unique name", None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_ingredient(self):
        db = get_db()
        # Valid input
        insert_ingredient(db, "insert ingredient", False)
        cur = db.cursor()
        try:
            cur.execute("SELECT i_name, available FROM ingredient WHERE i_id = (SELECT MAX(i_id) FROM ingredient)")
            values = cur.fetchone()
            name = values[0]
            availability = values[1]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(name, "insert ingredient")
        self.assertEqual(availability, False)

        # Insert invalid name
        self.assertEqual(insert_ingredient(db,"asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", True),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert invalid availability
        self.assertEqual(insert_ingredient(db, "ingredient with valid name", "a"),
                         INVALID_TYPE_EXCEPTION)

        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_ingredient(db, "ingredient alpha", True),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_ingredient(db, None, False),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty availability
        self.assertEqual(insert_ingredient(db, "ingredient unique name", None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_allergene(self):
        db = get_db()
        # Valid input
        insert_allergene(db, "insert allergene")
        cur = db.cursor()
        try:
            cur.execute("SELECT a_name FROM allergene WHERE a_id = (SELECT MAX(a_id) FROM allergene)")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(name, "insert allergene")

        # Insert invalid name
        self.assertEqual(insert_allergene(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf"),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_allergene(db, "allergene alpha"),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_allergene(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_course_ingredient(self):
        db = get_db()
        # Valid input
        insert_course_ingredient(db, 3, 2)
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id, i_id FROM course_ingredient WHERE c_id = 3 AND i_id = 2")
            values = cur.fetchone()
            course = values[0]
            ingredient = values[1]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(course, 3)
        self.assertEqual(ingredient, 2)

        # Insert invalid course reference
        self.assertEqual(insert_course_ingredient(db, 999, 3),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid ingredient reference
        self.assertEqual(insert_course_ingredient(db, 5, 999),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid course value
        self.assertEqual(insert_course_ingredient(db, "a", 3),
                         INVALID_TYPE_EXCEPTION)

        # Insert invalid ingredient value
        self.assertEqual(insert_course_ingredient(db, 5, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Insert with empty course value
        self.assertEqual(insert_course_ingredient(db, None, 3),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty ingredient value
        self.assertEqual(insert_course_ingredient(db, 3, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()

    def test_ingredient_allergene(self):
        db = get_db()
        # Valid input
        insert_ingredient_allergene(db, 3, 2)
        cur = db.cursor()
        try:
            cur.execute("SELECT i_id, a_id FROM ingredient_allergene WHERE i_id = 3 AND a_id = 2")
            values = cur.fetchone()
            ingredient = values[0]
            allergene = values[1]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(ingredient, 3)
        self.assertEqual(allergene, 2)

        # Insert invalid ingredient reference
        self.assertEqual(insert_ingredient_allergene(db, 999, 3),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid allergene reference
        self.assertEqual(insert_ingredient_allergene(db, 3, 999),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid ingredient value
        self.assertEqual(insert_ingredient_allergene(db, "a", 3),
                         INVALID_TYPE_EXCEPTION)

        # Insert invalid allergene value
        self.assertEqual(insert_ingredient_allergene(db, 3, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Insert with empty ingredient value
        self.assertEqual(insert_ingredient_allergene(db, None, 3),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty allergene value
        self.assertEqual(insert_ingredient_allergene(db, 4, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


if __name__ == '__main__':
    unittest.main()