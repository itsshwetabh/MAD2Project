import datetime
from datetime import datetime, timezone
from flask import json, request, jsonify
from flask_security  import current_user
from flask_restful import Resource, Api
from flask_security import auth_required, verify_password, hash_password, roles_required
from models import Chapter, db, Subject,Quiz,Question,QuizAttempt,UserAnswer  # Import the Subject model
from flask import current_app as app
import pytz
api = Api(app)  
datastore = app.security.datastore

class HomeResource(Resource):
    def get(self):
        return {"message": "Welcome to the home page"}  

class ProtectedResource(Resource):
    @auth_required('token')
    def get(self):
        return {"message": "Only accessible by authenticated users"}  

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"message": "Invalid inputs"}, 404  

        user = datastore.find_user(email=email)
        if not user:
            return {"message": "Invalid email"}, 404  

        if verify_password(password, user.password):
            return {
                "token": user.get_auth_token(),
                "email": user.email,
                "role": user.roles[0].name,
                "id": user.id
            }, 200  

        return {"message": "Wrong password"}, 400  

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"message": "Invalid inputs"}, 404  

        user = datastore.find_user(email=email)
        if user:
            return {"message": "User already exists"}, 404  

        try:
            datastore.create_user(email=email, password=hash_password(password), roles=['user'], active=True)
            db.session.commit()
            return {"message": "User created successfully"}, 200  
        except:
            db.session.rollback()
            return {"message": "Error creating user"}, 400  

class SubjectResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')   
        edit=data.get('edit')
        if edit:
                
            print("edit value is", edit)
            print("Received data:", data)


            editTuple = Subject.query.filter_by(id=data['subject_id']).first()

            if editTuple:  
                formatted_name = data['name'].strip().capitalize()
                editTuple.name = formatted_name
                editTuple.description = data['description']
                db.session.commit()
                return {"message": "Subject updated successfully!"}, 200
            else:
                return {"message": "Subject not found!"}, 404
            if not name or not description:
                return {"message": "Name and description are required"}, 400  

        formatted_name = name.strip().capitalize()

        existing_subject = Subject.query.filter_by(name=formatted_name).first()
        if existing_subject:
            return {"message": "Subject already exists"}, 400  

        try:
            new_subject = Subject(name=formatted_name, description=description)
            db.session.add(new_subject)
            db.session.commit()
            return {"message": "Subject added successfully", "id": new_subject.id}, 201  
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error adding subject: {str(e)}"}, 500  
    
    @auth_required('token')
    def get(self):
        try:
            subjects = Subject.query.all()  
            subject_list = [
                {"id": subject.id, "name": subject.name, "description": subject.description}
                for subject in subjects
            ]
            return {"subjects": subject_list}, 200 
        except Exception as e:
            return {"message": f"Error fetching subjects: {str(e)}"}, 500  
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self, subject_id):
        print(subject_id)
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404
        chapters = Chapter.query.filter_by(subject_id=subject_id)
        for chapter in chapters:
            db.session.delete(chapter)
        db.session.delete(subject)
        db.session.commit()
        return {"message": "Subject deleted successfully"}, 200

class ChapterResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        chapter_id = data.get('id')
        print("chapter id=",chapter_id)
        print(data)
        if(chapter_id):
            print("yes")
            chapter=Chapter.query.filter_by(id=chapter_id).first()
            chapter.name=name
            chapter.description=description
            db.session.commit()
            return {"message": "Chapter added successfully"}, 201

        if not name or not description:
            return {"message": "Name and description are required"}, 400


        formatted_name = name.strip().capitalize()

        existing_chapter = Chapter.query.filter_by(id=data.get('id')).first()
        if existing_chapter:
            return {"message": "Chapter already exists in the subject"}, 400

        try:

            print("no")
            new_chapter = Chapter(name=formatted_name, description=description, subject_id=data.get('subject_id'))
            db.session.add(new_chapter)
            db.session.commit()
            return {"message": "Chapter added successfully", "id": new_chapter.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error adding chapter: {str(e)}"}, 500

    @auth_required('token')
    def get(self):
        print(1234)
        try:
            chapters = Chapter.query.all()
            chapter_list = [
                {
                    "id": chapter.id,
                    "subject_id": chapter.subject_id,
                    "name": chapter.name,
                    "description": chapter.description
                }
                for chapter in chapters
            ]
            return {"chapters": chapter_list}, 200
        except Exception as e:
            return {"message": f"Error fetching chapters: {str(e)}"}, 500
        
    @auth_required('token')
    @roles_required('admin')
    def delete(self,chapter_id):
        try:
            chapter = Chapter.query.filter_by(id=chapter_id).first()
            db.session.delete(chapter)
            db.session.commit()
            return {"message":"Chapter deleted successfully"}
        except Exception as e:
            return {"message":"There was some error while deleting the chapter"}
        
class QuizResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        id=data.get('id')
        subject_name = data.get('subject_name')
        chapter_name = data.get('chapter_name')
        date_of_quiz = data.get('date_of_quiz') 
        time_duration = data.get('time_duration')
        print("data=",data)
        subject = Subject.query.filter_by(name=subject_name.strip().capitalize()).first()
        chapter = Chapter.query.filter_by(name=chapter_name.strip().capitalize(), subject_id=subject.id).first()
        quiz_date = datetime.strptime(date_of_quiz, "%d/%m/%Y").date()
        duration_obj = datetime.strptime(time_duration, "%H:%M").time()

        if(id):
            try:
                quiz=Quiz.query.filter_by(id=id).first()
                quiz.id=id
                quiz.chapter_id=chapter.id
                quiz.title=data.get('title')
                quiz.date_of_quiz=quiz_date
                quiz.time_duration=duration_obj
                db.session.commit()
                return {"message":"quiz edited successfully!"},201
            except Exception as e:
                return {"message":"some error occured while editing the quiz"}
                
                

        subject = Subject.query.filter_by(name=subject_name.strip().capitalize()).first()
        if not subject:
            return {"message": "Subject not found!"}, 404


        chapter = Chapter.query.filter_by(name=chapter_name.strip().capitalize(), subject_id=subject.id).first()
        if not chapter:
            return {"message": "Chapter not found in the specified subject!"}, 404


        try:
            quiz_date = datetime.strptime(date_of_quiz, "%d/%m/%Y").date()
        except ValueError:
            return {"message": "Invalid date format. Use dd/mm/yyyy."}, 400

        try:
            duration_obj = datetime.strptime(time_duration, "%H:%M").time()
        except ValueError:
            return {"message": "Invalid time format. Use hh:mm."}, 400


        try:
            new_quiz = Quiz(chapter_id=chapter.id,title=data.get('title') ,date_of_quiz=quiz_date, time_duration=duration_obj)
            
            db.session.add(new_quiz)
            db.session.commit()
            return {"message": "Quiz added successfully!", "quiz_id": new_quiz.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error adding quiz: {str(e)}"}, 500
    
    
    @auth_required('token')
    def get(self):
        print(7777)
        try:
            quizes=Quiz.query.all()
            quiz_list = [
                {
                    "id": quiz.id,
                    "chapter_id": quiz.chapter_id,
                    "name": quiz.title,
                    "date_of_quiz": str(quiz.date_of_quiz),
                    "time_duration":str(quiz.time_duration),
                    "title":quiz.title
                }
                for quiz in quizes
            ]
            print(quiz_list)
            return {"quizes": quiz_list}, 200
        except Exception as e:
            return {"message": f"Error fetching Quizes: {str(e)}"}, 500
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self, quiz_id):
        try:
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            print("#####1")
            for question in questions:
                db.session.delete(question)
                db.session.commit()
            print("#####2")
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            print("quiz=",quiz)
            print("#####3")
            if quiz:
                db.session.delete(quiz)
                db.session.commit()
                print("#####4")
                return {"message": "Quiz and associated questions deleted successfully"}, 200
            else:
                return {"message": "Quiz not found"}, 404

        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500

class QuestionResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        data =  request.get_json()
        print(data)
        id=data.get('id')
        if(id):
            try:
                que=Question.query.filter_by(id=id).first()
                que.quiz_id=data.get('quiz_id')
                que.question_title=data.get('question_title')
                que.question_statement=data.get('question_statement')
                que.option_1=data.get('option_1')
                que.option_2=data.get('option_2')
                que.option_3=data.get('option_3')
                que.option_4=data.get('option_4')
                que.correct_option=data.get('correct_option')
                que.marks=data.get('marks')
                db.session.commit()
                return {"message":"question edited successfully"}
            except:
                return {"message":"error occured during editing question"}
        quiz_id=data.get('quiz_id')
        question_title=data.get('question_title')
        question_statement=data.get('question_statement')
        option_1=data.get('option_1')
        option_2=data.get('option_2')
        option_3=data.get('option_3')
        option_4=data.get('option_4')
        correct_option=data.get('correct_option')
        marks=data.get('marks')
        question= Question(quiz_id=quiz_id,question_title=question_title,question_statement=question_statement,option_1=option_1,option_2=option_2,option_3=option_3,option_4=option_4,correct_option=correct_option,marks=marks)
        try:
            db.session.add(question)
            db.session.commit()
            return {"message":"question added successfully"}
        except:
             return {"message":"error occured during adding question"}
    

    @auth_required('token')
    def get(self):
        try:
            questions = Question.query.all()


            is_admin = "admin" in [role.name for role in current_user.roles]

            resp = [{
                "id": question.id,
                "quiz_id": question.quiz_id,
                "question_title": question.question_title,
                "question_statement": question.question_statement,
                "option_1": question.option_1,
                "option_2": question.option_2,
                "option_3": question.option_3,
                "option_4": question.option_4,
                "marks": question.marks,
                **({"correct_option": question.correct_option} if is_admin else {})  # Include correct_option only for admin
            } for question in questions]

            return {"questions": resp}
        except Exception as e:
            return {"message": f"Error fetching Quizzes: {str(e)}"}, 500
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self,question_id):
        print(question_id)
        try:
            question = Question.query.filter_by(id=question_id).first()
            db.session.delete(question)
            db.session.commit()
            return {"message":"question deleted successfully"}, 201
        except Exception as e:
            return {"message": f"Error fetching Quizes: {str(e)}"}, 500
    
    
    @auth_required()
    def post(self, quiz_id):
        user = request.json['user_id']
        attempt = QuizAttempt(user_id=user, quiz_id=quiz_id)
        db.session.add(attempt)
        db.session.commit()
        return jsonify({'message': 'Quiz attempt started', 'attempt_id': attempt.id})




class QuizAttemptResource(Resource):
    @auth_required('token')
    def post(self):
        data = request.get_json()
        attempt_id = data.get('id')
        user = data.get('user_id')
        quiz_id = data.get('quiz_id')
        ch_id=Quiz.query.filter_by(id=int(quiz_id)).first().chapter_id
        sb_id=Chapter.query.filter_by(id=ch_id).first().subject_id
        r = data.get('response')
        if(not r):
            r='{}'
        resp = json.loads(r)
        print("************************************************************")
        print("resp=",resp)
        print(type(resp))

        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(ist)

        if not attempt_id:

            attempt = QuizAttempt(user_id=user, quiz_id=quiz_id, started_at=current_time,subject_id=sb_id)
            db.session.add(attempt)
            db.session.commit()
            return {"message": 'Quiz Attempt added', "attempt_id": attempt.id}

        quiz_attempt = QuizAttempt.query.filter_by(id=attempt_id).first()
        
        if not quiz_attempt:
            return jsonify({"message": "Quiz attempt not found"}), 404


        quiz_attempt.completed_at = current_time

        if quiz_attempt.started_at.tzinfo is None:
            quiz_attempt.started_at = quiz_attempt.started_at.replace(tzinfo=ist)

        time_taken = quiz_attempt.completed_at - quiz_attempt.started_at  
        quiz_attempt.total_time_taken = int(time_taken.total_seconds())  # Store in seconds
        score=0
        max_score=0
        for keys,values in resp.items():
            question = Question.query.filter_by(id=int(keys)).first()
            question_marks = question.marks
            max_score+=question_marks
            correct_opt = question.correct_option
            if(int(correct_opt)==values):
                score+=question_marks
        print("################################################")
        print(score)
        quiz_attempt.responses=resp
        quiz_attempt.score=score
        quiz_attempt.max_score=max_score
        db.session.commit()
        return {'message': 'Quiz attempt updated', 'attempt_id': quiz_attempt.id, 'total_time': quiz_attempt.total_time_taken}
    
    
    
    @auth_required('token')
    def get(self):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(request.args)  
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%")
        attempts=[]

        try:

            user_id = request.args.get("user_id")
        
            if not user_id:
                return jsonify({"error": "Missing user_id in request"}), 400

            print("User ID received:", user_id)

            if(int(user_id)==1):
                attempts=QuizAttempt.query.all()
                print("yes user id is 1")
            else:
                attempts = QuizAttempt.query.filter_by(user_id=int(user_id)).all()

            attempt_list = [
            {
                "id": attempt.id,
                "user_id": attempt.user_id,
                "quiz_id": attempt.quiz_id,
                "subject_id":attempt.subject_id,
                "score": attempt.score,
                "max_score": attempt.max_score,
                "started_at": attempt.started_at,
                "completed_at": attempt.completed_at,
                "total_time_taken": attempt.total_time_taken,
                "responses": attempt.responses,
            }
            for attempt in attempts
            ]

            return jsonify({"attempts": attempt_list})

        except Exception as e:
            return jsonify({"error": str(e)}), 500



    
    
    
class UserAnswerResource(Resource):
    @auth_required('token')
    def post(self, attempt_id):
        data = request.json
        answer = UserAnswer(attempt_id=attempt_id, question_id=data['question_id'], selected_option=data['selected_option'], is_correct=data['is_correct'])
        db.session.add(answer)
        db.session.commit()
        return jsonify({'message': 'Answer submitted'})
    
            
            
            
            
api.add_resource(HomeResource, '/')
api.add_resource(ProtectedResource, '/protected')
api.add_resource(LoginResource, '/login')
api.add_resource(RegisterResource, '/register')
api.add_resource(SubjectResource, '/addsubject','/fetchsubjects','/subject/<int:subject_id>') 
api.add_resource(ChapterResource,'/addchapter','/fetchchapters','/deletechapter/<int:chapter_id>')
api.add_resource(QuizResource, '/addquiz','/fetchquiz','/deletequiz/<int:quiz_id>')
api.add_resource(QuestionResource,'/addquestion','/fetchquestion','/deletequestion/<int:question_id>')
api.add_resource(QuizAttemptResource, '/quizzes/attempt','/quizzes/fetchAttempts')
api.add_resource(UserAnswerResource, '/attempts/<int:attempt_id>/answer')
