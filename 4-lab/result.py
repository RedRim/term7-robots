import sqlite3

conn = sqlite3.connect('company_data.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT * FROM project_finance_status
''')

cursor.execute('''
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
rows = cursor.fetchall()

for row in rows:
    if row[3] == 'Рисковые':
        print(row)
print('\n=====\n')
for row in rows[:5]:
    print(row)