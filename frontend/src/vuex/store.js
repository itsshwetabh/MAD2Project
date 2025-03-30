import { createStore } from "vuex";
import axios from "axios";
export default createStore({
  state: {
    name: "Code Improve",
    mainTitle: "**** No Title ***",
    email: "",
    role: "",
    token: "",
    subjects: [],
    chapters: [],
    Quiz: [],
    questions: [],
    quiz_attempts: [],
  },
  mutations: {

    setDetails(state, payload) {
      state.email = JSON.parse(localStorage.getItem("userData")).email;

      state.role = JSON.parse(localStorage.getItem("userData")).role;
      state.token = JSON.parse(localStorage.getItem("userData")).token;
    },
    setSubjects(state, payload) {
      state.subjects = payload;
    },
    setChapters(state, payload) {
      state.chapters = payload;
    },
    setQuiz(state, payload) {
      state.Quiz = payload;
    },
    setQuestion(state, payload) {
      state.questions = payload;
    },
    setAttempts(state, payload) {
      state.quiz_attempts = payload;
    },
  },

  actions: {
    async fetchSubjects(context) {
      try {
        const token = JSON.parse(localStorage.getItem("userData")).token;
        console.log("this is the token:" + token);
        if (!token) {
          console.error("No authentication token found");
          return;
        }

        const response = await axios.get(
          "http://127.0.0.1:5000/fetchsubjects",
          {
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": token,
            },
          }
        );

        context.commit("setSubjects", response.data.subjects);
      } catch (error) {
        console.error(
          "Error fetching subjects:",
          error.response ? error.response.data : error.message
        );
      }
    },
    async addChapter(context, payload) {
      try {
        const token = JSON.parse(localStorage.getItem("userData")).token;
        console.log("this is the token:" + token);
        if (!token) {
          console.error("No authentication token found");
          return;
        }

        const response = await axios.post(
          "http://127.0.0.1:5000/addchapter",
          {
            chapter_id: payload.id,
            subject_id: payload.subject_id,
            name: payload.name,
            description: payload.description,
          },
          {
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": token,
            },
          }
        );


        await context.dispatch("fetchChapters");

      } catch (error) {
        console.error(
          "Error fetching subjects:",
          error.response ? error.response.data : error.message
        );
      }
    },
    async fetchChapters(context, payload) {
      const token = JSON.parse(localStorage.getItem("userData")).token;
      const chapters = await axios.get("http://127.0.0.1:5000/fetchchapters", {
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": token,
        },
      });
      context.commit("setChapters", chapters.data.chapters);
    },
    async fetchQuiz(context, payload) {
      const token = JSON.parse(localStorage.getItem("userData")).token;
      const headers = {
        "Authentication-Token": token,
      };

      const quizes = await axios.get("http://127.0.0.1:5000/fetchquiz", {
        headers,
      });

      context.commit("setQuiz", quizes.data.quizes);
    },
    async fetchQuestion(context, payload) {
      const token = JSON.parse(localStorage.getItem("userData")).token;
      const headers = {
        "Authentication-Token": token,
      };

      const questions = await axios.get("http://127.0.0.1:5000/fetchquestion", {
        headers,
      });
      context.commit("setQuestion", questions.data.questions);
    },
    async fetchAttempts(context) {
      const userData = JSON.parse(localStorage.getItem("userData"));
      const token = userData.token;

      const headers = {
        "Authentication-Token": token,
      };

      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/quizzes/fetchAttempts",
          {
            headers,
            params: { user_id: userData.id }, 
          }
        );

        context.commit("setAttempts", response.data.attempts);
      } catch (error) {
        console.error("Error fetching attempts:", error);
      }
    },
  },
});
