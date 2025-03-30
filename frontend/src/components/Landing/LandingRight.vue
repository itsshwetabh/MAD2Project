<template>
    <div class="container">
      <div class="form-box">
        <h2>{{ isSignUp ? "Sign Up" : "Sign In" }}</h2>
        <form @submit.prevent="handleSubmit">
          <input type="text" v-model="username" placeholder="Username" required />
          <input type="password" v-model="password" placeholder="Password" required />
          <button type="submit">{{ isSignUp ? "Register" : "Login" }}</button>
        </form>
        <p @click="toggleForm">
          {{ isSignUp ? "Already have an account? Sign In" : "Don't have an account? Sign Up" }}
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { RouterLink } from 'vue-router';
  
  export default {
    name: 'LandingRight',
    data() {
      return {
        username: "",
        password: "",
        isSignUp: false, 
      };
    },
    methods: {
      async handleSubmit() {
  if (this.isSignUp) {
    try {
      const resp = await axios.post('http://127.0.0.1:5000/register', {
        email: this.username,
        password: this.password
      });

      console.log(resp.data);

      if (resp.data.ok) {  
        alert(`Sign Up Successful!\nUsername: ${this.username}`);
        this.$router.push('/UserDashboard');
      }
    } catch (error) {
      console.error('Sign Up Failed:', error);

      if (error.response && error.response.status === 404) {
        alert('User already exists!');
      } else {
        alert('Sign Up failed. Please try again.');
      }
    }
  } else {
    this.sendPostRequest();
  }
}
,
      toggleForm() {
        this.isSignUp = !this.isSignUp;
        this.username = "";
        this.password = "";
      },
      async sendPostRequest() {
        try {
          const resp = await axios.post('http://127.0.0.1:5000/login', {
            email: this.username, 
            password: this.password
          });
  
          console.log('Response from backend:', resp);
  

          localStorage.setItem('userData', JSON.stringify(resp.data));
  
          console.log("Login successful! Data stored.");
          alert(`Sign In Successful!\nWelcome back, ${this.username}!`);
          console.log("##"+resp.data.role)
          if(resp.data.role=='user')
          this.$router.push('/UserDashboard');
          else
          this.$router.push('/AdminDashboard');
        } catch (error) {
          console.error('Login failed:', error);
          alert("Login failed. Please check your credentials.");
        }
      }
    }
  };
  </script>
  
  
  <style scoped>
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width:50vw;
    background: #f4f4f4;
  }
  
  .form-box {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    width: 50%;
    height:auto;
  }
  
  h2 {
    margin-bottom: 20px;
  }
  
  input {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background: #0056b3;
  }
  
  p {
    margin-top: 10px;
    color: #007bff;
    cursor: pointer;
  }
  
  p:hover {
    text-decoration: underline;
  }
  </style>
  