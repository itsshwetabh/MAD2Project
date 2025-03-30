<template>
    <div>
        <UserNavbarComponent/>
        <router-view/>
    </div>
</template>

<script>
import UserNavbarComponent from './UserNavbarComponent.vue';
export default {
    name: 'UserDashboard',
    components:{
        UserNavbarComponent
    },
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
        }
    },
    mounted() {
        this.$store.commit('setDetails',{})
        this.fetchDetails();
    }
};
</script>
