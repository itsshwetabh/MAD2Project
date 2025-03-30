<template>
    <div class="parent">

        <div>
            <UpcomingQuizzes/>
        </div>
        <div>
            <LiveQuizzes/>
        </div>
        <div>
            <PastQuizzes/>
        </div>
    </div>

</template>
<script>
import UpcomingQuizzes from './UpcomingQuizzes.vue';
import LiveQuizzes from './LiveQuizzes.vue';
import PastQuizzes from './PastQuizzes.vue';
export default {
    name: "UserHome",
    components: {
        UpcomingQuizzes,
        LiveQuizzes,
        PastQuizzes
    },
    async mounted(){
        await this.$store.dispatch("fetchQuiz")
        console.log("fetchQuiz dispatched")
        await this.$store.dispatch("fetchQuestion")
        console.log("fetchQuestion dispatched")
        await this.$store.dispatch("fetchSubjects")
        console.log("fetchSubjects called")
        await this.$store.dispatch("fetchChapters")
        console.log("fetchChapters called")
        await this.$store.dispatch("fetchAttempts")
        console.log("fetch Attempts called")
        console.log(this.$store.state.quiz_attempts[0])

    }
}

</script>
<style scoped>
.parent{
    background-color:#f8f9fa

}
</style>