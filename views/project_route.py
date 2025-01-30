from flask import Blueprint, request, jsonify
from models import Project, db

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects', methods=['POST'])
def create_project():
   data= request.get_json()
   
   new_project= Project(title=data['title'], description=data.get('description'), owner_id=data['owner_id'])
   
   db.session.add(new_project)
   db.session.commit()
   
   return jsonify({"message": "Project created successfully"}), 201

@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
   project= Project.query.get_or_404(project_id)
   
   return jsonify({
       "id": project.project_id,
       "title": project.title,
       "description": project.description,
       "status": project.status,
       "owner_id": project.owner_id,
       "tasks": [task.title for task in project.tasks]
     })

@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
   data= request.get_json()
   
   project= Project.query.get_or_404(project_id)

   #! Update fields only if provided in the request body.
   if 'title' in data:
       project.title= data['title']
   
   if 'description' in data:
       project.description= data['description']
   
   if 'status' in data:
       project.status= data['status']
   
   db.session.commit()
   
   return jsonify({"message": "Project updated successfully"}), 200

@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
   project= Project.query.get_or_404(project_id)

   db.session.delete(project)
   db.session.commit()

   return jsonify({"message": "Project deleted successfully"}), 200

@project_bp.route('/projects', methods=['GET'])
def list_projects():
   projects= Project.query.all()

   return jsonify([{
       "id": project.project_id,
       "title": project.title,
       "status": project.status,
       "owner_id": project.owner_id,
       "tasks_count": len(project.tasks),
     } for project in projects]), 200
