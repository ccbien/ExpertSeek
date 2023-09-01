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
        
        
    def get_paper(self, paper_id):
        """Get paper by id"""
        query = f"""
            SELECT * FROM papers
            WHERE paper_id = '{paper_id}'
        """
        attrs = ["paper_id", "title", "doi", "year", "n_citation", "abstract"]
        data = [{attr: value for attr, value in zip(attrs, row)}
                    for row in self.execute(query)]
        return data[0]
    
    
    def get_author(self, author_id):
        """Get author by id"""
        query = f"""
            SELECT * FROM authors
            WHERE author_id = '{author_id}'
        """
        attrs = ["author_id", "name", "org"]
        data = [{attr: value for attr, value in zip(attrs, row)}
                    for row in self.execute(query)]
        return data[0]

    
    def get_top_coauthors(self, author_id, limit):
        """Get authors with the most collaborations"""
        query = f"""
            SELECT a2.author_id, COUNT(*) AS co_author_count
            FROM paper_author AS a1
            JOIN paper_author AS a2
            ON a1.paper_id = a2.paper_id AND a1.author_id <> a2.author_id
            WHERE a1.author_id = '{author_id}'
            GROUP BY a2.author_id
            ORDER BY co_author_count DESC
            LIMIT {limit}; 
        """
        attrs = ["author_id", "count"]
        data = [{attr: value for attr, value in zip(attrs, row)}
                    for row in self.execute(query)]
        return data
    
    
    def get_num_citations(self, author_id):
        """Get number of citation of an author"""
        query = f"""
            SELECT pa.author_id, SUM(p.n_citation) AS total_citations
            FROM paper_author AS pa
            JOIN papers AS p ON pa.paper_id = p.paper_id
            WHERE pa.author_id = '{author_id}'
            GROUP BY pa.author_id;
        """
        data = self.execute(query)
        return data[0][1]
    
    
    def search_authors(self, name, org, limit):
        """Search authors by name and organization, sort the result by the number of citations"""
        query = f"""
            SELECT a.author_id, a.name, a.org, SUM(p.n_citation) AS total_citations
            FROM authors AS a
            LEFT JOIN paper_author AS pa ON a.author_id = pa.author_id
            LEFT JOIN papers AS p ON pa.paper_id = p.paper_id
            WHERE (LOWER(a.name) LIKE LOWER('%{name}%') AND LOWER(a.org) LIKE LOWER('%{org}%'))
            GROUP BY a.author_id, a.name, a.org
            ORDER BY total_citations DESC
            LIMIT {limit};
        """
        attrs = ["author_id", "name", "org", "n_citation"]
        data = [{attr: value for attr, value in zip(attrs, row)}
                    for row in self.execute(query)]
        return data
    
    
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
