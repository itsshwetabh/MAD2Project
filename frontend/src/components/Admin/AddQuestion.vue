<template>
  <div v-if="visible" class="overlay">
    <div class="toast-form">
      <h2>Add New Question {{ quiz_id }}</h2>
      <form @submit.prevent="submitQuestion">

        <label>Question Title:</label>
        <input v-model="question.question_title" type="text" required />

        <label>Question Statement:</label>
        <textarea v-model="question.question_statement" required></textarea>

        <label>Option 1:</label>
        <input v-model="question.option_1" type="text" required />

        <label>Option 2:</label>
        <input v-model="question.option_2" type="text" required />

        <label>Option 3:</label>
        <input v-model="question.option_3" type="text" required />

        <label>Option 4:</label>
        <input v-model="question.option_4" type="text" required />

        <label>Correct Option (1-4):</label>
        <input v-model="question.correct_option" type="number" min="1" max="4" required />

        <label>Marks:</label>
        <input v-model="question.marks" type="number" required />
        question.
        <div class="buttons">
          <button @click="addQuestion">Save and Next</button>
          <button type="button" @click="closeForm">Close</button>
        </div>
        <h3>{{ this.question }}</h3>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'AddQuestion',
  props: {
    quiz_id: Number,
  },
  data() {
    return {
      visible: false,
      question: {
        id: '',
        question_title: '',
        question_statement: '',
        option_1: '',
        option_2: '',
        option_3: '',
        option_4: '',
        correct_option: '',
        marks: '',
      },
      edit: false,
    };
  },
  methods: {
    openForm(payload) {
      this.visible = true;
      this.question.question_title = payload.question.question_title;
      this.question.question_statement = payload.question.question_statement;
      this.question.option_1 = payload.question.option_1;
      this.question.option_2 = payload.question.option_2;
      this.question.option_3 = payload.question.option_3;
      this.question.option_4 = payload.question.option_4;
      this.question.correct_option = payload.question.correct_option;
      this.question.marks = payload.question.marks;
      this.edit = payload.edit
      this.id = payload.question.id


    },
    closeForm() {
      this.visible = false;
    },
    submitQuestion() {
      this.closeForm();
    },
    async addQuestion() {
      const data = {
        id: this.id,
        quiz_id: this.quiz_id,
        question_title: this.question.question_title,
        question_statement: this.question.question_statement,
        option_1: this.question.option_1,
        option_2: this.question.option_2,
        option_3: this.question.option_3,
        option_4: this.question.option_4,
        correct_option: this.question.correct_option,
        marks: this.question.marks

      }
      const headers = {
        "Authentication-Token": JSON.parse(localStorage.getItem('userData')).token
      }
      const resp = await axios.post('http://127.0.0.1:5000/addquestion', data, { headers })
      console.log(resp)
      await this.$store.dispatch("fetchQuestion")
    }
  },
};
</script>

<style scoped>

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(5px);
  z-index:100
}


.toast-form {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  width: 600px;
  animation: fadeIn 0.3s ease-in-out;
}

h2 {
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-top: 10px;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

button {
  padding: 10px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
}

button[type="submit"] {
  background: #28a745;
  color: white;
}

button[type="button"] {
  background: #dc3545;
  color: white;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>