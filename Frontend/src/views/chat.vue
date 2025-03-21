<template>
  <div class="container-fluid bg-light vh-100 d-flex flex-column">
    
    <nav class="navbar navbar-light bg-warning px-3 w-100">
      <div class="mt-100">
        <img src="../assets/image.png" alt="IITM Logo" class="logo me-2" width="50" height="50"/>
        <router-link to="/course" class="btn btn-light border-dark ms-2">Back</router-link>
      </div>
      <span class="navbar-brand mb-0 h1 text-dark">WELCOME TO AI HELP BOT</span>
      <button class="btn btn-light border-dark" @click="logout">Logout</button>
    </nav>

    <div class="row flex-grow-1">
      <!-- Sidebar -->
      <div class="col-3 bg-white d-flex flex-column p-3">
        <h5 class="text-dark mb-4 text-center" style="margin-top: 20px;">Subjects</h5>
        
        <div v-for="(chatList, subject) in chats" :key="subject" class="mb-4">
          <!-- Subject Button -->
          <div class="d-flex justify-content-center mb-1">
            <button 
              class="btn w-75 text-center" 
              :class="{'btn-danger text-white': selectedSubject === subject, 'btn-warning': selectedSubject !== subject}"
              @click="joinChat(subject)"
              style="background-color: #ffffff; color: black;">
              {{ subject }}
            </button>
          </div>

          <!-- Chat Titles under Subject -->
          <div v-if="selectedSubject === subject" class="chat-titles">
            <div v-for="chat in chatList" :key="chat.chat_id" class="d-flex justify-content-center mt-1">
              <button 
                class="btn w-75 text-center btn-light border border-dark"
                @click="selectedChatId = chat.chat_id">
                {{ chat.title }}
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Chat Area -->
      <div class="col-9 d-flex flex-column bg-light p-3 border">
        <div class="flex-grow-1 border rounded p-3 bg-white">
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
import axios from "axios";
import "@/axios";

export default {
  data() {
    return {
      chats: {},
      selectedSubject: null,
      selectedChatId: null,
      query: "",
      messages: [],
    };
  },
  methods: {
    joinChat(subject) {
      this.selectedSubject = subject;
      this.selectedChatId = this.chats[subject]?.[0]?.chat_id || null;
      this.messages = [];
    },
    async askQuestion() {
      let user = localStorage.getItem("user-info");
      const token = JSON.parse(user)["access_token"];

      if (!this.selectedChatId) {
        this.selectedChatId = Object.values(this.chats)?.[0]?.[0]?.chat_id;
      }
      
      if (!this.selectedChatId) return;

      if (!this.query.trim()) return;
      
      const userQuery = this.query;
      this.query = "";
      this.messages.push(`You: ${userQuery}`);
      
      try {
        let response = await axios.post("/message/send", {
          chat_id: this.selectedChatId,
          content: userQuery,
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          }, 
        });

        if (response.status === 200) {
          this.messages.push(`AI Tutor: ${response.data}`);
        }
      } catch (error) {
        console.error("Error sending message:", error);
        this.messages.push("AI Tutor: Failed to send your message.");
      }
    },
    logout(){
      localStorage.clear();
      this.$router.push({name:"HOME"})
    }
  },
  async mounted() {


    let user = localStorage.getItem("user-info");
    if (!user) {
      this.$router.push({ name: "Login" });
      return;
    }
    
    const token = JSON.parse(user)["access_token"];
    try {
      let response = await axios.get("/chats/", {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      this.chats = response.data.reduce((acc, chat) => {
        const subjectName = chat.subject.subject_name;
        if (!acc[subjectName]) acc[subjectName] = [];
        acc[subjectName].push(chat);
        return acc;
      }, {});



      
    } catch (error) {
      if (error.response?.status === 401) {
        alert("Session expired. Please log in again.");
        localStorage.clear();
        this.$router.push({name:"Login"});
      }
    }
    try {
      let response = await axios.get("/chats/", {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        
      });
      //creating chat if no chats are there
      console.log("here1")
      if(Array(response.data)[0].length==0){
        try {
        
     
          console.log("here2")
        const token = JSON.parse(user)["access_token"];
        
        let response = await axios.post(
          "/chats/",
          {
            subject_id: 1, // You might need to dynamically set this based on the subject
            title: "chat", // Using the clicked subject as the chat title
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        console.log("here3")
         this.$router.go(0)
        if (response.status === 200) {
          alert(`New chat created for ${subject}`);
          console.log("Chat Created:", response.data);
          
          
        }
      } catch (error) {
        console.error("Error creating chat:", error);
        alert("Failed to create chat. Please try again.");
      }
    
      }
      // Group chats by subject
      this.chats = response.data.reduce((acc, chat) => {
        const subjectName = chat.subject.subject_name;
        if (!acc[subjectName]) acc[subjectName] = [];
        acc[subjectName].push(chat);
        return acc;
      }, {});

      console.log("Grouped Chats:", this.chats);
    } catch (error) {
      if (error.response) {
        if (error.response.status === 401) {
          alert("Session expired. Please log in again.");
          localStorage.clear();
          this.$router.push({name:"Login"})
        } else {
          alert(`Error: ${error.response.status} - ${error.response.data?.message || "Unknown error"}`);
        }
      } else {
        console.error("Network/Server error:", error);
      }
      
      
    }
    let history = await axios.get(`/chats/${this.chat_id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        }})
    console.log(history)
    

  },
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
.chat-titles {
  padding-left: 20px;
}
</style>