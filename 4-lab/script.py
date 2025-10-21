import sqlite3

conn = sqlite3.connect('company_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_finance_status (
        project_id INTEGER PRIMARY KEY,
        project_name TEXT NOT NULL,
        utilization_percent REAL NOT NULL,
        status TEXT NOT NULL
    )
''')

cursor.execute('''
    INSERT INTO project_finance_status (
        project_id,
        project_name,
        utilization_percent,
        status
    )
    SELECT
        project_id,
        project_name,
        ROUND((spent / budget) * 100, 2) AS utilization_percent,
        CASE
            WHEN (spent / budget) * 100 > 90 THEN 'Рисковые'
            ELSE 'Стабильные'
        END AS status
    FROM Projects;
''')

conn.commit()
conn.close()