<template>
    <div v-if="isOpen" class="modal-overlay">
        <div class="modal-container">
            <h2 class="modal-title">New Quiz</h2>

            <div class="form-group">
                <label>Quiz Title :</label>
                <input type="text" v-model="quizTitle" />
            </div>
            <div class="form-group">
                <label>Subject Name :</label>
                <select v-model="subjectName">
                    <option value="" disabled>Select Subject</option>
                    <option v-for="(subject, index) in subjects" :key="index" :value="subject.name">
                        {{ subject.name }}
                    </option>
                </select>
            </div>
            <div class="form-group">
                <label>Chapter Name :</label>
                <select v-model="chapterName">
                    <option value="" disabled>Select Chapter</option>
                    <option v-for="(chapter, index) in chapters" :key="index" :value="chapter.name">
                        {{ chapter.name }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Date :</label>
                <input type="text" placeholder="dd/mm/yyyy" v-model="date_of_quiz" />
            </div>

            <div class="form-group">
                <label>Duration :</label>
                <input type="text" placeholder="hh:mm" v-model="time_duration" />
            </div>


            <div class="button-group">
                <button class="save-btn" @click="saveQuiz">Save</button>
                <button class="cancel-btn" @click="closeQuizForm">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "QuizForm",
    props: {
        "isOpen": Boolean,
        "quizData": {
            type: Object
        }
    },
    data() {
        return {
            quiz_id: "",
            quizTitle: "",
            subjectName: "",
            chapterName: "",
            date_of_quiz: "",
            time_duration: "",
            subjects: this.$store.state.subjects,
            chapters: this.$store.state.chapters,
        };
    },
    methods: {
        closeQuizForm() {
            this.$emit("closeQuizForm");
        },
        async saveQuiz() {


            const quizData = {
                id: this.quiz_id,
                title: this.quizTitle,
                subject_name: this.subjectName,
                chapter_name: this.chapterName,
                date_of_quiz: this.date_of_quiz,  
                time_duration: this.time_duration  
            };

            try {

                const response = await fetch("http://localhost:5000/addquiz", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": JSON.parse(localStorage.getItem("userData")).token, 
                    },
                    body: JSON.stringify(quizData)
                });

                await this.$store.dispatch("fetchQuiz")

                const data = await response.json();
                if (response.ok) {
                    alert("Quiz Added Successfully!");
                    this.$emit("closeQuizForm");
                } else {
                    alert("Error: " + data.message);
                }
            } catch (error) {
                alert("Network error while adding quiz!");
            }
        },

    },
    async mounted() {
        await this.$store.dispatch("fetchSubjects")
        this.subjects = this.$store.state.subjects
        await this.$store.dispatch("fetchChapters")
        this.chapters = (this.$store.state.chapters)

    },
watch: {
    quizData: {
        handler(newData) {
            if (newData) {
                this.quiz_id = newData.id || "";
                this.quizTitle = newData.name || "";
                this.subjectName = newData.subject_name || "";
                this.chapterName = newData.chapter_name || "";


                if (newData.date_of_quiz) {
                    const date = new Date(newData.date_of_quiz);
                    if (!isNaN(date.getTime())) {
                        const day = String(date.getDate()).padStart(2, '0');
                        const month = String(date.getMonth() + 1).padStart(2, '0');
                        const year = date.getFullYear();
                        this.date_of_quiz = `${day}/${month}/${year}`;
                    } else {
                        this.date_of_quiz = newData.date_of_quiz;
                    }
                } else {
                    this.date_of_quiz = "";
                }


                if (newData.time_duration) {
                    const timeParts = newData.time_duration.split(":"); 
                    this.time_duration = `${timeParts[0]}:${timeParts[1]}`; 
                } else {
                    this.time_duration = "";
                }
            }
        },
        immediate: true
    }
}



};
</script>

<style scoped>
/* Background Blur */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
}

/* Modal Box */
.modal-container {
    background: white;
    padding: 20px;
    border-radius: 12px;
    width: 350px;
    text-align: center;
    border: 3px solid #0645AD;
    box-shadow: 3px 3px 0px #0645AD;
    font-family: 'Comic Sans MS', cursive, sans-serif;
}

/* Title */
.modal-title {
    font-size: 22px;
    color: #f4900c;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Form Fields */
.form-group {
    display: flex;
    justify-content: space-between;
    margin: 10px 0;
}

input,
select {
    border: 2px solid #0645AD;
    border-radius: 10px;
    padding: 5px;
    width: 150px;
    font-size: 16px;
    text-align: center;
}


/* Buttons */
.button-group {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 15px;
}

button {
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 12px;
    border: 2px solid #0645AD;
    box-shadow: 2px 2px 0px #0645AD;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
}

.save-btn {
    background: #6cb7f4;
    color: white;
}

.cancel-btn {
    background: white;
    color: #0645AD;
}

button:hover {
    transform: translateY(-2px);
}
</style>