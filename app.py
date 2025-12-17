from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/postomaty')
def index():
    # Данные о ячейках постомата
    cells_status = [
        {'cell_number': 1, 'documents': 'Паспорт РФ', 'department': 'Юридический отдел', 'status': 'Не отправлено'},
        {'cell_number': 2, 'documents': 'Справка о доходах', 'department': 'Бухгалтерия', 'status': 'Отправлено'},
        {'cell_number': 3, 'documents': 'Водительские права', 'department': 'Отдел кадров', 'status': 'Не отправлено'},
        {'cell_number': 4, 'documents': 'Фото 3x4', 'department': 'Отдел кадров', 'status': 'Отправлено'},
        {'cell_number': 5, 'documents': 'Трудовая книжка', 'department': 'Отдел кадров', 'status': 'Не отправлено'},
        {'cell_number': 6, 'documents': 'Диплом', 'department': 'Отдел кадров', 'status': 'Отправлено'},
        {'cell_number': 7, 'documents': 'Справка с места работы', 'department': 'Бухгалтерия', 'status': 'Не отправлено'},
        {'cell_number': 8, 'documents': 'Медицинская справка', 'department': 'Технический отдел', 'status': 'Отправлено'},
        {'cell_number': 9, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 10, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 11, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 12, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 13, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 14, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 15, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 16, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 17, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 18, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 19, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 20, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 21, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 22, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 23, 'documents': '', 'department': '', 'status': ''},
        {'cell_number': 24, 'documents': '', 'department': '', 'status': ''},
    ]

    return render_template('index.html', cells_status=cells_status, current_page='postomaty')

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

@app.route('/history')
def history():
    # История действий пользователя
    actions_history = [
        {
            'id': 1,
            'action': 'Сканирование документов',
            'description': 'Отсканирован документ: Паспорт РФ',
            'timestamp': '17.12.2025 15:30:15',
            'status': 'success',
            'user': 'Иванов И.И.'
        },
        {
            'id': 2,
            'action': 'Сканирование документов',
            'description': 'Отсканирован документ: Справка о доходах',
            'timestamp': '17.12.2025 15:25:42',
            'status': 'success',
            'user': 'Иванов И.И.'
        },
        {
            'id': 3,
            'action': 'Размещение документов',
            'description': 'Помещен документ "Паспорт РФ" в ячейку №1 для отдела "Юридический отдел"',
            'timestamp': '17.12.2025 15:20:33',
            'status': 'success',
            'user': 'Иванов И.И.'
        },
        {
            'id': 4,
            'action': 'Отправка уведомлений',
            'description': 'Отправлены уведомления получателям о готовности документов',
            'timestamp': '17.12.2025 15:15:21',
            'status': 'success',
            'user': 'Иванов И.И.'
        },
        {
            'id': 5,
            'action': 'Изменение статуса регистрации',
            'description': 'Изменен статус регистрации документа "Водительские права" на "Требует регистрации в ЕАСД-2"',
            'timestamp': '17.12.2025 15:10:18',
            'status': 'info',
            'user': 'Иванов И.И.'
        },
        {
            'id': 6,
            'action': 'Сканирование документов',
            'description': 'Отсканирован документ: Водительские права',
            'timestamp': '17.12.2025 15:08:55',
            'status': 'success',
            'user': 'Иванов И.И.'
        },
        {
            'id': 7,
            'action': 'Выбор сканера',
            'description': 'Выбран сканер: HP LaserJet Pro 400',
            'timestamp': '17.12.2025 15:05:12',
            'status': 'info',
            'user': 'Иванов И.И.'
        },
        {
            'id': 8,
            'action': 'Размещение документов',
            'description': 'Помещены документы в ячейку №2: Справка о доходах (Отдел: Бухгалтерия)',
            'timestamp': '17.12.2025 14:55:44',
            'status': 'success',
            'user': 'Петров П.П.'
        },
        {
            'id': 9,
            'action': 'Сканирование документов',
            'description': 'Отсканирован документ: Фото 3x4',
            'timestamp': '17.12.2025 14:50:22',
            'status': 'success',
            'user': 'Петров П.П.'
        },
        {
            'id': 10,
            'action': 'Изменение статуса регистрации',
            'description': 'Изменен статус регистрации документа "Справка о доходах" на "Регистрация не требуется"',
            'timestamp': '17.12.2025 14:45:31',
            'status': 'warning',
            'user': 'Петров П.П.'
        }
    ]
    
    return render_template('history.html',
                         actions_history=actions_history,
                         current_page='history')

if __name__ == '__main__':
    app.run(debug=True)
