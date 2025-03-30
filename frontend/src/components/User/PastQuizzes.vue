<template>
  <div class="quiz-container">
    <h2 class="heading">Past Quizzes</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>No. of Questions</th>
            <th>Date</th>
            <th>Duration (hh:mm)</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <ViewQuiz ref="toastRef" />
          <tr v-for="quiz in PastQuizzes" :key="quiz.id">
            <td>{{ quiz.id }}</td>
            <td>{{ no_of_questions[quiz.id] || 0 }}</td>
            <td>{{ quiz.date_of_quiz }}</td>
            <td>{{ quiz.time_duration }}</td>
            <td>
              <button class="start-btn"  @click="setRunnigQuiz(quiz.id)" >Start</button>
              <button @click="showToast(quiz, no_of_questions[quiz.id])" class="view-btn">View</button>

            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import ViewQuiz from './ViewQuiz.vue';
import axios from "axios"
export default {

  name: "PastQuizzes",
  components: { ViewQuiz },
  data() {
    return {
      quizzes: [
        { id: 1, questions: 5, date: "01/04/2025", duration: "00:10" },
        { id: 2, questions: 10, date: "02/04/2025", duration: "00:15" },
        { id: 3, questions: 15, date: "03/04/2025", duration: "00:30" },
        { id: 4, questions: 20, date: "04/04/2025", duration: "00:40" },
        { id: 5, questions: 25, date: "05/04/2025", duration: "00:50" },
        { id: 6, questions: 30, date: "06/04/2025", duration: "01:00" },
      ],
      no_of_questions: {}
    };
  },
  methods: {
    showToast(quiz, no_of_questions) {
      this.$refs.toastRef.openToast(quiz, no_of_questions);
    },
    async setRunnigQuiz(id) {

      if (localStorage.getItem('RunningQuiz') && id != localStorage.getItem("RunningQuiz"))
        alert("Quiz is already running")
      else {
        if (!localStorage.getItem('RunningQuiz')) {
          localStorage.setItem("RunningQuiz", id)
          const userData = JSON.parse(localStorage.getItem('userData'))

          const headers = {
            'Authentication-Token': userData.token
          }

          const resp=await axios.post(`http://127.0.0.1:5000/quizzes/attempt`, {
            user_id: userData.id,
            quiz_id: Number(id),

          }, {
            headers
          })

          localStorage.setItem("attempt_id",resp.data.attempt_id)
        }
        

        this.$router.push(`test/${id}`)

      }
    }
  },

  watch: {
    "$store.state.Quiz": {
      handler(newQuizzes) {
        this.quizzes = newQuizzes;
      },
      immediate: true, 
      deep: true 
    },
    "$store.state.questions": {
      handler(newQuestions) {
        this.no_of_questions = {}
        this.quizzes.forEach((quiz) => {
          newQuestions.forEach((question) => {
            if (question.quiz_id == quiz.id) {
              if (!this.no_of_questions[quiz.id])
                this.no_of_questions[quiz.id] = 1;
              else
                this.no_of_questions[quiz.id]++;
            }

          })
        })
      },
      immediate: true, 
      deep: true 
    }
  },
  computed: {

    PastQuizzes() {
      const today = new Date();
      today.setHours(0, 0, 0, 0); 

      return this.quizzes.filter(quiz => {
        if (!quiz.date_of_quiz) {
          console.error("Missing date_of_quiz:", quiz);
          return false;
        }

        const quizDate = new Date(quiz.date_of_quiz);
        quizDate.setHours(0, 0, 0, 0); 

        return quizDate.getTime() < today.getTime(); 
      });
    }

  }




};
</script>

<style scoped>
.quiz-container {
  max-width: 80%;
  margin: 20px auto;
  padding: 20px;
  background: #ffffff;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  font-family: Arial, sans-serif;
  height: 60vh;
  overflow: auto;
}

h2 {
  text-align: center;
  color: #333;
}

.table-wrapper {
  max-height: 600px;

  overflow-y: auto;

  border-radius: 8px;
  border: 1px solid #ddd;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #e6ccb2; 
  color: white;
  position: sticky;
  top: 0;
}

th,
td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

tbody tr:hover {
  background-color: #f8f9fa;
}

.view-btn,
.start-btn {
  border: none;
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 5px;
  transition: 0.3s;
  margin-left: 5px;
}

.view-btn {
  background-color: #3498db;
  color: white;
}

.view-btn:hover {
  background-color: #2980b9;
}

.start-btn {
  background-color: #2ecc71;
  color: white;
  margin-left: 5px;
}

.start-btn:hover {
  background-color: #27ae60;
}


.table-wrapper::-webkit-scrollbar {
  width: 8px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #555;
}


.heading {
  margin-bottom: 10px;
  color: #f4a261;
}
</style>