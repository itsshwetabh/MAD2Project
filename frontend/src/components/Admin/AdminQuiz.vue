
<template>
    <div class="admin-quiz-page">
        <h1>Quiz Management</h1>
        
        
        <div class="quiz-container">
            <QuizCard v-for="quiz in quizzes" :key="quiz.id" :quiz="quiz" />
        </div>
        <AddQuizButton @openQuizForm="openForm = true" />
        <QuizForm :isOpen="openForm" @closeQuizForm="openForm = false" />
    </div>
</template>

<script>
import QuizCard from "./Cards/QuizCard.vue";
import AddQuizButton from './Cards/Buttons/AddQuizButton.vue';
import QuizForm from './QuizForm.vue';

export default {
    name: "AdminQuizPage",
    components: {
        QuizCard,
        AddQuizButton,
        QuizForm
    },
    data() {
        return {
            openForm: false,
            quizzes: [] 
        };
    },
    mounted() {
        this.$store.dispatch("fetchQuiz").then(() => {
            this.quizzes = this.$store.state.Quiz; 
        });
        this.$store.dispatch("fetchQuestion")
    },
    computed: {
        quizzes() {
            return this.$store.state.Quiz;
        }
    }

};
</script>

<style scoped>
.admin-quiz-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: #f8f9fa;
    height: 80vh;
    overflow: auto;
}

h1 {
    font-size: 24px;
    color: #333;
    margin-bottom: 20px;
}

.quiz-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
    width: 100%;
}
</style>
