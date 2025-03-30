<template>
    <div class="quiz-scores">
      <h2>Quiz Scores</h2>
      <table>
        <thead>
          <tr>
            <th>attemptID</th>
            <th>quiz_id</th>
            <th>Started_at</th>
            <th>Completed_at</th>
            <th>Score</th>
            <th>Time taken(minutes)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(quiz, index) in quizScores" :key="index">
            <td>{{ quiz.id }}</td>
            <td>{{ quiz.quiz_id }}</td>
            <td>{{ quiz.started_at}}</td>
            <td>{{ quiz.completed_at}}</td>
            <td>{{ quiz.score }}/{{ quiz.max_score }}</td>
            <td>{{ (quiz.total_time_taken /60).toFixed(2)}}</td>



          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    name:'QuizScores',
    computed:{
      quizScores(){
        console.log("Quiz Scores:", this.$store.state.quiz_attempts);
        return this.$store.state.quiz_attempts
      },
    },
    mounted(){
      this.$store.dispatch("fetchAttempts")
    }
  };
  </script>
  
  <style scoped>
  .quiz-scores {
    width: 80%;
    margin: 20px auto;
    text-align: center;
    font-family: Arial, sans-serif;
    max-height: 80vh;
    overflow:auto;
  }
  
  h2 {
    color: #333;
    margin-bottom: 15px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    background: #f9f9f9;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 10px;
  }
  
  th {
    background: #007bff;
    color: white;
  }
  
  tr:nth-child(even) {
    background: #f2f2f2;
  }
  
  tr:hover {
    background: #ddd;
  }
  </style>
  