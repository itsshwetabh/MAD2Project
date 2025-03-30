<!-- <template>
  <div class="quiz-card">
      <h2>{{ quiz.name}}</h2>
      <table>
          <thead>
              <tr>
                  <th>ID</th>
                  <th>Q_Title</th>
                  <th>Action</th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="question in questions" :key="question.id">
                  <td>{{ question.id }}</td>
                  <td>{{ question.question_title }}</td>
                  <td>
                      <button class="edit-btn" @click="editQuestion(question)">Edit</button>
                      <button class="delete-btn" @click="deleteQuestion(question.id)">Delete</button>
                  </td>
              </tr>
          </tbody>
      </table>
      <button class="add-question" @click="openToastForm({'edit':false,'question':{}})">+ Question</button>
      <AddQuestion ref="toastForm" :quiz_id="quiz.id" />
  </div>
</template>

<script>
import AddQuestion from '../AddQuestion.vue';
import axios from 'axios';
export default {
  name: 'QuizCard',
  props: {
      quiz: {
          type: Object,
          required: true
      }
  },
  methods: {
      editQuestion(question) {
          this.openToastForm({"edit":true,"question":question})
      },
      async deleteQuestion(id) {
        try{
          const token=JSON.parse(localStorage.getItem('userData')).token
          const headers={'Authentication-Token':token}
          const resp = await axios.delete(`http://127.0.0.1:5000/deletequestion/${id}`,{headers})
          alert("question deleted successfully")
          await this.$store.dispatch("fetchQuestion")
        }
        catch(e){
          alert(`error occured while deleting the question ${e}`)
        }
          
      },
      openToastForm(payload) {
      this.$refs.toastForm.openForm({"edit":payload["edit"],"question":payload["question"]});
    }
  },
  components:{
    AddQuestion
  },
  computed:{
    questions(){
      // this.$store.state.questions.forEach((elm)=>{console.log(elm)
      //   console.log(elm.quiz_id==this.quiz.id)
      // })
      let filtered_questions=(this.$store.state.questions).filter((que)=>que.quiz_id==this.quiz.id)
      console.log(`filtered questions=${filtered_questions}`)
      return filtered_questions
      // return this.$store.state.questions
    }
  },
  mounted(){
    console.log("store questions=",this.$store.questions)
  }
};
</script>

<style scoped>
.quiz-card {
  border-radius: 12px;
  padding: 20px;
  width: 400px;
  background: #ffffff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

th {
  background-color: #007bff;
  color: white;
  text-transform: uppercase;
}

button {
  margin: 5px;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease-in-out;
}

.edit-btn {
  background-color: #28a745;
  color: white;
}

.edit-btn:hover {
  background-color: #218838;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
}

.add-question {
  margin-top: 15px;
  background-color: #ff69b4;
  color: white;
  border: none;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease-in-out;
}

.add-question:hover {
  background-color: #ff1493;
}
</style>





<!- **************************************************** -->




<template>
  <div class="quiz-card">
    <QuizForm :isOpen="openForm" :quizData="quiz"  @closeQuizForm="openForm = false" />
      <button class="edit-quiz-btn" @click="editQuiz">Edit Quiz</button>
      <button class="delete-quiz-btn" @click="deleteQuiz">Delete Quiz</button>
      <h2>{{ quiz.name}}</h2>
      <table>
          <thead>
              <tr>
                  <th>ID</th>
                  <th>Q_Title</th>
                  <th>Action</th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="question in questions" :key="question.id">
                  <td>{{ question.id }}</td>
                  <td>{{ question.question_title }}</td>
                  <td>
                      <button class="edit-btn" @click="editQuestion(question)">Edit</button>
                      <button class="delete-btn" @click="deleteQuestion(question.id)">Delete</button>
                  </td>
              </tr>
          </tbody>
      </table>
      <button class="add-question" @click="openToastForm({'edit':false,'question':{}})">+ Question</button>
      <AddQuestion ref="toastForm" :quiz_id="quiz.id" />
  </div>
</template>

<script>
import AddQuestion from '../AddQuestion.vue';
import axios from 'axios';
import QuizForm from '../QuizForm.vue';
export default {
  name: 'QuizCard',
  data() {
        return {
            openForm: false,
        };
    },
  props: {
      quiz: {
          type: Object,
          required: true
      }
  },
  methods: {
      editQuiz() {
          this.openForm=true;
      },
      async deleteQuiz() {
          if (confirm("Are you sure you want to delete this quiz?")) {
              try {
                  const token = JSON.parse(localStorage.getItem("userData")).token;
                  const headers = { "Authentication-Token": token };
                  await axios.delete(`http://127.0.0.1:5000/deletequiz/${this.quiz.id}`, { headers });
                  await this.$store.dispatch("fetchQuiz");
                  await this.$store.dispatch("fetchQuestion")
              } catch (e) {
                  alert(`Error occurred while deleting the quiz: ${e}`);
              }
          }
      },
      editQuestion(question) {
          this.openToastForm({"edit":true,"question":question})
      },
      async deleteQuestion(id) {
        try{
          const token=JSON.parse(localStorage.getItem('userData')).token
          const headers={'Authentication-Token':token}
          const resp = await axios.delete(`http://127.0.0.1:5000/deletequestion/${id}`,{headers})
          await this.$store.dispatch("fetchQuestion")
        }
        catch(e){
          alert(`error occured while deleting the question ${e}`)
        }
          
      },
      openToastForm(payload) {
      this.$refs.toastForm.openForm({"edit":payload["edit"],"question":payload["question"]});
    }
  },
  components:{
    AddQuestion,
    QuizForm
  },
  computed:{
    questions(){
      let filtered_questions=(this.$store.state.questions).filter((que)=>que.quiz_id==this.quiz.id)
      return filtered_questions
    }
  },
  async mounted(){
    console.log("store questions=",this.$store.questions)
    await this.$store.dispatch("fetchQuiz")
  }
};
</script>

<style scoped>
.quiz-card {
  position: relative;
  border-radius: 12px;
  padding: 20px;
  width: 400px;
  background: #ffffff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
  text-align: center;
}

.edit-quiz-btn,
.delete-quiz-btn {
  position: absolute;
  top: 10px;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease-in-out;
}

.edit-quiz-btn {
  left: 10px;
  background-color: #28a745;
  color: white;
}

.edit-quiz-btn:hover {
  background-color: #218838;
}

.delete-quiz-btn {
  right: 10px;
  background-color: #dc3545;
  color: white;
}

.delete-quiz-btn:hover {
  background-color: #c82333;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

th {
  background-color: #007bff;
  color: white;
  text-transform: uppercase;
}

button {
  margin: 5px;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease-in-out;
}

.edit-btn {
  background-color: #28a745;
  color: white;
}

.edit-btn:hover {
  background-color: #218838;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
}

.add-question {
  margin-top: 15px;
  background-color: #ff69b4;
  color: white;
  border: none;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease-in-out;
}

.add-question:hover {
  background-color: #ff1493;
}
</style>

