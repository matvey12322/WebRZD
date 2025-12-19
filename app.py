from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from pathlib import Path
from datetime import datetime
import asyncio
from postomat_client import get_status, open_cell, scan_folder, send_email, generate_barcode

app = Flask(__name__)

# Minimal POC data storage - in-memory
cells_data = {}  # cell_id: {'documents': [], 'department': None, 'status': None}
scanned_staging = []  # [{'id': str, 'name': str, 'scanned_at': str}]
documents_folder = Path('scanned_documents')

# Hardcoded cells for POC (24 cells, all empty initially)
hardcoded_cells = [
    {'id': i, 'name': str(i), 'cell_id': i, 'active': 1, 'session_id': None, 'position': None, 'block': None, 'created_at': datetime.now(), 'updated_at': datetime.now()}
    for i in range(1, 25)
]

# Departments
departments = [
    'Юридический отдел',
    'Бухгалтерия',
    'Отдел кадров',
    'Технический отдел',
    'Отдел маркетинга',
    'Служба безопасности'
]

@app.route('/')
@app.route('/postomaty')
def index():
    # Build cells_status from hardcoded_cells and cells_data
    cells_status = []
    for cell in hardcoded_cells:
        cell_id = cell['cell_id']
        if cell_id in cells_data:
            data = cells_data[cell_id]
            documents = ', '.join(data.get('documents', [])) if data.get('documents') else ''
            department = data.get('department', '')
            status = data.get('status', '')
        else:
            documents = ''
            department = ''
            status = ''
        cells_status.append({
            'cell_number': cell_id,
            'documents': documents,
            'department': department,
            'status': status
        })

    return render_template('index.html', cells_status=cells_status, current_page='postomaty')

@app.route('/scan-documents')
def scan_documents():
    # Mock scanning devices
    scanning_devices = [
        {'id': 'scanner_1', 'name': 'HP LaserJet Pro 400', 'status': 'Готов к сканированию', 'connected': True},
        {'id': 'scanner_2', 'name': 'Canon ImageCLASS', 'status': 'Занят', 'connected': True},
        {'id': 'scanner_3', 'name': 'Brother DCP-7030', 'status': 'Отключен', 'connected': False},
    ]

    # Show staged documents
    scanned_documents = scanned_staging.copy()

    return render_template('scan_documents.html',
                         scanning_devices=scanning_devices,
                         scanned_documents=scanned_documents,
                         current_page='scan-documents')

@app.route('/put-documents')
def put_documents():
    # Get scanned documents from folder
    documents_folder.mkdir(exist_ok=True)
    scanned_files = scan_folder(documents_folder)
    scanned_documents = []
    for i, filename in enumerate(scanned_files):
        scanned_documents.append({
            'id': f'doc_{i+1}',
            'name': filename,
            'requires_registration': True,  # Mock
            'scanned_at': datetime.now().strftime('%d.%m.%Y %H:%M')
        })

    # Recipients (departments)
    recipients = departments

    # Cells status
    cells = []
    for i in range(1, 25):
        if i in cells_data:
            status = 'occupied'
            documents = cells_data[i].get('documents', [])
            recipient = cells_data[i].get('department')
        else:
            status = 'free'
            documents = []
            recipient = None
        cells.append({
            'id': i,
            'number': i,
            'status': status,
            'documents': documents,
            'recipient': recipient
        })

    return render_template('put_documents.html',
                         scanned_documents=scanned_documents,
                         recipients=recipients,
                         cells=cells,
                         current_page='put-documents')

@app.route('/scan', methods=['POST'])
def scan():
    # Mock scan: add to staging
    doc_name = request.form.get('doc_name', f'document_{len(scanned_staging)+1}.pdf')
    scanned_staging.append({
        'id': f'staged_{len(scanned_staging)+1}',
        'name': doc_name,
        'scanned_at': datetime.now().strftime('%d.%m.%Y %H:%M')
    })
    return jsonify({'status': 'success', 'message': f'Document {doc_name} scanned'})

@app.route('/save-scan', methods=['POST'])
def save_scan():
    # Move staged documents to network folder
    documents_folder.mkdir(exist_ok=True)
    for doc in scanned_staging:
        # Create dummy file
        file_path = documents_folder / doc['name']
        file_path.write_text(f'Mocked scanned document: {doc["name"]}')
    scanned_staging.clear()  # Clear staging
    return jsonify({'status': 'success', 'message': 'Documents saved to network folder'})

@app.route('/assign-document', methods=['POST'])
def assign_document():
    doc_name = request.form.get('doc_name')
    cell_id = int(request.form.get('cell_id'))
    department = request.form.get('department')

    if cell_id not in cells_data:
        cells_data[cell_id] = {'documents': [], 'department': None, 'status': None}

    cells_data[cell_id]['documents'].append(doc_name)
    cells_data[cell_id]['department'] = department
    cells_data[cell_id]['status'] = 'Не отправлено'

    return jsonify({'status': 'success', 'message': f'Document assigned to cell {cell_id}'})

@app.route('/send-notifications', methods=['POST'])
def send_notifications():
    # Send emails for all "not sent" documents
    sent_count = 0
    for cell_id, data in cells_data.items():
        if data.get('status') == 'Не отправлено':
            department = data.get('department')
            documents = data.get('documents', [])
            # Mock email send (skip actual send for POC)
            print(f'Sending email to {department} about documents: {", ".join(documents)}')
            # send_email('mock@example.com', f'{department}@example.com', 'mock_pass', 'Documents Ready', f'Documents ready: {", ".join(documents)}')
            data['status'] = 'Отправлено'
            sent_count += 1

    return jsonify({'status': 'success', 'message': f'Sent notifications for {sent_count} cells'})

@app.route('/history')
def history():
    # Mock history for now
    actions_history = [
        {
            'id': 1,
            'action': 'Сканирование документов',
            'description': 'Отсканирован документ: Паспорт РФ',
            'timestamp': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            'status': 'success',
            'user': 'Иванов И.И.'
        }
    ]

    return render_template('history.html',
                         actions_history=actions_history,
                         current_page='history')

if __name__ == '__main__':
    app.run(debug=True)
