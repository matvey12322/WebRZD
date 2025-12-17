from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/postomaty')
def index():
    groups = [
        {
            'name': 'Soft-logic, 656006, Малахова, 146Б',
            'items': [
                {'id': 100, 'name': 'Dev 1(VK)', 'state': 'Активен', 'date': '20.07.2020 00:52'},
                {'id': 104, 'name': 'Dev 2(Unit)', 'state': 'Активен', 'date': '20.07.2020 00:52'},
                {'id': 103, 'name': 'Dev 2(Engy)', 'state': 'Активен', 'date': '20.07.2020 00:52'},
                {'id': 101, 'name': 'Dev 2(Unit)', 'state': 'Активен', 'date': '20.07.2020 00:52'},
                {'id': 102, 'name': 'Dev 2(Engy)', 'state': 'Активен', 'date': '20.07.2020 00:52'},
            ]
        },
        {
            'name': 'Холодильник',
            'items': [{'id': 200, 'name': 'Холодильник', 'state': 'Активен', 'date': '20.07.2020 00:52'}]
        },
        {
            'name': 'Агент 3, 656031, Строителей проспект, 117',
            'items': [
                {'id': 207, 'name': 'Агент 3/p1', 'state': 'Активен', 'date': '20.07.2020 00:52'},
                {'id': 206, 'name': 'Агент 3/p2', 'state': 'Активен', 'date': '20.07.2020 00:52'},
            ]
        },
        {
            'name': 'Агент 2, 656057, Павловский тракт, 251в',
            'items': [
                {'id': 202, 'name': 'Агент 2/p1', 'state': 'Активен', 'date': '20.07.2020 00:52'},
                {'id': 201, 'name': 'Агент 2/p2', 'state': 'Активен', 'date': '20.07.2020 00:52'},
            ]
        },
        {
            'name': 'Агент 1, 656006, Балтийская, 65',
            'items': [{'id': 203, 'name': 'Агент1/p3', 'state': 'Активен', 'date': '20.07.2020 00:52'}]
        },
        {
            'name': 'Агент 1, 656922, Павловский тракт, 188',
            'items': [
                {'id': 205, 'name': 'Агент1/p1', 'state': 'Активен', 'date': '20.07.2020 00:52'},
                {'id': 204, 'name': 'Агент1/p2', 'state': 'Активен', 'date': '20.07.2020 00:52'},
            ]
        },
    ]

    return render_template('index.html', groups=groups, current_page='postomaty')

@app.route('/scan-documents')
def scan_documents():
    # Мок-данные для сканирования
    scanning_devices = [
        {'id': 'scanner_1', 'name': 'HP LaserJet Pro 400', 'status': 'Готов к сканированию', 'connected': True},
        {'id': 'scanner_2', 'name': 'Canon ImageCLASS', 'status': 'Занят', 'connected': True},
        {'id': 'scanner_3', 'name': 'Brother DCP-7030', 'status': 'Отключен', 'connected': False},
    ]
    
    scanned_documents = [
        {'id': 'doc_1', 'name': 'Паспорт РФ', 'requires_registration': True, 'scanned_at': '17.12.2025 15:30'},
        {'id': 'doc_2', 'name': 'Справка о доходах', 'requires_registration': False, 'scanned_at': '17.12.2025 15:25'},
        {'id': 'doc_3', 'name': 'Водительские права', 'requires_registration': True, 'scanned_at': '17.12.2025 15:20'},
        {'id': 'doc_4', 'name': 'Фото 3x4', 'requires_registration': False, 'scanned_at': '17.12.2025 15:15'},
    ]
    
    return render_template('scan_documents.html', 
                         scanning_devices=scanning_devices,
                         scanned_documents=scanned_documents,
                         current_page='scan-documents')

@app.route('/put-documents')
def put_documents():
    # Получаем отсканированные документы из предыдущего экрана
    scanned_documents = [
        {'id': 'doc_1', 'name': 'Паспорт РФ', 'requires_registration': True, 'scanned_at': '17.12.2025 15:30'},
        {'id': 'doc_2', 'name': 'Справка о доходах', 'requires_registration': False, 'scanned_at': '17.12.2025 15:25'},
        {'id': 'doc_3', 'name': 'Водительские права', 'requires_registration': True, 'scanned_at': '17.12.2025 15:20'},
        {'id': 'doc_4', 'name': 'Фото 3x4', 'requires_registration': False, 'scanned_at': '17.12.2025 15:15'},
    ]
    
    # Список получателей
    recipients = [
        'Юридический отдел',
        'Бухгалтерия', 
        'Отдел кадров',
        'Технический отдел',
        'Отдел маркетинга',
        'Служба безопасности'
    ]
    
    # Состояние ячеек постомата (мок-данные)
    cells = []
    for i in range(1, 25):  # 24 ячейки (6x4)
        cell = {
            'id': i,
            'number': i,
            'status': 'free',  # free, selected, occupied
            'documents': [],
            'recipient': None
        }
        cells.append(cell)
    
    return render_template('put_documents.html',
                         scanned_documents=scanned_documents,
                         recipients=recipients,
                         cells=cells,
                         current_page='put-documents')

if __name__ == '__main__':
    app.run(debug=True)
