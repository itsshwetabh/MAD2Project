<template>
    <nav class="navbar">
      <div class="nav-links">
        <router-link to="/AdminDashboard">Home</router-link>
        <router-link to="/AdminDashboard/quiz">Quiz</router-link>
        <router-link to="/AdminDashboard/summary">Summary</router-link>
        <router-link to="#" @click="logout">Logout</router-link>
      </div>
      <div class="search-container">
        <input type="text" placeholder="Search..." class="search-box" />
      </div>
      <span class="welcome-text">Welcome, Admin</span>
    </nav>
  </template>
  
  <script>
  export default {
    name: "NavbarComponent",
    methods:{
      logout(){
        localStorage.removeItem("userData");
        this.$router.push('/')
      },
    },
  };
  </script>
  
  <style>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(to right, #141414, #222222, #3a3a3a, #b8860b);

    padding: 15px 30px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    font-family: Arial, sans-serif;
    height: 8vh;
  }
  
  .nav-links a {
    text-decoration: none;
    color: white;
    font-weight: bold;
    margin: 0 15px;
    transition: color 0.3s ease-in-out;
    font-size: 16px;
  }
  
  .nav-links a:hover {
    color: yellow;
  }
  
  .search-container {
    flex-grow: 1;
    display: flex;
    justify-content: center;
  }
  
  .search-box {
    padding: 8px 12px;
    border: none;
    border-radius: 20px;
    font-size: 14px;
    width: 200px;
    outline: none;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  }
  
  .welcome-text {
    color: white;
    font-weight: bold;
    font-size: 16px;
  }
  </style>
  