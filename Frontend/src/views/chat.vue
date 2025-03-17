<template>

    <div class="container-fluid bg-light vh-100 d-flex flex-column">
      
      <nav class="navbar navbar-light bg-warning px-3 w-100">
  
        <div class="mt-100">
          <img src="../assets/image.png" alt="IITM Logo" class="logo me-2" width="50" height="50"/>
          <button class="btn btn-light border-dark ms-2" @click="reloadPage">Refresh</button>
        </div>
  
        <span class="navbar-brand mb-0 h1 text-dark">Welcome to the AI Tutor, Sandeep</span>
        
        <router-link to="/" class="btn btn-light border-dark">Log out</router-link>
  
      </nav>
      
      <div class="row flex-grow-1">
        <!-- Sidebar -->
        <div class="col-3 bg-white d-flex flex-column p-3">
          <h5 class="text-dark mb-4 text-center" style="margin-top: 20px;">Subjects</h5>
          <div v-for="(chats, subject) in chats" :key="subject" class="mb-4">
            <div class="d-flex justify-content-center mb-1">
              <button 
                class="btn w-75 text-center" 
                :class="{'btn-danger text-white': selectedChat === subject, 'btn-warning': selectedChat !== subject}"
                @click="joinChat(subject)"
                style="background-color: #ffffff; color: black;">
                {{ subject }}
              </button>
            </div>
          </div>
        </div>
        
        <!-- Chat Area -->
        <div class="col-9 d-flex flex-column bg-light p-3 border">
          
          <!-- New Button Above Chat Box -->
          <div class="d-flex justify-content-center mb-3">
            <button 
              class="btn btn-warning w-50 text-dark" 
              @click="goToWeekLecture">
              📚 Week Lectures
            </button>
          </div>
  
          <div class="flex-grow-1 border rounded p-3 bg-white">
            <p v-if="selectedChat">Chatting in: {{ selectedChat }}</p>
            <p v-else>Select a subject to start conversation ...</p>

            <div v-for="(message, index) in messages" :key="index" class="mt-2">
                
              <p class="mb-1">{{ message }}</p>
            </div>
          </div>

          <div class="d-flex mt-3">
            <input v-model="query" type="text" class="form-control border border-dark" placeholder="Enter your query here ........" @keyup.enter="askQuestion"/>
            <button class="btn btn-warning ms-2" @click="askQuestion">Ask</button>
          </div>
  
        </div>
        
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        chats: {
          PDSA: [],
          Physics: [],
          Chemistry: [],
          Biology: []
        },
        selectedChat: null,
        query: '',
        messages: []
      };
    },
    methods: {
      joinChat(subject) {
        this.selectedChat = subject;
        this.messages = [];
      },
      askQuestion() {
        if (this.query.trim()) {
          this.messages.push(`You: ${this.query}`);
          this.messages.push(`AI Tutor: You posted the following query -- ${this.query} --. This is a dummy response to your query.`);
          this.query = '';
        }
      },
      reloadPage() {
        window.location.reload();
      },
      goToWeekLecture() {
        this.$router.push('/week-lectures'); // Make sure this route is defined in your router
      }
    }
  };
  </script>
  
  <style scoped>
  .container-fluid {
    height: 100vh;
  }
  .navbar {
    width: 100%;
  }
  .btn-light:hover, .btn-primary:hover {
    background-color: lightblue;
  }
  .text-center {
    text-align: center;
  }
  .btn-danger {
    background-color: #a61c00 !important;
    border-color: #a61c00 !important;
  }
  .mb-4 {
    margin-bottom: 1.5rem !important;
  }
  </style>
  