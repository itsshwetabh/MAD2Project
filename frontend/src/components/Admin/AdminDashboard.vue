<template>
    <div>
        <NavbarComponent/>
        <router-view/>
    </div>
</template>

<script>
import NavbarComponent from './AdminNavbarComponent.vue';
export default {
    name: 'UserDashboard',
    data() {
        return {
            email: "",
            role: "",
            token: "",
        };
    },
    methods: {
        fetchDetails() {
            const userData = JSON.parse(localStorage.getItem('userData'));
            if (userData) {
                this.email = this.$store.state.email;
                this.role = this.$store.state.role;
                this.token = this.$store.state.token;
            }
        },
        fetchSubjects() {
            this.$store.dispatch("fetchSubjects"); 
        }
    },
    async mounted() {
        await this.$store.commit('setDetails',{})
         this.fetchDetails();
         this.fetchSubjects();
        await this.$store.dispatch("fetchChapters")
        await this.$store.dispatch("fetchQuestion")
        await this.$store.dispatch("fetchQuiz")
        await this.$store.dispatch("fetchAttempts")

        
    },
    components:{
        NavbarComponent
    }
};
</script>
