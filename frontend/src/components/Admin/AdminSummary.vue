<template>
    <div class="charts">
        <div class="chart1">
            <h1>Subject-wise Max Scores</h1>
            <canvas ref="scoreChart"></canvas>
        </div>
        <div class="chart2">
            <h1>Subject-wise Attempts</h1>
            <canvas ref="attemptChart"></canvas>
        </div>
    </div>

</template>

<script>
import Chart from "chart.js/auto";

export default {
    name: 'AdminSummary',
    data() {
        return {
            scoreChart: null,
            attemptChart: null,
        };
    },
    async mounted() {
        await this.$store.dispatch("fetchChapters");
        await this.$store.dispatch("fetchQuestion");
        await this.$store.dispatch("fetchQuiz");
        await this.$store.dispatch("fetchAttempts");

        this.createScoreChart();
        this.createAttemptChart();
    },
    methods: {
        createScoreChart() {
            const ctx = this.$refs.scoreChart.getContext("2d");
            this.scoreChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: Object.keys(this.subject_max_score),
                    datasets: [
                        {
                            label: "Max Score (%)",
                            data: Object.values(this.subject_max_score),
                            backgroundColor: "rgba(75, 192, 192, 0.2)",
                            borderColor: "rgba(75, 192, 192, 1)",
                            borderWidth: 1,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, max: 100 },
                    },
                },
            });
        },
        createAttemptChart() {
            const ctx = this.$refs.attemptChart.getContext("2d");
            this.attemptChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: Object.keys(this.subject_wise_attempts),
                    datasets: [
                        {
                            label: "Total Attempts",
                            data: Object.values(this.subject_wise_attempts),
                            backgroundColor: "rgba(255, 99, 132, 0.2)",
                            borderColor: "rgba(255, 99, 132, 1)",
                            borderWidth: 1,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true },
                    },
                },
            });
        },
        updateScoreChart() {
            if (this.scoreChart) {
                this.scoreChart.data.labels = Object.keys(this.subject_max_score);
                this.scoreChart.data.datasets[0].data = Object.values(this.subject_max_score);
                this.scoreChart.update();
            }
        },
        updateAttemptChart() {
            if (this.attemptChart) {
                this.attemptChart.data.labels = Object.keys(this.subject_wise_attempts);
                this.attemptChart.data.datasets[0].data = Object.values(this.subject_wise_attempts);
                this.attemptChart.update();
            }
        }
    },
    computed: {
        subject_max_score() {
            let subject_max = {};
            this.$store.state.subjects.forEach((subject) => {
                let attempts = this.$store.state.quiz_attempts.filter((attempt) => attempt.subject_id == subject.id);
                let max_score = 0;
                attempts.forEach((a) => {
                    max_score = Math.max(max_score, (a.score / a.max_score).toFixed(2) * 100);
                });
                subject_max[subject.name] = max_score;
            });
            return subject_max;
        },
        subject_wise_attempts() {
            let subject_attempts = {};
            this.$store.state.subjects.forEach((subject) => {
                subject_attempts[subject.name] = this.$store.state.quiz_attempts.filter(
                    (a) => subject.id == a.subject_id
                ).length;
            });
            return subject_attempts;
        }
    },

};
</script>

<style scoped>
.chart1, .chart2 {
    width: 40%;
}
.charts{
    display:flex;
    align-items: center;
    justify-content: space-around;
    height:80vh;
    width:100vw;
}
</style>
