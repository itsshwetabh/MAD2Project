<template>
    <button class="floating-button" @click="openQuizForm">
      + New Quiz
    </button>
  </template>
  
  <script>
  export default {
    name: "AddQuizButton",
    methods: {
    openQuizForm() {
      this.$emit("openQuizForm"); // Emits event to parent
    }
  }
  };
  </script>
  
  <style scoped>
  .floating-button {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #b2e8a4;
    color: #065f06;
    font-size: 18px;
    font-weight: bold;
    padding: 12px 24px;
    border: 3px solid #2a8a28;
    border-radius: 25px;
    box-shadow: 2px 3px 0px #2a8a28;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
  }
  
  .floating-button:hover {
    background-color: #a3db96;
    box-shadow: 3px 4px 0px #1f6b1f;
    transform: translateX(-50%) translateY(-2px);
  }
  </style>
  