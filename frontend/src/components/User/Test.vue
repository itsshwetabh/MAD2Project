<template>
  <div class="quiz-container">

    <div class="header">

      <div class="question-number">
        <span>QNo. <strong>{{ currentQuestionIndex + 1 }}/{{ quizQuestions.length }}</strong></span>
      </div>


      <div class="timer">
        ⏳ {{ formattedTime }}
      </div>
    </div>


    <div class="question-box">
      <div class="questionHeader">
        <h2>{{ quizQuestions[currentQuestionIndex]?.question_statement }} </h2>
        <h3>marks:{{quizQuestions[currentQuestionIndex]?.marks}}</h3>
      </div>
      
      <div class="options">
        <label class="option-label"
          v-for="(option, index) in [quizQuestions[currentQuestionIndex]?.option_1, quizQuestions[currentQuestionIndex]?.option_2, quizQuestions[currentQuestionIndex]?.option_3, quizQuestions[currentQuestionIndex]?.option_4]"
          :key="index">
          <input type="radio" :name="'question_' + currentQuestionIndex" :value="index + 1"
            v-model="selectedAnswers[(quizQuestions[currentQuestionIndex])?.id]" class="radio-input"
            @change="saveAnswersToStorage" />
          <span class="custom-radio"></span> {{ option }}
        </label>
      </div>
    </div>


    <div class="buttons">
      <button v-if="currentQuestionIndex > 0" @click="previousQuestion">Previous</button>
      <button v-if="currentQuestionIndex < quizQuestions.length - 1" @click="saveAndNext">Next</button>
      <button v-else @click="submitQuiz">Submit</button>
    </div>
  </div>
</template>

<script>
import axios from "axios"
export default {
  data() {
    return {
      currentQuestionIndex: 0,
      selectedAnswers: {},
      timer: this.convertTimeToSeconds("01:06:00"),
      timerInterval: null,
      quizData: null,
      quizQuestions: [],
    };
  },
  props: {
    id: String
  },
  computed: {
    formattedTime() {
      const hours = Math.floor(this.timer / 3600);
      const minutes = Math.floor((this.timer % 3600) / 60);
      const seconds = this.timer % 60;
      return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
    }
  },
  methods: {
    convertTimeToSeconds(timeString) {
      const [hours, minutes, seconds] = timeString.split(":").map(Number);
      return hours * 3600 + minutes * 60 + (seconds || 0);
    },
    saveAndNext() {
      this.saveAnswersToStorage();
      if (this.currentQuestionIndex < this.quizQuestions.length - 1) {
        this.currentQuestionIndex++;
        this.saveQuestionIndexToStorage();
      }
    },
    previousQuestion() {
      this.saveAnswersToStorage();
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
        this.saveQuestionIndexToStorage();
      }
    },
    async submitQuiz() {
      this.saveAnswersToStorage();
      const userData = JSON.parse(localStorage.getItem('userData'))

      const headers = {
        'Authentication-Token': userData.token
      }

      await axios.post(`http://127.0.0.1:5000/quizzes/attempt`, {
        user_id: userData.id,
        quiz_id: Number(this.id),
        id: Number(localStorage.getItem("attempt_id")),
        response: localStorage.getItem(`selectedAnswers_${this.id}`)


      }, {
        headers
      })


      this.$router.push(`/UserDashboard`)
      alert("Quiz Submitted!");
      console.log(this.selectedAnswers);
      localStorage.removeItem(`selectedAnswers_${this.id}`); // Clear answers on submit
      localStorage.removeItem(`currentQuestionIndex_${this.id}`); // Clear question index on submit
      localStorage.removeItem(`quizStartTime_${this.id}`)
      localStorage.removeItem("RunningQuiz")
      localStorage.removeItem("attempt_id")
      alert("Your quiz has been submitted")
      this.$router.push('/UserDashboard/home')
    }
    ,
    saveAnswersToStorage() {
      localStorage.setItem(`selectedAnswers_${this.id}`, JSON.stringify(this.selectedAnswers));
    },
    saveQuestionIndexToStorage() {
      localStorage.setItem(`currentQuestionIndex_${this.id}`, this.currentQuestionIndex);
    },
    loadAnswersAndIndexFromStorage() {
      const savedAnswers = localStorage.getItem(`selectedAnswers_${this.id}`);
      if (savedAnswers) {
        this.selectedAnswers = JSON.parse(savedAnswers);
      }

      const savedIndex = localStorage.getItem(`currentQuestionIndex_${this.id}`);
      if (savedIndex !== null) {
        this.currentQuestionIndex = parseInt(savedIndex);
      }
    },
    startTimer() {
      this.timerInterval = setInterval(() => {
        if (this.timer > 0) {
          this.timer--;
        } else {
          clearInterval(this.timerInterval);
          this.submitQuiz();
        }
      }, 1000);
    }
  },
  async mounted() {
    await this.$store.dispatch("fetchQuiz");
    await this.$store.dispatch("fetchQuestion");


    this.quizData = this.$store.state.Quiz.find(quiz => quiz.id === Number(this.id));

    if (this.quizData && this.quizData.time_duration) {
      const timeObj = new Date(`1970-01-01T${this.quizData.time_duration}Z`);
      const hours = timeObj.getUTCHours();
      const minutes = timeObj.getUTCMinutes();
      const seconds = timeObj.getUTCSeconds();
      const totalDuration = (hours * 3600) + (minutes * 60) + seconds;
      const storedStartTime = localStorage.getItem(`quizStartTime_${this.quizData.id}`);

      if (storedStartTime) {
        const elapsedTime = Math.floor((Date.now() - Number(storedStartTime)) / 1000);
        this.timer = Math.max(totalDuration - elapsedTime, 0);
      } else {
        localStorage.setItem(`quizStartTime_${this.quizData.id}`, Date.now());
        this.timer = totalDuration;
      }
    }

    this.quizQuestions = this.$store.state.questions.filter(que => que.quiz_id === Number(this.id));

    this.loadAnswersAndIndexFromStorage();
    this.startTimer();
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
  },
};
</script>

<style scoped>

.quiz-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 70%;
  margin: auto;
  margin-top: 50px;
}


.header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 10px 0;
}

.question-number {
  font-size: 18px;
  font-weight: bold;
  color: #28a745;
  background: #d4edda;
  padding: 5px 15px;
  border-radius: 8px;
}

.timer {
  font-size: 18px;
  font-weight: bold;
  color: #0056b3;
  background: #cce5ff;
  padding: 5px 15px;
  border-radius: 8px;
}

/* Question Box */
.question-box {
  width: 100%;
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  margin: 20px 0;
  border: 2px solid #007bff;
}

.options {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 15px;
}

.option-label {
  display: flex;
  align-items: center;
  width: 100%;
  font-size: 18px;
  padding: 10px;
  background: #f1f1f1;
  border-radius: 8px;
  margin: 5px 0;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
}

.option-label:hover {
  background: #e0e0e0;
}

/* Buttons */
.buttons {
  display: flex;
  gap: 10px;
}

button {
  background-color: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
}

button:hover {
  background-color: #0056b3;
}

.questionHeader{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
