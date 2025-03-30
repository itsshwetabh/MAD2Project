<template>
  <Teleport to="body">
    <div v-if="isOpen" class="overlay">
      <div class="toast-container">
        <button class="close-btn" @click="closeToast">✖</button>
        <h2 v-if="editchapter">Edit Chapter #{{ ChapterName }}</h2>
        <h2 v-if="!editchapter">Add Chapter </h2>
        <input type="text" v-model="ChapterName" placeholder="Enter Chapter Name" class="input-field" />
        <textarea v-model="description" placeholder="Enter Description" class="input-field"></textarea>
        <button class="submit-btn" @click="submitForm">Submit</button>
      </div>
    </div>
  </Teleport>
</template>

<script>
export default {
  name: 'ChapterForm',
  props: {
    isOpen: Boolean,
    editchapter: Boolean,
    chapter: {
      type: Object,
    }

  },
  data() {
    return {
      ChapterName: this.chapter?.name,
      description: this.chapter.description,
      subject_id: this.chapter.subject_id
    };
  },
  methods: {
    closeToast() {
      this.$emit("close");
    },
    submitForm() {
      if (this.editchapter == true) {
        this.$emit("edit", {
          id: this.chapter.id,
          name: this.ChapterName,
          description: this.description,
        });
      }
      else {
        this.$emit("submit", {
          name: this.ChapterName,
          description: this.description,
        });
      }

      this.closeToast();
    },
  },
  watch: {
    chapter: {
      handler(newVal) {
        if (newVal) {
          this.ChapterName = newVal.name;
          this.description = newVal.description;
        }
      },
      deep: true,
      immediate: true
    }
  }

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
  z-index: 9999;
}

/* Toast Box */
.toast-container {
  background: white;
  padding: 20px;
  width: 300px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  position: relative;
}

/* Close (X) Button */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: none;
  font-size: 18px;
  cursor: pointer;
}

/* Input Fields */
.input-field {
  width: 100%;
  margin: 10px 0;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

/* Submit Button */
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