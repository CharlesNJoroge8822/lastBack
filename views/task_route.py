from flask import Blueprint, request, jsonify
from models import Task, db

task_bp = Blueprint('task', __name__)


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    new_task = Task(title=data['title'], description=data.get('description'), project_id=data['project_id'], assigned_to_id=data['assigned_to_id'])
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"message": "Task created successfully"}), 201


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
   task= Task.query.get_or_404(task_id)

   return jsonify({
       "id": task.task_id,
       "title": task.title,
       "description": task.description,
       "status": task.status,
       "project_id": task.project_id,
       "assigned_to_id": task.assigned_to_id,
   })

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
   data= request.get_json()
   task= Task.query.get_or_404(task_id)

   #! Update fields only if provided in the request body.
   if 'title' in data:
       task.title= data['title']
   
   if 'description' in data:
       task.description= data['description']
   
   if 'status' in data:
       task.status= data['status']
   
   db.session.commit()
   
   return jsonify({"message": "Task updated successfully"}), 200

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
   task= Task.query.get_or_404(task_id)

   db.session.delete(task)
   db.session.commit()

   return jsonify({"message": "Task deleted successfully"}), 200

@task_bp.route('/tasks', methods=['GET'])
def list_tasks():
   tasks= Task.query.all()

   return jsonify([{
       "id": task.task_id,
       "title": task.title,
       "status": task.status,
       "project_id": task.project_id,
       "assigned_to_id": task.assigned_to_id,
   } for task in tasks]), 200
