<template>
  <div class="subject-card">
    <!-- Edit and Delete Buttons -->
    <button @click="showEditForm=true" class="edit-card-btn">Edit</button>
    <button @click="Delete" class="delete-card-btn">Delete</button>

    <ChapterForm :chapter="chapter" :editchapter="editchapter" :isOpen="showToast" @close="showToast = false" @submit="handleSubmit" @edit="modifyChapter" />
    <SubjectForm :isOpen="showEditForm" @close="showEditForm = false" @submit="handleEdit" :edit="true" :subjectData="subjectData" />

    <h2 class="subject-title">{{ subjectData.name }}</h2>
    <h3>{{ subjectData.description }}</h3>
    <hr/>

    <!-- Scrollable table container -->
    <div class="table-container">
      <table class="chapters-table">
        <thead>
          <tr>
            <th>Chapter Name</th>
            <th>No. of Questions</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(chapter, index) in Chapters" :key="index">
            <td>{{ chapter.name }}</td>
            <td>{{ questionsCount[chapter.id] || 0 }}</td> <!-- Placeholder for API data -->
            <td class="action-buttons">
              <button @click="editChapter(chapter)" class="edit-btn">Edit</button>
              <button @click="deleteChapter(chapter.id)" class="delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="add-container">
      <button class="add-chapter" @click="openToast">+ Chapter</button>
    </div>
  </div>
</template>

<script>
import ChapterForm from "../ChapterForm.vue";
import SubjectForm from "../SubjectForm.vue";
import axios from 'axios'
export default {
  name: "Subjects",

  data() {
    return {
      showToast: false,
      edit:false,
      showEditForm:false,
      editchapter:false,
      chapter:{},
    };
  },
  methods: {
    editChapter(chapter)
    {
      
      this.chapter=chapter;
      this.editchapter=true;
      this.showToast=true;
    }
    ,
    async modifyChapter(data){
      const userData = JSON.parse(localStorage.getItem('userData'));
            const token = userData.token
            const headers = {
                'Authentication-Token': token,
                'Content-Type': 'application/json'  // Ensure JSON format

            };
        const resp= await axios.post(`http://127.0.0.1:5000/addchapter`,data,{headers:headers})
        await this.$store.dispatch('fetchChapters')

    },
    async deleteChapter(id){
      const userData = JSON.parse(localStorage.getItem('userData'));
            const token = userData.token
            const headers = {
                'Authentication-Token': token,
                'Content-Type': 'application/json'  // Ensure JSON format

            };
        const resp= await axios.delete(`http://127.0.0.1:5000/deletechapter/${id}`,{headers:headers})
        await this.$store.dispatch('fetchChapters')

    }
  ,
    openToast() {
      this.editchapter=false;
      this.showToast = true;
    },
    async handleSubmit(data) {
      const newChapter = {
        subject_id: this.subjectData.id, // Example subject ID
        name: data.name,
        description: data.description,
      };

      await this.$store.dispatch("addChapter", newChapter);
    },
    async handleEdit(data) {
            const userData = JSON.parse(localStorage.getItem('userData'));
            const token = userData.token
            const headers = {
                'Authentication-Token': token,
                'Content-Type': 'application/json'  // Ensure JSON format

            };
            if (data.name && data.description) {
                try {
                    const editedData={...data,edit:true,subject_id:this.subjectData.id}
                    const response = await axios.post('http://127.0.0.1:5000/addsubject', editedData, { headers });
                    this.$store.dispatch("fetchSubjects");
                }
                catch (err) {
                    alert("There was some issue, may be the subject already exists in the database")

                }
            }
            else {
                alert("please enter the values of both the fields")
            }

        },
      async Delete(){
        const userData = JSON.parse(localStorage.getItem('userData'));
            const token = userData.token
            const headers = {
                'Authentication-Token': token,
                'Content-Type': 'application/json'  // Ensure JSON format

            };
        const resp= await axios.delete(`http://127.0.0.1:5000/subject/${this.subjectData.id}`,{headers:headers})
        await this.$store.dispatch('fetchSubjects')
      }
      
  },
  props: {
    subjectData: {
      type: Object,
    },
  },
  components: {
    ChapterForm,
    SubjectForm,
  },
  computed: {
    Chapters() {
      const allChapters = this.$store.state.chapters;
      const chapters = allChapters.filter(
        (chapter) => chapter.subject_id == this.subjectData.id
      );
      return chapters;
    },
    questionsCount() {
    const quizzes = this.$store.state.Quiz; // All quizzes
    const questions = this.$store.state.questions; // All questions

    const countMap = {};

    // Loop through each chapter
    this.$store.state.chapters.forEach(chapter => {
      // Find all quizzes linked to this chapter
      const chapterQuizzes = quizzes.filter(quiz => quiz.chapter_id === chapter.id);


      // Get quiz IDs
      const quizIds = chapterQuizzes.map(quiz => quiz.id);


      // Count questions belonging to those quiz IDs
      const questionCount = questions.filter(q => quizIds.includes(q.quiz_id)).length;


      countMap[chapter.id] = questionCount;
    });

    return countMap;
  }

  },
};
</script>

<style scoped>
/* Card Container */
.subject-card {
  width: 500px;
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  /* background: antiquewhite; */
  /* background: linear-gradient(to bottom, #FAE6B1, #F5D88E); */
  background: white;


  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  font-family: "Arial", sans-serif;
  text-align: center;
  margin: 20px auto;
  /* border: 2px solid black; */
  position: relative; /* Needed for absolute positioning of buttons */
}


/* Edit and Delete Buttons (Top-Left & Top-Right) */
.edit-card-btn,
.delete-card-btn {
  position: absolute;
  top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.edit-card-btn {
  left: 10px;
  background: #4caf50;
  color: white;
}

.delete-card-btn {
  right: 10px;
  background: #f44336;
  color: white;
}

.edit-card-btn:hover {
  background: #388e3c;
}

.delete-card-btn:hover {
  background: #d32f2f;
}

/* Title */
.subject-title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 3px;
}

/* Scrollable Table Container */
.table-container {
  flex-grow: 1;
  max-height: 180px;
  overflow-y: auto;
  /* border: 1px solid black; */
}

/* Table Styling */
.chapters-table {
  width: 100%;
  border-collapse: collapse;
}

.chapters-table th,
.chapters-table td {
  border: 1px solid black;
  padding: 8px;
  text-align: left;
}

.chapters-table th {
  background: #dce8ff;
  font-weight: bold;
  text-align: center;
  position: sticky;
  top: 0;
}

.chapters-table td {
  text-align: center;
}

/* Scrollbar Styling */
.table-container::-webkit-scrollbar {
  width: 8px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.edit-btn {
  background: #4caf50;
  color: white;
}

.delete-btn {
  background: #f44336;
  color: white;
}

.edit-btn:hover {
  background: #388e3c;
}

.delete-btn:hover {
  background: #d32f2f;
}

/* Add Chapter Button */
.add-container {
  flex-shrink: 0;
}

.add-chapter {
  background: #ff9ea6;
  padding: 10px 15px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.3s ease-in-out;
}

.add-chapter:hover {
  background: #ff7b85;
}
</style>
