import os
import sqlite3


class Database:
    def __init__(self, db_path):
        if not os.path.isfile(db_path):
            Database.create_database(db_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        
    def __exit__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
        
    def execute(self, query, data=()):
        self.cursor.execute(query, data)
        self.conn.commit()
        return self.cursor.fetchall()
    
    
    @staticmethod
    def create_database(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE papers (
                paper_id TEXT PRIMARY KEY,
                title TEXT,
                doi TEXT,
                year INT,
                n_citation INT,
                abstract TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE authors (
                author_id TEXT PRIMARY KEY,
                name TEXT,
                org TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE paper_author (
                paper_id TEXT,
                author_id TEXT,
                FOREIGN KEY (paper_id) REFERENCES papers(paper_id),
                FOREIGN KEY (author_id) REFERENCES authors(author_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE paper_keyword (
                paper_id TEXT,
                keyword TEXT,
                FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
    