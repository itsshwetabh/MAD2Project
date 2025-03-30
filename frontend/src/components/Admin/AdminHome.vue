<template>

    <div class="parent">



        <div @click="showToast = true" class="addSubject">+</div>
        <SubjectForm :isOpen="showToast" @close="showToast = false" @submit="handleSubmit" />




        <Subjects v-for="(subject) in Subjects" :key="subject.id" :subjectData="subject" />







    </div>

</template>
<script>
import Subjects from './Cards/Subjects.vue';
import SubjectForm from './SubjectForm.vue';
import axios from 'axios';

export default {
    name: 'AdminHome',
    components: { Subjects, SubjectForm },
    data() {
        return {
            showToast: false,
        } 
    },
    methods: {
        async handleSubmit(data) {
            const userData = JSON.parse(localStorage.getItem('userData'));
            const token = userData.token
            const headers = {
                'Authentication-Token': token,
                'Content-Type': 'application/json'  

            };
            if (data.name && data.description) {
                try {
                    const response = await axios.post('http://127.0.0.1:5000/addsubject', data, { headers });
                    this.$store.dispatch("fetchSubjects");
                }
                catch (err) {
                    alert("There was some issue, may be the subject already exists in the database!")

                }
            }
            else {
                alert("please enter the values of both the fields")
            }

        },

    },
    computed:
    {
        Subjects() {
            const subjects = this.$store.state.subjects
            return (subjects)
        }
    }

};
</script>
<style scoped>
.parent {
    display: flex;
    height: 80vh;
    flex-wrap: wrap;
    overflow: auto;
    padding: 10px;
    background-color: #f8f9fa;


}

.addSubject {
    font-size: 40px;
    background-color: black;
    color: white;
    border-radius: 50%;
    height: 50px;
    width: 50px;
    text-align: center;
    position: absolute;
    left: 50%;
    top: 90%;
    z-index: 10;
    cursor: pointer;
}
</style>