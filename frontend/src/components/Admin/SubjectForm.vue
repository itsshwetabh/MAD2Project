<template>
    <Teleport to="body">
      <div v-if="isOpen" class="overlay">
        <div class="toast-container">
          <button class="close-btn" @click="closeToast">✖</button>
          <h2 v-if="edit==false">Add Subject</h2>
          <h2 v-if="edit==true">Edit Subject</h2>
          <input type="text" v-model="SubjectName" placeholder="Enter Subject Name" class="input-field"  />
          <textarea v-model="description" placeholder="Enter Subject Description" class="input-field" ></textarea>
          <button class="submit-btn" @click="submitForm">Submit</button>
        </div>
      </div>
    </Teleport>
  </template>
  
  <script>
  export default {
    name:'SubjectForm',
    props: {
      isOpen: Boolean, 
      edit:Boolean,
      subjectData:{
        type:Object,
      }
    },
    data() {
      return {
        SubjectName: this.subjectData?.name, 
        description: this.subjectData?.description, 
      };
    },
    methods: {
      closeToast() {
        this.$emit("close"); 
      },
      submitForm() {
        this.$emit("submit", { 
          name: this.SubjectName, 
          description: this.description 
        });
        this.closeToast(); 
      },
    },
  };
  </script>
  
  <style scoped>

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); 
    backdrop-filter: blur(5px); 
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
  }
  

  .toast-container {
    background: white;
    padding: 20px;
    width: 300px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    position: relative;
  }
  

  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    border: none;
    background: none;
    font-size: 18px;
    cursor: pointer;
  }
  

  .input-field {
    width: 100%;
    margin: 10px 0;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
  }
  
 
  .submit-btn {
    width: 100%;
    padding: 8px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .submit-btn:hover {
    background: #0056b3;
  }
  </style>
  