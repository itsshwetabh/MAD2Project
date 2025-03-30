

<template>
    <Teleport to="body">
        <div v-if="show" class="toast-overlay">
            <div class="toast-box">
                <h2 class="title">Quiz Details</h2>
                <div class="quiz-info">
                    <p><strong>ID:</strong> {{ quizData.id }}</p>
                    <p><strong>Subject:</strong> <span>{{ subject }}</span></p>
                    <p><strong>Chapter:</strong> <span>{{ chapter.name }}</span></p>
                    <p><strong>Number of Questions:</strong> {{ no_of_questions || 0 }}</p>
                    <p><strong>Scheduled Date:</strong> {{ quizData.date_of_quiz }}</p>
                    <p><strong>Duration (hh:mm):</strong> {{ quizData.time_duration }}</p>
                </div>
                <button @click="closeToast" class="close-btn">Close</button>
            </div>
        </div>
    </Teleport>
</template>

<script>
export default {
    name: "ViewQuiz",
    data() {
        return {
            show: false,
            quizData: {},
            no_of_questions: 0,
        };
    },
    methods: {
        openToast(quiz, no_of_questions) {
            this.show = true;
            this.quizData = quiz;
            this.no_of_questions = no_of_questions
        },
        closeToast() {
            this.show = false;
        }
    },
    computed: {
        chapter() {
            if (!this.quizData || !this.quizData.chapter_id) {
                console.log("quizData or chapter_id is not set yet.");
                return "#";
            }
            const chapter = this.$store.state.chapters.find(ch => ch.id === this.quizData.chapter_id);
            console.log(`chaptername=${chapter ? chapter.name : "Not Found"}`);
            return chapter ? chapter: "#";
        },
        subject(){
            console.log("************")
            const chapterhere = this.chapter
            console.log(`%%%%%${chapterhere.name}`)
            console.log(this.$store.state.subjects)
            const subject = this.$store.state.subjects.find(subject=> chapterhere.subject_id===subject.id)
            return subject ? subject.name : "#"
        }
    }
    ,

};
</script>

<style scoped>
/* Blurred Background */
.toast-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(8px);
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Toast Box */
.toast-box {
    background: #fff;
    border-radius: 12px;
    padding: 20px 30px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    text-align: center;
    font-family: "Arial", sans-serif;
    width: 320px;
    color: #333;
}

/* Title */
.title {
    font-size: 22px;
    margin-bottom: 15px;
    font-weight: bold;
    color: #2c3e50;
}

/* Quiz Info */
.quiz-info p {
    font-size: 16px;
    margin: 8px 0;
    font-weight: 500;
}

/* Close Button */
.close-btn {
    margin-top: 20px;
    padding: 10px 15px;
    background: #3498db;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 6px;
    font-size: 16px;
    transition: 0.3s;
}

.close-btn:hover {
    background: #2980b9;
}
</style>